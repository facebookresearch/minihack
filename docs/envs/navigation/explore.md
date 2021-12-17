# MazeExplore

These tasks test the agent's ability to perform deep
exploration. It's inspired by the Apple-Gold domain from
, where a small reward can be achieved easily, but to learn
the optimal policy deeper exploration is required. The agent must first explore
a simple randomised maze to reach the staircase down, which they can take for
+1 reward. However, if they navigate through a further randomised maze, they
reach a room with apples. Eating the apples gives +0.5 reward, and once the
apples are eaten the agent should then return to the staircase down.

We provide
an easy and a hard version of this task (`MazeExplore-Easy-v0` and
`MiniHack-MazeExplore-Hard-v0`), with the harder version having a larger maze both
before and after the staircase down. Variants can also be mapped
(`MiniHack-MazeExplore-Easy-Mapped-v0` and `MiniHack-MazeExplore-Hard-Mapped-v0`), where
the agent can observe the layout of the entire grid, making it easier to
navigate the maze. Even in the mapped setting the apples aren't visible until
the agent reaches the final room.

Examples of the `MiniHack-MazeExplore-Hard-v0` task. The apples are located near the right
vertical wall (unobservable in the figure). The goal is located in the middle
area of the grid.

![](../imgs/mazeexplores.png)

## Reward

The agent receives a reward of +1 for reaching the goal and +0.5 for eating an apple.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/exploremaze.py)

## All Environments

| Name                                  | Capability       |
| ------------------------------------- | ---------------- |
| `MiniHack-MazeExplore-Easy-v0`        | Deep Exploration |
| `MiniHack-MazeExplore-Hard-v0`        | Deep Exploration |
| `MiniHack-MazeExplore-Easy-Mapped-v0` | Deep Exploration |
| `MiniHack-MazeExplore-Hard-Mapped-v0` | Deep Exploration |