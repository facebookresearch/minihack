# Room

These tasks are set in a single square room, where the goal is to reach the
staircase down. There are multiple variants of this level.

There are two sizes
of the room (`5x5, 15x15`). In the simplest variants, (`MiniHack-Room-5x5-v0`
and `MiniHack-Room-15x15-v0`), the start and goal position are fixed. In the
`MiniHack-Room-Random-5x5-v0` and `MiniHack-Room-Random-15x15-v0` tasks, the start and
goal position are randomised. The rest of the variants add additional
complexity to the randomised version of the environment by introducing monsters
(`MiniHack-Room-Monster-5x5-v0` and `MiniHack-Room-Monster-15x15-v0`), teleportation traps
(`MiniHack-Room-Trap-5x5-v0` and `MiniHack-Room-Trap-15x15-v0`), darkness
(`MiniHack-Room-Dark-5x5-v0` and `MiniHack-Room-Dark-15x15-v0`), or all three combined
(`MiniHack-Room-Ultimate-5x5-v0` and `MiniHack-Room-Ultimate-15x15-v0`). The
agent can attack monsters by moving towards them when located in an adjacent
grid cell. Stepping on a lava tile instantly kills the agent. When the room is
dark, the agent can only observe adjacent grid cells.

Examples of the `MiniHack-Room-Ultimate-15x15-v0` task:

![](../imgs/rooms.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/room.py)

## All Environments

| Name                              | Capability     |
| --------------------------------- | -------------- |
| `MiniHack-Room-5x5-v0`            | Basic Learning |
| `MiniHack-Room-15x15-v0`          | Basic Learning |
| `MiniHack-Room-Random-5x5-v0`     | Basic Learning |
| `MiniHack-Room-Random-15x15-v0`   | Basic Learning |
| `MiniHack-Room-Dark-5x5-v0`       | Basic Learning |
| `MiniHack-Room-Dark-15x15-v0`     | Basic Learning |
| `MiniHack-Room-Monster-5x5-v0`    | Basic Learning |
| `MiniHack-Room-Monster-15x15-v0`  | Basic Learning |
| `MiniHack-Room-Trap-5x5-v0`       | Basic Learning |
| `MiniHack-Room-Trap-15x15-v0`     | Basic Learning |
| `MiniHack-Room-Ultimate-5x5-v0`   | Basic Learning |
| `MiniHack-Room-Ultimate-15x15-v0` | Basic Learning |