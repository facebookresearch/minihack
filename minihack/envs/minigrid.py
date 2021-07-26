# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from nle.nethack import Command, CompassDirection
from gym.envs import registration
import gym


MOVE_AND_KICK_ACTIONS = tuple(
    list(CompassDirection) + [Command.OPEN, Command.KICK]
)


class MiniGridHack(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        # Only ask users to install gym-minigrid if they actually need it
        try:
            import gym_minigrid  # noqa: F401
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "To use MiniGrid-based environments, please install"
                " gym-minigrid: pip3 install gym-minigrid"
            )

        self.minigrid_env = gym.make(kwargs.pop("env_name"))
        self.num_mon = kwargs.pop("num_mon", 0)
        self.num_trap = kwargs.pop("num_trap", 0)
        self.door_state = kwargs.pop("door_state", "closed")
        if self.door_state == "locked":
            kwargs["actions"] = MOVE_AND_KICK_ACTIONS

        lava_walls = kwargs.pop("lava_walls", False)
        if lava_walls:
            self.wall = "L"
        else:
            self.wall = "|"

        des_file = self.get_env_desc()
        super().__init__(*args, des_file=des_file, **kwargs)

    def get_env_map(self, env):
        door_pos = []
        goal_pos = None
        empty_strs = 0
        empty_str = True
        env_map = []

        for j in range(env.grid.height):
            str = ""
            for i in range(env.width):
                c = env.grid.get(i, j)
                if c is None:
                    str += "."
                    continue
                empty_str = False
                if c.type == "wall":
                    str += self.wall
                elif c.type == "door":
                    str += "+"
                    door_pos.append((i, j - empty_strs))
                elif c.type == "floor":
                    str += "."
                elif c.type == "lava":
                    str += "L"
                elif c.type == "goal":
                    goal_pos = (i, j - empty_strs)
                    str += "."
                elif c.type == "player":
                    str += "."
            if not empty_str and j < env.grid.height - 1:
                if set(str) != {"."}:
                    str = str.replace(".", " ", str.index(self.wall))
                    inv = str[::-1]
                    str = inv.replace(".", " ", inv.index(self.wall))[::-1]
                    env_map.append(str)
            elif empty_str:
                empty_strs += 1

        start_pos = (int(env.agent_pos[0]), int(env.agent_pos[1]) - empty_strs)
        env_map = "\n".join(env_map)

        return env_map, start_pos, goal_pos, door_pos

    def get_env_desc(self):
        self.minigrid_env.reset()
        env = self.minigrid_env

        map, start_pos, goal_pos, door_pos = self.get_env_map(env)

        lev_gen = LevelGenerator(map=map)

        lev_gen.add_stair_down(goal_pos)
        lev_gen.add_stair_up(start_pos)

        for d in door_pos:
            lev_gen.add_door(self.door_state, d)

        lev_gen.wallify()

        for _ in range(self.num_mon):
            lev_gen.add_monster()

        for _ in range(self.num_trap):
            lev_gen.add_trap()

        return lev_gen.get_des()

    def reset(self, wizkit_items=None):
        des_file = self.get_env_desc()
        self.update(des_file)
        return super().reset(wizkit_items=wizkit_items)


class MiniHackMultiRoomN2(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 40)
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N2-S4-v0", **kwargs
        )


class MiniHackMultiRoomN4(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 120)
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N4-S5-v0", **kwargs
        )


class MiniHackMultiRoomN6(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 240)
        super().__init__(*args, env_name="MiniGrid-MultiRoom-N6-v0", **kwargs)


registration.register(
    id="MiniHack-MultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2",
)
registration.register(
    id="MiniHack-MultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4",
)
registration.register(
    id="MiniHack-MultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6",
)


# MiniGrid: LockedMultiRoom
class MiniHackMultiRoomN2Locked(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 40)
        kwargs["door_state"] = "locked"
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N2-S4-v0", **kwargs
        )


class MiniHackMultiRoomN4Locked(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 120)
        kwargs["door_state"] = "locked"
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N4-S5-v0", **kwargs
        )


class MiniHackMultiRoomN6Locked(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 240)
        kwargs["door_state"] = "locked"
        super().__init__(*args, env_name="MiniGrid-MultiRoom-N6-v0", **kwargs)


