# Tristan Allen and Will Cox 

from dataclasses import dataclass
import mysql.connector
from mysql.connector import Error
import glob
import lxml
import lxml.etree
import datetime
import csv 

HOST = 'localhost'
USER = 'root'


# This function takes a connection and then reads and executes a given sql file 
def createSchema(connection):
	# reading schema file 
	sqlFile = open("Schema.sql", 'r')
	schema_string = sqlFile.readlines()
	sqlFile.close()
	cursor = connection.cursor()

	newQuery = []
	for line in schema_string:
		line = line.strip()
		line = line.replace(';', '; ')
		newQuery.append(line)
	singleQuery = "".join(newQuery)

	listQuery = singleQuery.split("; ")

	# running each command line by line 
	for q in listQuery:
		if q != '':
			cursor = connection.cursor()
			cursor.execute(f'{q};', multi=False)
			connection.commit()

	cursor.close()
	return

def sqlInsert(table, tupleAttributes):
    if table == 'tournament':
        sqlStr = f'INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s)'

    cursor.execute(sqlStr, tupleAttributes)
    connection.commit()


################
# Main execution starts here
################

i = 1 

try: 
	connection = mysql.connector.connect(host=HOST, user=USER, database="Tennis") 
except Exception as e:
	print(f'error: {e}')

# running the Schema.sql 
# createSchema(connection)
cursor = connection.cursor()

import os
print(os.getcwd())

tourneyIdSet = set()

print(f'starting to parse files')
for filename in glob.glob(f"{os.getcwd()}/tennis_atp/atp_matches_????.csv"):
    print(f'parsing file {i}')
    i += 1

    with open(filename, 'r') as curFile:
        curCsv = csv.DictReader(curFile)
        for row in curCsv:

            if not row['tourney_id'] in tourneyIdSet:
                # print(f'cur t id set: {tourneyIdSet}')
                # print(f"cur val: {row['tourney_id']}")
                curTourneyTuple = (row['tourney_id'], row['tourney_name'], row['surface'], (row['draw_size'] if not row['draw_size'] == '' else 0), row['tourney_level'], row['tourney_date'])
                sqlInsert('tournament', curTourneyTuple)            
                tourneyIdSet.add(row['tourney_id'])

            

cursor.close()