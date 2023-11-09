// You have to do an 'npm install mysql2' to get the package
// Documentation in: https://www.npmjs.com/package/mysql2

import { query } from 'express';
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

	else if(queryType == 'aggregateQuery'){


		connection.query("CALL showAggregateStatistics(?, ?, ?)", [queryParam[0], queryParam[1], queryParam[2]], (error, results, fields) => {
			if (error) throw error;

			console.log(results)
			callback(results);
		});

	}

	//SELECT aceCount('Rafael Nadal', '20180101', '20220101');



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