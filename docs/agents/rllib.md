# RLLib

Griddly provides support for reinforcement learning using the `RLLib <https://docs.ray.io/en/latest/rllib.html>`_ reinforcement learning library.

While RLLib doesn't support OpenAI Gym registered environments, it does provide a similar interface which is supported by Griddly's ``RLLibEnv`` environment.

Griddly provides two classes, ``RLLibEnv`` and ``RLLibMultiAgentWrapper`` which abstract away all the tedious parts of wrapping environments for RL and leaves you to concentrate on training algorithms, designing networks and game mechanics.

Examples for :ref:`single-agent <doc_rllib_single_agent>` and :ref:`multi-agent <doc_rllib_multi_agent>` training are provided.


## Examples Setup

Griddly installs most of the dependencies for you automatically when it is installed, however you will need to install RLLlib and Pytorch to run the provided examples.

You can install RLLib and pytorch using the following command:

```bash
    pip install ray[rllib]==1.2.0 torch==1.8.0
```

All RLLib examples can be found in ``python/examples/rllib/``

## Environment Parameters

Parameters for the environments, such as the :ref:`GDY <doc_getting_started_gdy>` file for the game and :ref:`Observer options <doc_observation_spaces>` can be sent to the environment using the ``env_config`` dictionary.

Most of the parameters here are the same as the parameters that can be given to the ``gym.make()`` command when creating a :ref:`Griddly environment for OpenAI Gym <doc_getting_started_gym_advanced>`.


The above example will also record a video of the environment (rendered using the ``SPRITE_2D`` renderer) for one episode every 100000 steps.
Finally the max_steps of the environment will be override to be 1000 steps before the environment is reset automatically.