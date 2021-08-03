# Description files

MiniHack leverages the description files of NetHack to provide a means to easily design rich and diverse environments. The description files (or des-files) are human-readable specifications of levels: distributions of grid layouts together with monsters, objects on the floor, environment features (e.g. walls, water, lava), etc. The developers of NetHack created a special domain-specific language for describing the levels of the game, called _des-file format_. The des-files can be compiled into binary using the NetHack level compiler, and MiniHack maps them to [Gym environments](https://github.com/openai/gym).

For more information, check out [our tutorial](../tutorials/des_file/index), [jupyter notebook tutorial](https://github.com/MiniHackPlanet/MiniHack/blob/master/notebooks/des_file_tutorial.ipynb) or the [documentation](https://nethackwiki.com/wiki/Des-file_format) on NetHack Wiki.
