const express = require('express');
const { spawn } = require('child_process');
const app = express();
const port = 3000;
const multer = require('multer');
const upload = multer(); // Sets up multer for data parsing

// Express 4.16+ has built-in body-parser middleware for urlencoded form data
app.use(express.urlencoded({ extended: true }));

// Serve static files from 'public' folder
app.use(express.static('public'));

app.post('/predict', upload.none(), (req, res) => {
  console.log('Received body:', req.body); // Detailed logging of the body
  const userInput = req.body.textInput;

  if (typeof userInput === 'undefined') {
    console.error('userInput is undefined.');
    return res.status(400).send('No textInput provided.');
  }

  console.log('Received userInput:', userInput); // Log the userInput to see what you received

const pythonProcess = spawn('python3', ['IQ_predict_run.py', userInput]);

  let pythonOutput = '';
  pythonProcess.stdout.on('data', (data) => {
    pythonOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      return res.send(`Error: Python script exited with code ${code}`);
    }
    res.send(`Prediction: ${pythonOutput}`);
  });

});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
