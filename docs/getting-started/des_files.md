# Description files

````{note}
This is a brief overview of the des-file format. An in-depth, visually-aided tutorial can be found [here](../tutorials/des_file_tutorial.ipynb).
````

## Overview

MiniHack leverages the description files of NetHack to provide a means to easily design rich and diverse environments. The description files (or des-files) are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc. The developers of NetHack created a special domain-specific language for describing the levels of the game, called _des-file format_. The des-files can be compiled into binary using the NetHack level compiler, and MiniHack maps them to Gym environments.

![](../imgs/des_file.gif)

Levels defined via des-file format can be fairly rich, as the underlying programming language has support for variables, loops, conditional statements, as well as probability distributions. Crucially, it supports underspecified statements, such as generating a random monster or an object at a random location on the map. Furthermore, it features commands that procedurally generate diverse grid layouts in a single line.

Below we present a brief overview of the different kinds of des-files, how to add entities to levels, and the main sources of randomness that can be used to create a distribution of levels on which to train RL agents. __Please check out our in-depth, visually-aided tutorial [here](../tutorials/des_file/index)__. We also refer users to the des-file tutorial in [NetHack wiki](https://nethackwiki.com/wiki/Des-file_format).

````{note}
MiniHack addionally provides a convenient interface to describe the entire environment directly in Python. Check out our `LevelGenerator` [here](./interface.html#level-generator).
````

## Types of des-files

There are two types of levels that can be created using des-file format, namely *MAZE-type* and *ROOM-type*:
- MAZE-type levels are composed of maps of the level (specified with the `MAP` command) which are drawn using ASCII characters, followed by descriptions of the contents of the level, described in detail below. In MAZE-type environments, the layout of the map is fixed, but random terrain can be created around (or within) that map using the `MAZEWALK` command, which creates a random maze from a given location and filling all available space of a certain terrain type.
- ROOM-type levels are composed of descriptions of rooms (specified by the `ROOM` command), each of which can have its contents specified by the commands described below. Generally, the `RANDOM_CORRIDORS` command is then used to create random corridors between all the rooms so that they are accessible. On creation, the file specifies (or leaves random) the room's type, lighting and approximate location. It is also possible to create subrooms (using the `SUBROOM` command) which are rooms guaranteed to be within the outer room and are otherwise specified as normal rooms (but with a location relative to the outer room).

## Adding Entities to des-files

As we have seen above, there are multiple ways to define the layout of a level using the des-file format. Once the layout is defined, it is useful to be able to add entities to the level. These could be monsters, objects, traps or other specific terrain features (such as sinks, fountains or altars). In general, the syntax for adding one of these objects is:
```
ENTITY: specification, location, extra-details
```
For example:
```
MONSTER: ('F',"lichen"), (1,1)
OBJECT: ('%',"apple"), (10,10)
TRAP: 'teleportation', (1,1)
SINK: (1,1)
FOUNTAIN: (0,0)
```

Note that many of the details here can instead be set to `random`. In this case, the game engine chooses a suitable value for that argument randomly each time the level is generated. For monsters and objects, this randomness can be controlled by just specifying the class of the monster or object and letting the specific object or monster be chosen randomly. For example:
```
MONSTER: 'F', (1,1)
OBJECT: '%', (10,10)
```
This code would choose a random monster from the [Fungus class](https://nethackwiki.com/wiki/Fungus), and a random object from the [Comestible class](https://nethackwiki.com/wiki/Comestible).

## Sources of Randomness in des-files

We have seen how to create either very fixed (MAZE-type) or very random (ROOM-type) levels, and how to add entities with some degree of randomness.
The des-file format has many other ways of adding randomness, which can be used to control the level generation process, including where to add terrain and in what way. Many of these methods are used in \texttt{IF} statements, which can be in one of two forms:
```
IF[50%] {
    MONSTER: 'F', (1,1)
} ELSE {
    # ELSE is not always necessary
    OBJECT: '%', (1,1)
}

IF[$variable_name < 15] {
    MONSTER: 'F', (1,1)
}
```
In the first form, a simple percentage is used for the random choice, whereas in the second, a variable (which could have been randomly determined earlier in the file) is used. A natural way to specify this variable is either in other conditional statements (perhaps you randomly add some number of monsters, and want to count the number of monsters you add such that if there are many monsters, you also add some extra weapons for the agent), or through dice notation. Dice notation is used to specify random expressions which resolve to integers (and hence can be used in any place an integer would be). They are of the form \texttt{NdM}, which means to roll N M-sided dice and sum the result. For example:

```
$roll = 2d6
IF[$roll < 7] {
    MONSTER: random, random
}
```

Dice rolls can also be used for accessing arrays, another feature of the des-file format. Arrays are initialised with one or more objects of the same type, and can be indexed with integers (starting at 0), for example:
```
# An array of monster classes
$mon_letters = { 'A', 'L', 'V', 'H' }
# An array of monster names from each monster class respectively
$mon_names = { "Archon", "arch-lich", "vampire lord", "minotaur" }
# The monster to choose
$mon_index = 1d4 - 1
MONSTER:($mon_letters[$mon_index],$mon_names[$mon_index]),(10,18)
```

Another way to perform random operations with arrays is using the `SHUFFLE` command. This command takes an array and randomly shuffles it. This would not work with the above example, as the monster name needs to match the monster class (i.e. we could not use `('A', "minotaur")`. For example:
```
$object = object: { '[',')','*','%' }
SHUFFLE: $object
```
Now the `$object` array will be randomly shuffled. Often, something achievable with shuffling can also be achieved with dice-rolls, but it is simpler to use shuffled arrays rather than dice-rolls (for example, if you wanted to guarantee each of the elements of the array was used exactly once, but randomise the order, it is much easier to just shuffle the array and select them in order rather than try and generate exclusive dice rolls).

## Random Terrain Placement

When creating a level, we may want to specify the structure or layout of the level (using a MAZE-type level), but then randomly create the terrain within the level, which will determine accessibility and observability for the agent and monsters in the level. As an example, consider the following example. In this level, we start with an empty 11x9 `MAP`. We first replace 33% of the squares with clouds `'C'`, and then 25% with trees `'T'`. To ensure that any corner is accessible from any other, we create two random-walk lines using `randline` from opposite corners and make all squares on those lines floor `.`. To give the agent a helping hand, we choose a random square in the centre of the room with `rndcoord` (which picks a random coordinate from a selection of coordinates) and place an apple there.

```
MAZE: "mylevel", ' '
GEOMETRY:center,center
MAP
...........
...........
...........
...........
...........
...........
...........
...........
...........
ENDMAP
REGION:(0,0,11,9),lit,"ordinary"
REPLACE_TERRAIN:(0,0,11,9), '.', 'C', 33%
REPLACE_TERRAIN:(0,0,11,9), '.', 'T', 25%
TERRAIN:randline (0,9),(11,0), 5, '.'
TERRAIN:randline (0,0),(11,9), 5, '.'
$center = selection: fillrect (5,5,8,8)
$apple_location = rndcoord $center
OBJECT: ('%', "apple"), $apple_location

$monster = monster: { 'L','N','H','O','D','T' }
SHUFFLE: $monster
$place = { (10,8),(0,8),(10,0) }
SHUFFLE: $place
MONSTER: $monster[0], $place[0], hostile
STAIR:$place[2],down
BRANCH:(0,0,0,0),(1,1,1,1)
```

Several other methods of randomly creating selections such as `filter` (randomly remove points from a selection) and `gradient` (create a selection based on a probability gradient across an area) are described in the [NetHack wiki](https://nethackwiki.com/wiki/Des-file_format).

## Further Information

For more information on the des-file format, be sure to check out our in-depth, visually-aided tutorial [here](../tutorials/des_file/index).
