USE Tennis;

CREATE FUNCTION aceCount(name, start, finish)
RETURNS DOUBLE

BEGIN 

DECLARE average DOUBLE;

SET average = (SELECT AVG(T2.ace) INTO average
    FROM player AS cp
    JOIN (SELECT pl.player_id, pl.ace 
        FROM plays as pl 
        JOIN (SELECT t.tourney_date, m.match_id 
            FROM tournament AS t 
            JOIN matches AS m ON t.tournament_id=m.tournament_id
            WHERE t.tourney_date > start
                AND t.tourney_date < finish) AS T1 ON pl.match_id=T1.match_id) 
            AS T2 ON cp.player_id=T2.player_id
    WHERE cp.name=name);

RETURN average;

END;


-- combining tournament and matches 
-- SELECT t.tourney_date, m.match_id 
--     FROM tournament AS t 
--     JOIN matches AS m ON t.tournament_id=m.tournament_id
--     WHERE t.tourney_date > 20180000 
--         AND t.tourney_date < 20220000

-- getting match data from certain matches 
-- SELECT pl.player_id, pl.ace 
--     FROM plays AS pl 
--     JOIN (SELECT t.tourney_date, m.match_id 
--         FROM tournament AS t 
--         JOIN matches AS m ON t.tournament_id=m.tournament_id
--         WHERE t.tourney_date > 20180000 
--             AND t.tourney_date < 20220000) AS T1 ON pl.match_id=T1.match_id


SELECT aceCount('Rafael Nadal', 20180000, 20220000);