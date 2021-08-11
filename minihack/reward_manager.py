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
    """An event which can occur in a MiniHack episode.

    This is the base class of all other events.
    """

    def __init__(
        self,
        reward: float,
        repeatable: bool,
        terminal_required: bool,
        terminal_sufficient: bool,
    ):
        """Initialise the Event.

        :param reward: The reward for the event occuring
        :param repeatable: Whether the event can occur repeated (i.e. if the
            reward can be collected repeatedly
        :param terminal_required: Whether this event is required for the
            episode to terminate
        :param terminal_sufficient: Whether this event causes the episode to
            terminate on it's own
        """
        self.reward = reward
        self.repeatable = repeatable
        self.terminal_required = terminal_required
        self.terminal_sufficient = terminal_sufficient
        self.achieved = False

    @abstractmethod
    def check(self, env, previous_observation, action, observation) -> float:
        """Check whether the environment is in the state such that this event
        has occured.

        :param env: The MiniHack environment in question.
        :param previous_observation: The previous state observation.
        :param action: The action taken.
        :param observation: The current observation.
        :returns: A float reward.
        """
        pass

    def reset(self):
        """Reset the event, if there's any state necessary."""
        self.achieved = False

    def _set_achieved(self) -> float:
        if not self.repeatable:
            self.achieved = True
        return self.reward


def _standing_on_top(env, location):
    return not env.screen_contains(location)


class LocActionEvent(Event):
    """An event which checks whether `action` is performed at `loc` location."""

    def __init__(
        self,
        *args,
        loc: str,
        action: Command,
    ):
        """Initialise the Event.

        :param loc: The name of the location to reach
        :param action: The action to perform
        :param reward: The reward for the event occuring
        :param repeatable: Whether the event can occur repeated (i.e. if the
            reward can be collected repeatedly
        :param terminal_required: Whether this event is required for the
            episode to terminate
        :param terminal_sufficient: Whether this event causes the episode to
            terminate on it's own
        """
        super().__init__(*args)
        self.loc = loc
        self.action = action
        self.status = False

    def check(self, env, previous_observation, action, observation) -> float:
        if env._actions[action] == self.action and _standing_on_top(
            env, self.loc
        ):
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
    """An event which checks whether `loc` location is reached."""

    def __init__(self, *args, loc: str):
        super().__init__(*args)
        """Initialise the Event.

        :param loc: The name of the location to reach.
        :param reward: The reward for the event occuring
        :param repeatable: Whether the event can occur repeated (i.e. if the
            reward can be collected repeatedly
        :param terminal_required: Whether this event is required for the
            episode to terminate
        :param terminal_sufficient: Whether this event causes the episode to
            terminate on it's own
        """
        self.loc = loc

    def check(self, env, previous_observation, action, observation) -> float:
        if _standing_on_top(env, self.loc):
            return self._set_achieved()
        return 0.0


class CoordEvent(Event):
    """An event which occurs when reaching certain `coordinates`."""

    def __init__(self, *args, coordinates: Tuple[int, int]):
        """Initialise the Event.

        :param coordinates: The coordinates to reach for the event.
        :param reward: The reward for the event occuring
        :param repeatable: Whether the event can occur repeated (i.e. if the
            reward can be collected repeatedly
        :param terminal_required: Whether this event is required for the
            episode to terminate
        :param terminal_sufficient: Whether this event causes the episode to
            terminate on it's own
        """
        super().__init__(*args)
        self.coordinates = coordinates

    def check(self, env, previous_observation, action, observation) -> float:
        coordinates = tuple(observation[env._blstats_index][:2])
        if self.coordinates == coordinates:
            return self._set_achieved()
        return 0.0


