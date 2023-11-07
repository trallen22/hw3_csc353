// This is a framework to handle server-side content

// You have to do an 'npm install express' to get the package
// Documentation in: https://expressjs.com/en/starter/hello-world.html
import express from 'express';

import * as db from "./db_mysql.mjs";

var app = express();
let port = 3001

db.connect();

// Serve static HTML files in the current directory (called '.')
app.use(express.static('.'))

// For GET requests to "/student?field1=value1&field2=value2"
app.get('/player', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let playerName = request.query["name"]

    db.queryCallback(playerName, 'playerQuery', (results) => {
        response.json(results)
    })
});

app.get('/tournament', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"]);

    let year = request.query["tourney_date"]

    console.log("SELECT * FROM tournament WHERE tourney_date > '" + year + "-01-01' AND tourney_date < '" + year + "-12-31'")
    db.queryCallback("SELECT * FROM tournament WHERE tourney_date > '" + year + "-01-01' AND tourney_date < '" + year + "-12-31'", 'yearQuery', (results) => {
        response.json(results)
    })
});


app.listen(port, () => console.log('Server is starting on PORT,', port))

process.on('exit', () => {
    db.disconnect()
})