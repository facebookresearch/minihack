# Simple Tasks

The simplest skill acquisition tasks require
discovering interaction between one object and the actions of the agent. These
include: eating comestibles (`Eat`), praying on an altar
(`Pray`), wearing armour (`Wear`), and kicking locked doors
(`LockedDoors`). In the regular versions of these tasks, the starting
location of the objects and the agent is randomised, whereas in the fixed
versions of these tasks (`Eat-Fixed`, `Pray-Fixed`,
`Wear-Fixed` and `LockedDoors-Fixed`) both are fixed. To add a
slight complexity to the randomised version of these tasks, distractions in the
form of a random object and a random monster are added to the third version of
these tasks (`Eat-Distract`, `Pray-Distract` and
`Wear-Distract`). These tasks can be used as building blocks for more
advanced skill acquisition tasks.

Examples of `Eat-Distract`, `Wear-Distract` and `Pray-Distract`:

![](../imgs/simple_skills.png)

## All Environments

| Name                   | Skill                            |
| ---------------------- | -------------------------------- |
| `Eat-v0`               | Confirmation or PickUp+Inventory |
| `Eat-Fixed-v0`         | Confirmation or PickUp+Inventory |
| `Eat-Distract-v0`      | Confirmation or PickUp+Inventory |
| `Pray-v0`              | Confirmation                     |
| `Pray-Fixed-v0`        | Confirmation                     |
| `Pray-Distract-v0`     | Confirmation                     |
| `Wear-v0`              | PickUp+Inventory                 |
| `Wear-Fixed-v0`        | PickUp+Inventory                 |
| `Wear-Distract-v0`     | PickUp+Inventory                 |
| `LockedDoor-v0`        | Direction                        |
| `LockedDoor-Random-v0` | Direction                        |