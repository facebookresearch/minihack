# Copyright (c) Facebook, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
from typing import Any, Dict, Optional, Tuple

import gym
import torch
from nle import nethack
from minihack.agent.common.models.embed import GlyphEmbedding
from minihack.agent.common.models.transformer import TransformerEncoder
from omegaconf import DictConfig
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.utils.annotations import override
from torch import nn
from torch.nn import functional as F

NUM_GLYPHS = nethack.MAX_GLYPH
NUM_FEATURES = nethack.BLSTATS_SHAPE[0]
PAD_CHAR = 0
NUM_CHARS = 128


class RLLibGlyphEmbedding(GlyphEmbedding):
    def glyphs_to_idgroup(self, glyphs):
        B, H, W = glyphs.shape
        ids_groups = self.id_pairs_table.index_select(
            0, glyphs.contiguous().view(-1).long()
        )
        ids = ids_groups.select(1, 0).view(B, H, W).long()
        groups = ids_groups.select(1, 1).view(B, H, W).long()
        return (ids, groups)

    def prepare_input(self, inputs):
        """Take the inputs to the network as dictionary and return a namedtuple
        of the input/index tensors to be embedded (GlyphTuple)"""
        embeddable_data = {}
        # Only flatten the data we want
        for key, value in inputs.items():
            if key in self.embeddings:
                # -- [ B x ...] -> [ B' x ... ]
                # embeddable_data[key] = torch.flatten(value, 0, 1).long()
                embeddable_data[key] = value.long()

        # add our group id and subgroup id if we want them
        if self.requires_id_pairs_table:
            ids, groups = self.glyphs_to_idgroup(inputs["glyphs"])
            embeddable_data["groups"] = groups
            embeddable_data["subgroup_ids"] = ids

        # convert embeddable_data to a named tuple
        return self.GlyphTuple(**embeddable_data)


class NetHackNet(nn.Module):
    AgentOutput = collections.namedtuple(
        "AgentOutput", "action policy_logits baseline"
    )

    def __init__(self):
        super(NetHackNet, self).__init__()

        self.register_buffer("reward_sum", torch.zeros(()))
        self.register_buffer("reward_m2", torch.zeros(()))
        self.register_buffer("reward_count", torch.zeros(()).fill_(1e-8))

    def forward(self, inputs, core_state):
        raise NotImplementedError

    def initial_state(self, batch_size=1):
        return ()

    def prepare_input(self, inputs):
        # -- [B x H x W]
        glyphs = inputs["glyphs"]

        # -- [B x F]
        features = inputs["blstats"]

        B, *_ = glyphs.shape

        return glyphs, features

    def embed_state(self, inputs):
        raise NotImplementedError

    @torch.no_grad()
    def update_running_moments(self, reward_batch):
        """Maintains a running mean of reward."""
        new_count = len(reward_batch)
        new_sum = torch.sum(reward_batch)
        new_mean = new_sum / new_count

        curr_mean = self.reward_sum / self.reward_count
        new_m2 = torch.sum((reward_batch - new_mean) ** 2) + (
            (self.reward_count * new_count)
            / (self.reward_count + new_count)
            * (new_mean - curr_mean) ** 2
        )

        self.reward_count += new_count
        self.reward_sum += new_sum
        self.reward_m2 += new_m2

    @torch.no_grad()
    def get_running_std(self):
        """Returns standard deviation of the running mean of the reward."""
        return torch.sqrt(self.reward_m2 / self.reward_count)


