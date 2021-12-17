# KeyRoom

These tasks require the agent to pickup a key, navigate to
a door, and use the key to unlock the door, reaching the staircase down within
the locked room. The action space is the standard movement actions plus the
pickup and apply action.

In the simplest variant of this task,
(`MiniHack-KeyRoom-Fixed-S5-v0`), the location of the key, door and staircase are
fixed. In the rest of the variants these locations randomised. The size the
outer room is 5x5 for `MiniHack-KeyRoom-S5-v0` and 15x15 for `MiniHack-KeyRoom-S15-v0`.
To increase the difficulty of the tasks, dark versions of the tasks are
introduced (`MiniHack-KeyRoom-Dark-S5-v0` and `MiniHack-KeyRoom-Dark-S15-v0`), where the
key cannot be seen if it is not in any of the agent's adjacent grid cells.

Examples of the `MiniHack-KeyRoom-S15-v0` task:

![](../imgs/keyrooms.png)

## Reward

The agent receives a reward of +1 for reaching the goal located in the locked room.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/keyroom.py).

## All Environments

| Name                           | Capability  |
| ------------------------------ | ----------- |
| `MiniHack-KeyRoom-Fixed-S5-v0` | Exploration |
| `MiniHack-KeyRoom-S5-v0`       | Exploration |
| `MiniHack-KeyRoom-Dark-S5-v0`  | Exploration |
| `MiniHack-KeyRoom-S15-v0`      | Exploration |
| `MiniHack-KeyRoom-Dark-S15-v0` | Exploration |