registration.register(
    id="MiniHack-LockedMultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Locked",
)
registration.register(
    id="MiniHack-LockedMultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Locked",
)
registration.register(
    id="MiniHack-LockedMultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Locked",
)


# MiniGrid: LavaMultiRoom
class MiniHackMultiRoomN2Lava(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 40)
        kwargs["lava_walls"] = True
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N2-S4-v0", **kwargs
        )


class MiniHackMultiRoomN4Lava(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 120)
        kwargs["lava_walls"] = True
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N4-S5-v0", **kwargs
        )


class MiniHackMultiRoomN6Lava(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 240)
        kwargs["lava_walls"] = True
        super().__init__(*args, env_name="MiniGrid-MultiRoom-N6-v0", **kwargs)


registration.register(
    id="MiniHack-LavaMultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Lava",
)
registration.register(
    id="MiniHack-LavaMultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Lava",
)
registration.register(
    id="MiniHack-LavaMultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Lava",
)


# MiniGrid: MonsterpedMultiRoom
class MiniHackMultiRoomN2Monster(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 40)
        kwargs["num_mon"] = 3
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N2-S4-v0", **kwargs
        )


class MiniHackMultiRoomN4Monster(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 120)
        kwargs["num_mon"] = 6
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N4-S5-v0", **kwargs
        )


class MiniHackMultiRoomN6Monster(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 240)
        kwargs["num_mon"] = 9
        super().__init__(*args, env_name="MiniGrid-MultiRoom-N6-v0", **kwargs)


# MiniGrid: MonsterMultiRoom
registration.register(
    id="MiniHack-MonsterMultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Monster",
)
registration.register(
    id="MiniHack-MonsterMultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Monster",
)
registration.register(
    id="MiniHack-MonsterMultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Monster",
)


# MiniGrid: ExtremeMultiRoom
class MiniHackMultiRoomN2Extreme(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 40)
        kwargs["num_mon"] = 3
        kwargs["lava_walls"] = True
        kwargs["door_state"] = "locked"
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N2-S4-v0", **kwargs
        )


class MiniHackMultiRoomN4Extreme(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 120)
        kwargs["num_mon"] = 6
        kwargs["lava_walls"] = True
        kwargs["door_state"] = "locked"
        super().__init__(
            *args, env_name="MiniGrid-MultiRoom-N4-S5-v0", **kwargs
        )


class MiniHackMultiRoomN6Extreme(MiniGridHack):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 240)
        kwargs["num_mon"] = 9
        kwargs["lava_walls"] = True
        kwargs["door_state"] = "locked"
        super().__init__(*args, env_name="MiniGrid-MultiRoom-N6-v0", **kwargs)


registration.register(
    id="MiniHack-ExtremeMultiRoom-N2-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN2Extreme",
)
registration.register(
    id="MiniHack-ExtremeMultiRoom-N4-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN4Extreme",
)
registration.register(
    id="MiniHack-ExtremeMultiRoom-N6-v0",
    entry_point="minihack.envs.minigrid:MiniHackMultiRoomN6Extreme",
)

# MiniGrid: LavaCrossing
registration.register(
    id="MiniHack-LavaCrossingS9N1-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N1-v0"},
)
registration.register(
    id="MiniHack-LavaCrossingS9N2-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N2-v0"},
)
registration.register(
    id="MiniHack-LavaCrossingS9N3-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS9N3-v0"},
)
registration.register(
    id="MiniHack-LavaCrossingS11N5-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-LavaCrossingS11N5-v0"},
)

# MiniGrid: Simple Crossing
registration.register(
    id="MiniHack-SimpleCrossingS9N1-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N1-v0"},
)
registration.register(
    id="MiniHack-SimpleCrossingS9N2-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N2-v0"},
)
registration.register(
    id="MiniHack-SimpleCrossingS9N3-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS9N3-v0"},
)
registration.register(
    id="MiniHack-SimpleCrossingS11N5-v0",
    entry_point="minihack.envs.minigrid:MiniGridHack",
    kwargs={"env_name": "MiniGrid-SimpleCrossingS11N5-v0"},
)
