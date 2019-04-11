import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './App.css';

//for axios
import API from './api';

//for bootstrap
import { Container, Form, Row, Col, Button, Table, Alert, Spinner, Modal } from 'react-bootstrap';

//for charts
import { Doughnut } from 'react-chartjs-2';

//Sentiment labels
const SENTIMENT_POSITIVE = "Positive";
const SENTIMENT_NEGATIVE = "Negative";

//Sentiment Colors
const SENTIMENT_POSITIVE_COLOR = "#7ad17a"; // green
const SENTIMENT_POSITIVE_COLOR_LIGHT = "#a0dea0"; // light green
const SENTIMENT_NEGATIVE_COLOR = "#F7464A"; // red
const SENTIMENT_NEGATIVE_COLOR_LIGHT = "#FF5A5E"; // light red

//Model names
const MNB = 'Multinomial Naive Bayes';
const SVM = 'Support Vector Machine';
const LR = 'Linear Regression'

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

      mnb_sentiment_positive_tweets_table: '',
      mnb_sentiment_negative_tweets_table: '',
      svm_sentiment_positive_tweets_table: '',
      svm_sentiment_negative_tweets_table: '',
      lr_sentiment_positive_tweets_table: '',
      lr_sentiment_negative_tweets_table: '',

      showTweets: false,
      modalHeading: '',
      modalTableBody: '',

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
                    {!this.state.isLoading ? 'Analyse' : <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />}
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
                    <div id="SentimentChart_MNB"></div>
                  </td>
                  <td style={{ width: '50%' }}>
                    <div id="SentimentChart_SVM"></div>
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
                    <div id="SentimentChart_LR"></div>
                  </td>
                </tr>
              </tbody>
            </Table>
          </Row>
          <Modal size="lg" show={this.state.showTweets} onHide={(e) => this.setState({ showTweets: false })}>
            <Modal.Header closeButton>
              <Modal.Title>{this.state.modalHeading}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Table responsive striped bordered>
                <thead>
                  <tr>
                    <th>Username</th>
                    <th>Tweet</th>
                  </tr>
                </thead>
                <tbody>
                  {this.state.modalTableBody}
                </tbody>
              </Table>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={(e) => this.setState({ showTweets: false })}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>
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
    if (vInputText.length === 0 || vInputText.trim().length === 0) {
      this.setState({ showInvalidInputAlert: true });
      this.setState({ vQueries: '' });
      this.setState({ analyzeDisabled: false });
    } else {
      this.setState({ isLoading: true });
      this.setState({ showFetchAlert: true });
      this.getSentiment();
    }

  }

  showTweets(event, modelName) {
    console.log('\nInisde showTweets')
    if(event.length !== 0){
      console.log(event);
      console.log(event[0]._model.label);
      console.log(modelName);

      var tempSentiment = event[0]._model.label;
      var modalHeading = modelName + ' ' + tempSentiment + ' Tweets'; 
      var modalBody = '';

      if(modelName === MNB)
        if(tempSentiment === SENTIMENT_POSITIVE)
          modalBody = this.state.mnb_sentiment_positive_tweets_table;
        else
          modalBody = this.state.mnb_sentiment_negative_tweets_table;
      else if(modelName === SVM)
        if(tempSentiment === SENTIMENT_POSITIVE)
          modalBody = this.state.svm_sentiment_positive_tweets_table;
        else
          modalBody = this.state.svm_sentiment_negative_tweets_table;
      else if(modelName === LR)
        if(tempSentiment === SENTIMENT_POSITIVE)
          modalBody = this.state.lr_sentiment_positive_tweets_table;
        else
          modalBody = this.state.lr_sentiment_negative_tweets_table;

      this.setState({modalHeading: modalHeading});
      this.setState({modalTableBody: modalBody});
      this.setState({showTweets: true});
    }
  }

  //API functions
  getSentiment() {

    API.get('getSentiment', {
      params: {
        Queries: this.state.vQueries,
        Filename: new Date().getTime()
      }
    })
      .then(res => {
        console.log('getting responses...');
        console.log(res);
        console.log(res.data);
        var result = res.data;

        var toDisplay_mnb = "";
        var toDisplay_svm = "";
        var toDisplay_lr = "";

        if (result.length === 0) {
          toDisplay_mnb = <p>No Data</p>;
          toDisplay_svm = <p>No Data</p>;
          toDisplay_lr = <p>No Data</p>;
        }
        else {
          var mnb_pos_count = result.mnb_pos_count;
          var mnb_neg_count = result.mnb_neg_count;
          var svm_pos_count = result.svm_pos_count;
          var svm_neg_count = result.svm_neg_count;
          var lr_pos_count = result.lr_pos_count;
          var lr_neg_count = result.lr_neg_count;

          var vTmpObj = this.state.sentimentChart_MNB;
          vTmpObj.datasets[0].data = [mnb_pos_count, mnb_neg_count];
          this.setState({ sentimentChart_MNB: vTmpObj });
          this.setState({ mnb_sentiment_positive: mnb_pos_count });
          this.setState({ mnb_sentiment_negative: mnb_neg_count });
          toDisplay_mnb = <Doughnut width={250} data={this.state.sentimentChart_MNB} legend={{ display: true }} redraw onElementsClick={(e) => this.showTweets(e, MNB)} />;

          vTmpObj = this.state.sentimentChart_SVM;
          vTmpObj.datasets[0].data = [svm_pos_count, svm_neg_count];
          this.setState({ sentimentChart_SVM: vTmpObj });
          this.setState({ svm_sentiment_positive: svm_pos_count });
          this.setState({ svm_sentiment_negative: svm_neg_count });
          toDisplay_svm = <Doughnut width={250} data={this.state.sentimentChart_SVM} legend={{ display: true }} redraw onElementsClick={(e) => this.showTweets(e, SVM)}/>;

          vTmpObj = this.state.sentimentChart_LR;
          vTmpObj.datasets[0].data = [lr_pos_count, lr_neg_count];
          this.setState({ sentimentChart_LR: vTmpObj });
          this.setState({ lr_sentiment_positive: lr_pos_count });
          this.setState({ lr_sentiment_negative: lr_neg_count });
          toDisplay_lr = <Doughnut width={250} data={this.state.sentimentChart_LR} legend={{ display: true }} redraw onElementsClick={(e) => this.showTweets(e, LR)}/>;

          var i = 0;

          var mnb_tweets = result.mnb_tweets;
          mnb_tweets = JSON.parse(mnb_tweets);
          i = 0;
          const mnb_neg_tweets = mnb_tweets[0]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          i = 0;
          const mnb_pos_tweets = mnb_tweets[1]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          this.setState({mnb_sentiment_positive_tweets_table: mnb_pos_tweets});
          this.setState({mnb_sentiment_negative_tweets_table: mnb_neg_tweets});

          var svm_tweets = result.svm_tweets;
          svm_tweets = JSON.parse(svm_tweets);
          i = 0;
          const svm_neg_tweets = svm_tweets[0]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          i = 0;
          const svm_pos_tweets = svm_tweets[1]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          this.setState({svm_sentiment_positive_tweets_table: svm_pos_tweets});
          this.setState({svm_sentiment_negative_tweets_table: svm_neg_tweets});

          var lr_tweets = result.lr_tweets;
          lr_tweets = JSON.parse(lr_tweets);
          i = 0;
          const lr_neg_tweets = lr_tweets[0]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          i = 0;
          const lr_pos_tweets = lr_tweets[1]["Data"].map((data) =>
            <tr key={i++}>
              <td>{data[0]}</td>
              <td>{data[1]}</td>
            </tr>
          );
          this.setState({lr_sentiment_positive_tweets_table: lr_pos_tweets});
          this.setState({lr_sentiment_negative_tweets_table: lr_neg_tweets});
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
