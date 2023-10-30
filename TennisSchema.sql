DROP SCHEMA IF EXISTS Tennis;
CREATE SCHEMA Tennis; 
USE Tennis; 

CREATE TABLE player 
	(player_id 			INT, 
	name 			VARCHAR(50) NULL,
	hand 			VARCHAR(1) NULL CHECK (hand = 'L' OR hand = 'R' OR hand = 'U'),
	height			INT NULL, 
	ioc 			VARCHAR(3) NULL, 
	age 			DOUBLE NULL, 
	PRIMARY KEY (player_id)
	);
	
CREATE TABLE tournament 
	(tournament_id  	INT AUTO_INCREMENT,
	name 				VARCHAR(50) NULL, 
	surface 			VARCHAR(10) NULL, 
	draw_size 			INT NULL, 
	tourney_level 		VARCHAR(3) NULL, 
	tourney_date 		DATE NULL, 
	PRIMARY KEY (tournament_id) 
	);

CREATE TABLE matches 
	(tournament_id 		INT,
	match_id  			INT AUTO_INCREMENT, 
	score 			VARCHAR(40) NULL, 
	best_of 		INT NULL, 
	round 			VARCHAR(4) NULL, 
	minutes 		INT NULL, 
	PRIMARY KEY (match_id, tournament_id),
	FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE
	);

CREATE TABLE plays 
	(player_id 			INT, 
	player_rank 		INT CHECK (player_rank > 0), 
	match_id 			INT, 
	win_loss			VARCHAR(4) NULL, 
	ace 				INT NULL, 
	dbl_fault 			INT NULL, 
	serve_point 		INT NULL, 
	brk_points_saved 	INT NULL, 
	FOREIGN KEY (player_id) REFERENCES player (player_id) ON DELETE SET NULL, 
	FOREIGN KEY (match_id) REFERENCES matches (match_id)
	);
	