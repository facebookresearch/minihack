# Copyright (c) Facebook, Inc. and its affiliates.

from collections import defaultdict
import gym
import numpy as np
import queue
import threading


class CounterWrapper(gym.Wrapper):
    def __init__(self, env, state_counter="none"):
        # intialize state counter
        self.state_counter = state_counter
        if self.state_counter != "none":
            self.state_count_dict = defaultdict(int)
        # this super() goes to the parent of the particular task, not to object
        super().__init__(env)

    def step(self, action):
        # add state counting to step function if desired
        step_return = self.env.step(action)
        if self.state_counter == "none":
            # do nothing
            return step_return

        obs, reward, done, info = step_return

        if self.state_counter == "ones":
            # treat every state as unique
            state_visits = 1
        elif self.state_counter == "coordinates":
            # use the location of the agent in the dungeon to accumulate visits
            features = obs["blstats"]
            x = features[0]
            y = features[1]
            d = features[12]
            coord = (d, x, y)
            self.state_count_dict[coord] += 1
            state_visits = self.state_count_dict[coord]
        else:
            raise NotImplementedError("state_counter=%s" % self.state_counter)

        obs.update(state_visits=np.array([state_visits]))

        if done:
            self.state_count_dict.clear()

        return step_return

    def reset(self, wizkit_items=None):
        # reset state counter when env resets
        obs = self.env.reset(wizkit_items=wizkit_items)
        if self.state_counter != "none":
            self.state_count_dict.clear()
            # current state counts as one visit
            obs.update(state_visits=np.array([1]))
        return obs


class CropWrapper(gym.Wrapper):
    def __init__(self, env, h=9, w=9, pad=0, keys=("tty_chars", "tty_colors")):
        super().__init__(env)
        self.env = env
        self.h = h
        self.w = w
        self.pad = pad
        self.keys = keys
        assert self.h % 2 == 1
        assert self.w % 2 == 1
        self.last_observation = None
        self._actions = self.env._actions

    def render(self, mode="human", crop=True):
        self.env.render()
        obs = self.last_observation
        tty_chars_crop = obs["tty_chars_crop"]
        tty_colors_crop = obs["tty_colors_crop"]
        rendering = self.env.get_tty_rendering(
            tty_chars_crop, tty_colors_crop, print_guides=True
        )
        print(rendering)

    def step(self, action):
        next_state, reward, done, info = self.env.step(action)

        dh = self.h // 2
        dw = self.w // 2

        (y, x) = next_state["tty_cursor"]
        x += dw
        y += dh

        for key in self.keys:
            obs = next_state[key]
            obs = np.pad(
                obs,
                pad_width=(dw, dh),
                mode="constant",
                constant_values=self.pad,
            )
            next_state[key + "_crop"] = obs[
                y - dh : y + dh + 1, x - dw : x + dw + 1
            ]

        self.last_observation = next_state

        return next_state, reward, done, info

    def reset(self, wizkit_items=None):
        obs = self.env.reset(wizkit_items=wizkit_items)
        obs["tty_chars_crop"] = np.zeros((self.h, self.w), dtype=np.uint8)
        obs["tty_colors_crop"] = np.zeros((self.h, self.w), dtype=np.int8)
        self.last_observation = obs
        return obs


class PrevWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.env = env
        self.last_observation = None
        self._actions = self.env._actions

    def step(self, action):
        next_state, reward, done, info = self.env.step(action)
        next_state["prev_reward"] = np.array([reward], dtype=np.float32)
        next_state["prev_action"] = np.array([action], dtype=np.uint8)

        self.last_observation = next_state

        return next_state, reward, done, info

    def reset(self, wizkit_items=None):
        obs = self.env.reset(wizkit_items=wizkit_items)
        obs["prev_reward"] = np.zeros(1, dtype=np.float32)
        obs["prev_action"] = np.zeros(1, dtype=np.uint8)
        self.last_observation = obs
        return obs


def target(resetqueue, readyqueue):
    while True:
        env = resetqueue.get()
        if env is None:
            return
        obs = env.reset()
        readyqueue.put((obs, env))


class CachedEnvWrapper(gym.Env):
    def __init__(self, envs, num_threads=2):
        self._envs = envs

        # This could alternatively also use concurrent.futures. I hesitate to do
        # that as futures.wait would have me deal with sets all the time where they
        # are really not necessary.
        self._resetqueue = queue.SimpleQueue()
        self._readyqueue = queue.SimpleQueue()

        self._threads = [
            threading.Thread(
                target=target, args=(self._resetqueue, self._readyqueue)
            )
            for _ in range(num_threads)
        ]
        for t in self._threads:
            t.start()

        for env in envs[1:]:
            self._resetqueue.put(env)
        self._env = envs[0]

    def reset(self):
        self._resetqueue.put(self._env)
        obs, self._env = self._readyqueue.get()
        return obs

    def step(self, action):
        return self._env.step(action)

    def close(self):
        for _ in self._threads:
            self._resetqueue.put(None)

        for t in self._threads:
            t.join()

        for env in self._envs:
            env.close()

    def seed(self, seed=None):
        self._env.seed(seed)

    def unwrapped(self):
        return self._env

    def __str__(self):
        return "<CachedEnvWrapper envs=%s>" % [str(env) for env in self._envs]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False  # Propagate exception.
