# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackSkill, LevelGenerator, RewardManager
from minihack.envs import register


class MiniHackEat(MiniHackSkill):
    """Environment for "eat" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackEatFixed(MiniHackSkill):
    """Environment for "eat" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackEatDistr(MiniHackSkill):
    """Environment for "eat" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("apple", "%")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_eat_event("apple")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWield(MiniHackSkill):
    """Environment for "wield" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("dagger", ")")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wield_event("dagger")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWieldFixed(MiniHackSkill):
    """Environment for "wield" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("dagger", ")", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wield_event("dagger")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWieldDistr(MiniHackSkill):
    """Environment for "wield" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("dagger", ")")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wield_event("dagger")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWear(MiniHackSkill):
    """Environment for "wear" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWearFixed(MiniHackSkill):
    """Environment for "wear" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackWearDistr(MiniHackSkill):
    """Environment for "wear" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("robe", "[")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_wear_event("robe")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOn(MiniHackSkill):
    """Environment for "put on" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("amulet of life saving", '"')
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_amulet_event()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOnFixed(MiniHackSkill):
    """Environment for "put on" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("amulet of life saving", '"', place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_amulet_event()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPutOnDistr(MiniHackSkill):
    """Environment for "put on" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("amulet of life saving", '"')
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_amulet_event()

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZap(MiniHackSkill):
    """Environment for "zap" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("enlightenment", "/")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The feeling subsides."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZapFixed(MiniHackSkill):
    """Environment for "zap" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("enlightenment", "/", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The feeling subsides."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackZapDistr(MiniHackSkill):
    """Environment for "zap" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("enlightenment", "/")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["The feeling subsides."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackRead(MiniHackSkill):
    """Environment for "read" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("blank paper", "?")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["This scroll seems to be blank."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackReadFixed(MiniHackSkill):
    """Environment for "read" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("blank paper", "?", place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["This scroll seems to be blank."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackReadDistr(MiniHackSkill):
    """Environment for "read" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_object("blank paper", "?")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_message_event(["This scroll seems to be blank."])

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPray(MiniHackSkill):
    """Environment for "pray" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_altar("random", "neutral", "altar")
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPrayFixed(MiniHackSkill):
    """Environment for "pray" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_altar((0, 0), "neutral", "altar")
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackPrayDistr(MiniHackSkill):
    """Environment for "pray" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_altar("random", "neutral", "altar")
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("altar", "pray")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSink(MiniHackSkill):
    """Environment for "sink" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_sink()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("sink", "quaff")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSinkFixed(MiniHackSkill):
    """Environment for "sink" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_sink(place=(0, 0))
        lvl_gen.set_start_pos((2, 2))
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("sink", "quaff")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackSinkDistr(MiniHackSkill):
    """Environment for "sink" task."""

    def __init__(self, *args, **kwargs):
        lvl_gen = LevelGenerator(w=5, h=5, lit=True)
        lvl_gen.add_sink()
        lvl_gen.add_monster()
        lvl_gen.add_object()
        des_file = lvl_gen.get_des()

        reward_manager = RewardManager()
        reward_manager.add_positional_event("sink", "quaff")

        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackClosedDoor(MiniHackSkill):
    """Environment for "open" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="closed_door.des", **kwargs)


class MiniHackLockedDoor(MiniHackSkill):
    """Environment for "kick" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="locked_door.des", **kwargs)


class MiniHackLockedDoorFixed(MiniHackSkill):
    """Environment for "kick" task."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="locked_door_fixed.des", **kwargs)


# Tasks (w/o doors)
register(
    id="MiniHack-Eat-v0",
    entry_point="minihack.envs.skills_simple:MiniHackEat",
)
register(
    id="MiniHack-Pray-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPray",
)
register(
    id="MiniHack-Sink-v0",
    entry_point="minihack.envs.skills_simple:MiniHackSink",
)
register(
    id="MiniHack-Wield-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWield",
)
register(
    id="MiniHack-Wear-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWear",
)
register(
    id="MiniHack-PutOn-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPutOn",
)
register(
    id="MiniHack-Zap-v0",
    entry_point="minihack.envs.skills_simple:MiniHackZap",
)
register(
    id="MiniHack-Read-v0",
    entry_point="minihack.envs.skills_simple:MiniHackRead",
)

# Fixed version of tasks
register(
    id="MiniHack-Eat-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackEatFixed",
)
register(
    id="MiniHack-Pray-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPrayFixed",
)
register(
    id="MiniHack-Sink-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackSinkFixed",
)
register(
    id="MiniHack-Wield-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWieldFixed",
)
register(
    id="MiniHack-Wear-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWearFixed",
)
register(
    id="MiniHack-PutOn-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPutOnFixed",
)
register(
    id="MiniHack-Zap-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackZapFixed",
)
register(
    id="MiniHack-Read-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackReadFixed",
)

# Task versions with random distractions
register(
    id="MiniHack-Eat-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackEatDistr",
)
register(
    id="MiniHack-Pray-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPrayDistr",
)
register(
    id="MiniHack-Sink-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackSinkDistr",
)
register(
    id="MiniHack-Wield-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWieldDistr",
)
register(
    id="MiniHack-Wear-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackWearDistr",
)
register(
    id="MiniHack-PutOn-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackPutOnDistr",
)
register(
    id="MiniHack-Zap-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackZapDistr",
)
register(
    id="MiniHack-Read-Distr-v0",
    entry_point="minihack.envs.skills_simple:MiniHackReadDistr",
)

# Tasks involvign doors
register(
    id="MiniHack-ClosedDoor-v0",
    entry_point="minihack.envs.skills_simple:MiniHackClosedDoor",
)
register(
    id="MiniHack-LockedDoor-v0",
    entry_point="minihack.envs.skills_simple:MiniHackLockedDoor",
)
register(
    id="MiniHack-LockedDoor-Fixed-v0",
    entry_point="minihack.envs.skills_simple:MiniHackLockedDoorFixed",
)
