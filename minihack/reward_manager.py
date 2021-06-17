# Copyright (c) Facebook, Inc. and its affiliates.
from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, List, Tuple

if TYPE_CHECKING:
    from minihack import MiniHack

from nle.nethack import Command, CompassDirection

Y_cmd = CompassDirection.NW


class EventType(enum.IntEnum):
    MESSAGE = 0
    LOC_ACTION = 1
    COORD = 2
    LOC = 3


COMESTIBLES = [
    "orange",
    "meatball",
    "meat ring",
    "meat stick",
    "kelp frond",
    "eucalyptus leaf",
    "clove of garlic",
    "sprig of wolfsbane",
    "carrot",
    "egg",
    "banana",
    "melon",
    "candy bar",
    "lump of royal jelly",
]


class Event(ABC):
    def __init__(
        self,
        reward: float,
        repeatable: bool,
        terminal_required: bool,
        terminal_sufficient: bool,
    ):
        self.reward = reward
        self.repeatable = repeatable
        self.terminal_required = terminal_required
        self.terminal_sufficient = terminal_sufficient
        self.achieved = False

    @abstractmethod
    def check(self, env, previous_observation, action, observation) -> float:
        pass

    def reset(self):
        self.achieved = False

    def _set_achieved(self) -> float:
        if not self.repeatable:
            self.achieved = True
        return self.reward


def _standing_on_top(env, location):
    return not env.screen_contains(location)


class LocActionEvent(Event):
    def __init__(
        self, *args, loc: str, action: Command, status: bool = False, index: int = -1
    ):
        super().__init__(*args)
        self.loc = loc
        self.action = action
        self.status = status
        self.index = index

    def check(self, env, previous_observation, action, observation) -> float:
        if env._actions[action] == self.action and _standing_on_top(env, self.loc):
            self.status = True
        elif env._actions[action] == Y_cmd and self.status:
            return self._set_achieved()
        else:
            self.status = False
        return 0

    def reset(self):
        super().reset()
        self.status = False


class LocEvent(Event):
    def __init__(self, *args, loc: str):
        super().__init__(*args)
        self.loc = loc

    def check(self, env, previous_observation, action, observation) -> float:
        if _standing_on_top(env, self.loc):
            return self._set_achieved()
        return 0.0


class CoordEvent(Event):
    def __init__(self, *args, coordinates: Tuple[int, int]):
        super().__init__(*args)
        self.coordinates = coordinates

    def check(self, env, previous_observation, action, observation) -> float:
        coordinates = tuple(observation[env._blstats_index][:2])
        if self.coordinates == coordinates:
            return self._set_achieved()
        return 0.0


class MessageEvent(Event):
    def __init__(self, *args, messages: List[str]):
        super().__init__(*args)
        self.messages = messages

    def check(self, env, previous_observation, action, observation) -> float:
        curr_msg = (
            observation[env._original_observation_keys.index("message")]
            .tobytes()
            .decode("utf-8")
        )
        for msg in self.messages:
            if msg in curr_msg:
                return self._set_achieved()
        return 0.0


