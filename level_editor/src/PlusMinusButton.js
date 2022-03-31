import {faMinus, faPlus} from '@fortawesome/free-solid-svg-icons'
import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {Row, Col, Button, InputGroup} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { propTypes } from 'react-bootstrap/esm/Image';


class PlusMinusButton extends Component {
  constructor(props) {
    super(props);

  }

  incr = () => {
    this.props.onChange(Math.min(15,this.props.value+1));
  }

  decr = () => {
    this.props.onChange(Math.max(5,this.props.value-1));
  }

  render() {
    return (
      <Row>
        <Col md={12}>
          <div className="ep-size-plus-minus"><span>{this.props.text}</span>
          <InputGroup>
          <Button onClick={this.incr}>
            <FontAwesomeIcon icon={faPlus} size="xs" />
          </Button>
          <InputGroup.Text>{this.props.value}</InputGroup.Text>
          <Button onClick={this.decr}>
            <FontAwesomeIcon icon={faMinus} size="xs" />
          </Button>
          </InputGroup>
          </div>
        </Col>
      </Row>
    );
  }

};

PlusMinusButton.propTypes = {
  value: PropTypes.any,
  text: PropTypes.any,
  onChange: PropTypes.any
};

export default PlusMinusButton;