# Wand of Death

MiniHack is very convenient for making incremental
changes to the difficulty of a task. To illustrate this, we provide a sequence
of tasks that require mastering the usage of the wand of death. Zapping a WoD it in any direction fires a death ray which
instantly kills almost any monster it hits. In `WoD-Easy` environment,
the agent starts with a WoD in its inventory and needs to zap it towards a
sleeping monster. `WoD-Medium` requires the agent pick it up, approach
the sleeping monster, kill it, and go to staircase. In `WoD-Hard` the
WoD needs to be found first, only then the agent should enter the corridor with
a monster (who is awake and hostile this time), kill it, and go to the
staircase. In the most difficult task of the sequence, the `WoD-Pro`,
the agent starts inside a big labyrinth. It needs to find the WoD inside the
maze and reach its centre, which is guarded by a deadly Minotaur.

An example of the `WoD-Hard` task:

![](../imgs/wod.png)

## All Environments

| Name         | Skill                                 |
| ------------ | ------------------------------------- |
| `WoD-Easy`   | Inventory+Direction                   |
| `WoD-Medium` | PickUp+Inventory+Direction            |
| `WoD-Hard`   | PickUp+Inventory+Direction            |
| `WoD-Pro`    | Navigation+PickUp+Inventory+Direction |