class MessageEvent(Event):
    """An event which occurs when any of the `messages` appear."""

    def __init__(self, *args, messages: List[str]):
        """Initialise the Event.

        :param messages: The messages to be seen to trigger the event.
        :param reward: The reward for the event occuring
        :param repeatable: Whether the event can occur repeated (i.e. if the
            reward can be collected repeatedly
        :param terminal_required: Whether this event is required for the
            episode to terminate
        :param terminal_sufficient: Whether this event causes the episode to
            terminate on it's own
        """
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
        """Return reward calculated and accumulated in check_episode_end_call,
        and then reset it.

        :returns: Float reward.
        """
        raise NotImplementedError

    @abstractmethod
    def check_episode_end_call(
        self, env, previous_observation, action, observation
    ) -> bool:
        """Check if the task has ended, and accumulate any reward from the
        transition in self._reward.

        :param env: The MiniHack environment in question.
        :param previous_observation: The previous state observation.
        :param action: The action taken.
        :param observation: The current observation.
        :returns: Boolean whether the episode has ended

        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """Reset all events, to be called when a new episode occurs."""
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
        """Add a custom reward function which is called every step to calculate
        reward.

        The function should be a callable which takes the environment, previous
        observation, action and current observation and returns a float reward.

        :param reward_fn: A reward function which takes an environment,
            previous observation, action, next observation and returns a reward.

        """
        self.custom_reward_functions.append(reward_fn)

    def add_event(self, event: Event):
        """Add an event to be managed by the reward manager.

        :param event: The event to be added.
        """
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
        self,
        loc,
        action,
        reward,
        repeatable,
        terminal_required,
        terminal_sufficient,
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
        name: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add an event which is triggered when `name` is eaten.

        :param name: The (string) name of the object being eaten.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        name: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add event which is triggered when `name` is wielded.

        :param name: The name of the weapon to be wielded
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
        msgs = [
            f"{name} wields itself to your hand!",
            f"{name} (weapon in hand)",
        ]
        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_wear_event(
        self,
        name: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add event which is triggered when `name` is worn.

        :param name: The name of the armour to be worn.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        """Add event which is triggered when an amulet is worn.

        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
        self._add_message_event(
            ["amulet (being worn)."],
            reward,
            repeatable,
            terminal_required,
            terminal_sufficient,
        )

    def add_kill_event(
        self,
        name: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add event which is triggered when `name` is killed.

        :param name: The name of the monster to be killed.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        """Add event which is triggered when any `msgs` are seen..

        :param msgs: A list of messages to trigger this event.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
        self._add_message_event(
            msgs, reward, repeatable, terminal_required, terminal_sufficient
        )

    def add_positional_event(
        self,
        place_name: str,
        action_name: str,
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add event which is triggered on taking `action_name` at `place_name`..

        :param place_name: The name of place to trigger the event.
        :param action_name: The name of the action to trigger the event.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        coordinates: Tuple[int, int],
        reward=1,
        repeatable=False,
        terminal_required=True,
        terminal_sufficient=False,
    ):
        """Add event which is triggered on when reaching `coordinates`.

        :param coordinates: The coordinates to be reached (tuple of ints).
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        """Add event which is triggered on reaching `location`.

        :param name: The location to be reached.
        :param reward: The reward for this event.
        :param repeatable: Whether this event can be triggered multiple times.
        :param terminal_required: Whether this event is required for termination.
        :param terminal_sufficient: Whether this event is sufficient for termination.
        """
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
        reward = 0.0
        for event in self.events:
            if event.achieved:
                continue
            reward += event.check(
                env, previous_observation, action, observation
            )

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

    def collect_reward(self) -> float:
        result = self._reward
        self._reward = 0.0
        return result

    def reset(self):
        self._reward = 0.0
        for event in self.events:
            event.reset()


class SequentialRewardManager(RewardManager):
    """A reward manager that ignores terminal_required and terminal_sufficient,
    and just require every event is completed in the order it is added to the
    reward manager.
    """

    def __init__(self):
        self.current_event_idx = 0
        super().__init__()

    def check_episode_end_call(
        self, env, previous_observation, action, observation
    ):
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
            # This reward manager has completed and it's sufficient so we're
            # done
            if reward_manager.terminal_sufficient and result:
                return True
            # This reward manager is required and hasn't completed, so we're
            # not done
            if reward_manager.terminal_required and not result:
                return False

        # If we've got here we've completed all required reward managers, so
        # we're done
        return True

    def add_reward_manager(
        self,
        reward_manager: AbstractRewardManager,
        terminal_required: bool,
        terminal_sufficient: bool,
    ) -> None:
        """Add a new reward manager, with `terminal_sufficient` and
        `terminal_required` acting as for individual events.

        :param: reward_manager: The reward manager to be added.
        :param terminal_required: Whether this reward manager terminating is
                                  required for the episode to terminate.
        :param terminal_sufficient: Whether this reward manager terminating is
                                    sufficient for the episode to terminate.

        """
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
