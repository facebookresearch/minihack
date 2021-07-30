# Other Tools

## Hydra

If a multi-agent environment has the conditions in which agents in the environment can be removed, for example they are defeated and are not longer in the episode, a RLLib needs to know that this agent no longer can receive actions.

Griddly's ``RLlibMultiAgentWrapper`` handles this by detecting a ``player_done_variable``, defined per-player in the GDY. When this variable is set to ``1`` for a player, RLLib will consider this player has been removed.

## Weights and  Biases

The Foragers environment as seen from the "Global Observer" view.

The following code will run the Foragers example for 10M steps using IMPALA to train.
