# River

This group of tasks requires the agent to cross a river
using boulders and reach the goal located on the other side.
Boulders, when pushed into water, create a dry land to walk on,
allowing the agent to cross it.

While the `MiniHack-River-Narrow-v0` task can be
solved by pushing one boulder into the water, other `MiniHack-River-v0` require the
agent plan a sequence of at least two boulder pushes into the river next to
each other. In the more challenging tasks of the group, the agent needs to
additionally fight monsters (`MiniHack-River-Monster-v0`), avoid pushing boulders
into lava rather than water (`MiniHack-River-Lava-v0`), or both
(`MiniHack-River-MonsterLava-v0`).

Examples of the `MiniHack-River-v0` task:

![](../imgs/rivers.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/river.py)

## All Environments

| Name                            | Capability |
| ------------------------------- | ---------- |
| `MiniHack-River-Narrow-v0`      | Planning   |
| `MiniHack-River-v0`             | Planning   |
| `MiniHack-River-Monster-v0`     | Planning   |
| `MiniHack-River-Lava-v0`        | Planning   |
| `MiniHack-River-MonsterLava-v0` | Planning   |