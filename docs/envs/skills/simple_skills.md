# Simple Tasks

The simple skill acquisition tasks require
discovering interaction between one object and the actions of the agent. These
include: eating comestibles (`MiniHack-Eat-v0`), praying on an altar
(`MiniHack-Pray-v0`), wearing armour (`MiniHack-Wear-v0`), and kicking locked doors
(`LockedDoors`). In the regular versions of these tasks, the starting
location of the objects and the agent is randomised, whereas in the fixed
versions of these tasks (`MiniHack-Eat-Fixed-v0`, `MiniHack-Pray-Fixed-v0`,
`MiniHack-Wear-Fixed-v0` and `MiniHack-LockedDoors-Fixed-v0`) both are fixed. To add a
slight complexity to the randomised version of these tasks, distractions in the
form of a random object and a random monster are added to the third version of
these tasks (`MiniHack-Eat-Distract-v0`, `MiniHack-Pray-Distract-v0` and
`MiniHack-Wear-Distract-v0`). These tasks can be used as building blocks for more
advanced skill acquisition tasks.

Examples of `MiniHack-Eat-Distract-v0`, `MiniHack-Wear-Distract-v0` and `MiniHack-Pray-Distract-v0` tasks:

![](../imgs/simple_skills.png)

## Reward

The agent receives a reward of +1 for using the required skill in the given environment, such as eating comestibles in `MiniHack-Eat-v0` or wearing armour in `MiniHack-Wear-v0`.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/skills_simple.py)

## All Environments

| Name                            | Skill                              |
| ------------------------------- | ---------------------------------- |
| `MiniHack-Eat-v0`               | Confirmation or PickUp + Inventory |
| `MiniHack-Eat-Fixed-v0`         | Confirmation or PickUp + Inventory |
| `MiniHack-Eat-Distract-v0`      | Confirmation or PickUp + Inventory |
| `MiniHack-Pray-v0`              | Confirmation                       |
| `MiniHack-Pray-Fixed-v0`        | Confirmation                       |
| `MiniHack-Pray-Distract-v0`     | Confirmation                       |
| `MiniHack-Wear-v0`              | PickUp + Inventory                 |
| `MiniHack-Wear-Fixed-v0`        | PickUp + Inventory                 |
| `MiniHack-Wear-Distract-v0`     | PickUp + Inventory                 |
| `MiniHack-LockedDoor-v0`        | Direction                          |
| `MiniHack-LockedDoor-Random-v0` | Direction                          |