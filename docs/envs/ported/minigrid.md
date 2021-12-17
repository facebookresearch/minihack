# MiniGrid

This family of environments is ported to MiniHack from [MiniGrid](https://github.com/maximecb/gym-minigrid), a popular suite of procedurally generated grid-based environments that assess various capabilities of RL agents, such as exploration, memory, and generalisation. For more information, check out [MiniGrid's documentation](https://github.com/maximecb/gym-minigrid/blob/master/README.md).
After porting environments to MiniHack, one can make them substantially harder by adding additional environment dynamics to the task, such as monsters, dungeon features and objects.

The MultiRoom environments have a series of connected rooms. The final room has the goal location the agent needs to get to. We have ported the `MultiRoom` in three different room numbers, namely 2, 4 and 6 rooms. Moreover, we added additional complexity to them by adding monsters (e.g. `MiniHack-MultiRoom-N4-Monster-v0`), locked doors (e.g. `MiniHack-MultiRoom-N4-Locked-v0`), lava tiles instead of walls (e.g. `MiniHack-MultiRoom-N4-Lava-v0`), or all at one (e.g. `MiniHack-MultiRoom-N4-Extreme-v0`).

The LavaCrossing and SimpleCrossing environments require the agent to reach the goal on the other corner in the same room. In the case of LavaCrossing, there are several lava stream running across the room either horizontally or vertically, and only have a single crossing point which can be safely used. The agent needs to avoid the lava which would otherwise it will die immediately. In SimpleCrossing, on the other hand the lava is replaced by the walls.
Several versions of the environments are ported from MiniGrid and provided in the table below.


````{note}
More tasks could have similarly been ported from MiniGrid.
However, our goal was to showcase MiniHack's ability to port existing grid-world environments and easily enrich them, rather then porting all possible tasks.
````

The following figure presents examples of `MiniHack-MultiRoom-N4-v0` and `MiniHack-MultiRoom-N4-Extreme-v0` environments rendered using MiniHack's tiles:

![](./imgs/multiroom.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/tree/main/minihack/envs/minigrid.py)

## All Environments

| Name                               | Capability  |
| ---------------------------------- | ----------- |
| `MiniHack-MultiRoom-N2-v0`         | Exploration |
| `MiniHack-MultiRoom-N4-v0`         | Exploration |
| `MiniHack-MultiRoom-N6-v0`         | Exploration |
| `MiniHack-MultiRoom-N2-Monster-v0` | Exploration |
| `MiniHack-MultiRoom-N4-Monster-v0` | Exploration |
| `MiniHack-MultiRoom-N6-Monster-v0` | Exploration |
| `MiniHack-MultiRoom-N2-Locked-v0`  | Exploration |
| `MiniHack-MultiRoom-N4-Locked-v0`  | Exploration |
| `MiniHack-MultiRoom-N6-Locked-v0`  | Exploration |
| `MiniHack-MultiRoom-N2-Lava-v0`    | Exploration |
| `MiniHack-MultiRoom-N4-Lava-v0`    | Exploration |
| `MiniHack-MultiRoom-N6-Lava-v0`    | Exploration |
| `MiniHack-MultiRoom-N2-Extreme-v0` | Exploration |
| `MiniHack-MultiRoom-N4-Extreme-v0` | Exploration |
| `MiniHack-MultiRoom-N6-Extreme-v0` | Exploration |
| `MiniHack-LavaCrossingS9N1-v0`     | Exploration |
| `MiniHack-LavaCrossingS9N2-v0`     | Exploration |
| `MiniHack-LavaCrossingS9N3-v0`     | Exploration |
| `MiniHack-LavaCrossingS11N5-v0`    | Exploration |
| `MiniHack-SimpleCrossingS9N1-v0`   | Exploration |
| `MiniHack-SimpleCrossingS9N2-v0`   | Exploration |
| `MiniHack-SimpleCrossingS9N3-v0`   | Exploration |
| `MiniHack-SimpleCrossingS11N5-v0`  | Exploration |