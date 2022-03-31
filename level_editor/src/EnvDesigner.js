import PropTypes from "prop-types";
import React, { Component } from "react";
import { Col, Row } from "react-bootstrap";
import * as THREE from "three";
import EditorStateHandler, { locationKey } from "./EditorStateHandler";
import StateCompiler from "./StateCompiler";
import { createTileIdKey } from "./TileSet";

class EnvDesigner extends Component {
  constructor(props) {
    super(props);
    const points = [];
    points.push(new THREE.Vector3(-0.5, -0.5, 1));
    points.push(new THREE.Vector3(-0.5, 0.5, 1));
    points.push(new THREE.Vector3(0.5, 0.5, 1));
    points.push(new THREE.Vector3(0.5, -0.5, 1));
    points.push(new THREE.Vector3(-0.5, -0.5, 1));

    this.geometries = {};
    this.components = {};
    this.tiles = new Map();

    
    this.geometries.square = new THREE.BufferGeometry().setFromPoints(points);

    this.state = {
      cursorGridPosition: new THREE.Vector2(),
      camera: new THREE.OrthographicCamera(
        0,
        this.props.gridWidth,
        this.props.gridHeight,
        0,
        -100,
        100
      ),
      gridHeight: this.props.gridHeight,
      gridWidth: this.props.gridWidth,
    };

    this.currentSelectedTile = {
      tileId: false,
    };

    this.editorStateHandler = new EditorStateHandler(props.tileset);
    this.stateCompiler = new StateCompiler();
    this.renderer = new THREE.WebGLRenderer();
  }

  createHighlightSquare = (color = 0xaaaaaa) => {
    const material = new THREE.LineBasicMaterial({ color });
    return new THREE.Line(this.geometries.square, material);
  };

  isTileCategory(category, key) {
    return key in this.tiles && this.tiles[key].category === category;
  }

  createTileSprite = (tileData, key) => {
    let tileId;
    console.log("creating tile sprite for", tileData);
    console.log("Category:", tileData.category);
    if (tileData.category === "Walls") {
      const upKey = locationKey(tileData.x, tileData.y + 1);
      const downKey = locationKey(tileData.x, tileData.y - 1);
      const leftKey = locationKey(tileData.x + 1, tileData.y);
      const rightKey = locationKey(tileData.x - 1, tileData.y);
      const upWall = this.isTileCategory("Walls", upKey);
      const rightWall = this.isTileCategory("Walls", rightKey);
      const downWall = this.isTileCategory("Walls", downKey);
      const leftWall = this.isTileCategory("Walls", leftKey);

      let tileOffset = 0;

      console.log("Up", upWall);
      console.log("Right", rightWall);
      console.log("Down", downWall);
      console.log("Left", leftWall);
      if ((rightWall || leftWall) && !upWall && !downWall) {
        tileOffset = 1;
      } else if (!rightWall && !leftWall && (upWall || downWall)) {
        tileOffset = 0;
      } else if (!downWall) {
        tileOffset = 4;
      } else {
        tileOffset = 3;
      }

      tileId = createTileIdKey("Walls", tileOffset);
    } else {
      tileId = tileData.tileId;
    }

    const material = this.tilesetMaterial[tileId].clone();
    return new THREE.Sprite(material);
  };

  recompileState = () => {
    const state = this.editorStateHandler.getState();
    const desString = this.stateCompiler.compile(state);
    this.props.onCompile(desString);
  };

  resizeCanvas = (gridWidth, gridHeight) => {

    const camera = new THREE.OrthographicCamera(
      0,
      gridWidth,
      gridHeight,
      0,
      -100,
      100
    );

    if(this.mount === null || this.mount.parentNode === null ) {
      return;
    }

    const canvasWidth = this.mount.parentNode.offsetWidth;
    const canvasHeight = (gridHeight*canvasWidth)/gridWidth;

    this.renderer.setSize(canvasWidth, canvasHeight);

    this.setState((state) => {
      return {
        ...state,
        camera,
      };
    });
  }

  onCanvasResize = (e) => {
    this.resizeCanvas(this.props.gridWidth, this.props.gridHeight);
  }

  componentDidUpdate(prevProps) {
    if(prevProps.gridWidth != this.props.gridWidth || prevProps.gridHeight != this.props.gridHeight) {
      this.resizeCanvas(this.props.gridWidth, this.props.gridHeight);
    }
  }

