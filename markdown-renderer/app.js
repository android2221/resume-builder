require ('dotenv').config()
const express = require('express');
const app = express();

const MarkdownIt = require('markdown-it'),
    md = new MarkdownIt();

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));


app.get('/', (req, res) => {
  return res.send('Received a GET HTTP method');
});

app.post('/', (req, res) => {
  console.log('Received a request to render markdown');
  var result = md.render(req.body.markdownContent);
  return res.send(result);
});

app.put('/', (req, res) => {
  return res.send('Received a PUT HTTP method');
});
app.delete('/', (req, res) => {
  return res.send('Received a DELETE HTTP method');
});
app.listen(process.env.PORT, () =>
  console.log(`Markdown Renderer listening on port ${process.env.PORT}!`),
);
