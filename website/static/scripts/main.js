"use strict";
(function(){
    window.addEventListener("load", init);
    
    function init() {
        qs("form button").addEventListener('click', (e) => {
            e.preventDefault(); //event.preventdefault() is used as Bootstrap buttons tend to refresh the page when clicked.
            sendData();
            open("results.html", "_self"); //redirects the user to results.html
        });
    }

    //This function is used to store the data input by the user in sessionStorage, which can then be sent to the server in a POST request in results.js.
    function sendData() {
        const text = id("exampleFormControlTextarea1").value;
        window.sessionStorage.setItem("text", text);
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