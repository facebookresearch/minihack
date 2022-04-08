import PropTypes from "prop-types";
import React, { Component } from "react";
import { Col, Row } from "react-bootstrap";
import TileInfoList from "./TileInfoList";

class TileSelection extends Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <>
        <Row className="ep-tiles-selection">
          <Col>
            <TileInfoList
              tileset={this.props.tileset}
              onTileSelect={this.props.onTileSelect}
              selectedTile={this.props.selectedTile}
            />
          </Col>
        </Row>
      </>
    );
  }
}

TileSelection.propTypes = {
  tileset: PropTypes.any,
  onTileSelect: PropTypes.func,
  onBackgroundTileSelect: PropTypes.func,
  selectedTile: PropTypes.any,
  selectedBackgroundTile: PropTypes.any,
};

export default TileSelection;
