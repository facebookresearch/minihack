import SyntaxHighlighter from "react-syntax-highlighter";
import { darcula } from "react-syntax-highlighter/dist/esm/styles/hljs";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy } from "@fortawesome/free-solid-svg-icons";

class DESEditor extends Component {
  constructor(props) {
    super();
  }

  copyToClipboard = () => {
    navigator.clipboard.writeText(this.props.desString);
  }

  render() {
    return (
      <>
        <SyntaxHighlighter language="text" style={darcula}>
          {this.props.desString}
        </SyntaxHighlighter>
        <Button variant="dark" onClick={this.copyToClipboard}>Copy DES <FontAwesomeIcon size="xs" icon={faCopy}/></Button>
      </>
    );
  }
}

DESEditor.propTypes = {
  desString: PropTypes.any,
};

export default DESEditor;
