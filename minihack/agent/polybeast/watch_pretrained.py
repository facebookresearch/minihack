import argparse
import ast
import contextlib
import os
import time
import timeit

import gym
import torch
from omegaconf import OmegaConf

import nle  # noqa: F401
import minihack.agent.polybeast.models
from nle import nethack
import polyhydra

_ACTIONS = tuple(
    [nethack.MiscAction.MORE]
    + list(nethack.CompassDirection)
    + list(nethack.CompassDirectionLonger)
)


@contextlib.contextmanager
def dummy_context():
    yield None


def get_action(pretrained_model, obs, hidden, done):
    with torch.no_grad():
        for key in obs.keys():
            shape = obs[key].shape
            obs[key] = torch.Tensor(obs[key].reshape((1, 1, *shape)))

        obs["done"] = torch.BoolTensor([done])

        out, hidden = pretrained_model(obs, hidden)

        action = out["action"]
    input()
    return action, hidden


def load_model(env, pretrained_path, pretrained_config_path):
    flags = OmegaConf.load(pretrained_config_path)
    flags["env"] = env
    flags = polyhydra.get_common_flags(flags)
    flags = polyhydra.get_environment_flags(flags)
    flags = polyhydra.get_learner_flags(flags)
    model = minihack.agent.polybeast.models.create_model(
        flags, torch.device("cpu")
    )

    checkpoint_states = torch.load(
        pretrained_path, map_location=torch.device("cpu")
    )

    model.load_state_dict(checkpoint_states["model_state_dict"])

    hidden = model.initial_state(batch_size=1)
    return model, hidden


def play(
    env,
    ngames,
    max_steps,
    seeds,
    savedir,
    no_render,
    render_mode,
    debug,
    agent_env,
    pretrained_path,
    pretrained_config_path,
):
    env = gym.make(
        env,
        savedir=savedir,
        max_episode_steps=max_steps,
        observation_keys=[
            "glyphs",
            "chars",
            "colors",
            "specials",
            "blstats",
            "message",
        ],
    )
    if seeds is not None:
        env.seed(seeds)
    if not no_render:
        print("Available actions:", env._actions)

    obs = env.reset()
    done = False

    pretrained_model, hidden = load_model(
        agent_env, pretrained_path, pretrained_config_path
    )

    steps = 0
    episodes = 0
    reward = 0.0
    action = None

    mean_sps = 0
    mean_reward = 0.0

    total_start_time = timeit.default_timer()
    start_time = total_start_time
    while True:
        if not no_render:
            print("Previous reward:", reward)
            if action is not None:
                print("Previous action: %s" % repr(env._actions[action]))
            env.render(render_mode)

        action, hidden = get_action(pretrained_model, obs, hidden, done)
        if action is None:
            break

        obs, reward, done, info = env.step(action)
        steps += 1

        mean_reward += (reward - mean_reward) / steps

        if not done:
            continue

        time_delta = timeit.default_timer() - start_time

        print("Final reward:", reward)
        print("End status:", info["end_status"].name)
        print("Mean reward:", mean_reward)
        print("Total reward:", mean_reward * steps)

        sps = steps / time_delta
        print("Episode: %i. Steps: %i. SPS: %f" % (episodes, steps, sps))

        episodes += 1
        mean_sps += (sps - mean_sps) / episodes

        start_time = timeit.default_timer()

        steps = 0
        mean_reward = 0.0

        if episodes == ngames:
            break
        env.reset()
    env.close()
    print(
        "Finished after %i episodes and %f seconds. Mean sps: %f"
        % (episodes, timeit.default_timer() - total_start_time, mean_sps)
    )


def main():
    parser = argparse.ArgumentParser(
        description="Tool for evaluating pretrained models."
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enables debug mode, which will drop stack into "
        "an ipdb shell if an exception is raised.",
    )
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="NetHackScore-v0",
        help="Gym environment spec. Defaults to 'NetHackStaircase-v0'.",
    )
    parser.add_argument(
        "--agent_env",
        type=str,
        default="",
        help="Agent name for environment.  Must correspond to "
        + "environment agent was trained in.",
    )
    parser.add_argument(
        "--pretrained_path",
        type=str,
        default="",
        help="Path to checkpoint to load pretrained model.",
    )
    parser.add_argument(
        "--pretrained_config_path",
        type=str,
        default="",
        help="Path to config for pretrained model.",
    )
    parser.add_argument(
        "-n",
        "--ngames",
        type=int,
        default=1,
        help="Number of games to be played before exiting. "
        "NetHack will auto-restart if > 1.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="Number of maximum steps per episode.",
    )
    parser.add_argument(
        "--seeds",
        default=None,
        help="Seeds to send to NetHack. Can be a dict or int. "
        "Defaults to None (no seeding).",
    )
    parser.add_argument(
        "--savedir",
        default="nle_data/play_data",
        help="Directory path where data will be saved. "
        "Defaults to 'nle_data/play_data'.",
    )
    parser.add_argument(
        "--no-render", action="store_true", help="Disables env.render()."
    )
    parser.add_argument(
        "--render_mode",
        type=str,
        default="human",
        choices=["human", "full", "ansi"],
        help="Render mode. Defaults to 'human'.",
    )
    flags = parser.parse_args()

    if flags.debug:
        import ipdb

        cm = ipdb.launch_ipdb_on_exception
    else:
        cm = dummy_context

    with cm():
        if flags.seeds is not None:
            # to handle both int and dicts
            flags.seeds = ast.literal_eval(flags.seeds)

        if flags.savedir == "args":
            flags.savedir = "{}_{}_{}.zip".format(
                time.strftime("%Y%m%d-%H%M%S"), flags.mode, flags.env
            )

        play(**vars(flags))


if __name__ == "__main__":
    main()
