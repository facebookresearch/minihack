# Lava Crossing

An example of a more advanced task involves crossing
a river of lava. The agent can accomplish this by either levitating over it
(via a potion of levitation or levitation boots) or freezing it (by zapping the
wand of cold or playing the frost horn). In the simplest version of the task
(`LavaCross-Levitate-Potion-Inv` and
`LavaCross-Levitate-Ring-Inv`), the agent starts with one of the
necessary objects in the inventory. Requiring the agent to pickup the
corresponding object first makes the tasks more challenging
(`LavaCross-Levitate-Potion-PickUp` and
`LavaCross-Levitate-Ring-PickUp`). Most difficult variants of this task
group require the agent to cross the lava river using one of the appropriate
objects randomly sampled and placed at the random location. In
`LavaCross-Levitate`, one of the objects of levitation is placed on the
map, while in the `LavaCross` task these include all of the objects for
levitation as well as freezing.

Five random instances of the `LavaCross` task, where the agent needs to cross
the lava using (i) potion of levitation, (ii) ring of levitation, (iii)
levitation boots, (iv) frost horn, or (v) wand of cold.

![](../imgs/lavacross.png)

## All Environments

| Name                                  | Skill            |
| ------------------------------------- | ---------------- |
| `LavaCross-Levitate-Ring-Inv-v0`      | Inventory        |
| `LavaCross-Levitate-Potion-Inv-v0`    | Inventory        |
| `LavaCross-Levitate-Ring-Pickup-v0`   | PickUp+Inventory |
| `LavaCross-Levitate-Potion-PickUp-v0` | PickUp+Inventory |
| `LavaCross-Levitate-v0`               | PickUp+Inventory |
| `LavaCross-v0`                        | PickUp+Inventory |
