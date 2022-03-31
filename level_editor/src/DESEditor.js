import SyntaxHighlighter from "react-syntax-highlighter";
import { darcula } from "react-syntax-highlighter/dist/esm/styles/hljs";
import React, { Component } from "react";
import PropTypes from "prop-types";

class DESEditor extends Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <SyntaxHighlighter style={darcula}>
        {this.props.desString}
      </SyntaxHighlighter>
    );
  }
}

DESEditor.propTypes = {
  desString: PropTypes.any,
};

export default DESEditor;
