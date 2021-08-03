# How to build documentation

1. Make sure that you installed MiniHack in the [dev mode](../README.md#extending-minihack)
2. `sphinx-apidoc -o api/  --module-first ../minihack/ ../minihack/agent/ ../minihack/envs/ ../minihack/tiles
/ ../minihack/scripts/`
3. `make html`