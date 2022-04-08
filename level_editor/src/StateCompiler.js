import { locationKey } from "./EditorStateHandler";

/**
 * Converts editor state into DES file format for use with NetHack
 */
class StateCompiler {
  getMapBoundary = (state) => {
    let minx = Number.MAX_VALUE;
    let maxx = 0;
    let miny = Number.MAX_VALUE;
    let maxy = 0;

    for (const key in state.tiles) {
      const tile = state.tiles[key];
      if (tile.x > maxx) maxx = tile.x;
      if (tile.x < minx) minx = tile.x;
      if (tile.y > maxy) maxy = tile.y;
      if (tile.y < miny) miny = tile.y;
    }

    return {
      minx,
      miny,
      maxx,
      maxy,
    };
  };

  generateMap = (state, mapBounds) => {
    console.log("State", state);

    const mapGridRows = [];

    for (let y = 0; y <= mapBounds.maxy - mapBounds.miny; y++) {
      const mapRow = [];
      for (let x = 0; x <= mapBounds.maxx - mapBounds.minx; x++) {
        const tileKey = locationKey(x + mapBounds.minx, y + mapBounds.miny);
        if (tileKey in state.tiles) {
          const tileData = state.tiles[tileKey];

          // If we have a player character, then put a floor. The "player" is dealth with by adding a BRANCH
          if (
            tileData.category !== "Player" &&
            tileData.category !== "Staircase" &&
            tileData.category !== "Monster"
          ) {
            mapRow.push(tileData.glyphChar);
          } else {
            mapRow.push(".");
          }
        } else {
          mapRow.push(" ");
        }
      }
      mapGridRows.push(mapRow.join(""));
    }

    const mapGridAscii = mapGridRows.reverse().join("\n");

    const mapString = `
MAP
${mapGridAscii}
ENDMAP

`;
    return mapString;
  };

  generateHeader = (state) => {
    const header = `
MAZE: "${state.levelName}", ' '
FLAGS:premapped
GEOMETRY:center,center
`;

    return header;
  };

  generateFooter = (state, mapBounds) => {
    for (const key in state.tiles) {
      const tileData = state.tiles[key];
    }

    const startLocation = { x: -1, y: -1 };
    const stairLocation = { x: -1, y: -1 };
    const monsterLocations = [];
    for (const key in state.tiles) {
      const tileData = state.tiles[key];
      if (tileData.category === "Staircase") {
        stairLocation.x = tileData.x - mapBounds.minx;
        stairLocation.y = mapBounds.maxy - tileData.y;
      } else if (tileData.category === "Player") {
        startLocation.x = tileData.x - mapBounds.minx;
        startLocation.y = mapBounds.maxy - tileData.y;
      } else if (tileData.category === "Monster") {
        monsterLocations.push({
          x: tileData.x - mapBounds.minx,
          y: mapBounds.maxy - tileData.y,
        });
      }
    }

    let footer = "";

    if (stairLocation.x >= 0) {
      footer += `STAIR:(${stairLocation.x}, ${stairLocation.y}),down\n`;
    }

    if (startLocation.x >= 0) {
      footer += `BRANCH: (${startLocation.x},${startLocation.y},${
        startLocation.x
      },${startLocation.y}),(${startLocation.x + 1},${startLocation.y + 1},${
        startLocation.x + 1
      },${startLocation.y + 1})\n`;
    }

    if (monsterLocations.length > 0) {
      monsterLocations.map(location => {
        footer += `MONSTER: random, random, (${location.x},${location.y})\n`;
      });
        
    }
    return footer;
  };

  compile = (state) => {
    const mapBounds = this.getMapBoundary(state);
    const header = this.generateHeader(state);
    const map = this.generateMap(state, mapBounds);
    const footer = this.generateFooter(state, mapBounds);
    return header + map + footer;
  };
}

export default StateCompiler;
