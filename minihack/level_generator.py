# Copyright (c) Facebook, Inc. and its affiliates.
import numpy as np
import os

PATH_DAT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dat")

MAZE_FLAGS = (
    "noteleport",
    "hardfloor",
    "nommap",
    "arboreal",
    "shortsighted",
    "mazelevel",
    "premapped",
    "shroud",
    "graveyard",
    "icedpools",
    "solidify",
    "corrmaze",
    "inaccessibles",
)

MAP_CHARS = [
    " ",  # solid wall
    "#",  # corridor
    ".",  # room floor
    "-",  # horizontal wall
    "|",  # vertical wall
    "+",  # door
    "A",  # air
    "B",  # crosswall
    "C",  # cloud
    "S",  # secret door
    "H",  # secret corridor
    "{",  # fountain
    "\\",  # throne
    "K",  # soml
    "}",  # moat
    "P",  # pool of water
    "L",  # lava pool
    "I",  # ice
    "W",  # water
    "T",  # tree
    "F",  # iron bars
]

TRAP_NAMES = [
    "anti magic",
    "arrow",
    "bear",
    "board",
    "dart",
    "falling rock",
    "fire",
    "hole",
    "land mine",
    "level teleport",
    "magic portal",
    "magic",
    "pit",
    "polymorph",
    "rolling boulder",
    "rust",
    "sleep gas",
    "spiked pit",
    "statue",
    "teleport",
    "trap door",
    "web",
]


