# Creating New Environments

## Overview

Creating new environments using MiniHack is very simple. There are two main MiniHack base classes to chose from.

[MiniHackNavigation](../api/minihack.html#minihack.MiniHackNavigation) ba can be used to design mazes and navigation tasks that only require a small action space. All MiniHack navigation tasks make use of the MiniHackNavigation interface. The in-game multiple-choice question prompts, which are used for interacting with objects and using the inventory, are turned off by default here.

[MiniHackSkill](../api/minihack.html#minihack.MiniHackSkill) provides a convenient mean for designing diverse skill acquisition tasks that require a large action space, interactions with objects and more complex goals. All skill acquisition tasks in MiniHack use this base class. The in-game multiple-choice question prompts is turned on by default.

The quickest way for creating a new environment is to use `gym.make` and pass the description file to the environment:
```python
import gym
import minihack
des_file = """
MAZE: "mylevel",' '
GEOMETRY:center,center
MAP
-------------
|.....|.....|
|.....|.....|
|.....+.....|
|.....|.....|
|.....|.....|
-------------
ENDMAP
REGION:(0,0,12,6),lit,"ordinary"
BRANCH:(1,1,6,6),(0,0,0,0)
DOOR:locked,(6,3)
STAIR:(8,3),down
"""
env = gym.make(
    "MiniHack-Navigation-Custom-v0",
    des_file=des_file,
    max_episode_steps=50,
)
```

Additional parameters for the environment can also be passed to `gym.make`, such as `observation_keys`, etc.
By default, the goal of the agent is to reach the stair down. However, reward functions in MiniHack can easily be configured. See [here](../reward) for more information.

Alternatively, the users can subclass either [MiniHackNavigation](../api/minihack.html#minihack.MiniHackNavigation) or [MiniHackSkill](../api/minihack.html#minihack.MiniHackSkill) classes.

```python
from minihack import MiniHackNavigation
from gym.envs import registration

class MiniHackNewTask(MiniHackNavigation):
    def __init__(self, *args, des_file, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        super().__init__(*args, des_file=des_file, **kwargs)

registration.register(
    id="MiniHack-NewTask-v0",
    entry_point="path.to.file:MiniHackNewTask", # use the actual the path
)
```

For information about the description files, check out our [brief overview](./des_files), [detailed tutorial](../tutorials/des_file/index) or [community wiki](https://nethackwiki.com/wiki/Des-file_format).

## Level Generator

When creating a new MiniHack environment, a description file must be provided. One way of providing this des-file is writing it entirely from scratch. However, this requires learning the des-file format and is more difficult to do programmatically, so as part of MiniHack we provide the [LevelGenerator](../api/minihack.html#minihack.LevelGenerator) class which provides a convenient wrapper around writing a des-file. The `LevelGenerator` class can be used to create MAZE-type levels with specified heights and widths, and can then fill those levels with objects, monsters and terrain, and specify the start point of the level. Combined with the [RewardManager](../api/minihack.html#minihack.RewardManager) which handles rewards, this enables flexible creation of a wide variety of environments.

The level generator can start with either an empty maze (in which case only height and width are specified, see [Example 1](#example-1)) or with a pre-drawn map (see [Example 2](#example-2)). After initialisation, the level generator can be used to add objects, traps, monsters and other terrain features. Terrain can also be added (\cref{code:python} line 9). Once the level is complete, the `get_des()` function returns the des-file which can then be passed to the environment creation.

[Example 1](#example-1) shows how to create a simple skill acquisition task that challenges the agent to eat an apple and wield a dagger that is randomly placed in a 10x10 room surrounded by lava, alongside a goblin and a teleportation trap. Here, a [RewardManager](../api/minihack.html#minihack.RewardManager) is used to specify the tasks that need to be completed.

[Example 2](#example-2) illustrates how to create a labyrinth task. Here, the agent starts near the entrance of a maze and needs to reach its centre. A Minotaur is placed deep inside the maze, which is a powerful monster capable of instantly killing the agent in melee combat. There is a wand of death placed in a random location in the maze. The agent needs to pick it up, and upon seeing the Minotaur, zap it in the direction of the monster. Once the Minotaur is killed, the agent needs to navigate itself towards the staircase (this is the default goal when `RewardManager` is not used). Tools such as [Monodraw](https://monodraw.helftone.com) can help draw the map layout.

## Examples

### Example 1

Creating a skill task using the [LevelGenerator](../api/minihack.html#minihack.LevelGenerator) and [RewardManager](../api/minihack.html#minihack.RewardManager).

```python
# Define a 10x10 room and populate it with
# different objects, monster and features
lvl_gen = LevelGenerator(w=10, h=10)
lvl_gen.add_object("apple", "%")
lvl_gen.add_object("dagger", ")")
lvl_gen.add_trap(name="teleport")
lvl_gen.add_sink()
lvl_gen.add_monster("goblin")
lvl_gen.fill_terrain("rect",
    0, 0, 9, 9, flag="L")

# Define a reward manager
reward_gen = RewardManager()
# +1 reward and termination for eating
# an apple or wielding a dagger
reward_gen.add_eat_event("apple")
reward_gen.add_wield_event("dagger")
# -1 reward for standing on a sink
# but isn't required for terminating
# the episode
reward_gen.add_location_event("sink",
    reward=-1, terminal_required=False)

env = gym.make(
    "MiniHack-Skill-Custom-v0",
    def_file=lvl_gen.get_des(),
    reward_manager=reward_manager,
)
```

### Example 2

Creating a MiniHack skill task using [LevelGenerator](../api/minihack.html#minihack.LevelGenerator) with a pre-defined map layout.

```python
# Define the maze as a string
maze = """
--------------------
|.......|.|........|
|.-----.|.|.-----|.|
|.|...|.|.|......|.|
|.|.|.|.|.|-----.|.|
|.|.|...|....|.|.|.|
|.|.--------.|.|.|.|
|.|..........|...|.|
|.|--------------|.|
|..................|
--------------------
"""
# Set a start and goal positions
lvl_gen = LevelGenerator(map=maze)
lvl_gen.set_start_pos((9, 1))
lvl_gen.add_goal_pos((14, 5))
# Add a Minotaur at fixed position
lvl_gen.add_monster(name="minotaur",
    place=(19, 9))
# Add wand of death
lvl_gen.add_object("death", "/")

env = gym.make(
    "MiniHack-Skill-Custom-v0",
    def_file = lvl_gen.get_des(),
)
```
