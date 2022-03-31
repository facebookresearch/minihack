import React, {Component} from 'react';
import {Col, Container, Row, Tab, Tabs} from 'react-bootstrap';

import DESEditor from './DESEditor';
import EnvDesigner from './EnvDesigner';
import TileSelection from './TileSelection';
import NethackTileset from './tilesets/nethack/NethackTileset_loophack';
import PlusMinusButton from './PlusMinusButton';

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
      selectedTile: '',
      selectedBackgroundTile: '',
      tabKey: 'tile-select',
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
  }

  onChangeHeight = (height) => {
    this.setState((state) => {
      return {
        ...state,
        gridHeight: height,
      };
    });
  }

  render() {
    return (
      <Container fluid className='ep-container'>
        <Row>
          <Col md={2}/>
          <Col md={8} className='ep-header'>
              <h1>MiniHack Level Editor</h1>
          </Col>
          <Col md={2}/>
        </Row>
        <Row>
          <Col md={2}>
            <Row className='ep-ide-header'>
              <Col md={12} className="ep-size">
                <PlusMinusButton value={this.state.gridWidth} text="Width" onChange={this.onChangeWidth} /> 
                <PlusMinusButton value={this.state.gridHeight} text="Height" onChange={this.onChangeHeight} />
              </Col>
            </Row>
            <Row className='ep-tiles'>
              <Col md={12}>
                <TileSelection 
                  tileset={this.nethackTileset} 
                  onTileSelect ={this.onTileSelect} 
                  onBackgroundTileSelect={this.onBackgroundTileSelect} 
                  selectedTile={this.state.selectedTile} 
                  selectedBackgroundTile = { this.state.selectedBackgroundTile} 
                />
              </Col>
            </Row>
          </Col>
          <Col md={7} className='ep-ide'>
            <Row className="ep-ide-map-builder">
              <Col md={10} className="ep-ide-editor">
                <EnvDesigner
                  tileset={this.nethackTileset}
                  selectedTile={this.state.selectedTile}
                  onCompile={this.onCompile}
                  gridWidth={this.state.gridWidth}
                  gridHeight={this.state.gridHeight}
                />
              </Col>
            </Row>
          </Col>
          <Col md={3} className=''>
              <DESEditor desString={this.state.desString} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default App;
// import React, { useState } from 'react';

// import Jumbotron from 'react-bootstrap/Jumbotron';
// import Toast from 'react-bootstrap/Toast';
// import Container from 'react-bootstrap/Container';
// import Button from 'react-bootstrap/Button';

// import './App.css';

// const ExampleToast = ({ children }) => {
//   const [show, toggleShow] = useState(true);

//   return (
//     <>
//       {!show && <Button onClick={() => toggleShow(true)}>Show Toast</Button>}
//       <Toast show={show} onClose={() => toggleShow(false)}>
//         <Toast.Header>
//           <strong className="mr-auto">React-Bootstrap</strong>
//         </Toast.Header>
//         <Toast.Body>{children}</Toast.Body>
//       </Toast>
//     </>
//   );
// };

// const App = () => (
//   <Container className="p-3">
//     <Jumbotron>
//       <h1 className="header">Welcome To React-Bootstrap</h1>
//       <ExampleToast>
//         We now have Toasts
//         <span role="img" aria-label="tada">
//           🎉
//         </span>
//       </ExampleToast>
//     </Jumbotron>
//   </Container>
// );

// export default App;
