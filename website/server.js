"use strict";

//This script handles the API requests by the client-side javascript. It aso uses child_process to run query_models.py on startup
const express = require("express");
const child_process = require('child_process')
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.static('static'));
app.use(bodyParser.json());

const spawn = child_process.spawn;
const python = spawn('C:\\Users\\kmbbm\\anaconda3\\python.exe', ['./query_models.py']); //spawn requires a route to the local Python installation, to run on another machine this MUST be changed.
python.stderr.on('data', (data) => { //Any errors or warnings are passed as stderr, I was getting serveral warnings when running the scripts.
    console.error(`stderr: ${data}`);
});

app.post('/predict', (req, res) => { //POST request handler
    const text = String(req.body.text); 
    const pythonModels = spawn('C:\\Users\\kmbbm\\anaconda3\\python.exe', ['./query_models.py', text]); //spawn uses a route to local Python installation. This MUST be changed to use on another machine.
    pythonModels.stdout.on('data', (data) => { //when results are generated in query_models.py, they are printed, thus sent through stdout
        try{
            const data_str = data.toString(); //converts the raw data to a string so it can be parsed into JSON. Otherwise, it outputs in binary. 
            console.log(data_str);
            const result = JSON.parse(data_str);
            return res.status(200).json(result);  //Send the result back as a JSON.
        }catch(e){
            console.log(e);
        }

    });
    pythonModels.stderr.on('data', (data) => { //this handles spawn's errors with Python
        console.error(`stderr: ${data}`);
    });
    python.stdin.end();
});

app.use('/images', express.static(path.join(__dirname, 'images'))); //this line is used for express to serve images to a client using the server's IP.

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});