import React, { Component } from 'react';
import './App.css';

//for axios
import API from './api';

//for bootstrap
import { Container, Form, Row, Col, Button, Table } from 'react-bootstrap';

class App extends Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      vQueries: "",

      mnb_sentiment: "",
      svm_sentiment: "",
      lr_sentiment: ""
    }

  }

  render() {
    return (
      <div className="App">
        <Container>
          <Row className="show-grid justify-content-center">
            <Form inline>
              <Form.Group as={Row} controlId="form">
                <Col sm={10} xs={"auto"}>
                  <Form.Control type="text" placeholder="Type a query(s) or keyword(s). Please use comma(,) as seperator. Eg: batman, nolan movie" value={this.state.vQueries} onChange={(e) => this.changeQuery(e)} style={{ width: '45em' }} />
                </Col>
                <Col sm={2} xs={"auto"}>
                  <Button variant="primary" onClick={(e) => this.analyseQueries(e)}>Analyse</Button>
                </Col>
              </Form.Group>
            </Form>
          </Row>
          <Row>&nbsp;</Row> 
          <Row className="show-grid justify-content-md-center">
            <Table responsive striped bordered>
              <thead>
                <tr>
                  <th>Naive Bayes</th>
                  <th>SVM</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{this.state.mnb_sentiment}</td>
                  <td>{this.state.svm_sentiment}</td>
                </tr>
              </tbody>
            </Table>
          </Row>
          <Row className="show-grid justify-content-md-center">
            <Table responsive striped bordered>
              <thead>
                <tr>
                  <th>Ensemble Approach</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{this.state.lr_sentiment}</td>
                </tr>
              </tbody>
            </Table>
          </Row>
        </Container>
      </div>
    );
  }

  // functions

  changeQuery(e) {
    this.setState({ vQueries: e.target.value });
  }

  analyseQueries(event) {
    //event.preventDefault();

    console.log('analyseQueries');

    this.getSentiment();
  }

  //API functions
  getSentiment() {

    API.get('getSentiment', {
      params: {Queries : this.state.vQueries}
    })
      .then(res => {
        console.log('getting responses...');
        console.log(res);
        console.log(res.data);

        var result = res.data;
        this.setState({ mnb_sentiment: result.mnb_sentiment });
        this.setState({ svm_sentiment: result.svm_sentiment });
        this.setState({ lr_sentiment: result.lr_sentiment });
      })
      .catch(function (error) {
        console.log('Error getting responses...!!!');
        console.log(error);
      });
  }
}

export default App;
