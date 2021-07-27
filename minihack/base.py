# Copyright (c) Facebook, Inc. and its affiliates.

import os
import subprocess
import random

import gym
import numpy as np
import pkg_resources
from nle import _pynethack, nethack
from nle.nethack.nethack import SCREEN_DESCRIPTIONS_SHAPE
from nle.env.base import FULL_ACTIONS, NLE_SPACE_ITEMS
from nle.env.tasks import NetHackStaircase
from minihack.wiki import NetHackWiki
from minihack.tiles import GlyphMapper

PATH_DAT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dat")
LIB_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
PATCH_SCRIPT = os.path.join(
    pkg_resources.resource_filename("minihack", "scripts"),
    "mh_patch_nhdat.sh",
)
MH_FULL_ACTIONS = list(FULL_ACTIONS)
# MH_FULL_ACTIONS.remove(nethack.MiscDirection.DOWN)
MH_FULL_ACTIONS.remove(nethack.MiscDirection.UP)
MH_FULL_ACTIONS = tuple(MH_FULL_ACTIONS)
HACKDIR = os.getenv(
    "HACKDIR", pkg_resources.resource_filename("nle", "nethackdir")
)

RGB_MAX_VAL = 255
N_TILE_PIXEL = 16

MH_NETHACKOPTIONS = (
    "color",  # Display color for different monsters, objects, etc
    "showexp",  # Display the experience points on the status line
    "nobones",  # Disallow saving and loading bones files
    "nolegacy",  # Not display an introductory message when starting the game
    "nocmdassist",  # No command assistance
    "disclose:+i +a +v +g +c +o",  # End of game prompt replies
    "runmode:teleport",  # Update the map after movement has finished
    "mention_walls",  # Give feedback when walking against a wall
    "nosparkle",  # Not display sparkly effect for resisted magical attacks
    "showscore",  # Shows approximate accumulated score on the bottom line
    "pettype:none",  # No pet
)
# Autopickup on by default (all items)
# Manually adding "!autopickup" basen of env flag

MINIHACK_SPACE_FUNCS = {
    "glyphs_crop": lambda x, y: gym.spaces.Box(
        low=0, high=nethack.MAX_GLYPH, shape=(x, y), dtype=np.uint16
    ),
    "chars_crop": lambda x, y: gym.spaces.Box(
        low=0, high=255, shape=(x, y), dtype=np.uint8
    ),
    "colors_crop": lambda x, y: gym.spaces.Box(
        low=0, high=15, shape=(x, y), dtype=np.uint8
    ),
    "specials_crop": lambda x, y: gym.spaces.Box(
        low=0, high=255, shape=(x, y), dtype=np.uint8
    ),
    "tty_chars_crop": lambda x, y: gym.spaces.Box(
        low=0, high=255, shape=(x, y), dtype=np.uint8
    ),
    "tty_colors_crop": lambda x, y: gym.spaces.Box(
        low=0, high=31, shape=(x, y), dtype=np.uint8
    ),
    "screen_descriptions_crop": lambda x, y: gym.spaces.Box(
        low=0,
        high=127,
        shape=(x, y, _pynethack.nethack.NLE_SCREEN_DESCRIPTION_LENGTH),
        dtype=np.uint8,
    ),
    "pixel_crop": lambda x, y: gym.spaces.Box(
        low=0,
        high=RGB_MAX_VAL,
        shape=(x * N_TILE_PIXEL, y * N_TILE_PIXEL, 3),
        dtype=np.uint8,
    ),
}

MH_DEFAULT_OBS_KEYS = (
    "glyphs",
    "chars",
    "colors",
    "specials",
    "glyphs_crop",
    "chars_crop",
    "colors_crop",
    "specials_crop",
    "blstats",
    "message",
)


