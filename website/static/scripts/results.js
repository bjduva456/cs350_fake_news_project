"use strict";
(function(){
    window.addEventListener('load', init);

    function init() {
        try {
            const text = window.sessionStorage.getItem("text"); //retrieve text from Session Storage
            fetch("http://localhost:8080/predict/", { method: "POST", //send POST request to server. If hosted, this IP changes.
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})})
            .then(checkStatus)
            .then(createObjects)
            .catch((e) => console.log('Error:', e));
        }catch(e){
            console.log(`There was an issue retrieving your text: \n${e}`);
        }
    }

    //This function is used for parsing the results of the POST request and populating the page.
    function createObjects(data) {
        console.log(data);
        let jsondata = JSON.parse(data); //get JSON data
        console.log(jsondata.filepath);
        let graph = document.createElement('img'); //Create an image element for the graph.
        graph.src = "http://localhost:8080/images/" + jsondata.filepath; //This IP is based on localhosting the server. Any other hosting this must be changed.
        graph.classList.add('graph');
        document.getElementById("imgbox").appendChild(graph); //Add graph to imgbox
        let preds = qsa('.pred');
        let confs = qsa('.conf');
        const modelKeys = Object.keys(jsondata.models)
        for(let i = 0; i < modelKeys.length; i++){ //for each model, update the label and confidence <span>'s.
            const modelName = modelKeys[i]; 
            const model = jsondata.models[modelName];
            preds[i].textContent = model.label;
            confs[i].textContent = (model.confidence * 100).toFixed(2) + '%'; //Truncate the decimal to 2 places and attach a %.
        }
    }
    /**
     * Returns the array of elements that match the given CSS selector.
     * @param {string} query - CSS query selector
     * @returns {object[]} array of DOM objects matching the query.
     */
    function qsa(query) {
        return document.querySelectorAll(query);
    }
     /**
     * This function needs documentation.
     * @returns {} response as json format
     */
     function checkStatus(response) {
        if (!response.ok) {
            throw Error("Error in request: " + response.statusText);
        }
        return response.json();
    }
})()