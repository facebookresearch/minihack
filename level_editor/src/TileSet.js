function TileData(
  category,
  name,
  id,
  wikiLink,
  image,
  glyphChar,
  visibleInEditor = true,
  maxInstances = -1,
) {
  this.category = category;
  this.name = name;
  this.tileId = id;
  this.wikiLink = wikiLink;
  this.image = image;
  this.glyphChar = glyphChar;
  this.visibleInEditor = visibleInEditor;
  this.maxInstances = maxInstances;
}

function createTileIdKey(categoryName, t) {
  return categoryName + "-" + t;
}

class TileSet {
  constructor() {
    this.allTiles = {};
  }

  preprocessTiles = (tileConfig) => {
    for (let c = 0; c < tileConfig.length; c++) {
      const category = tileConfig[c];
      const categoryObjects = category.objects;
      this.allTiles[category.class] = [];
      for (let t = 0; t < categoryObjects.length; t++) {
        const tile = categoryObjects[t];

        const tileData = new TileData(
          category.class,
          tile.name,
          createTileIdKey(category.class, t),
          tile.wiki_link,
          tile.image,
          tile.glyph.character,
          tile.visible_in_editor,
          tile.max_instances
        );

        this.allTiles[category.class].push(tileData);
      }
    }
  };

  getTiles = () => {
    return this.allTiles;
  };
}

export default TileSet;
export { createTileIdKey };
