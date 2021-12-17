# HideNSeek

In these tasks, the agent is spawned in
a big room full of trees and clouds. The trees and clouds block the line of
sight of the player and a random monster (chosen to be more powerful than the
agent). The agent, monsters and spells can pass through clouds unobstructed.
The agent and monster cannot pass through trees. The goals is to make use of
the environment features, avoid being seen by the monster and quickly run
towards the goal. The layout of the map is procedurally generated, hence
requires systematic generalisation.


`MiniHack-HideNSeek-v0` is the standard version of the environment.
Alternative versions of this environment
additionally include lava tiles that need to be avoided
`MiniHack-HideNSeek-Lava-v0`, have bigger size `MiniHack-HideNSeek-Big-v0`, or provide
the locations of all environment features but not the powerful monster
`MiniHack-HideNSeek-Mapped-v0`.

Examples of the `MiniHack-HideNSeek-v0` task:

![](../imgs/hidenseeks.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/hidenseek.py)

### All Environments

| Name                           | Capability |
| ------------------------------ | ---------- |
| `MiniHack-HideNSeek-v0`        | Planning   |
| `MiniHack-HideNSeek-Mapped-v0` | Planning   |
| `MiniHack-HideNSeek-Lava-v0`   | Planning   |
| `MiniHack-HideNSeek-Big-v0`    | Planning   |