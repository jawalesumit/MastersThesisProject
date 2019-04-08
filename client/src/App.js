import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './App.css';

//for axios
import API from './api';

//for bootstrap
import { Container, Form, Row, Col, Button, Table, Alert, Spinner } from 'react-bootstrap';

//for charts
import { Doughnut } from 'react-chartjs-2';

//Sentiment labels
const SENTIMENT_POSITIVE = "POSITIVE";
const SENTIMENT_NEGATIVE = "NEGATIVE";

//Sentiment Colors
const SENTIMENT_POSITIVE_COLOR = "#7ad17a"; // green
const SENTIMENT_POSITIVE_COLOR_LIGHT = "#a0dea0"; // light green
const SENTIMENT_NEGATIVE_COLOR = "#F7464A"; // red
const SENTIMENT_NEGATIVE_COLOR_LIGHT = "#FF5A5E"; // light red

class App extends Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      showInvalidInputAlert: false,
      showFetchAlert: false,
      showSuccessInputAlert: false,
      isLoading: false,
      analyzeDisabled: false,

      vQueries: "",

      mnb_sentiment_positive: 0,
      mnb_sentiment_negative: 0,
      svm_sentiment_positive: 0,
      svm_sentiment_negative: 0,
      lr_sentiment_positive: 0,
      lr_sentiment_negative: 0,

      sentimentChart_MNB: {
        labels: [SENTIMENT_POSITIVE, SENTIMENT_NEGATIVE],
        datasets: [
          {
            data: [],
            backgroundColor: [SENTIMENT_POSITIVE_COLOR, SENTIMENT_NEGATIVE_COLOR],
            hoverBackgroundColor: [SENTIMENT_POSITIVE_COLOR_LIGHT, SENTIMENT_NEGATIVE_COLOR_LIGHT]
          }
        ]
      },
      sentimentChart_SVM: {
        labels: [SENTIMENT_POSITIVE, SENTIMENT_NEGATIVE],
        datasets: [
          {
            data: [],
            backgroundColor: [SENTIMENT_POSITIVE_COLOR, SENTIMENT_NEGATIVE_COLOR],
            hoverBackgroundColor: [SENTIMENT_POSITIVE_COLOR_LIGHT, SENTIMENT_NEGATIVE_COLOR_LIGHT]
          }
        ]
      },
      sentimentChart_LR: {
        labels: [SENTIMENT_POSITIVE, SENTIMENT_NEGATIVE],
        datasets: [
          {
            data: [],
            backgroundColor: [SENTIMENT_POSITIVE_COLOR, SENTIMENT_NEGATIVE_COLOR],
            hoverBackgroundColor: [SENTIMENT_POSITIVE_COLOR_LIGHT, SENTIMENT_NEGATIVE_COLOR_LIGHT]
          }
        ]
      }
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
                  <Form.Control type="text" placeholder="Type a query(s) or keyword(s). Please use semicolon(;) as seperator. Eg: batman, nolan movie" value={this.state.vQueries} onChange={(e) => this.changeQuery(e)} style={{ width: '45em' }} />
                </Col>
                <Col sm={2} xs={"auto"}>
                  <Button style={{ margin: '0.2em' }} variant="primary" disabled={this.state.analyzeDisabled} onClick={!this.state.isLoading ? (e) => this.analyseQueries(e) : null}>
                    {!this.state.isLoading ? 'Analyse' : <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true"/>}
                  </Button>
                </Col>
              </Form.Group>
            </Form>
          </Row>
          <Row className="show-grid justify-content-center">
            <div id="alert_msgs" style={{ margin: '1em' }}>
              <Alert id="invalid_alert" dismissible show={this.state.showInvalidInputAlert} variant="danger" onClose={(e) => this.setState({ showInvalidInputAlert: false })}>
                <Alert.Heading>Oh snap! You got an error!</Alert.Heading>
                <p>
                  The input cannot be blank!
                </p>
              </Alert>
              <Alert id="fetch_alert" show={this.state.showFetchAlert} variant="secondary" onClose={(e) => this.setState({ showFetchAlert: false })}>
                <p>
                  Finding related tweets...
                </p>
              </Alert>
              <Alert id="success_alert" show={this.state.showSuccessInputAlert} variant="primary" onClose={(e) => this.setState({ showSuccessInputAlert: false })}>
                <Alert.Heading>Found {this.state.mnb_sentiment_positive + this.state.mnb_sentiment_negative} related tweets!</Alert.Heading>
              </Alert>
            </div>
          </Row>
          <Row className="show-grid justify-content-md-center">
            <Table responsive striped bordered>
              <thead>
                <tr>
                  <th style={{ width: '50%' }}>Naive Bayes</th>
                  <th style={{ width: '50%' }}>SVM</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ width: '50%' }}>
                    Accuracy: 78.24%
                  </td>
                  <td style={{ width: '50%' }}>
                    Accuracy: 78.02%
                  </td>
                </tr>
                <tr>
                  <td style={{ width: '50%' }}>
                    <div id ="SentimentChart_MNB"></div>
                  </td>
                  <td style={{ width: '50%' }}>
                    <div id ="SentimentChart_SVM"></div>
                  </td>
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
                  <td>
                    Accuracy: 78.61%
                  </td>
                </tr>
                <tr>
                  <td>
                    <div id ="SentimentChart_LR"></div>
                  </td>
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
    this.setState({ analyzeDisabled: false });
  }

  analyseQueries(event) {
    //event.preventDefault();

    console.log('analyseQueries');

    this.setState({ showSuccessInputAlert: false });
    this.setState({ showInvalidInputAlert: false });
    this.setState({ analyzeDisabled: true });

    var vInputText = this.state.vQueries;
    //console.log(vInputText);
    //console.log(vInputText.length);
    //console.log(vInputText.trim().length);
    if(vInputText.length === 0 || vInputText.trim().length === 0) {
      this.setState({ showInvalidInputAlert: true });
      this.setState({ vQueries: '' });
      this.setState({ analyzeDisabled: false });
    }else{
      this.setState({ isLoading: true });
      this.setState({ showFetchAlert: true });
      this.getSentiment();
    }

  }

  //API functions
  getSentiment() {

    API.get('getSentiment', {
      params: {
        Queries : this.state.vQueries,
        Filename : new Date().getTime()
      }
    })
      .then(res => {
        console.log('getting responses...');
        console.log(res);
        console.log(res.data);

        var result = res.data;
        this.setState({ mnb_sentiment_positive: result.mnb_positive });
        this.setState({ mnb_sentiment_negative: result.mnb_negative });

        this.setState({ svm_sentiment_positive: result.svm_positive });
        this.setState({ svm_sentiment_negative: result.svm_negative });

        this.setState({ lr_sentiment_positive: result.lr_positive });
        this.setState({ lr_sentiment_negative: result.lr_negative });

        var toDisplay_mnb = "";
        var toDisplay_svm = "";
        var toDisplay_lr = "";
        if (result.length === 0) {
          toDisplay_mnb = <p>No Data</p>;
          toDisplay_svm = <p>No Data</p>;
          toDisplay_lr = <p>No Data</p>;
        }
        else {
          var vTmpObj = this.state.sentimentChart_MNB;
          vTmpObj.datasets[0].data = [result.mnb_positive, result.mnb_negative];
          this.setState({ sentimentChart_MNB: vTmpObj });
          toDisplay_mnb = <Doughnut width={250} data={this.state.sentimentChart_MNB} legend={{ display: true }} redraw />;

          vTmpObj = this.state.sentimentChart_SVM;
          vTmpObj.datasets[0].data = [result.svm_positive, result.svm_negative];
          this.setState({ sentimentChart_SVM: vTmpObj });
          toDisplay_svm = <Doughnut width={250} data={this.state.sentimentChart_SVM} legend={{ display: true }} redraw />;

          vTmpObj = this.state.sentimentChart_LR;
          vTmpObj.datasets[0].data = [result.lr_positive, result.lr_negative];
          this.setState({ sentimentChart_LR: vTmpObj });
          toDisplay_lr = <Doughnut width={250} data={this.state.sentimentChart_LR} legend={{ display: true }} redraw />;
        }

        ReactDOM.render(toDisplay_mnb, document.getElementById('SentimentChart_MNB'));

        ReactDOM.render(toDisplay_svm, document.getElementById('SentimentChart_SVM'));

        ReactDOM.render(toDisplay_lr, document.getElementById('SentimentChart_LR'));

        this.setState({ isLoading: false });
        this.setState({ showFetchAlert: false });
        this.setState({ showSuccessInputAlert: true });
      })
      .catch(function (error) {
        console.log('Error getting responses...!!!');
        console.log(error);
      });
  }
}

export default App;
