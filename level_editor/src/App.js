import React, { Component } from "react";
import { Col, Container, Row, Tab, Tabs } from "react-bootstrap";
import Alert from "react-bootstrap/Alert";

import DESEditor from "./DESEditor";
import EnvDesigner from "./EnvDesigner";
import TileSelection from "./TileSelection";
import NethackTileset from "./tilesets/nethack/NethackTileset_loophack";
import PlusMinusButton from "./PlusMinusButton";

class App extends Component {
  constructor() {
    super();

    const defaultGridWidth = 15;
    const defaultGridHeight = 10;

    const desString = `
    DES will appear here when you add tiles...
    `;

    this.state = {
      desString,
      selectedTile: "",
      selectedBackgroundTile: "",
      tabKey: "tile-select",
      gridWidth: defaultGridWidth,
      gridHeight: defaultGridHeight,
    };

    this.nethackTileset = new NethackTileset();
  }

  onTileSelect = (tileInfo) => {
    this.setState((state) => {
      return {
        ...state,
        selectedTile: tileInfo,
      };
    });
  };

  setKey = (key) => {
    this.setState((state) => {
      return {
        ...state,
        tabKey: key,
      };
    });
  };

  onCompile = (desString) => {
    this.setState((state) => {
      return {
        ...state,
        desString,
      };
    });
  };

  onChangeWidth = (width) => {
    this.setState((state) => {
      return {
        ...state,
        gridWidth: width,
      };
    });
  };

  onChangeHeight = (height) => {
    this.setState((state) => {
      return {
        ...state,
        gridHeight: height,
      };
    });
  };

  render() {
    return (
      <Container fluid className="ep-container">
        <Row>
          <Col md={2} className="ep-logo"><img src="header.png" /></Col>
          <Col md={8} className="ep-header">
            <h1>Level Editor</h1>
          </Col>
          <Col md={2} />
        </Row>
        <Row>
          <Col md={2}>
            <Row className="ep-ide-header">
              <Col md={12} className="ep-size">
                <PlusMinusButton
                  value={this.state.gridWidth}
                  text="Width"
                  onChange={this.onChangeWidth}
                  max={79}
                  min={5}
                />
                <PlusMinusButton
                  value={this.state.gridHeight}
                  text="Height"
                  onChange={this.onChangeHeight}
                  max={21}
                  min={5}
                />
              </Col>
            </Row>
            <Row className="ep-tiles">
              <Col md={12}>
                <TileSelection
                  tileset={this.nethackTileset}
                  onTileSelect={this.onTileSelect}
                  onBackgroundTileSelect={this.onBackgroundTileSelect}
                  selectedTile={this.state.selectedTile}
                  selectedBackgroundTile={this.state.selectedBackgroundTile}
                />
              </Col>
            </Row>
          </Col>
          <Col md={6} className="ep-ide">
            <Row className="ep-ide-map-builder">
              <Col md={11} className="ep-ide-editor">
                <EnvDesigner
                  tileset={this.nethackTileset}
                  selectedTile={this.state.selectedTile}
                  onCompile={this.onCompile}
                  gridWidth={this.state.gridWidth}
                  gridHeight={this.state.gridHeight}
                />
              </Col>
            </Row>
            <Row>
              <Col md={10} className="ep-ide-instructions">
                <Alert variant="info">
                  <Alert.Heading>Instructions</Alert.Heading>
                  <p>
                    Select tiles from the left menu and place them on in the
                    grid to make levels. Des file text will be compiled for the
                    level and placed on the right.
                  </p>
                  <p>
                    You can then copy the DES file to use it as a MiniHack
                    level.
                  </p>
                  <p>Resize the level using the +/- buttons on the top left.</p>
                  <hr />
                  <p className="mb-0">
                    You can also remove tiles using the mouse-click.
                  </p>
                </Alert>
              </Col>
            </Row>
          </Col>
          <Col md={4} className="">
            <DESEditor desString={this.state.desString} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;
