import monsters from "./monsters.json";
import items from "./items.json";

class NethackTileset {
  constructor() {
    this.all_tiles = {
      monsters: monsters,
      items: items,
    };
  }

  createTileIdKey(categoryName, s, t) {
    return categoryName + "-" + s + "-" + t;
  }

  getTiles = () => {
    return this.all_tiles;
  };

  getTileById = (tileId) => {
    return this.all_tiles[tileId.category][tileId.subcategoryIdx][
      tileId.tileIdx
    ];
  };

  getBackgroundTiles = () => {
    return {
      0: {
        mapCharacter: ".",
        name: "Floor",
        imageSrc: "tilesets/nethack/images/Floor.png",
      },
      1: {
        mapCharacter: ".",
        name: "Floor",
        imageSrc: "tilesets/nethack/images/Floor_dark.png",
      },
    };
  };
}

export default NethackTileset;
