#!/usr/bin/env python
#
# Copyright (c) Facebook, Inc. and its affiliates.
import os
import random
import sys
import tempfile

import gym
import numpy as np
import pytest

import minihack
import nle
from nle import nethack


def get_minihack_env_ids():
    specs = gym.envs.registry.all()
    skip_envs_list = [
        "MiniHack-Navigation-Custom-v0",
        "MiniHack-Skill-Custom-v0",
    ]
    skip_env_substring = [
        "Boxoban",
        "MultiRoom",
        "SimpleCrossingS",
        "LavaCrossingS",
    ]
    return [
        spec.id
        for spec in specs
        if spec.id.startswith("MiniHack")
        and spec.id not in skip_envs_list
        and all(env_sub not in spec.id for env_sub in skip_env_substring)
    ]


def rollout_env(env, max_rollout_len):
    """Produces a rollout and asserts step outputs.

    Returns final reward. Does not assume that the environment has already been
    reset.
    """
    obs = env.reset()
    assert env.observation_space.contains(obs)

    for _ in range(max_rollout_len):
        a = env.action_space.sample()
        obs, reward, done, info = env.step(a)
        assert env.observation_space.contains(obs)
        assert isinstance(reward, float)
        assert isinstance(done, bool)
        assert isinstance(info, dict)
        if done:
            break
    env.close()
    return reward


def term_screen(obs):
    return "\n".join("".join(chr(c) for c in row) for row in obs["tty_chars"])


def compare_rollouts(env0, env1, max_rollout_len):
    """Checks that two active environments return the same rollout.

    Assumes that the environments have already been reset.
    """
    step = 0
    while True:
        a = env0.action_space.sample()
        obs0, reward0, done0, info0 = env0.step(a)
        obs1, reward1, done1, info1 = env1.step(a)
        step += 1

        s0, s1 = term_screen(obs0), term_screen(obs1)
        top_ten_msg = "You made the top ten list!"
        if top_ten_msg in s0:
            assert top_ten_msg in s1
        else:
            np.testing.assert_equal(obs0, obs1)
        assert reward0 == reward1
        assert done0 == done1

        assert info0 == info1

        if done0 or step >= max_rollout_len:
            return


@pytest.mark.parametrize("env_name", get_minihack_env_ids())
@pytest.mark.parametrize("wizard", [False, True])
class TestGymEnv:
    @pytest.fixture(autouse=True)  # will be applied to all tests in class
    def make_cwd_tmp(self, tmpdir):
        """Makes cwd point to the test's tmpdir."""
        with tmpdir.as_cwd():
            yield

    def test_init(self, env_name, wizard):
        """Tests default initialization given standard env specs."""
        env = gym.make(env_name, wizard=wizard)
        del env

    def test_reset(self, env_name, wizard):
        """Tests default initialization given standard env specs."""
        env = gym.make(env_name, wizard=wizard)
        obs = env.reset()
        assert env.observation_space.contains(obs)

    def test_chars_colors_specials(self, env_name, wizard):
        env = gym.make(
            env_name,
            observation_keys=("chars", "colors", "specials", "blstats"),
        )
        obs = env.reset()

        assert "specials" in obs
        x, y = obs["blstats"][:2]

        # That's where you're @.
        assert obs["chars"][y, x] == ord("@")

        # You're bright (4th bit, 8) white (7), too.
        assert obs["colors"][y, x] == 8 ^ 7

    def test_default_wizard_mode(self, env_name, wizard):
        if wizard:
            env = gym.make(env_name, wizard=wizard)
            assert "playmode:debug" in env.env._options
        else:
            # do not send a parameter to test a default
            env = gym.make(env_name)
            assert "playmode:debug" not in env.env._options


