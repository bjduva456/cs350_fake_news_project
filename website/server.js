"use strict";
//this will be where the models will be hosted, users will submit their text input through the website (post request) and the server will return the models' results.
const express = require("express");
//const { spawn } = require('child_process');
const child_process = require('child_process')
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.static('static'));
app.use(bodyParser.json());

const spawn = child_process.spawn;
//const python = spawn('C:\\Users\\kmbbm\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe', ['./query_models.py']);
const python = spawn('C:\\Users\\kmbbm\\anaconda3\\python.exe', ['./query_models.py']);
//const scriptPath = path.join(__dirname, 'query_models.py')
//const python = spawn('python', ['./query_models']);
python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});
/*
python.on('close', (code) => {
    if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
    }
});*/


app.post('/predict', (req, res) => {
    const text = String(req.body.text); 
    //const pythonModels = spawn('C:\\Users\\kmbbm\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe', ['./query_models.py', text]);
    const pythonModels = spawn('C:\\Users\\kmbbm\\anaconda3\\python.exe', ['./query_models.py', text]);
    pythonModels.stdout.on('data', (data) => {
        try{
            const data_str = data.toString();
            //.replace(/[\s\n\\]/g, "");
            console.log(data_str);
            const result = JSON.parse(data_str);
            return res.status(200).json(result);  
        }catch(e){
            console.log(e);
        }

    });
    pythonModels.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    //python.stdin.write(JSON.stringify({ text: text }) + '\n');
    python.stdin.end();
});
/*
app.get('/images/:id', (req, res) => {
    const id = req.params.id;
    const imgUrl = `http://localhost:{PORT}/images/${id}`;
    res.status(200).json({src:imgUrl})
});
app.use("/images", express.static(path.join(__dirname, "images")));
*/
app.use('/images', express.static(path.join(__dirname, 'images')));

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});