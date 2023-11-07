# Tristan Allen and Will Cox 

import mysql.connector
from mysql.connector import Error
import glob
import csv 
import os
import sys

HOST = 'localhost'
USER = 'root'

# sqlInsert: executes a SQL insert statement on a given table
# parameters: 
# 	table - str, name of table to insert values into 
#	curTuple - tuple, tuple of values to insert into table 	
def sqlInsert(table, curTuple):
	if table == 'plays':
		sqlStr = f'INSERT INTO plays VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
	else: 
		sqlStr = f'INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s);'

	try:
		cursor.execute(sqlStr, curTuple)
	except Exception as e:
		print(f"failed table: {table}")
		print(f"failed insert: {curTuple}")
		print(f"ERROR: {e}")


################
# Main execution starts here
################


try: 
	connection = mysql.connector.connect(host=HOST, user=USER, password='123456', database="Tennis") 
except Exception as e:
	print(f'error: {e}')
	sys.exit()

cursor = connection.cursor()

# these sets are used to check if values have already been inserted into the table 
tourneyIdSet = set() 
playerIdSet = set()
matchIdSet = set()
playsIdSet = set()

# keeps track of tourney_ids that use AUTO_INCREMENT
tourneyId = 0
tourneyIdMap ={}

# keeps track of match_ids that use AUTO_INCREMENT
matchId = 0
matchIdMap = {}

for filename in glob.glob(f"{os.getcwd()}/tennis_atp/atp_matches_????.csv"):

	with open(filename, 'r') as curFile:
		curCsv = csv.DictReader(curFile)
		for row in curCsv:

			# tournament table 
			if not row['tourney_id'] in tourneyIdSet:
				curTourneyTuple = (0, 
								row['tourney_name'], 
								row['surface'], 
								(row['draw_size'] if not row['draw_size'] == '' else None), 
								row['tourney_level'], row['tourney_date'])

				sqlInsert('tournament', curTourneyTuple)      
				tourneyIdSet.add(row['tourney_id'])
				tourneyId += 1
				tourneyIdMap[row['tourney_id']] = tourneyId

			# player table using winner from match
			if not row['winner_id'] in playerIdSet:
				curPlayerTuple = (row['winner_id'], 
								row['winner_name'], 
								(row['winner_hand'] if (row['winner_hand'] == 'R' or row['winner_hand'] == 'L') else 'U'), 
								(row['winner_ht'] if not row['winner_ht'] == '' else None),
								row['winner_ioc'], 
								(row['winner_age'] if not row['winner_age'] == '' else None))
				sqlInsert('player', curPlayerTuple)
				playerIdSet.add(row['winner_id'])

			# player table using loser from match 
			if not row['loser_id'] in playerIdSet:
				curPlayerTuple = (row['loser_id'], 
								row['loser_name'], 
								(row['loser_hand'] if (row['loser_hand'] == 'R' or row['loser_hand'] == 'L') else 'U'), 
								(row['loser_ht'] if not row['loser_ht'] == '' else None), 
								row['loser_ioc'], 
								(row['loser_age'] if not row['loser_age'] == '' else None))
				sqlInsert('player', curPlayerTuple)
				playerIdSet.add(row['loser_id'])
			
			# match table 
			if not (row['tourney_id'], row['match_num']) in matchIdSet:
				curMatchTuple = (tourneyIdMap.get(row['tourney_id']), 
								0, 
								row['score'], 
								row['best_of'], 
								row['round'], 
								(row['minutes'] if not row['minutes'] == '' else None))

				sqlInsert('matches', curMatchTuple)
				matchIdSet.add((row['tourney_id'], row['match_num']))
				matchId += 1
				matchIdMap[(row['tourney_id'],row['match_num'])] = matchId

			# plays table 
			if not ((row['tourney_id'], row['match_num'])) in playsIdSet:
				curWinnerTuple = (row['winner_id'],
											(row['winner_rank'] if not row['winner_rank'] == '' else None),
											matchIdMap.get((row['tourney_id'], row['match_num'])), 'win', 
											(row['w_ace'] if not row['w_ace'] == '' else None), 
											(row['w_df'] if not row['w_df'] == '' else None), 
											(row['w_svpt'] if not row['w_svpt'] == '' else None), 
											(row['w_bpSaved'] if not row['w_bpSaved'] == '' else None))

				curLoserTuple = (row['loser_id'], 
											(row['loser_rank'] if not row['loser_rank'] == '' else None), 
											matchIdMap.get((row['tourney_id'], row['match_num'])), 'lose', 
											(row['l_ace'] if not row['l_ace'] == '' else None), 
											(row['l_df'] if not row['l_df'] == '' else None), 
											(row['l_svpt'] if not row['l_svpt'] == '' else None), 
											(row['l_bpSaved'] if not row['l_bpSaved'] == '' else None))

				sqlInsert('plays', curWinnerTuple)
				sqlInsert('plays', curLoserTuple)
				playsIdSet.add((row['tourney_id'], row['match_num']))

connection.commit()

cursor.close()