@pytest.mark.parametrize(
    "env_name",
    [
        e
        for e in get_minihack_env_ids()
        if "MazeWalk" in e or "WoD" in e or "Room" in e or "Eat" in e
    ],
)
@pytest.mark.parametrize("rollout_len", [500])
class TestGymEnvRollout:
    @pytest.fixture(autouse=True)  # will be applied to all tests in class
    def make_cwd_tmp(self, tmpdir):
        """Makes cwd point to the test's tmpdir."""
        with tmpdir.as_cwd():
            yield

    def test_rollout(self, env_name, rollout_len):
        """Tests rollout_len steps (or until termination) of random policy."""
        with tempfile.TemporaryDirectory() as savedir:
            env = gym.make(env_name, savedir=savedir)
            rollout_env(env, rollout_len)
            env.close()

            assert os.path.exists(
                os.path.join(savedir, "nle.%i.0.ttyrec.bz2" % os.getpid())
            )

    def test_rollout_no_archive(self, env_name, rollout_len):
        """Tests rollout_len steps (or until termination) of random policy."""
        env = gym.make(env_name, savedir=None)
        assert env.savedir is None
        assert env._stats_file is None
        assert env._stats_logger is None
        rollout_env(env, rollout_len)

    def test_seed_interface_output(self, env_name, rollout_len):
        """Tests whether env.seed output can be reused correctly."""

        env0 = gym.make(env_name)
        env1 = gym.make(env_name)

        seed_list0 = env0.seed()
        env0.reset()

        assert env0.get_seeds() == seed_list0

        seed_list1 = env1.seed(*seed_list0)
        assert seed_list0 == seed_list1

    def test_seed_rollout_seeded(self, env_name, rollout_len):
        """Tests that two seeded envs return same step data."""

        observation_keys = (
            "tty_chars",
            "glyphs",
            "chars",
            "specials",
            "colors",
        )
        env0 = gym.make(env_name, observation_keys=observation_keys)
        env1 = gym.make(env_name, observation_keys=observation_keys)

        env0.seed(123456, 789012)
        obs0 = env0.reset()
        seeds0 = env0.get_seeds()

        assert seeds0 == (123456, 789012, False)

        env1.seed(*seeds0)
        obs1 = env1.reset()
        seeds1 = env1.get_seeds()

        assert seeds0 == seeds1

        np.testing.assert_equal(obs0, obs1)
        compare_rollouts(env0, env1, rollout_len)

    def test_seed_rollout_seeded_int(self, env_name, rollout_len):
        """Tests that two seeded envs return same step data."""

        observation_keys = (
            "tty_chars",
            "glyphs",
            "chars",
            "specials",
            "colors",
        )
        env0 = gym.make(env_name, observation_keys=observation_keys)
        env1 = gym.make(env_name, observation_keys=observation_keys)

        initial_seeds = (
            random.randrange(sys.maxsize),
            random.randrange(sys.maxsize),
            False,
        )
        env0.seed(*initial_seeds)
        obs0 = env0.reset()
        seeds0 = env0.get_seeds()

        env1.seed(*seeds0)
        obs1 = env1.reset()
        seeds1 = env1.get_seeds()

        assert seeds0 == seeds1 == initial_seeds

        np.testing.assert_equal(obs0, obs1)
        compare_rollouts(env0, env1, rollout_len)

    def test_render_ansi(self, env_name, rollout_len):
        env = gym.make(env_name)
        env.reset()
        for _ in range(rollout_len):
            action = env.action_space.sample()
            _, _, done, _ = env.step(action)
            if done:
                env.reset()
            output = env.render(mode="ansi")
            assert isinstance(output, str)
            assert len(output.replace("\n", "")) == np.prod(
                nle.env.DUNGEON_SHAPE
            )


class TestRoomReward:
    """Tests a few game dynamics."""

    @pytest.fixture(autouse=True)  # will be applied to all tests in class
    def make_cwd_tmp(self, tmpdir):
        """Makes cwd point to the test's tmpdir."""
        with tmpdir.as_cwd():
            yield

    @pytest.fixture
    def env(self):
        e = gym.make("MiniHack-Room-5x5-v0")
        try:
            yield e
        finally:
            e.close()

    def test_reward(self, env):
        _ = env.reset()

        for _ in range(4):
            _, reward, done, _ = env.step(env._actions.index(ord("j")))
            assert reward == 0.0
            assert not done

        for _ in range(3):
            _, reward, done, _ = env.step(env._actions.index(ord("l")))
            assert reward == 0.0
            assert not done

        # Hack to quit.
        _, reward, done, _ = env.step(env._actions.index(ord("l")))

        assert done
        assert reward == 1.0
