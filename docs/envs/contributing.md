# Submitting New Environments

Create a Pull Request on MiniHack's [GitHub repository](https://github.com/facebookresearch/minihack) which includes the following changes:
- The .py file implementing the environment (with appropriate [registration](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/__init__.py#L7)) should be put into `minihack/envs` repository.
- If the environment includes a .des file, please put it into the `minihack/dat` directory.
- The description of the environment should be reside into the `minihack/doc/envs` directory
  - Create a separete .md in the corresponding directory (`navigation`, `skills` or `ported`) describing the environment (and its possible variations), its objective, capabilities it assesses, reward and action space used, as well as link to the source code.
  - Include a screenshot of the environment in `minihack/doc/envs/imgs` directory.
  - Update the tables (both Markdown table and {toctree} block) in `minihack/doc/envs/index.md` to reference your new environment (or family of environments).

We look forward to accepting diverse environment contributions from the community.