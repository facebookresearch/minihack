# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill
from gym.envs import registration


class MiniHackQuestEasy(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 500)
        kwargs["autopickup"] = kwargs.pop("autopickup", True)
        super().__init__(*args, des_file="quest_easy.des", **kwargs)


class MiniHackQuestMedium(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        kwargs["character"] = "kni-hum-law-fem"  # tested on human knight
        kwargs["autopickup"] = kwargs.pop("autopickup", True)
        super().__init__(*args, des_file="quest_medium.des", **kwargs)


class MiniHackQuestHard(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        super().__init__(*args, des_file="quest_hard.des", **kwargs)


registration.register(
    id="MiniHack-Quest-Easy-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestEasy",
)
registration.register(
    id="MiniHack-Quest-Medium-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestMedium",
)
registration.register(
    id="MiniHack-Quest-Hard-v0",
    entry_point="minihack.envs.skills_quest:MiniHackQuestHard",
)
