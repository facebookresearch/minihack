# Description files

The des-file format is a domain-specific language created by the developers of NetHack for describing the levels of the game. des-files are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc.

Levels defined via des-file can be fairly rich, as the underlying programming language has support for variables, loops, conditional statements, as well as probability distributions. Crucially, it supports underspecified statements, such as generating a random monster or an object at a random location on the map. Furthermore, it features commands that procedurally generate diverse grid layouts in a single line.

For more information, check out [our tutorial](../tutorials/des_file/index), [jupyter notebook tutorial](https://github.com/MiniHackPlanet/MiniHack/blob/master/notebooks/des_file_tutorial.ipynb) or the [documentation](https://nethackwiki.com/wiki/Des-file_format) on NetHack Wiki.