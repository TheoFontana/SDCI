/**
 *  Author: Theo Fontana and Daniel Organista
 *  File : monitor.js
 *  Version : 0.1.0
 */

var express = require('express')
var app = express()
var request = require('request');

app.get('/monitor', function(req, res) {
    console.log(req.body);
    request({method: 'GET', uri: `http://10.1.0.10:8181/health`}, (error, response, body) => {
        console.log("response: ", body);
        if (!error && response.statusCode == 200){
            res.send(body);
        } else {
            res.send(error);
        }
    });
});

app.listen(8888 , function () {
    console.log("monitoring vnf " + ' listening on : ' + "1234" );
});
