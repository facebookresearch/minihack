import PropTypes from "prop-types";
import React, { Component } from "react";
import { Col, ListGroupItem, ListGroup, Row } from "react-bootstrap";

// Scrollable list of tiles with names next to them... maybe a text search for drilling down?
class TileInfoList extends Component {
  constructor(props) {
    super();
  }

  render() {
    // Create and display list of tiles
    const tileInfos = [];
    const allTiles = this.props.tileset.getTiles();
    for (const categoryName in allTiles) {
      const category = allTiles[categoryName];

      const categoryHeader = (
        <ListGroupItem className="ep-tiles-selection-title" key={categoryName}>{categoryName}</ListGroupItem>
      );
      tileInfos.push(categoryHeader);

      const clickableTiles = [];
      for (let t = 0; t < category.length; t++) {
        const tileData = category[t];
        if (tileData.visibleInEditor) {
          const className =
            "ep-tiles-selection-item-tile" +
            (this.props.selectedTile.tileId === tileData.tileId
              ? " selected"
              : " selectable");
          const clickableTile = (
            <Col
              onClick={() => this.props.onTileSelect(tileData)}
              className={className}
              key={tileData.tileId}
            >
              <img src={"tilesets/nethack/" + tileData.image} />
            </Col>
          );

          // const tileInfo = <ListGroupItem key={tileId} onClick={() => this.props.onTileSelect(tileId)} className={className}><TileInfo tileData={tileData} /></ListGroupItem>
          clickableTiles.push(clickableTile);
        }
      }
      
      const tilesFlexbox = (
        <ListGroupItem key={categoryName + "_tiles"}>
          <Row className="ep-tiles-selection-item">{clickableTiles}</Row>
        </ListGroupItem>
      );
      tileInfos.push(tilesFlexbox);
    }

    return (
      <>
        <Row>
          <Col>
            <ListGroup className="ep-tiles-selection-scroll">
              {tileInfos}
            </ListGroup>
          </Col>
        </Row>
      </>
    );
  }
}

TileInfoList.propTypes = {
  tileset: PropTypes.any,
  onTileSelect: PropTypes.func,
  selectedTile: PropTypes.any,
};

TileInfoList.defaultProps = {
  tileset: {},
  onTileSelect: () => {},
  selectedTile: -1,
};

export default TileInfoList;
