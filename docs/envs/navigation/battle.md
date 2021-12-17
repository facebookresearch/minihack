# CorridorBattle

The `MiniHack-CorridorBattle-v0` task challenges the
agent to make best use of the dungeon features to effectively defeat a horde of
hostile monsters. Here, if the agent lures the rats
into the narrow corridor, it can defeat them one at a time. Fighting in rooms,
on the other hand, would result the agent simultaneously incurring damage from
several directions and a quick death. The task also is offered in dark mode
(`MiniHack-CorridorBattle-Dark-v0`), challenging the agent to remember the number of
rats killed in order to plan subsequent actions.

An example of the `MiniHack-CorridorBattle-v0` task:

![](../imgs/battle.png)

## Reward

The agent receives a reward of +1 for reaching the goal.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/fightcorridor.py)

## All Environments

| Name                              | Capability        |
| --------------------------------- | ----------------- |
| `MiniHack-CorridorBattle-v0`      | Planning & Memory |
| `MiniHack-CorridorBattle-Dark-v0` | Planning & Memory |