# Lava Crossing

This family of skill acquisition tasks requires crossing a river of lava. The agent can accomplish this by either levitating over it
(via a potion of levitation or levitation boots) or freezing it (by zapping the
wand of cold or playing the frost horn).

In the simplest version of the task
(`MiniHack-LavaCross-Levitate-Potion-Inv-v0` and
`MiniHack-LavaCross-Levitate-Ring-Inv-v0`), the agent starts with one of the
necessary objects in the inventory. Requiring the agent to pickup the
corresponding object first makes the tasks more challenging
(`MiniHack-LavaCross-Levitate-Potion-PickUp-v0` and
`MiniHack-LavaCross-Levitate-Ring-PickUp-v0`). Most difficult variants of this task
group require the agent to cross the lava river using one of the appropriate
objects randomly sampled and placed at the random location. In
`LMiniHack-avaCross-Levitate-v0`, one of the objects of levitation is placed on the
map, while in the `MiniHack-LavaCross-v0` task these include all of the objects for
levitation as well as freezing.

Five random instances of the `MiniHack-LavaCross-v0` task, where the agent needs to cross
the lava using (i) potion of levitation, (ii) ring of levitation, (iii)
levitation boots, (iv) frost horn, or (v) wand of cold.

![](../imgs/lavacross.png)

## Reward

The agent receives a reward of +1 for reaching the goal on the other side of the lava river.

## Source

[Source](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/skills_lava.py)


## All Environments

| Name                                           | Skill              |
| ---------------------------------------------- | ------------------ |
| `MiniHack-LavaCross-Levitate-Ring-Inv-v0`      | Inventory          |
| `MiniHack-LavaCross-Levitate-Potion-Inv-v0`    | Inventory          |
| `MiniHack-LavaCross-Levitate-Ring-Pickup-v0`   | PickUp + Inventory |
| `MiniHack-LavaCross-Levitate-Potion-PickUp-v0` | PickUp + Inventory |
| `MiniHack-LavaCross-Levitate-v0`               | PickUp + Inventory |
| `MiniHack-LavaCross-v0`                        | PickUp + Inventory |
