import TileSet from "../../TileSet";
import tiles from "./loophack/tiles.json";

class NethackTileset extends TileSet {
  constructor() {
    super();
    this.preprocessTiles(tiles);
  }
}

export default NethackTileset;
