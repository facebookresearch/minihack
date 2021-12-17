# Quest

This family of environments features a mini-quest for the agent to complete.

The agents needs to make use of an object is laying around for crossing a lava rivver
(this can be any object allowing levitation or freezing), while fighting monsters and navigating rooms or mazes. Towards the end of the quests, the agent needs to utlise a wand of death to kill a deadly monster guarding the goal location.

In `MiniHack-Quest-Easy-v0`, the map layout is relatively
simple and fixed.
The `MiniHack-Quest-Medium-v0` task features a narrow corridor. The agents needs to lure monsters into a narrow corridor and defeat them one at a time, before progressing further.
In the most challenging version of the task, `MiniHack-Quest-Hard-v0`, features large procedurally generated maze which needs to solved first before embarking on the next steps of the quest.

Examples of the `MiniHack-Quest-Hard-v0` task:

![](../imgs/quest_hard.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/skills_quest.py)

## All Environments

| Name                       | Skill                                       |
| -------------------------- | ------------------------------------------- |
| `MiniHack-Quest-Easy-v0`   | Inventory                                   |
| `MiniHack-Quest-Medium-v0` | Navigation + Inventory                      |
| `MiniHack-Quest-Hard-v0`   | Navigation + PickUp + Inventory + Direction |