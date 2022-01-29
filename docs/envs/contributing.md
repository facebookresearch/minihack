# Submitting New Environments

For submitting a new environment to MiniHack Environment Zoo, open a Pull Request on [GitHub](https://github.com/facebookresearch/minihack) that includes the following:
- The .py file implementing the environment should be put into `minihack/envs` directory (with appropriate [registration](https://github.com/facebookresearch/minihack/blob/main/minihack/envs/__init__.py#L7)).
- If the environment includes a .des file, please put it into the `minihack/dat` directory.
- The description of the environment should reside in the `docs/envs` directory
  - Create a separate markdown file in the corresponding directory (`navigation`, `skills` or `ported`) describing the environment (and its possible variations), its objective, capabilities it assesses, reward, action space used, as well as the link to the source code.
  - Include a screenshot of the environment in `docs/envs/imgs` directory.
  - Update the tables (both Markdown table and {toctree} block) in `docs/envs/index.md` to reference your new environment (or family of environments).

We look forward to accepting diverse environment contributions from the community.
