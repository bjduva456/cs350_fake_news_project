"use strict";
(function(){
    window.addEventListener('load', init);

    function init() {
        try {
            const text = window.sessionStorage.getItem("text");
            fetch("http://localhost:8080/predict/", { method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})})
            .then(checkStatus)
            .then(createObjects)
            .catch((e) => console.log('Error:', e));
        }catch(e){
            console.log(`There was an issue retrieving your text: \n${e}`);
        }
    }
    function createObjects(data) {
        console.log(data);
        let jsondata = JSON.parse(data);
        console.log(jsondata.filepath);
        let graph = document.createElement('img');
        graph.src = "http://localhost:8080/images/" + jsondata.filepath;
        graph.classList.add('graph');
        document.getElementById("imgbox").appendChild(graph);
        let preds = qsa('.pred');
        let confs = qsa('.conf');
        const modelKeys = Object.keys(jsondata.models)
        for(let i = 0; i < modelKeys.length; i++){
            const modelName = modelKeys[i]; 
            const model = jsondata.models[modelName];
            preds[i].textContent = model.label;
            confs[i].textContent = (model.confidence * 100).toFixed(2) + '%';
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