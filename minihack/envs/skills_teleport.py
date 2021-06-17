# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration


class MiniHackTeleport(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(["Do you wish to teleport?"])

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackTeleportScroll(MiniHackTeleport):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("teleportation", "?", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackTeleportRing(MiniHackTeleport):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("teleportation", "=", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackTeleportWand(MiniHackTeleport):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("teleportation", "/", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackTeleportRandom(MiniHackTeleport):
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
IF [33%] {
    OBJECT:('/',"teleportation"),random,blessed
} ELSE {
    IF [33%] {
        OBJECT:('=',"teleportation"),random,blessed
    } ELSE {
        OBJECT:('?',"teleportation"),random,blessed
    }
}
"""
        for _ in range(n_distract):
            des_file += "OBJECT:random,random\n"
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackTeleportRandomDist(MiniHackTeleportRandom):
    def __init__(self, *args, n_distract=3, **kwargs):
        super().__init__(n_distract)


registration.register(
    id="MiniHack-Teleport-Scroll-v0",
    entry_point="minihack.envs.skills_teleport:MiniHackTeleportScroll",
)
registration.register(
    id="MiniHack-Teleport-Ring-v0",
    entry_point="minihack.envs.skills_teleport:MiniHackTeleportRing",
)
registration.register(
    id="MiniHack-Teleport-Wand-v0",
    entry_point="minihack.envs.skills_teleport:MiniHackTeleportWand",
)
registration.register(
    id="MiniHack-Teleport-Random-v0",
    entry_point="minihack.envs.skills_teleport:MiniHackTeleportRandom",
)
registration.register(
    id="MiniHack-Teleport-Random-Distract-v0",
    entry_point="minihack.envs.skills_teleport:MiniHackTeleportRandomDist",
)