class MiniHack(NetHackStaircase):
    def __init__(
        self,
        *args,
        des_file: str,
        reward_win=1,
        reward_lose=0,
        obs_crop_h=9,
        obs_crop_w=9,
        obs_crop_pad=0,
        reward_manager=None,
        use_wiki=False,
        autopickup=True,
        observation_keys=MH_DEFAULT_OBS_KEYS,
        seeds=None,
        **kwargs,
    ):
        # NetHack options
        options = MH_NETHACKOPTIONS
        if not autopickup:
            options += ("!autopickup",)
        kwargs["options"] = kwargs.pop("options", options)
        # Actions space - move only
        kwargs["actions"] = kwargs.pop("actions", MH_FULL_ACTIONS)

        # Enter Wizard mode - turned off by default
        kwargs["wizard"] = kwargs.pop("wizard", False)
        # Allowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop(
            "allow_all_yn_questions", True
        )
        # Episode limit
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        # Not saving NLE data by detauls
        kwargs["savedir"] = kwargs.pop("savedir", None)
        # Not spawning random monsters
        kwargs["spawn_monsters"] = kwargs.pop("spawn_monsters", False)

        # MiniHack's observation keys are kept separate
        self._minihack_obs_keys = observation_keys
        # Handle RGB pixel observations
        if any("pixel" in key for key in self._minihack_obs_keys):
            self._glyph_mapper = GlyphMapper()
            if "pixel_crop" in self._minihack_obs_keys:
                # Make sure glyphs_crop is there
                self._minihack_obs_keys.append("glyphs_crop")

        self.reward_manager = reward_manager
        if self.reward_manager is not None:
            self.reward_manager.reset()

        self._level_seeds = seeds

        super().__init__(*args, **kwargs)

        # Patch the nhdat library by compling the given .des file
        self.update(des_file)

        self.obs_crop_h = obs_crop_h
        self.obs_crop_w = obs_crop_w
        self.obs_crop_pad = obs_crop_pad

        assert self.obs_crop_h % 2 == 1
        assert self.obs_crop_w % 2 == 1

        self.reward_win = reward_win
        self.reward_lose = reward_lose

        self._scr_descr_index = self._observation_keys.index(
            "screen_descriptions"
        )
        self.observation_space = gym.spaces.Dict(
            self.get_obs_space_dict(dict(NLE_SPACE_ITEMS))
        )

        self.use_wiki = use_wiki
        if self.use_wiki:
            self.wiki = NetHackWiki()

    def get_obs_space_dict(self, space_dict):
        obs_space_dict = {}
        for key in self._minihack_obs_keys:
            if key in space_dict.keys():
                obs_space_dict[key] = space_dict[key]
            elif key in MINIHACK_SPACE_FUNCS.keys():
                space_func = MINIHACK_SPACE_FUNCS[key]
                obs_space_dict[key] = space_func(
                    self.obs_crop_h, self.obs_crop_w
                )
            else:
                if "pixel" in self._minihack_obs_keys:
                    d_shape = nethack.OBSERVATION_DESC["glyphs"]["shape"]
                    shape = (
                        d_shape[0] * N_TILE_PIXEL,
                        d_shape[1] * N_TILE_PIXEL,
                        3,
                    )
                    obs_space_dict["pixel"] = gym.spaces.Box(
                        low=0,
                        high=RGB_MAX_VAL,
                        shape=shape,
                        dtype=np.uint8,
                    )
                else:
                    raise ValueError(
                        f'Observation key "{key}" is not supported'
                    )

        return obs_space_dict

    def reset(self, *args, **kwargs):
        if self.reward_manager is not None:
            self.reward_manager.reset()
        if self._level_seeds is not None:
            seed = random.choice(self._level_seeds)
            self.seed(seed, seed, reseed=False)
        return super().reset(*args, **kwargs)

    def _reward_fn(self, last_observation, action, observation, end_status):
        """Use reward_manager to collect reward calculated in _is_episode_end,
        or revert to standard sparse reward."""
        del action  # Unused
        if self.reward_manager is not None:
            reward = self.reward_manager.collect_reward()
        else:
            if end_status == self.StepStatus.TASK_SUCCESSFUL:
                reward = self.reward_win
            elif end_status == self.StepStatus.RUNNING:
                reward = 0
            else:  # death or aborted
                reward = self.reward_lose
        return reward + self._get_time_penalty(last_observation, observation)

    def step(self, action: int):
        self._previous_obs = tuple(a.copy() for a in self.last_observation)
        self._previous_action = action
        # Within this call, _is_episode_end is called and then _reward_fn,
        # both using self.reward_manager
        return super().step(action)

    def _is_episode_end(self, observation):
        if self.reward_manager is not None:
            # This also calculates reward, to be collected in _reward_fn by
            # collect_reward
            result = self.reward_manager.check_episode_end_call(
                self, self._previous_obs, self._previous_action, observation
            )
            if result:
                return self.StepStatus.TASK_SUCCESSFUL

        # Revert to staircase check (so we always end if we reach it)
        return super()._is_episode_end(observation)

    def update(self, des_file):
        """Update the current environment by replacing its description file"""
        self._patch_nhdat(des_file)

    def _patch_nhdat(self, des_file):
        """Patch the nhdat library. This includes compiling the given
        description file and replacing the new nhdat file in the temporary
        hackdir directory of the environment.
        """
        if not des_file.endswith(".des"):
            fpath = os.path.join(self.env._vardir, "mylevel.des")
            # If the des-file is passed as a string
            with open(fpath, "w") as f:
                f.writelines(des_file)
            des_file = fpath

        # Use the .des file if exists, otherwise search in minihack directory
        des_path = os.path.abspath(des_file)
        if not os.path.exists(des_path):
            des_path = os.path.abspath(os.path.join(PATH_DAT_DIR, des_file))
        if not os.path.exists(des_path):
            print(
                "{} file doesn't exist. Please provide a path to a valid .des \
                    file".format(
                    des_path
                )
            )
        try:
            _ = subprocess.call(
                [
                    PATCH_SCRIPT,
                    self.env._vardir,
                    HACKDIR,
                    LIB_DIR,
                    des_path,
                ]
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Couldn't patch the nhdat file.\n{e}")

    def _get_observation(self, observation):
        # Filter out observations that we don't need
        observation = super()._get_observation(observation)
        obs_dict = {}
        for key in self._minihack_obs_keys:
            if "pixel" in key:
                continue
            if key in self._observation_keys:
                obs_dict[key] = observation[key]
            elif key in MINIHACK_SPACE_FUNCS.keys():
                orig_key = key.replace("_crop", "")
                if "tty" in orig_key:
                    loc = observation["tty_cursor"][::-1]
                else:
                    loc = observation["blstats"][:2]
                obs_dict[key] = self._crop_observation(
                    observation[orig_key], loc
                )

        if "pixel" in self._minihack_obs_keys:
            obs_dict["pixel"] = self._glyph_mapper.to_rgb(
                observation["glyphs"]
            )

        if "pixel_crop" in self._minihack_obs_keys:
            obs_dict["pixel_crop"] = self._glyph_mapper.to_rgb(
                obs_dict["glyphs_crop"]
            )

        return obs_dict

    def _crop_observation(self, obs, loc):
        dh = self.obs_crop_h // 2
        dw = self.obs_crop_w // 2

        (x, y) = loc
        x += dw
        y += dh

        obs = np.pad(
            obs,
            pad_width=(dw, dh),
            mode="constant",
            constant_values=self.obs_crop_pad,
        )
        return obs[y - dh : y + dh + 1, x - dw : x + dw + 1]

    def key_in_inventory(self, name):
        """Returns key of the object in the inventory.

        Arguments:
            name [str]: name of the object
        Returns:
            the key of the first item in the inventory that includes the
            argument name as a substring
        """
        assert "inv_strs" in self._observation_keys
        assert "inv_letters" in self._observation_keys

        inv_strs_index = self._observation_keys.index("inv_strs")
        inv_letters_index = self._observation_keys.index("inv_letters")

        inv_strs = self.last_observation[inv_strs_index]
        inv_letters = self.last_observation[inv_letters_index]

        for letter, line in zip(inv_letters, inv_strs):
            if np.all(line == 0):
                break
            if name in line.tobytes().decode("utf-8"):
                return letter.tobytes().decode("utf-8")

        return None

    def index_to_dir_action(self, index):
        """Returns the ASCII code for direction corresponding to given
        index in reshaped vector of adjacent 9 tiles (None for agent's
        position).
        """
        assert 0 <= index < 9
        index_to_dir_dict = {
            0: ord("y"),
            1: ord("k"),
            2: ord("u"),
            3: ord("h"),
            4: None,
            5: ord("l"),
            6: ord("b"),
            7: ord("j"),
            8: ord("n"),
        }
        return index_to_dir_dict[index]

    def get_direction_obj(self, name, observation=None):
        """Find the game direction of the (first) object in neighboring nine
        tiles that contains given name in its description.
        Return None if not found.
        """
        if observation is None:
            observation = self.last_observation

        neighbors = self.get_neighbor_descriptions(observation)
        for i, tile_description in enumerate(neighbors):
            if name in tile_description:
                return self.index_to_dir_action(i)
        return None

    def get_neighbor_descriptions(self, observation=None):
        """Returns the description of nine neighboring glyphs of the agent."""
        if observation is None:
            observation = self.last_observation
        blstats = observation[self._blstats_index]
        x, y = blstats[:2]

        neighbors = [
            self.get_screen_description(i, j, observation)
            for j in range(y - 1, y + 2)
            for i in range(x - 1, x + 2)
        ]
        return neighbors

    def get_neighbor_wiki_pages(self, observation=None):
        if not self.use_wiki:
            raise NotImplementedError(
                "use_wiki is set to false - initialise your environment with"
                "use_wiki=True to use the wiki"
            )
        neighbors_descriptions = self.get_neighbor_descriptions(observation)
        neighbor_pages = [
            self.wiki.get_page_text(description)
            for description in neighbors_descriptions
        ]
        return neighbor_pages

    def get_screen_description(self, x, y, observation=None):
        """Returns the description of the screen on (x,y) coordinates."""
        if observation is None:
            observation = self.last_observation

        des_arr = observation[self._scr_descr_index][y, x]
        symb_len = np.where(des_arr == 0)[0][0]

        return des_arr[:symb_len].tobytes().decode("utf-8")

    def get_screen_wiki_page(self, x, y, observation=None):
        """Returns the wiki page matching the object on (x,y) coordinates."""
        if not self.use_wiki:
            raise NotImplementedError(
                "use_wiki is set to false - initialise your environment with"
                "use_wiki=True to use the wiki"
            )
        description = self.get_screen_description(x, y, observation)
        return self.wiki.get_page_text(description)

    def screen_contains(self, name, observation=None):
        """Whether the given name is included in screen descriptions of
        the observations.
        """
        if observation is None:
            observation = self.last_observation

        y, x = SCREEN_DESCRIPTIONS_SHAPE[0:2]
        for j in range(y):
            for i in range(x):
                des_arr = observation[self._scr_descr_index][j, i]
                symb_len = np.where(des_arr == 0)[0][0]
                if name in des_arr[:symb_len].tobytes().decode("utf-8"):
                    return True
        return False