class AbstractRewardManager(ABC):
    def __init__(self):
        self.terminal_sufficient = None
        self.terminal_required = None

    @abstractmethod
    def collect_reward(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def check_episode_end_call(
        self, env, previous_observation, action, observation
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError


class RewardManager(AbstractRewardManager):
    """This class is used for managing rewards, events and termination for
    MiniHack tasks.

    Some notes on the ordering or calls in the MiniHack/NetHack base class:
    * `step(action)` is called on the environment
    * Within `step`, first a copy of the last observation is made, and then the
      underlying NetHack game is stepped
    * Then `_is_episode_end(observation)` is called to check whether this the
      episode has ended (and this is overridden if we've gone over our
      max_steps, or the underlying NetHack game says we're done (i.e. we died)
    * Then `_reward_fn(last_observation, observation)` is called to calculate
      the reward at this time-step
    * if `end_status` tells us the game is done, we quit the game
    * then `step` returns the observation, calculated reward, done and some stats

    All this means that we need to check whether an observation is terminal in
    `_is_episode_end` before we're calculating the reward function.

    The call of `_is_episode_end` in `MiniHack` will call `check_episode_end_call` in
    this class, which checks for termination and accumulates any reward, which
    is returned and zeroed in `collect_reward`
    """

    def __init__(self):
        self.events: List[Event] = []
        self.custom_reward_functions: List[
            Callable[[MiniHack, Any, int, Any], float]
        ] = []
        self._reward = 0.0

        # Only used for GroupedRewardManager
        self.terminal_sufficient = None
        self.terminal_required = None

    def add_custom_reward_fn(
        self, reward_fn: Callable[[MiniHack, Any, int, Any], float]
    ) -> None:
        """Add a custom reward function which is called every step to calculate reward.

        The function should be a callable which takes the environment, previous
        observation, action and current observation and returns a float reward.
        """
        self.custom_reward_functions.append(reward_fn)

    def add_event(self, event: Event):
        self.events.append(event)

    def _add_message_event(
        self, msgs, reward, repeatable, terminal_required, terminal_sufficient
    ):
        self.add_event(
            MessageEvent(
                reward,
                repeatable,
                terminal_required,
                terminal_sufficient,
                messages=msgs,
            )
        )

    def _add_loc_action_event(
        self, loc, action, reward, repeatable, terminal_required, terminal_sufficient
    ):
        try:
            action = Command[action.upper()]
        except KeyError:
            raise KeyError(
                "Action {} is not in the action space.".format(action.upper())
            )

        self.add_event(
            LocActionEvent(
                reward,
                repeatable,
                terminal_required,
                terminal_sufficient,
                loc=loc.lower(),
                action=action,
            )
        )

    def add_eat_event(
        self,
        name,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        msgs = [
            f"This {name} is delicious",
            "Blecch!  Rotten food!",
            "last bite of your meal",
        ]
        if name == "apple":
            msgs.append("Delicious!  Must be a Macintosh!")
            msgs.append("Core dumped.")
        if name == "pear":
            msgs.append("Core dumped.")

        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_wield_event(
        self,
        name,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        msgs = [f"{name} wields itself to your hand!", f"{name} (weapon in hand)"]
        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_wear_event(
        self,
        name,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        msgs = [f"You are now wearing a {name}"]
        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_amulet_event(
        self,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        self._add_message_event(
            ["amulet (being worn)."],
            reward,
            repeatable,
            terminal_required,
            terminal_sufficient,
        )

    def add_kill_event(
        self,
        name,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        # TODO investigate
        self._add_message_event(
            [f"You kill the {name}"],
            reward,
            repeatable,
            terminal_required,
            terminal_sufficient,
        )

    def add_message_event(
        self,
        msgs: List[str],
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_positional_event(
        self,
        place_name,
        action_name,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        self._add_loc_action_event(
            place_name,
            action_name,
            reward,
            repeatable,
            terminal_required,
            terminal_sufficient,
        )

    def add_coordinate_event(
        self,
        coordinates,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        self.add_event(
            CoordEvent(
                reward,
                repeatable,
                terminal_required,
                terminal_sufficient,
                coordinates=coordinates,
            )
        )

    def add_location_event(
        self,
        location: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        self.add_event(
            LocEvent(
                reward,
                repeatable,
                terminal_required,
                terminal_sufficient,
                loc=location,
            )
        )

    def _set_achieved(self, event: Event) -> float:
        if not event.repeatable:
            event.achieved = True
        return event.reward

    def _standing_on_top(self, env, name):
        """Returns whether the agents is standing on top of the given object.
        The object name (e.g. altar, sink, fountain) must exist on the map.
        The function will return True if the object name is not in the screen
        descriptions (with agent info taking the space of the corresponding
        tile rather than the object).
        """
        return not env.screen_contains(name)

    def check_episode_end_call(
        self, env, previous_observation, action, observation
    ) -> bool:
        """Check if the task has ended, and accumulate any reward from the
        transition in self._reward."""
        reward = 0.0
        for event in self.events:
            if event.achieved:
                continue
            reward += event.check(env, previous_observation, action, observation)

        for custom_reward_function in self.custom_reward_functions:
            reward += custom_reward_function(
                env, previous_observation, action, observation
            )
        self._reward += reward
        return self._check_complete()

    def _check_complete(self) -> bool:
        """Checks whether the episode is complete.

        Requires any event which is sufficient to be achieved, OR all required
        events to be achieved."""
        result = True
        for event in self.events:
            # This event is enough, we're done
            if event.achieved and event.terminal_sufficient:
                return True
            # We need this event and we haven't done it, we're not done
            if not event.achieved and event.terminal_required:
                result = False

        # We've achieved all terminal_required events, we're done
        return result

    def collect_reward(self):
        """Return reward calculated and accumulated in check_episode_end_call,
        and then reset it."""
        result = self._reward
        self._reward = 0.0
        return result

    def reset(self):
        self._reward = 0.0
        for event in self.events:
            event.reset()


class SequentialRewardManager(RewardManager):
    """Ignore terminal_required and terminal_sufficient, and just require every
    event is completed in the order it is added to the reward manager."""

    def __init__(self):
        self.current_event_idx = 0
        super().__init__()

    def check_episode_end_call(self, env, previous_observation, action, observation):
        event = self.events[self.current_event_idx]
        reward = event.check(env, previous_observation, action, observation)
        if event.achieved:
            self.current_event_idx += 1
        self._reward += reward
        return self._check_complete()

    def _check_complete(self) -> bool:
        return self.current_event_idx == len(self.events)


class GroupedRewardManager(AbstractRewardManager):
    """Operates as a collection of reward managers.

    The rewards from each reward manager are summed, and termination can be
    specified by terminal_sufficient and terminal_required on each reward
    manager.

    Given this can be nested arbitrarily deeply (as each reward manager could
    itself be a GroupedRewardManager), this enables complex specification of
    groups of rewards.
    """

    def __init__(self):
        self.reward_managers: List[AbstractRewardManager] = []

    def check_episode_end_call(
        self, env, previous_observation, action, observation
    ) -> bool:
        for reward_manager in self.reward_managers:
            result = reward_manager.check_episode_end_call(
                env, previous_observation, action, observation
            )
            # This reward manager has completed and it's sufficient so we're done
            if reward_manager.terminal_sufficient and result:
                return True
            # This reward manager is required and hasn't completed, so we're not done
            if reward_manager.terminal_required and not result:
                return False

        # If we've got here we've completed all required reward managers, so we're done
        return True

    def add_reward_manager(
        self,
        reward_manager: AbstractRewardManager,
        terminal_required: bool,
        terminal_sufficient: bool,
    ) -> None:
        reward_manager.terminal_required = terminal_required
        reward_manager.terminal_sufficient = terminal_sufficient
        self.reward_managers.append(reward_manager)

    def collect_reward(self):
        reward = 0.0
        for reward_manager in self.reward_managers:
            reward += reward_manager.collect_reward()
        return reward

    def reset(self):
        self._reward = 0.0
        for reward_manager in self.reward_managers:
            reward_manager.reset()