class Crop(nn.Module):
    def __init__(self, height, width, height_target, width_target):
        super(Crop, self).__init__()
        self.width = width
        self.height = height
        self.width_target = width_target
        self.height_target = height_target

        width_grid = self._step_to_range(
            2 / (self.width - 1), self.width_target
        )[None, :].expand(self.height_target, -1)
        height_grid = self._step_to_range(
            2 / (self.height - 1), height_target
        )[:, None].expand(-1, self.width_target)

        # "clone" necessary, https://github.com/pytorch/pytorch/issues/34880
        self.register_buffer("width_grid", width_grid.clone())
        self.register_buffer("height_grid", height_grid.clone())

    def _step_to_range(self, step, num_steps):
        return torch.tensor(
            [step * (i - num_steps // 2) for i in range(num_steps)]
        )

    def forward(self, inputs, coordinates):
        """Calculates centered crop around given x,y coordinates.

        Args:
           inputs [B x H x W] or [B x H x W x C]
           coordinates [B x 2] x,y coordinates

        Returns:
           [B x H' x W'] inputs cropped and centered around x,y coordinates.
        """
        assert inputs.shape[1] == self.height, "expected %d but found %d" % (
            self.height,
            inputs.shape[1],
        )
        assert inputs.shape[2] == self.width, "expected %d but found %d" % (
            self.width,
            inputs.shape[2],
        )

        permute_results = False
        if inputs.dim() == 3:
            inputs = inputs.unsqueeze(1)
        else:
            permute_results = True
            inputs = inputs.permute(0, 2, 3, 1)
        inputs = inputs.float()

        x = coordinates[:, 0]
        y = coordinates[:, 1]

        x_shift = 2 / (self.width - 1) * (x.float() - self.width // 2)
        y_shift = 2 / (self.height - 1) * (y.float() - self.height // 2)

        grid = torch.stack(
            [
                self.width_grid[None, :, :] + x_shift[:, None, None],
                self.height_grid[None, :, :] + y_shift[:, None, None],
            ],
            dim=3,
        )

        crop = (
            torch.round(F.grid_sample(inputs, grid, align_corners=True))
            .squeeze(1)
            .long()
        )

        if permute_results:
            # [B x C x H x W] -> [B x H x W x C]
            crop = crop.permute(0, 2, 3, 1)

        return crop


class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)


class BaseNet(NetHackNet):
    def __init__(self, processed_observation_shape, flags: DictConfig):
        super(BaseNet, self).__init__()

        self.observation_space = processed_observation_shape.original_space

        self.H = self.observation_space["glyphs"].shape[0]
        self.W = self.observation_space["glyphs"].shape[1]

        self.k_dim = flags.embedding_dim
        self.h_dim = flags.hidden_dim

        self.crop_model = flags.crop_model
        self.crop_dim = flags.crop_dim

        self.num_features = NUM_FEATURES

        self.crop = Crop(self.H, self.W, self.crop_dim, self.crop_dim)

        self.glyph_type = flags.glyph_type
        self.glyph_embedding = RLLibGlyphEmbedding(
            flags.glyph_type,
            flags.embedding_dim,
            None,
            flags.use_index_select,
        )

        K = flags.embedding_dim  # number of input filters
        F = 3  # filter dimensions
        S = 1  # stride
        P = 1  # padding
        M = 16  # number of intermediate filters
        self.Y = 8  # number of output filters
        L = flags.layers  # number of convnet layers

        in_channels = [K] + [M] * (L - 1)
        out_channels = [M] * (L - 1) + [self.Y]

        def interleave(xs, ys):
            return [val for pair in zip(xs, ys) for val in pair]

        conv_extract = [
            nn.Conv2d(
                in_channels=in_channels[i],
                out_channels=out_channels[i],
                kernel_size=(F, F),
                stride=S,
                padding=P,
            )
            for i in range(L)
        ]

        self.extract_representation = nn.Sequential(
            *interleave(conv_extract, [nn.ELU()] * len(conv_extract))
        )

        if self.crop_model == "transformer":
            self.extract_crop_representation = TransformerEncoder(
                K,
                N=L,
                heads=8,
                height=self.crop_dim,
                width=self.crop_dim,
                device=None,
            )
        elif self.crop_model == "cnn":
            conv_extract_crop = [
                nn.Conv2d(
                    in_channels=in_channels[i],
                    out_channels=out_channels[i],
                    kernel_size=(F, F),
                    stride=S,
                    padding=P,
                )
                for i in range(L)
            ]

            self.extract_crop_representation = nn.Sequential(
                *interleave(conv_extract_crop, [nn.ELU()] * len(conv_extract))
            )

        # MESSAGING MODEL
        if "msg" not in flags:
            self.msg_model = "none"
        else:
            self.msg_model = flags.msg.model
            self.msg_hdim = flags.msg.hidden_dim
            self.msg_edim = flags.msg.embedding_dim
        if self.msg_model in ("gru", "lstm", "lt_cnn"):
            # character-based embeddings
            self.char_lt = nn.Embedding(
                NUM_CHARS, self.msg_edim, padding_idx=PAD_CHAR
            )
        else:
            # forward will set up one-hot inputs for the cnn, no lt needed
            pass

        if self.msg_model.endswith("cnn"):
            # from Zhang et al, 2016
            # Character-level Convolutional Networks for Text Classification
            # https://arxiv.org/abs/1509.01626
            if self.msg_model == "cnn":
                # inputs will be one-hot vectors, as done in paper
                self.conv1 = nn.Conv1d(NUM_CHARS, self.msg_hdim, kernel_size=7)
            elif self.msg_model == "lt_cnn":
                # replace one-hot inputs with learned embeddings
                self.conv1 = nn.Conv1d(
                    self.msg_edim, self.msg_hdim, kernel_size=7
                )
            else:
                raise NotImplementedError("msg.model == %s", flags.msg.model)

            # remaining convolutions, relus, pools, and a small FC network
            self.conv2_6_fc = nn.Sequential(
                nn.ReLU(),
                nn.MaxPool1d(kernel_size=3, stride=3),
                # conv2
                nn.Conv1d(self.msg_hdim, self.msg_hdim, kernel_size=7),
                nn.ReLU(),
                nn.MaxPool1d(kernel_size=3, stride=3),
                # conv3
                nn.Conv1d(self.msg_hdim, self.msg_hdim, kernel_size=3),
                nn.ReLU(),
                # conv4
                nn.Conv1d(self.msg_hdim, self.msg_hdim, kernel_size=3),
                nn.ReLU(),
                # conv5
                nn.Conv1d(self.msg_hdim, self.msg_hdim, kernel_size=3),
                nn.ReLU(),
                # conv6
                nn.Conv1d(self.msg_hdim, self.msg_hdim, kernel_size=3),
                nn.ReLU(),
                nn.MaxPool1d(kernel_size=3, stride=3),
                # fc receives -- [ B x h_dim x 5 ]
                Flatten(),
                nn.Linear(5 * self.msg_hdim, 2 * self.msg_hdim),
                nn.ReLU(),
                nn.Linear(2 * self.msg_hdim, self.msg_hdim),
            )  # final output -- [ B x h_dim x 5 ]
        elif self.msg_model in ("gru", "lstm"):

            def rnn(flag):
                return nn.LSTM if flag == "lstm" else nn.GRU

            self.char_rnn = rnn(self.msg_model)(
                self.msg_edim,
                self.msg_hdim // 2,
                batch_first=True,
                bidirectional=True,
            )
        elif self.msg_model != "none":
            raise NotImplementedError("msg.model == %s", flags.msg.model)

        self.embed_features = nn.Sequential(
            nn.Linear(self.num_features, self.k_dim),
            nn.ReLU(),
            nn.Linear(self.k_dim, self.k_dim),
            nn.ReLU(),
        )

        self.equalize_input_dim = flags.equalize_input_dim
        if not self.equalize_input_dim:
            # just added up the output dimensions of the input featurizers
            # feature / status dim
            out_dim = self.k_dim
            # CNN over full glyph map
            out_dim += self.H * self.W * self.Y
            if self.crop_model == "transformer":
                out_dim += self.crop_dim ** 2 * K
            elif self.crop_model == "cnn":
                out_dim += self.crop_dim ** 2 * self.Y
            # messaging model
            if self.msg_model != "none":
                out_dim += self.msg_hdim
        else:
            # otherwise, project them all to h_dim
            NUM_INPUTS = 4 if self.msg_model != "none" else 3
            project_hdim = flags.equalize_factor * self.h_dim
            out_dim = project_hdim * NUM_INPUTS

            # set up linear layers for projections
            self.project_feature_dim = nn.Linear(self.k_dim, project_hdim)
            self.project_glyph_dim = nn.Linear(
                self.H * self.W * self.Y, project_hdim
            )
            c__2 = self.crop_dim ** 2
            if self.crop_model == "transformer":
                self.project_crop_dim = nn.Linear(c__2 * K, project_hdim)
            elif self.crop_model == "cnn":
                self.project_crop_dim = nn.Linear(c__2 * self.Y, project_hdim)
            if self.msg_model != "none":
                self.project_msg_dim = nn.Linear(self.msg_hdim, project_hdim)

        self.fc = nn.Sequential(
            nn.Linear(out_dim, self.h_dim),
            nn.ReLU(),
            nn.Linear(self.h_dim, self.h_dim),
            nn.ReLU(),
        )

    def prepare_input(self, inputs):
        # -- [B x H x W]
        B, H, W = inputs["glyphs"].shape

        # take our chosen glyphs and merge the time and batch

        glyphs = self.glyph_embedding.prepare_input(inputs)

        # -- [B x F]
        features = inputs["blstats"]

        return glyphs, features

    def forward(self, inputs):
        B, *_ = inputs["glyphs"].shape

        glyphs, features = self.prepare_input(inputs)

        # -- [B x 2] x,y coordinates
        coordinates = features[:, :2]

        # -- [B x K]
        features_emb = self.embed_features(features)
        if self.equalize_input_dim:
            features_emb = self.project_feature_dim(features_emb)

        assert features_emb.shape[0] == B

        reps = [features_emb]  # either k_dim or project_hdim

        # -- [B x H' x W']
        crop = self.glyph_embedding.GlyphTuple(
            *[self.crop(g, coordinates) for g in glyphs]
        )
        # -- [B x H' x W' x K]
        crop_emb = self.glyph_embedding(crop)

        if self.crop_model == "transformer":
            # -- [B x W' x H' x K]
            crop_rep = self.extract_crop_representation(crop_emb, mask=None)
        elif self.crop_model == "cnn":
            # -- [B x K x W' x H']
            crop_emb = crop_emb.transpose(1, 3)
            # -- [B x W' x H' x K]
            crop_rep = self.extract_crop_representation(crop_emb)

        # -- [B x K']
        crop_rep = crop_rep.view(B, -1)
        if self.equalize_input_dim:
            crop_rep = self.project_crop_dim(crop_rep)
        assert crop_rep.shape[0] == B

        reps.append(crop_rep)  # either k_dim or project_hdim

        # -- [B x H x W x K]
        glyphs_emb = self.glyph_embedding(glyphs)
        # glyphs_emb = self.embed(glyphs)
        # -- [B x K x W x H]
        glyphs_emb = glyphs_emb.transpose(1, 3)
        # -- [B x W x H x K]
        glyphs_rep = self.extract_representation(glyphs_emb)

        # -- [B x K']
        glyphs_rep = glyphs_rep.view(B, -1)
        # -- [B x K']
        if self.equalize_input_dim:
            glyphs_rep = self.project_glyph_dim(glyphs_rep)

        assert glyphs_rep.shape[0] == B

        # -- [B x K'']
        reps.append(glyphs_rep)

        # MESSAGING MODEL
        if self.msg_model != "none":
            messages = inputs["message"].long()
            if self.msg_model == "cnn":
                # convert messages to one-hot, [B x 96 x 256]
                one_hot = F.one_hot(messages, num_classes=NUM_CHARS).transpose(
                    1, 2
                )
                char_rep = self.conv2_6_fc(self.conv1(one_hot.float()))
            elif self.msg_model == "lt_cnn":
                # [B x E x 256 ]
                char_emb = self.char_lt(messages).transpose(1, 2)
                char_rep = self.conv2_6_fc(self.conv1(char_emb))
            else:  # lstm, gru
                char_emb = self.char_lt(messages)
                output = self.char_rnn(char_emb)[0]
                fwd_rep = output[:, -1, : self.h_dim // 2]
                bwd_rep = output[:, 0, self.h_dim // 2 :]
                char_rep = torch.cat([fwd_rep, bwd_rep], dim=1)

            if self.equalize_input_dim:
                char_rep = self.project_msg_dim(char_rep)
            reps.append(char_rep)

        st = torch.cat(reps, dim=1)

        # -- [B x K]
        st = self.fc(st)

        return st


class RLLibNLENetwork(TorchModelV2, nn.Module):
    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        num_outputs: Optional[int],
        model_config: dict,
        name: str,
        **kwargs: Any,
    ):
        TorchModelV2.__init__(
            self,
            observation_space,
            action_space,
            num_outputs,
            model_config,
            name,
        )
        nn.Module.__init__(self)

        flags = model_config["custom_model_config"]["flags"]
        self.num_outputs = num_outputs or flags.hidden_dim

        self.base = BaseNet(observation_space, flags)  # device is sorted later

    @override(TorchModelV2)
    def forward(self, x: Dict[str, Any], *_: Any) -> Tuple[torch.Tensor, list]:
        return self.base(x["obs"]), []


ModelCatalog.register_custom_model("rllib_nle_model", RLLibNLENetwork)
