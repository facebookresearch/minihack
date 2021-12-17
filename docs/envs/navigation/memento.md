# Memento

This group of tasks test the agent's ability to use memory
(within an episode) to pick the correct path. The agent is presented with a
prompt (in the form of a sleeping monster of a specific type), and then
navigates along a corridor. At the end of the corridor the agent reaches a
fork, and must choose a direction. One direction leads to a grid bug, which if
killed terminates the episode with +1 reward. All other directions lead to
failure through a invisible trap that terminates the episode when activated.
The correct path is determined by the cue seen at the beginning of the episode.

We provide three versions of this environment: one with a short corridor before
a fork with two paths to choose from (`MiniHack-Memento-Short-F2-v0`), one with a
long corridor with a two-path fork (`MiniHack-Memento-F2-v0`), and one with a long
corridor and a four-fork path (`MiniHack-Memento-F4-v0`).

An example of the `MiniHack-Memento-F4-v0` task:

![](../imgs/memento.png)

## Reward

The agent receives a reward of 1 for killing the grid bug (navigating along the correct corridor) and -1 for stepping on the trap (naving along the incorrect corridor). Both events terminate the episode.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/memento.py)

## All Environments

| Name                           | Capability |
| ------------------------------ | ---------- |
| `MiniHack-Memento-Short-F2-v0` | Memory     |
| `MiniHack-Memento-F2-v0`       | Memory     |
| `MiniHack-Memento-F4-v0`       | Memory     |