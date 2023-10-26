DROP SCHEMA IF EXISTS Tennis;
CREATE SCHEMA Tennis; 
USE Tennis; 

CREATE TABLE player 
	(player_id 			INT, 
	name 			VARCHAR(50),
	hand 			VARCHAR(1),
	height			INT, 
	ioc 			VARCHAR(3), 
	age 			DOUBLE, 
	PRIMARY KEY (player_id)
	);
	
CREATE TABLE tournament 
	(tournament_id  	VARCHAR(50),
	name 				VARCHAR(50), 
	surface 			VARCHAR(10), 
	draw_size 			INT, 
	tourney_level 		VARCHAR(3), 
	tourney_date 		INT, 
	PRIMARY KEY (tournament_id) 
	);

CREATE TABLE matches 
	(tournament_id 		VARCHAR(50),
	match_num  			INT, 
	score 			VARCHAR(40), 
	best_of 		INT, 
	round 			VARCHAR(4), 
	minutes 		INT, 
	PRIMARY KEY (match_num, tournament_id),
	FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id)
	);

CREATE TABLE plays 
	(player_id 			INT, 
	match_num 			INT, 
	win_loss			VARCHAR(4), 
	ace 				INT, 
	dbl_fault 			INT, 
	serve_point 		INT, 
	brk_points_saved 	INT, 
	FOREIGN KEY (player_id) REFERENCES player (player_id), 
	FOREIGN KEY (match_num) REFERENCES matches (match_num)
	);
	