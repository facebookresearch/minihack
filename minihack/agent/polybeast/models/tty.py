import torch
from torch import nn
from torch.nn import functional as F
from nle import nethack
from einops import rearrange
from typing import Dict
from nle.agent.polybeast.models.base import NetHackNet
import random
import math

NUM_GLYPHS = nethack.MAX_GLYPH
NUM_FEATURES = nethack.BLSTATS_SHAPE[0]
PAD_CHAR = 0
NUM_CHARS = 256
NUM_COLORS = 32


class BN(nn.Module):
    def __init__(self, channels):
        super(BN, self).__init__()
        self.bn = nn.BatchNorm2d(channels, momentum=0.01)

    def forward(self, x):
        if self.training:
            self.bn(x)
            self.eval()
            x = self.bn(x)
            self.train()
            return x
        else:
            return self.bn(x)


class ConvBlock(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(ConvBlock, self).__init__()

        self.conv1 = nn.Conv2d(
            in_channels, hidden_channels, 1, stride=1, padding=0, bias=False
        )
        self.conv21 = nn.Conv2d(
            hidden_channels,
            hidden_channels,
            [3, 1],
            stride=1,
            padding=[1, 0],
            groups=hidden_channels,
            bias=False,
        )
        self.conv22 = nn.Conv2d(
            hidden_channels,
            hidden_channels,
            [1, 3],
            stride=1,
            padding=[0, 1],
            groups=hidden_channels,
            bias=False,
        )
        self.conv23 = nn.Conv2d(
            hidden_channels,
            hidden_channels,
            [3, 1],
            stride=1,
            padding=[1, 0],
            groups=hidden_channels,
            bias=False,
        )
        self.conv3 = nn.Conv2d(
            hidden_channels, out_channels, 1, stride=1, padding=0, bias=False
        )

        self.bn1 = BN(hidden_channels)
        self.bn21 = BN(hidden_channels)
        self.bn22 = BN(hidden_channels)
        self.bn23 = BN(hidden_channels)
        self.bn3 = BN(out_channels)

        # torch.nn.init.xavier_uniform_(self.conv1.weight, gain=1.0)
        # torch.nn.init.xavier_uniform_(self.conv2.weight, gain=1.0)
        # torch.nn.init.xavier_uniform_(self.conv3.weight, gain=1.0)

    def forward(self, x):
        af = F.celu
        x = af(self.bn1(self.conv1(x)))
        x = af(self.bn21(self.conv21(x)))
        x = af(self.bn22(self.conv22(x)))
        x = af(self.bn23(self.conv23(x)))
        x = self.bn3(self.conv3(x))
        return x


class TtyBaseNet(NetHackNet):
    def __init__(self, observation_shape, num_actions, flags, device):

        super(TtyBaseNet, self).__init__()

        self.flags = flags

        self.observation_shape = observation_shape

        self.H = observation_shape[0]
        self.W = observation_shape[1]

        self.num_actions = num_actions
        self.use_lstm = flags.use_lstm
        self.sigmoid_baseline = flags.sigmoid_baseline
        self.tanh_baseline = flags.tanh_baseline
        self.pool_dim = flags.pool_dim if flags.pool_dim is not None else 1

        self.k_dim = flags.embedding_dim
        self.h_dim = flags.hidden_dim

        self.conv_dim = (
            flags.conv_dim if flags.conv_dim is not None else int(self.h_dim / 4)
        )

        self.is_half = False
        self.forwardcount = 0

        L = flags.layers  # number of convnet layers

        self.use_bn = flags.use_bn
        self.use_temp = flags.use_temp
        self.use_random = flags.use_random

        current_channels = 256 + 32 + 1
        hidden_channels = self.conv_dim
        layers = nn.ModuleList()
        for _i in range(L):
            layer = nn.ModuleDict()
            convs = nn.ModuleList()
            for _i2 in range(2):
                convs.append(
                    ConvBlock(current_channels, hidden_channels * 2, hidden_channels)
                )
                current_channels = hidden_channels
            layer["convs"] = convs
            layers.append(layer)

        self.layers = layers

        K = flags.embedding_dim  # number of input filters
        F = 3  # filter dimensions
        S = 1  # stride
        P = 1  # padding
        # M = 16  # number of intermediate filters
        M = 16
        # self.Y = 8  # number of output filters
        self.Y = 8

        in_channels = [2 * K] + [M] * (L - 1)
        out_channels = [M] * (L - 1) + [self.Y]

        # out_dim = self.H * self.W * self.Y + (9 ** 2) * self.Y

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

        # +2 as we are incorporating cursor position
        # +1 as we incorporate the previous reward
        self.embed_stats = nn.Sequential(
            nn.Linear(NUM_FEATURES + 3, self.k_dim),
            nn.ReLU(),
            nn.Linear(self.k_dim, self.k_dim),
            nn.ReLU(),
        )
        self.embed_colors = nn.Embedding(NUM_COLORS, self.k_dim)
        self.embed_chars = nn.Embedding(NUM_CHARS, self.k_dim)
        self.embed_actions = nn.Embedding(self.num_actions, self.k_dim)
        self.use_index_select = flags.use_index_select

        self.st_fc = nn.Sequential(
            # nn.Linear(self.h_dim + out_dim, self.h_dim),
            nn.Linear(18272, self.h_dim),  # FIXME: calculate
            # nn.Linear(36352, self.h_dim),  # FIXME: calculate
            nn.ReLU(),
            nn.Linear(self.h_dim, self.h_dim),
            nn.ReLU(),
        )

        out_channels = hidden_channels
        if flags.out_channels:
            out_channels = flags.out_channels
            self.out_conv = ConvBlock(hidden_channels, out_channels, out_channels)
            self.out_channels = flags.out_channels

        if flags.use_conv_lstm:
            self.conv_lstm = nn.LSTM(out_channels, out_channels)
            self.fc = nn.Linear(
                out_channels * self.pool_dim * self.pool_dim * 2 * 2, self.h_dim
            )
        else:
            self.fc = nn.Linear(
                out_channels * self.pool_dim * self.pool_dim * 2, self.h_dim
            )

        self.fc2 = nn.Linear(self.h_dim + self.num_actions, self.h_dim)

        if self.use_lstm:
            self.core = nn.LSTM(self.h_dim, self.h_dim, num_layers=1)

        self.policy = nn.Linear(self.h_dim, self.num_actions)
        self.baseline = nn.Linear(self.h_dim, 1)

    def initial_state(self, batch_size=1):
        if not self.use_lstm:
            tup = tuple()
        else:
            tup = tuple(
                torch.zeros(self.core.num_layers, batch_size, self.core.hidden_size)
                for _ in range(2)
            )
        if hasattr(self, "conv_lstm"):
            tup += tuple(
                torch.zeros(1, batch_size, 24, 80, self.conv_lstm.hidden_size)
                for _ in range(2)
            )
        return tup

    def _select(self, embedding_layer, x):
        if self.use_index_select:
            out = embedding_layer.weight.index_select(0, x.view(-1))
            # handle reshaping x to 1-d and output back to N-d
            return out.view(x.shape + (-1,))
        else:
            return embedding_layer(x)

    def to_half(self):
        self.is_half = True
        for layer in self.layers:
            for conv in layer["convs"]:
                conv.half()
            if "bn" in layer:
                layer["bn"].half()
        if hasattr(self, "out_conv"):
            self.out_conv.half()

    def forward(self, inputs: Dict[str, torch.Tensor], core_state, learning=False):
        T, B, H, W = inputs["tty_chars"].shape

        if learning:
            self.train()
        else:
            self.eval()

        chars = inputs["tty_chars"]
        colors = inputs["tty_colors"]
        cursor = inputs["tty_cursor"]
        stats = inputs["blstats"]

        chars_crop = inputs["tty_chars_crop"]
        colors_crop = inputs["tty_colors_crop"]
        _, _, CH, CW = chars_crop.shape
        chars_crop = chars_crop.view(T * B, CH, CW)
        colors_crop = colors_crop.view(T * B, CH, CW)

        at1 = inputs["prev_action"]
        at1 = at1.view(T * B, -1)

        rt1 = inputs["prev_reward"]

        # -- [(T B) K]
        at1 = self._select(self.embed_actions, at1.long()).squeeze(1)

        stats = torch.cat([stats, cursor, rt1], dim=2)
        # -- [(T B) F]
        stats = stats.view(T * B, -1).float()
        # -- [(T B) K]
        stats = self.embed_stats(stats)

        # -- [T B 25 80]
        chars = F.pad(input=chars, pad=(0, 1, 1, 2), mode="constant", value=ord(" "))
        colors = F.pad(input=colors, pad=(0, 1, 1, 2), mode="constant", value=0)

        # -- [(T B) 9 9 K]
        crop_chars = self._select(self.embed_chars, chars_crop.long())
        crop_colors = self._select(self.embed_colors, colors_crop.long())

        # -- [(T B) 9 9 (2 K)]
        ctx = torch.cat([crop_chars, crop_colors], dim=3)

        # -- [(T B) (2 K) 9 9]
        ctx = rearrange(ctx, "B H W K -> B K H W")

        chars = self._select(self.embed_chars, chars.long())
        colors = self._select(self.embed_colors, colors.long())
        # -- [T B 25 80 (2 K)]
        x = torch.cat([chars, colors], dim=4)
        # -- [(T B) (2 K) 25 80]
        x = rearrange(x, "T B H W K -> (T B) K H W")

        x = self.extract_representation(x).reshape(T * B, -1)
        ctx = self.extract_crop_representation(ctx).reshape(T * B, -1)

        # -- [(TB) (h+K)]
        st = torch.cat([x, ctx, stats, at1], dim=1)
        # -- [(T B) h]
        st = self.st_fc(st)

        if self.is_half:
            st = st.float()

        conv_lstm_state = None

        if self.use_lstm:
            core_state = (core_state[0], core_state[1])
            core_input = st.view(T, B, -1)
            core_output_list = []
            notdone = (~inputs["done"]).float()
            for input, nd in zip(core_input.unbind(), notdone.unbind()):
                # Reset core state to zero whenever an episode ended.
                # Make `done` broadcastable with (num_layers, B, hidden_size)
                # states:
                nd = nd.view(1, -1, 1)
                core_state = tuple(nd * t for t in core_state)
                # for v in core_state:
                #    print("core state %g" % v.sum())
                output, core_state = self.core(input.unsqueeze(0).float(), core_state)
                core_output_list.append(output)
            core_output = torch.flatten(torch.cat(core_output_list), 0, 1)
        else:
            core_output = st

        # -- [B x A]
        policy_logits = self.policy(core_output)
        # -- [B x A]
        baseline = self.baseline(core_output)

        if self.sigmoid_baseline:
            baseline = baseline.sigmoid()
        if self.tanh_baseline:
            baseline = baseline.tanh()

        if self.use_temp:
            x = self.forwardcount / 10
            self.forwardcount += 1
            itemp = math.exp(
                (
                    math.sin(x)
                    - math.sin(2 * x) / 2
                    - math.sin(4 * x) / 2
                    - math.sin(x / 8)
                )
                / 6
            )
        else:
            itemp = 0.95
            if self.use_random and random.randint(0, 10) == 0:
                itemp = 0.05

        action = torch.multinomial(
            F.softmax(policy_logits * itemp, dim=1), num_samples=1
        )

        policy_logits = policy_logits.view(T, B, self.num_actions)
        baseline = baseline.view(T, B)
        action = action.view(T, B)

        full_core_state = core_state
        if conv_lstm_state is not None:
            full_core_state += conv_lstm_state

        output = dict(policy_logits=policy_logits, baseline=baseline, action=action)
        return (output, full_core_state)
