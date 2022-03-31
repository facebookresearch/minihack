function locationKey(x, y) {
  return "[" + x + "," + y + "]";
}

class EditorStateHandler {
  constructor(tileset) {
    console.log("EditorState initialized");

    this.editorHistory = [];

    this.tileset = tileset;

    this.initialState = {
      tiles: {},
      levelName: "mylevel",
    };

    this.pushState(this.initialState);
  }

  getState = () => {
    return { ...this.editorHistory[0] };
  };

  pushState = (state) => {
    // Copy the state and add it to the history
    const stateCopy = { ...state };
    this.editorHistory.push(stateCopy);

    const historyLength = this.editorHistory.length;

    if (historyLength >= 20) {
      this.editorHistory.pop();
    }
  };

  addTile = (x, y, tileData) => {
    const state = this.getState();

    state.tiles[locationKey(x, y)] = { ...tileData, x, y };

    this.pushState(state);
  };

  removeTile = (x, y) => {
    const state = this.getState();

    delete state.tiles[locationKey(x, y)];

    this.pushState(state);
  };
}

export default EditorStateHandler;
export { locationKey };
