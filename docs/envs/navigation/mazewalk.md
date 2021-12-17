# MazeWalk

These navigation tasks make use of the `MAZEWALK`
command in the `des-file`, which procedurally generates diverse mazes.

We provide three maze sizes of 9x9, 15x15 and 45x19 grids corresponding to `MiniHack-MazeWalk-9x9-v0`, `MiniHack-MazeWalk-15x15-v0`,
and `MiniHack-MazeWalk-45x19-v0` environments. In the mapped versions of these tasks
(`MiniHack-MazeWalk-Mapped-9x9-v0`, `MiniHack-MazeWalk-Mapped-15x15-v0`, and
`MiniHack-MazeWalk-Mapped-45x19-v0`), the map of the maze and the goal's locations
are visible to the agent.

Examples of the `MiniHack-MazeWalk-15x15-v0` task:

![](../imgs/mazewalks.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/mazewalk.py)

## All environments

| Name                                | Capability           |
| ----------------------------------- | -------------------- |
| `MiniHack-MazeWalk-9x9-v0`          | Exploration & Memory |
| `MiniHack-MazeWalk-Mapped-9x9-v0`   | Exploration & Memory |
| `MiniHack-MazeWalk-15x15-v0`        | Exploration & Memory |
| `MiniHack-MazeWalk-Mapped-15x15-v0` | Exploration & Memory |
| `MiniHack-MazeWalk-45x19-v0`        | Exploration & Memory |
| `MiniHack-MazeWalk-Mapped-45x19-v0` | Exploration & Memory |