# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration

invis_msgs = [
    "All of a sudden, you can't see yourself",
    "a ring of invisibility (on left hand)",
    "a ring of invisibility (on right hand)",
    "You are now wearing a cloak of invisibility",
]


class MiniHackJump(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(invis_msgs)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackJumpBoots(MiniHackJump):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("jumping boots", "[", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackJumpSpell(MiniHackJump):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("jumping", "+", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackJumpRandom(MiniHackJump):
    def __init__(self, *args, n_distract=0, **kwargs):
        des_file = """
MAZE: "mylevel",' '
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
IF [33%] {
    OBJECT:('[',"jumping boots"),random,blessed
} ELSE {
    if [50%] {
        OBJECT:('+',"jumping"),random,blessed
    } ELSE {

    }
}
"""
        for _ in range(n_distract):
            des_file += "OBJECT:random,random\n"
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackJumpRandomDist(MiniHackJumpRandom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, n_distract=3, **kwargs)


registration.register(
    id="MiniHack-Jump-Boots-v0",
    entry_point="minihack.envs.skills_invis:MiniHackJumpBoots",
)
registration.register(
    id="MiniHack-Jump-Spell-v0",
    entry_point="minihack.envs.skills_invis:MiniHackJumpSpell",
)
registration.register(
    id="MiniHack-Jump-Random-v0",
    entry_point="minihack.envs.skills_invis:MiniHackJumpRandom",
)
registration.register(
    id="MiniHack-Jump-Random-Distract-v0",
    entry_point="minihack.envs.skills_invis:MiniHackJumpRandomDist",
)
