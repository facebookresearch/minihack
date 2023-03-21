# Corridor

These tasks make use of the `RANDOM_CORRIDORS`
command in the `des-file`. The objective is to reach the staircase located in one of the randomly generated rooms. The rooms have randomised positions and sizes. The corridors
between the rooms are procedurally generated and are different for every
episodes.

Different variants of this environment have different numbers of
rooms, making the exploration challenge more difficult (`MiniHack-Corridor-R2-v0`,
`MiniHack-Corridor-R3-v0`, and `MiniHack-Corridor-R5-v0` environments are composed of 2,
3, and 5 rooms, respectively).

Examples of the `MiniHack-Corridor-R5-v0` task:

![](../imgs/corridors.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/corridor.py)

## All Environments

| Name                      | Capability  |
| ------------------------- | ----------- |
| `MiniHack-Corridor-R2-v0` | Exploration |
| `MiniHack-Corridor-R3-v0` | Exploration |
| `MiniHack-Corridor-R5-v0` | Exploration |