  componentDidMount() {

    const canvasWidth = this.mount.parentNode.offsetWidth;
    const canvasHeight = (this.props.gridHeight*canvasWidth)/this.props.gridWidth;

    this.renderer.setSize(canvasWidth, canvasHeight);

    this.mount.appendChild(this.renderer.domElement);

    this.mouseX = 0;
    this.mouseY = 0;

    const scene = new THREE.Scene();

    const textureLoader = new THREE.TextureLoader();

    // Preload Tilesets
    this.tilesetMaterial = {};
    const allTiles = this.props.tileset.getTiles();
    for (const categoryName in allTiles) {
      const category = allTiles[categoryName];
      for (let t = 0; t < category.length; t++) {
        const tileData = category[t];
        const texture = textureLoader.load(
          "tilesets/nethack/" + tileData.image
        );
        const material = new THREE.SpriteMaterial({ map: texture });
        this.tilesetMaterial[tileData.tileId] = material;
      }
    }

    this.components.highlightSquare = this.createHighlightSquare(0xaaffaa);
    scene.add(this.components.highlightSquare);
    this.highlightSprite = null;

    const removeTile = (key) => {
      scene.remove(this.tiles[key].sprite);
      delete this.tiles[key];
    };

    const paintTile = (key, tileData) => {
      const sprite = this.createTileSprite(tileData, tileData);
      scene.add(sprite);
      sprite.position.x = tileData.x + 0.5;
      sprite.position.y = tileData.y + 0.5;
      tileData.sprite = sprite;
      this.tiles[key] = tileData;
    };

    const repaintTile = (key) => {
      const tileData = this.tiles[key];
      scene.remove(tileData.sprite);
      paintTile(key, tileData);
    };

    const repaintSurroundingWalls = (x, y) => {
      const upKey = locationKey(x, y + 1);
      const downKey = locationKey(x, y - 1);
      const leftKey = locationKey(x + 1, y);
      const rightKey = locationKey(x - 1, y);
      if (this.isTileCategory("Walls", upKey)) {
        repaintTile(upKey);
      }
      if (this.isTileCategory("Walls", downKey)) {
        repaintTile(downKey);
      }
      if (this.isTileCategory("Walls", leftKey)) {
        repaintTile(leftKey);
      }
      if (this.isTileCategory("Walls", rightKey)) {
        repaintTile(rightKey);
      }
    };

    const animate = () => {
      requestAnimationFrame(animate);

      const editorRect = this.renderer.domElement.getBoundingClientRect();

      const editorX = editorRect.left;
      const editorY = editorRect.bottom;

      const editorWidth = editorRect.right - editorRect.left;
      const editorHeight = editorRect.bottom - editorRect.top;

      const cursorGridPosition = new THREE.Vector2(
        Math.floor((this.mouseX - editorX) / (editorWidth / this.props.gridWidth)),
        Math.floor((editorY - this.mouseY) / (editorHeight / this.props.gridHeight))
      );

      this.components.highlightSquare.position.x = cursorGridPosition.x + 0.5;
      this.components.highlightSquare.position.y = cursorGridPosition.y + 0.5;

      // Tile selection and overlay
      if (
        this.currentSelectedTile.tileId !== this.props.selectedTile.tileId &&
        this.props.selectedTile.tileId
      ) {
        this.currentSelectedTile = this.props.selectedTile;
        if (this.highlightSprite) {
          this.components.highlightSquare.remove(this.highlightSprite);
        }
        this.highlightSprite = this.createTileSprite(
          this.props.selectedTile,
          cursorGridPosition
        );
        this.highlightSprite.material.opacity = 0.5;
        this.highlightSprite.material.transparent = true;
        this.components.highlightSquare.add(this.highlightSprite);
      }

      // Actually render the created map
      const editorState = this.editorStateHandler.getState();

      // loop through the tiles and render them
      for (const [key, tileData] of Object.entries(editorState.tiles)) {
        let addSprite = false;
        if (!(key in this.tiles)) {
          addSprite = true;
        } else if (this.tiles[key].tileId !== tileData.tileId) {
          scene.remove(this.tiles[key].sprite);
          addSprite = true;
        }

        if (addSprite) {
          paintTile(key, tileData);
          repaintSurroundingWalls(tileData.x, tileData.y);
        }
      }

      // Loop through scene and remove tiles we don't need anymore
      for (const [key, tileData] of Object.entries(this.tiles)) {
        if (!(key in editorState.tiles)) {
          removeTile(key);
          repaintSurroundingWalls(tileData.x, tileData.y);
        }
      }

      this.setState((state) => {
        return {
          ...state,
          cursorGridPosition,
        };
      });

      this.renderer.render(scene, this.state.camera);
    };

    animate(this);

    this.mount.addEventListener("mousemove", (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
    });

    this.mount.addEventListener("contextmenu", (e) => {
      e.preventDefault();
    });

    this.mount.addEventListener("mouseup", (e) => {
      const gridX = this.state.cursorGridPosition.x;
      const gridY = this.state.cursorGridPosition.y;

      e.preventDefault();

      console.log(e.button);

      console.log("Adding current tile:", this.currentSelectedTile);

      if (this.currentSelectedTile.tileId) {
        if (e.button === 0) {
          this.editorStateHandler.addTile(
            gridX,
            gridY,
            this.currentSelectedTile
          );
          this.recompileState();
        }
      }

      if (e.button === 2) {
        this.editorStateHandler.removeTile(gridX, gridY);
        this.recompileState();
      }
    });

    window.addEventListener( 'resize', this.onCanvasResize, false );
  }

  render() {
    return (
      <>
        <div className="ep-ide-editor" ref={(ref) => (this.mount = ref)} />
      </>
    );
  }
}

EnvDesigner.propTypes = {
  tileset: PropTypes.any,
  selectedTile: PropTypes.any,
  onCompile: PropTypes.any,
  gridHeight: PropTypes.any,
  gridWidth: PropTypes.any
};

export default EnvDesigner;
