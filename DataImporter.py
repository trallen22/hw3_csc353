# Tristan Allen and Will Cox 

from dataclasses import dataclass
import mysql.connector
from mysql.connector import Error
import glob
import csv 
import os

HOST = 'localhost'
USER = 'root'


# This function takes a connection and then reads and executes a given sql file 
def createSchema(connection):
	# reading schema file 
	sqlFile = open("TennisSchema.sql", 'r')
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

def sqlInsert(table, curTuple):
	if table == 'plays':
		sqlStr = f'INSERT INTO plays VALUES (%s, %s, %s, %s, %s, %s, %s);'
	else: 
		sqlStr = f'INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s);'

	cursor.execute(sqlStr, curTuple)


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

print(os.getcwd())

tourneyIdSet = set()
playerIdSet = set()
matchIdSet = set()
playsIdSet = set()

print(f'starting to parse files')
for filename in glob.glob(f"{os.getcwd()}/tennis_atp/atp_matches_????.csv"):
	print(f'parsing file {i}')
	i += 1
	sqlScript = ""
	with open(filename, 'r') as curFile:
		curCsv = csv.DictReader(curFile)
		for row in curCsv:

			if not row['tourney_id'] in tourneyIdSet:
				# print(f'cur t id set: {tourneyIdSet}')
				# print(f"cur val: {row['tourney_id']}")
				curTourneyTuple = (row['tourney_id'], row['tourney_name'], row['surface'], 
								(row['draw_size'] if not row['draw_size'] == '' else 0), 
								row['tourney_level'], row['tourney_date'])

				sqlInsert('tournament', curTourneyTuple)      
				tourneyIdSet.add(row['tourney_id'])

			if not row['winner_id'] in playerIdSet:
				curPlayerTuple = (row['winner_id'], row['winner_name'], row['winner_hand'], 
								(row['winner_ht'] if not row['winner_ht'] == '' else 0),
								row['winner_ioc'], 
								(row['winner_age'] if not row['winner_age'] == '' else 0))
				
				sqlInsert('player', curPlayerTuple)
				playerIdSet.add(row['winner_id'])

			if not row['loser_id'] in playerIdSet:
				curPlayerTuple = (row['loser_id'], row['loser_name'], row['loser_hand'], 
								(row['loser_ht'] if not row['loser_ht'] == '' else 0), 
								row['loser_ioc'], 
								(row['loser_age'] if not row['loser_age'] == '' else 0))

				sqlInsert('player', curPlayerTuple)
				playerIdSet.add(row['loser_id'])
			
			if not (row['tourney_id'], row['match_num']) in matchIdSet:
				curMatchTuple = (row['tourney_id'], row['match_num'], row['score'], 
								row['best_of'], row['round'], 
								(row['minutes'] if not row['minutes'] == '' else 0))

				sqlInsert('matches', curMatchTuple)
				matchIdSet.add((row['tourney_id'], row['match_num']))

			if not ((row['tourney_id'], row['match_num'])) in playsIdSet:
				curWinnerTuple = (row['winner_id'], row['match_num'], 'win', 
											(row['w_ace'] if not row['w_ace'] == '' else 0), 
											(row['w_df'] if not row['w_df'] == '' else 0), 
											(row['w_svpt'] if not row['w_svpt'] == '' else 0), 
											(row['w_bpSaved'] if not row['w_bpSaved'] == '' else 0))
				curLoserTuple = (row['loser_id'], row['match_num'], 'lose', 
											(row['l_ace'] if not row['l_ace'] == '' else 0), 
											(row['l_df'] if not row['l_df'] == '' else 0), 
											(row['l_svpt'] if not row['l_svpt'] == '' else 0), 
											(row['l_bpSaved'] if not row['l_bpSaved'] == '' else 0))

				sqlInsert('plays', curWinnerTuple)
				sqlInsert('plays', curLoserTuple)
				playsIdSet.add((row['tourney_id'], row['match_num']))

	connection.commit()

cursor.close()
