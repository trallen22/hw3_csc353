// You have to do an 'npm install mysql2' to get the package
// Documentation in: https://www.npmjs.com/package/mysql2

import { createConnection } from 'mysql2';

var connection = createConnection({
	host: 'localhost',
	user: 'root',
	password: '123456',
	database: 'Tennis'
});

function connect() {
	connection.connect();
}

function queryCallback(queryParam, queryType, callback) {
	if(queryType == 'playerQuery'){

		connection.query("SELECT * FROM player WHERE name = ?", [queryParam], (error, results, fields) => {
			if (error) throw error;

			console.log(results)
			callback(results);
		});

	}
	else if(queryType == 'yearQuery'){

		connection.query(queryParam, (error, results, fields) => {
			if (error) throw error;

			console.log(results)
			callback(results);
		});

	}

	// With parameters:
	// "... WHERE name = ?", ['Fernanda'], (error ...)
}

function disconnect() {
	connection.end();
}

// Setup exports to include the external variables/functions
export {
	connection,
	connect,
	queryCallback,
	disconnect
}

// For testing:
// connect()
// queryCallback(r => console.log(r))
// disconnect()