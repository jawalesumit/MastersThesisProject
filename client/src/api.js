import axios from 'axios';
import axiosRetry from 'axios-retry';

var config = require('./server_config.json');
var vURL = "http://" + config.server_ip + ":" + config.server_port + "/";

const server = axios.create({ baseURL: vURL });
axiosRetry(server, { retries: 3, retryDelay: axiosRetry.exponentialDelay }); // assign retries and retries delay if fetching from server fails

export default server;