class LevelGenerator:
    """
    LevelGenerator provides a convenient Python interface for quickly writing
    description files for MiniHack. The LevelGenerator class can be used to
    create MAZE-type levels with specified heights and widths, and can then
    fill those levels with objects, monsters and terrain, and specify the start
    point of the level.

    Args:
        map (str or None):
            The description of the map block of the environment. If None, the
            map will have a rectangle layout with the given height and width.
            Defaults to None.
        w (int):
            The width of map. Only used when `map=None`. Defaults to 8.
        h (int):
            The height of map. Only used when `map=None`. Defaults to 8.
        fill (str):
            A character describing the environment feature that fills the
            map. Only used when ``map=None``. Defaults to ".", which
            corresponds to floor.
        lit (bool):
            Whether the layout is lit or not. This affects the observations the
            agent will receive. If an area is not lit, the agent can only see
            directly adjacent grids. Defaults to True.
        flags (tuple):
            Flags of the environment. For the full list, see
            https://nethackwiki.com/wiki/Des-file_format#FLAGS.
            Defaults to ("hardfloor",).
        solidfill (str):
            A character describing the environment feature used for filling
            solid / unspecified parts of the map. Defaults to " ", which
            corresponds to solid wall.
    """

    def __init__(
        self,
        map=None,
        w=8,
        h=8,
        fill=".",
        lit=True,
        flags=("hardfloor",),
        solidfill=" ",
    ):
        assert all(
            f in MAZE_FLAGS for f in flags
        ), f"One of the provided maze flags is incorrect: {flags}"
        flags_str = ",".join(flags)

        self.header = f"""
MAZE: "mylevel", ' '
FLAGS:{flags_str}
INIT_MAP: solidfill,'{solidfill}'
GEOMETRY:center,center
"""
        self.mapify = lambda x: "MAP\n" + x + "ENDMAP\n"
        self.init_map(map, w, h, fill)

        litness = "lit" if lit else "unlit"
        self.footer = f'REGION:(0,0,{self.x},{self.y}),{litness},"ordinary"\n'

        self.stair_up_exist = False

    def init_map(self, map=None, x=8, y=8, fill="."):
        """Initialise the map block of the des-file."""
        if map is None:
            # Creating empty area
            self.x = x
            self.y = y
            self.map = np.array([[fill] * x] * y, dtype=str)
        else:
            lines = [list(line) for line in map.split("\n") if len(line) > 0]
            self.y = len(lines)
            self.x = max(len(line) for line in lines)
            new_lines = [line + [" "] * (self.x - len(line)) for line in lines]
            self.map = np.array(new_lines)

    def get_map_str(self):
        """Returns the map as a string."""
        map_list = [
            "".join(self.map[i]) + "\n" for i in range(self.map.shape[0])
        ]
        return "".join(map_list)

    def get_map_array(self):
        """Returns the map as a two-dimensional numpy array."""
        return self.map

    def get_des(self):
        """Returns the description file.

        Returns:
            str: the description file as a string.
        """
        return self.header + self.mapify(self.get_map_str()) + self.footer

    @staticmethod
    def _validate_place(place):
        """Validate a given place argument."""
        if place is None:
            place = "random"
        elif isinstance(place, tuple):
            place = LevelGenerator._validate_coord(place)
            place = str(place)
        elif isinstance(place, str):
            pass
        else:
            raise ValueError("Invalid place provided.")

        return place

    @staticmethod
    def _validate_coord(coord):
        """Validate a given typle of coordinates."""
        assert (
            isinstance(coord, tuple)
            and len(coord) == 2
            and isinstance(coord[0], int)
            and isinstance(coord[1], int)
        )
        return coord

    def add_object(
        self, name="random", symbol="%", place=None, cursestate=None
    ):
        """Add an object to the map.

        Args:
            name (str):
                The name of the object. Defaults to random.
            symbol (str):
                The symbol of the object. The symbol should correspond to the
                given object name. For example, "%" symbol corresponds to
                comestibles, so the name of the object should also correspond
                to commestibles (e.g. apple). Not used when name is "random".
                Defaults to "%".
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
            cursetstate (str or None):
                The cursed state of the object. Can be "blessed", "uncursed",
                "cursed" or "random". Defaults to None (not used).
        """
        place = self._validate_place(place)
        assert isinstance(symbol, str) and len(symbol) == 1
        assert isinstance(
            name, str
        )  # TODO maybe check object exists in NetHack

        if name != "random":
            name = f'"{name}"'
            self.footer += f"OBJECT:('{symbol}',{name}),{place}"

            if cursestate is not None:
                assert cursestate in [
                    "blessed",
                    "uncursed",
                    "cursed",
                    "random",
                ]
                if cursestate != "random":
                    self.footer += f",{cursestate}"

            self.footer += "\n"

        else:
            self.footer += f"OBJECT:random,{place}\n"

    def add_object_area(
        self, area_name, name="random", symbol="%", cursestate=None
    ):
        """Add an object in an area of the map defined by `area_name` variable.
        See ``add_object`` for more details.
        """

        place = f"rndcoord({area_name})"
        self.add_object(name, symbol, place, cursestate)

    def add_monster(self, name="random", symbol=None, place=None, args=()):
        """Add a monster to the map.

        Args:
            name (str):
                The name of the monster. Defaults to random.
            symbol (str or None):
                The symbol of the monster. The symbol should correspond to the
                family of the specified mosnter. For example, "d" symbol
                corresponds to canine monsters, so the name of the object should
                also correspond to canines  (e.g. jackal). Not used when name is
                "random". Defaults to None.
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
            args (tuple):
                Additional monster arguments, e.g. "hostile" or "peaceful",
                "asleep" or "awake", etc. For more details, see
                https://nethackwiki.com/wiki/Des-file_format#MONSTER.
        """
        place = self._validate_place(place)
        assert (
            symbol == "random"
            or symbol is None
            or (isinstance(symbol, str) and len(symbol) == 1)
        )
        assert isinstance(
            name, str
        )  # TODO maybe check object exists in NetHac

        if name != "random":
            name = f'"{name}"'

        if symbol is not None:
            name = f"('{symbol}',{name})"

        self.footer += f"MONSTER:{name},{place}"

        if len(args) > 0:
            assert any(
                arg in ["hostile", "peaceful", "asleep", "awake"]
                for arg in args
            )
            for arg in args:
                self.footer += f",{arg}"

        self.footer += "\n"

    def add_terrain(self, coord, flag, in_footer=False):
        """Add terrain features to the map.

        Args:
            coord (tuple):
                A tuple with length two representing the (x, y) coordinates.
            flag (str):
                The flag corresponding to the desired terrain feature. Should
                belong to minihack.level_generator.MAP_CHARS. For more details,
                see https://nethackwiki.com/wiki/Des-file_format#Map_characters
            in_footer (bool):
                Whether to define the terrain feature as an additional line
                in the description file (True) or directly modify the map block
                with the given flag (False). Defaults to False.
        """
        coord = self._validate_coord(coord)
        assert flag in MAP_CHARS

        if in_footer:
            self.footer += f"TERRAIN: {str(coord)}, '{flag}'\n"
        else:
            x, y = coord
            self.map[y, x] = flag

    def fill_terrain(
        self,
        type,
        flag,
        x1,
        y1,
        x2,
        y2,
    ):
        """Fill the areas between (x1, y1) and (x2, y2) with the given dungeon
        feature:

        Args:
            type (str):
                The type of filling. "rect" indicates an unfilled rectangle,
                containing just the edges and none of the interior points.
                "fillrect" denotes filled rectangle containing the edges and
                all of the interior points. "line" is used for a straight line
                drawn from one pair of coordinates to the other using
                Bresenham's line algorithm.
            flag (str):
                The flag corresponding to the desired terrain feature. Should
                belong to minihack.level_generator.MAP_CHARS. For more details,
                see https://nethackwiki.com/wiki/Des-file_format#Map_characters
            x1 (int): x coordinate of point 1.
            y1 (int): y coordinate of point 1.
            x2 (int): x coordinate of point 2.
            y2 (int): y coordinate of point 2.
        """
        assert type in ("rect", "fillrect", "line")
        assert flag in MAP_CHARS
        self.footer += f"TERRAIN:{type} ({x1},{y1},{x2},{y2}),'{flag}'\n"

    def set_area_variable(
        self,
        var_name,  # Should start with $ sign
        type,
        x1,
        y1,
        x2,
        y2,
    ):
        """Set a variable representing an area on the map.

        Args:
            var_name (str):
                The name of the variable.
            type (str):
                The type of filling. "rect" indicates an unfilled rectangle,
                containing just the edges and none of the interior points.
                "fillrect" denotes filled rectangle containing the edges and
                all of the interior points. "line" is used for a straight line
                drawn from one pair of coordinates to the other using
                Bresenham's line algorithm.
            x1 (int): x coordinate of point 1.
            y1 (int): y coordinate of point 1.
            x2 (int): x coordinate of point 2.
            y2 (int): y coordinate of point 2.
        """

        assert type in ("rect", "fillrect", "line")
        if var_name[0] != "$":
            var_name = "$" + var_name
        self.footer += f"{var_name} = selection:{type} ({x1},{y1},{x2},{y2})\n"

    def add_goal_pos(self, place=None):
        """Add a goal at the given place. Same as `add_stair_down`."""
        self.add_stair_down(place)

    def add_stair_down(self, place=None):
        """Add a stair down at the given place.

        Args:
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        self.footer += f"STAIR:{place},down\n"

    def set_start_pos(self, coord):
        """Set the starting position of the agent.

        Args:
            coord (tuple):
                A tuple with length two representing the (x, y) coordinates.
        """
        self._add_stair_up(coord)

    def set_start_rect(self, p1, p2):
        """Set the starting position of the agent.

        Args:
            coord (tuple):
                A tuple with length two representing the (x, y) coordinates.
        """
        self._add_stair_up_rect(p1, p2)

    def _add_stair_up(self, coord):
        """Add a stair up at a given coordanate."""
        if self.stair_up_exist:
            return
        x, y = self._validate_coord(coord)
        _x, _y = abs(x - 1), abs(y - 1)  # any different coordinate than (x,y)
        self.footer += f"BRANCH:({x},{y},{x},{y}),({_x},{_y},{_x},{_y})\n"
        self.stair_up_exist = True

    def _add_stair_up_rect(self, p1, p2):
        """Add a stair up at a given rectangle."""
        if self.stair_up_exist:
            return
        x1, y1 = self._validate_coord(p1)
        x2, y2 = self._validate_coord(p2)
        self.footer += f"BRANCH:({x1},{y1},{x2},{y2}),({0},{0},{0},{0})\n"
        self.stair_up_exist = True

    def add_door(self, state, place=None):
        """Add a door.

        Args:
            state (str):
                The state of the door. Possible values are "locked", "closed",
                "open", "nodoor", and "random". Defaults to "random".
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        assert state in ["nodoor", "locked", "closed", "open", "random"]
        self.footer += f"DOOR:{state},{place}\n"

    def add_altar(self, place=None, align="random", type="random"):
        """Add an altar.

        Args:
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
            align (str):
                The alignment. Possible values are "noalign", "law", "neutral",
                "chaos", "coaligned", "noncoaligned", and "random". Defaults
                to "random".
            type (str):
                The type of the altar. Possible values are "sanctum", "shrine",
                "altar", and "random". Defaults to random.
        """
        place = self._validate_place(place)
        assert align in [
            "noalign",
            "law",
            "neutral",
            "chaos",
            "coaligned",
            "noncoaligned",
            "random",
        ]
        assert type in ["sanctum", "shrine", "altar", "random"]
        self.footer += f"ALTAR:{place},{align},{type}\n"

    def add_sink(self, place=None):
        """Add a sink.

        Args:
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        self.footer += f"SINK:{place}\n"

    def add_trap(self, name="teleport", place=None):
        """Add a trap.

        Args:
            name (str):
                The name of the trap. For possible values, see
                `minihack.level_generator.TRAP_NAMES`. Defaults to "teleport".
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        assert name in TRAP_NAMES
        self.footer += f'TRAP:"{name}",{place}\n'

    def add_fountain(self, place=None):
        """Add a fountain.

        Args:
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        self.footer += f"FOUNTAIN: {place}\n"

    def add_gold(self, amount, place=None):
        """Add gold on the floor.

        Args:
            amount (int):
                The amount of gold.
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        assert amount > 0
        self.footer += f"GOLD: {amount},{place}\n"

    def add_boulder(self, place=None):
        """Add gold on the floor.

        Args:
            amount (int):
                The amount of gold.
            place (None, tuple or str):
                The place of the added object. If None, the location is
                selected randomly. Tuple values are used for providing exact
                (x, y) coordinates. String values are copied to des-file as is.
                Defaults to None.
        """
        place = self._validate_place(place)
        self.footer += f'OBJECT: "boulder", {place}\n'

    def wallify(self):
        """Wallify the map. Turns walls completely surrounded by other walls
        into solid stone ' '.
        """
        self.footer += "WALLIFY\n"

    def add_mazewalk(self, coord=None, dir="east"):
        """Creates a random maze, starting from the given coordinate.

        Mazewalk turns map grids with solid stone into floor. From the starting
        position, it checks the mapgrid in the direction given, and if it's
        solid stone, it will move there, and turn that place into floor. Then
        it will choose a random direction, jump over the nearest mapgrid in that
        direction, and check the next mapgrid for solid stone. If there is solid
        stone, mazewalk will move that direction, changing that place and the
        intervening mapgrid to floor. Normally the generated maze will not have
        any loops.

        Pointing mazewalk at that will create a small maze of trees, but unless
        the map (at the place where it's put into the level) is surrounded by
        something else than solid stone, mazewalk will get out of that MAP.
        Substituting floor characters for some of the trees "in the maze" will
        make loops in the maze, which are not otherwise possible. Substituting
        floor characters for some of the trees at the edges of the map
        will make maze entrances and exits at those places.

        For more details see
        https://nethackwiki.com/wiki/Des-file_format#MAZEWALK.

        Args:
             coord (tuple or None):
                 A tuple with length two representing the (x, y) coordinates.
                 If None is passed, the middle point of the map is selected.
                 Defaults to None.
            dir (str):
                The direction of the start of the maze. Possible values are
                "north", "east", "south", and "east". Defaults to "east".
        """
        if coord is not None:
            x, y = self._validate_coord(coord)
        else:
            x, y = self.x // 2, self.y // 2

        self.footer += f"MAZEWALK:({x},{y}),{dir}\n"

    def add_line(self, str):
        """Add a custom string to the buttom of the description file.

        Args:
            str (str):
                The string to be concatenated to the des-file.
        """
        self.footer += str + "\n"
