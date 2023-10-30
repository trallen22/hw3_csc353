USE Tennis;

DROP FUNCTION IF EXISTS aceCount;
DELIMITER //
CREATE FUNCTION aceCount(name VARCHAR(50), start DATE, finish DATE) 
RETURNS DOUBLE 
DETERMINISTIC
BEGIN 
    DECLARE average DOUBLE;
    
    SELECT AVG(T2.ace) INTO average
        FROM player AS cp
        JOIN (SELECT pl.player_id, pl.ace 
            FROM plays as pl 
            JOIN (SELECT t.tourney_date, m.match_id 
                FROM tournament AS t 
                JOIN matches AS m ON t.tournament_id=m.tournament_id
                WHERE t.tourney_date > start
                    AND t.tourney_date < finish) AS T1 ON pl.match_id=T1.match_id) 
                AS T2 ON cp.player_id=T2.player_id
        WHERE cp.name=name;

    RETURN average;
END;
// 
DELIMITER ;

SELECT aceCount('Rafael Nadal', '20180101', '20220101');



DROP PROCEDURE IF EXISTS showAggregateStatistics;
DELIMITER // 
CREATE PROCEDURE showAggregateStatistics(name VARCHAR(50), start DATE, finish DATE)
BEGIN
    SELECT cp.name, AVG(P1.ace) AS aces_per_match, AVG(P1.dbl_fault) AS dbl_faults_per_match, 
        AVG(P1.serve_point) AS serve_points_per_match, AVG(P1.brk_points_saved) AS brk_points_saved_per_match
    FROM player AS cp
    JOIN (SELECT pl.player_id, pl.ace, pl.dbl_fault, pl.serve_point, pl.brk_points_saved 
        FROM plays as pl 
        JOIN (SELECT t.tourney_date, m.match_id 
            FROM tournament AS t 
            JOIN matches AS m ON t.tournament_id=m.tournament_id
            WHERE t.tourney_date > start AND t.tourney_date < finish) 
            AS T1 ON pl.match_id=T1.match_id) 
        AS P1 ON cp.player_id=P1.player_id
    WHERE cp.name=name
    GROUP BY cp.name;    
END;
// 
DELIMITER ;

CALL showAggregateStatistics('Rafael Nadal', '20180101', '20210101');



DROP VIEW IF EXISTS topAces;
CREATE VIEW topAces AS 
SELECT p.name, SUM(m.ace) AS total_aces
FROM plays AS m 
JOIN player AS p ON m.player_id=p.player_id
GROUP BY m.player_id
ORDER BY SUM(m.ace) DESC
LIMIT 10;

SELECT * FROM topAces;



DROP TRIGGER IF EXISTS onInsertionPlayer;
DELIMITER // 
CREATE TRIGGER onInsertionPlayer 
BEFORE INSERT ON player 
FOR EACH ROW 
BEGIN 
    IF NEW.ioc='RUS' OR NEW.ioc='EST'
    THEN SET NEW.ioc='USR';
    END IF;
END; 
// 
DELIMITER ;

