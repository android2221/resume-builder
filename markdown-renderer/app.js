require ('dotenv').config()
const express = require('express');
const app = express();

var MarkdownIt = require('markdown-it'),
    md = new MarkdownIt();

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));


app.get('/', (req, res) => {
  return res.send('Received a GET HTTP method');
});

app.post('/', (req, res) => {
  console.log(req.body)
  return res.send(md.render(req.body.markdownContent));
});

app.put('/', (req, res) => {
  return res.send('Received a PUT HTTP method');
});
app.delete('/', (req, res) => {
  return res.send('Received a DELETE HTTP method');
});
app.listen(process.env.PORT, () =>
  console.log(`Example app listening on port ${process.env.PORT}!`),
);