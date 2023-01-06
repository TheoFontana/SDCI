
/**
 * Author: Théo FONTANA theo.fontana@insa-toulouse.fr
 * File : metadata_server.js
 * Version : 0.1.1
 */

const fs  = require ('fs');
const config = JSON.parse(fs.readFileSync('./config.json'))

var express = require('express')
var app = express()
app.use(express.json())
var LOCAL_ENDPOINT = {IP : 'localhost', PORT : 8080, NAME : 'metadata server'};

const E_OK = 200;
const E_NOT_FOUND = 404;
app.get('/:dck', function(req, res) {
    console.log(req.body);
    var dck = req.params.dck;
    var docker = config[dck];
    if (docker)
        res.status(E_OK).send(JSON.stringify(docker));
    else
        res.sendStatus(E_NOT_FOUND);
});
app.listen(LOCAL_ENDPOINT.PORT , function () {
    console.log(LOCAL_ENDPOINT.NAME + ' listening on : ' + LOCAL_ENDPOINT.PORT );
});