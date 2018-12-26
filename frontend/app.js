//Load HTTP module
const http = require("http");
require("")
const express = require('express')
const app = express();
// app.use(require('express-title')());

const hostname = '127.0.0.1';
const port = 3000;

app.get('/', (req, res) => {
  
  res.send('Hello World!')
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}!`)
});