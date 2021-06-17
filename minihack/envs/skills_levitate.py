# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration


levitation_msg = [
    "You float up",
    "You start to float in the air",
    "Up, up, and awaaaay!",
    "a ring of levitation (on left hand)",
    "a ring of levitation (on right hand)",
]


class MiniHackLevitate(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(levitation_msg)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackLevitateBoots(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation boots", "[", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateBootsFixed(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation boots", "[", place=(0, 0), cursestate="blessed")
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateRing(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "=", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateRingFixed(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "=", place=(0, 0), cursestate="blessed")
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitatePotion(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "!", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitatePotionFixed(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("levitation", "!", place=(0, 0), cursestate="blessed")
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackLevitateRandom(MiniHackLevitate):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
.....
.....
.....
.....
.....
ENDMAP
REGION:(0,0,5,5),lit,"ordinary"
IF [33%] {
    OBJECT:('!',"levitation"),random,blessed
} ELSE {
    IF [50%] {
        OBJECT:('=',"levitation"),random,blessed
    } ELSE {
        OBJECT:('[',"levitation boots"),random,blessed
    }
}
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Levitate-Boots-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitateBoots",
)
registration.register(
    id="MiniHack-Levitate-Ring-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitateRing",
)
registration.register(
    id="MiniHack-Levitate-Potion-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitatePotion",
)
registration.register(
    id="MiniHack-Levitate-Random-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitateRandom",
)
registration.register(
    id="MiniHack-Levitate-Boots-Fixed-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitateBootsFixed",
)
registration.register(
    id="MiniHack-Levitate-Ring-Fixed-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitateRingFixed",
)
registration.register(
    id="MiniHack-Levitate-Potion-Fixed-v0",
    entry_point="minihack.envs.skills_levitate:MiniHackLevitatePotionFixed",
)
