# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack.envs import register


class MiniHackHideAndSeekMapped(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, des_file="hidenseek_mapped.des", **kwargs)


class MiniHackHideAndSeek(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, des_file="hidenseek.des", **kwargs)


class MiniHackHideAndSeekLava(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, des_file="hidenseek_lava.des", **kwargs)


class MiniHackHideAndSeekBig(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        super().__init__(*args, des_file="hidenseek_big.des", **kwargs)


register(
    id="MiniHack-HideNSeek-Mapped-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekMapped",
)
register(
    id="MiniHack-HideNSeek-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeek",
)
register(
    id="MiniHack-HideNSeek-Lava-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekLava",
)
register(
    id="MiniHack-HideNSeek-Big-v0",
    entry_point="minihack.envs.hidenseek:MiniHackHideAndSeekBig",
)
