# Copyright (c) Facebook, Inc. and its affiliates.
import gym
import numpy as np
import time
import minihack
import argparse
from minihack.agent.common.envs.wrapper import CachedEnvWrapper


def compare_speed(env, num_steps, queue_size):
    env_vanila = gym.make(env)
    test_speed(env_vanila, env, num_steps)
    env_vanila.close()

    env_queue = []
    for _ in range(queue_size):
        env_queue.append(gym.make(env))
    env_cached = CachedEnvWrapper(env_queue)
    test_speed(env_cached, env, num_steps)
    env_cached.close()


def test_speed(env, env_name, num_steps):
    """Tests the speed of an environment for num_steps steps."""
    start_time = time.time()
    env.reset()
    for _ in range(num_steps):
        _, _, done, _ = env.step(np.random.randint(8))
        if done:
            env.reset()
    total_time = time.time() - start_time

    print(
        "Took {:.4f}s to perform {} steps on {} envs - {:.2f} FPS".format(
            total_time, num_steps, env_name, num_steps / total_time
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="MiniHack-MultiRoom-N2-Lava-v0",
        help="Gym environment spec. Defaults to 'MiniHack-MultiRoom-N2-Lava-v0'.",
    )
    parser.add_argument(
        "--num_steps",
        type=int,
        default=10000,
        help="Number of steps to run.",
    )
    parser.add_argument(
        "--queue_size",
        type=int,
        default=2,
        help="Number of environments in the queue.",
    )
    flags = parser.parse_args()

    compare_speed(**vars(flags))


if __name__ == "__main__":
    main()
