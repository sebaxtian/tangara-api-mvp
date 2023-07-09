/// version 1.2.2
/// copy tc-types.d.ts file for vscode autocompletion on tc object
/// <reference path="./tc-types.d.ts" />

// built-in node modules
//const CryptoJS = require("crypto-js");
//const { v4: uuid4 } = require("uuid");
const axios = require('axios');  // -- you can use async/await to make requests
// ---- more node modules supported
// tough-cookie, ajv, ajv-formats, papaparse, http, https, assert, buffer, stream, url

// ---- To load any additional node modules from npm
// await tc.loadModule("moduleName");  see example below.


async function totalComunas() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/comunas/');
        console.log("Response Status: ", response.status);
        console.log("Total Comunas: ", response.data.count)
        // ---- save to active environment
        tc.setVar("total_comunas", response.data.count);
    } catch (error) {
        console.error("Error: ", error.message);
    }
}

module.exports = [totalComunas];
