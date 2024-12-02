"use strict";
(function(){
    window.addEventListener("load", init);
    
    function init() {
        qs("form button").addEventListener('click', (e) => {
            e.preventDefault();
            sendData();
            open("results.html", "_self");
        });
    }

    function sendData() {
        const text = id("exampleFormControlTextarea1").value;
        window.sessionStorage.setItem("text", text);
        //open the results.html page...
    }
    /* ------------------------------ Helper Functions  ------------------------------ */

    /**
     * Returns the element that has the ID attribute with the specified value.
     * @param {string} id - element ID
     * @returns {object} DOM object associated with id.
     */
    function id(idName) {
        return document.getElementById(idName);
    }

    /**
     * Returns the first element that matches the given CSS selector.
     * @param {string} query - CSS query selector.
     * @returns {object} The first DOM object matching the query.
     */
    function qs(query) {
        return document.querySelector(query);
    }
})()