# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration

invis_msgs = [
    "All of a sudden, you can't see yourself",
    "a ring of invisibility (on left hand)",
    "a ring of invisibility (on right hand)",
    "You are now wearing a cloak of invisibility",
]


class MiniHackInvis(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(invis_msgs)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackInvisPotion(MiniHackInvis):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("invisibility", "!", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackInvisRing(MiniHackInvis):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("invisibility", "=", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackInvisWand(MiniHackInvis):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("make invisible", "/", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackInvisCloak(MiniHackInvis):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("cloak of invisibility", "[", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackInvisRandom(MiniHackInvis):
    def __init__(self, *args, n_distract=0, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
MESSAGE: "Welcome to MiniHack!"
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
IF [25%] {
    OBJECT:('[',"cloak of invisibility"),random,blessed
} ELSE {
    IF [25%] {
        OBJECT:('/',"make invisible"),random,blessed
    } ELSE {
        IF [25%] {
            OBJECT:('=',"invisibility"),random,blessed
        } ELSE {
            OBJECT:('!',"invisibility"),random,blessed
        }
    }
}
"""
        for _ in range(n_distract):
            des_file += "OBJECT:random,random\n"
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackInvisRandomDist(MiniHackInvisRandom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, n_distract=3, **kwargs)


registration.register(
    id="MiniHack-Invis-Potion-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisPotion",
)
registration.register(
    id="MiniHack-Invis-Ring-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisRing",
)
registration.register(
    id="MiniHack-Invis-Wand-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisWand",
)
registration.register(
    id="MiniHack-Invis-Cloak-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisCloak",
)
registration.register(
    id="MiniHack-Invis-Random-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisRandom",
)
registration.register(
    id="MiniHack-Invis-Random-Distract-v0",
    entry_point="minihack.envs.skills_invis:MiniHackInvisRandomDist",
)
