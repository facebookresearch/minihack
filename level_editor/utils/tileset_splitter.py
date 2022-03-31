from PIL import Image
from pathlib import Path

if __name__ == "__main__":

  tileset_dir = Path("split_tileset")
  if not tileset_dir.exists():
    tileset_dir.mkdir()

  im = Image.open("../misc/Nethack-Tiles16x16.png")

  print(im.size)

  tile_size = 16

  for x in range(0, im.size[0], tile_size):
    for y in range(0, im.size[1],tile_size):

      print(f"{x}, {y}")

      tile = im.crop(box=(x, y, x+tile_size, y+tile_size))
      tile.save(f"split_tileset/split({x},{y}).png")