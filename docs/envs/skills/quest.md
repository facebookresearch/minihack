# Quest

In the `Quest` tasks, the agents first needs
to cross a river of lava with whichever object it can find, which can be any
object allowing levitation or freezing. On the opposite side of the river, it
needs to find the key, use it to open a hidden chest in order to locate the
WoD. The WoD is required to kill the powerful monster standing between the
agent and the goal. In `Quest_Easy`, the map layout is relatively
simple and fixed, whereas in the `Quest_Pro` version it is procedurally
generated and also requires navigation through complicated mazes.

Examples of the `Quest-Hard` task:

![](../imgs/quest_hard.png)

## All Environments

| Name              | Skill                                 |
| ----------------- | ------------------------------------- |
| `Quest-Easy-v0`   | Inventory                             |
| `Quest-Medium-v0` | Navigation+Inventory                  |
| `Quest-Hard-v0`   | Navigation+PickUp+Inventory+Direction |