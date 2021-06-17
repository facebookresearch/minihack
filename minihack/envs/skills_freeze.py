# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from gym.envs import registration

freeze_msgs = [
    "The bolt of cold bounces!",  # checks if cold bounces from the wall
]


class MiniHackFreeze(MiniHackSkill):
    def __init__(self, *args, des_file, **kwargs):
        rwrd_mngr = RewardManager()
        rwrd_mngr.add_message_event(freeze_msgs)

        super().__init__(*args, des_file=des_file, reward_manager=rwrd_mngr, **kwargs)


class MiniHackFreezeWand(MiniHackFreeze):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=8, h=8, lit=True)
        lvl_gen.add_object("cold", "/", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeHorn(MiniHackFreeze):
    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=8, h=8, lit=True)
        lvl_gen.add_object("frost horn", "(", cursestate="blessed")
        des_file = lvl_gen.get_des()

        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeRandom(MiniHackFreeze):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
MESSAGE: "Welcome to MiniHack!"
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
........
........
........
........
........
........
........
........
ENDMAP
REGION:(0,0,7,7),lit,"ordinary"
IF [50%] {
    OBJECT:('/',"cold"),random,blessed
} ELSE {
    OBJECT:('(',"frost horn"),random,blessed
}
"""
        super().__init__(*args, des_file=des_file, **kwargs)


class MiniHackFreezeLava(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        des_file = """
MAZE: "mylevel", ' '
FLAGS:hardfloor
INIT_MAP: solidfill,' '
GEOMETRY:center,center
MAP
-------------
|.....L.....|
|.....L.....|
|.....L.....|
|.....L.....|
|.....L.....|
-------------
ENDMAP
REGION:(0,0,12,6),lit,"ordinary"
$left_bank = selection:fillrect (1,1,5,5)
$right_bank = selection:fillrect (7,1,11,5)
IF [50%] {
    # wand of cold
    OBJECT:('/',"cold"),rndcoord($left_bank),blessed
} ELSE {
    # frost horn
    OBJECT:('(',"frost horn"),rndcoord($left_bank),blessed
}
BRANCH:(1,1,5,5),(0,0,0,0)
STAIR:rndcoord($right_bank),down
"""
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Freeze-Wand-v0",
    entry_point="minihack.envs.skills_freeze:MiniHackFreezeWand",
)
registration.register(
    id="MiniHack-Freeze-Horn-v0",
    entry_point="minihack.envs.skills_freeze:MiniHackFreezeHorn",
)
registration.register(
    id="MiniHack-Freeze-Random-v0",
    entry_point="minihack.envs.skills_freeze:MiniHackFreezeRandom",
)
registration.register(
    id="MiniHack-Freeze-Lava-v0",
    entry_point="minihack.envs.skills_freeze:MiniHackFreezeLava",
)
