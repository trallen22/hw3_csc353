# Tristan Allen and Will Cox 

from dataclasses import dataclass
from socketserver import StreamRequestHandler
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
	return

def sqlInsert(table, curTuple):
	if table == 'plays':
		sqlStr = f'INSERT INTO plays VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
	else: 
		sqlStr = f'INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s);'

	cursor.execute(sqlStr, curTuple)

	# try:
	# 	cursor.execute(sqlStr, curTuple)
	# except Exception as e:
	# 	print(f"failed table: {table}")
	# 	print(f"failed insert: {curTuple}")
	# 	print(f"ERROR: {e}")


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

createSchema(connection)

tourneyIdSet = set() 
playerIdSet = set()
matchIdSet = set()
playsIdSet = set()
tourneyId = 0

print(f'starting to parse files')
for filename in glob.glob(f"{os.getcwd()}/tennis_atp/atp_matches_????.csv"):
	print(f'parsing file {i}: {filename}')
	i += 1
	
	with open(filename, 'r') as curFile:
		curCsv = csv.DictReader(curFile)
		x = 0
		for row in curCsv:

			# tournament table 
			if not row['tourney_id'] in tourneyIdSet:
				curTourneyTuple = (0, row['tourney_name'], row['surface'], 
								(row['draw_size'] if not row['draw_size'] == '' else None), 
								row['tourney_level'], row['tourney_date'])

				sqlInsert('tournament', curTourneyTuple)      
				tourneyIdSet.add(row['tourney_id'])
				tourneyId += 1

			# # player table using winner from match
			# if not row['winner_id'] in playerIdSet:
			# 	curPlayerTuple = (row['winner_id'], row['winner_name'], 
			# 					(row['winner_hand'] if (row['winner_hand'] == 'R' or row['winner_hand'] == 'L') else 'U'), 
			# 					(row['winner_ht'] if not row['winner_ht'] == '' else None),
			# 					row['winner_ioc'], 
			# 					(row['winner_age'] if not row['winner_age'] == '' else None))
			# 	# print(f"winner id: {row['winner_id']} hand: {row['winner_hand']}")
			# 	# print(f"cur player tuple: {curPlayerTuple}")
			# 	sqlInsert('player', curPlayerTuple)
			# 	playerIdSet.add(row['winner_id'])

			# # player table using loser from match 
			# if not row['loser_id'] in playerIdSet:
			# 	curPlayerTuple = (row['loser_id'], row['loser_name'], 
			# 					(row['loser_hand'] if (row['loser_hand'] == 'R' or row['loser_hand'] == 'L') else 'U'), 
			# 					(row['loser_ht'] if not row['loser_ht'] == '' else None), 
			# 					row['loser_ioc'], 
			# 					(row['loser_age'] if not row['loser_age'] == '' else None))
			# 	# print(f"loser id: {row['loser_id']} hand: {row['loser_hand']}")
			# 	# print(f"cur player tuple: {curPlayerTuple}")
			# 	sqlInsert('player', curPlayerTuple)
			# 	playerIdSet.add(row['loser_id'])
			
			# match table 
			if not (row['tourney_id'], row['match_num']) in matchIdSet:
				curMatchTuple = (tourneyId, row['match_num'], row['score'], 
								row['best_of'], row['round'], 
								(row['minutes'] if not row['minutes'] == '' else None))
				print(f"tourney_id: {row['tourney_id']} / {tourneyId} match num: {row['match_num']}")
				print(f"cur Match Tuple: {curMatchTuple}")

				sqlInsert('matches', curMatchTuple)
				matchIdSet.add((row['tourney_id'], row['match_num']))

			# # plays table 
			# if not ((row['tourney_id'], row['match_num'])) in playsIdSet:
			# 	curWinnerTuple = (row['winner_id'],
			# 								(row['winner_rank'] if not row['winner_rank'] == '' else None),
			# 								row['match_num'], 'win', 
			# 								(row['w_ace'] if not row['w_ace'] == '' else None), 
			# 								(row['w_df'] if not row['w_df'] == '' else None), 
			# 								(row['w_svpt'] if not row['w_svpt'] == '' else None), 
			# 								(row['w_bpSaved'] if not row['w_bpSaved'] == '' else None))

			# 	curLoserTuple = (row['loser_id'], 
			# 								(row['loser_rank'] if not row['loser_rank'] == '' else None), 
			# 								row['match_num'], 'lose', 
			# 								(row['l_ace'] if not row['l_ace'] == '' else None), 
			# 								(row['l_df'] if not row['l_df'] == '' else None), 
			# 								(row['l_svpt'] if not row['l_svpt'] == '' else None), 
			# 								(row['l_bpSaved'] if not row['l_bpSaved'] == '' else None))

				# sqlInsert('plays', curWinnerTuple)
				# sqlInsert('plays', curLoserTuple)
				# playsIdSet.add((row['tourney_id'], row['match_num']))
		# 	x += 1
		# 	if x == 5:
		# 		break

		# break

connection.commit()

cursor.close()
