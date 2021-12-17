# Wand of Death

These environments require mastering the usage of the [wand of death (WoD)](https://nethackwiki.com/wiki/Wand_of_death).
Zapping a WoD it in any direction fires a death ray which
instantly kills almost any monster it hits.

In `MiniHack-WoD-Easy-v0` environment,
the agent starts with a WoD in its inventory and needs to zap it towards a
sleeping monster. `MiniHack-WoD-Medium-v0` requires the agent pick it up, approach
the sleeping monster, kill it, and go to the staircase. In `MiniHack-WoD-Hard-v0` the
WoD needs to be found first, only then the agent should enter the corridor with
a monster (who is awake and hostile this time), kill it, and go to the
staircase. In the most difficult task of the sequence, the `MiniHack-WoD-Pro-v0`,
the agent starts inside a big labyrinth. It needs to find the WoD inside the
maze and reach its centre, which is guarded by a deadly Minotaur.

An example of the `MiniHack-WoD-Hard-v0` task:

![](../imgs/wod.png)

## Reward

The agent receives a reward of +1 for killing the minotaur `MiniHack-WoD-Easy-v0`. For the other versions, a reward of +1 is received upon reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/skills_wod.py)

## All Environments

| Name                     | Skill                                       |
| ------------------------ | ------------------------------------------- |
| `MiniHack-WoD-Easy-v0`   | Inventory + Direction                       |
| `MiniHack-WoD-Medium-v0` | PickUp + Inventory + Direction              |
| `MiniHack-WoD-Hard-v0`   | PickUp + Inventory + Direction              |
| `MiniHack-WoD-Pro-v0`    | Navigation + PickUp + Inventory + Direction |