-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also
-- 'create view' statements if you choose to use it.
--
-- You can write comments in this file by starting them with
-- two dashes, like these lines here.

-- If 'tournament' database exists, delete the database.
DROP DATABASE IF EXISTS tournament;

-- Create a database named 'tournament'.
CREATE DATABASE tournament;

-- Connect to tournament.
\c tournament;

-- If 'players' table exists, delete the table.
DROP TABLE IF EXISTS players CASCADE;

-- Create 'players' table with 'player_id' as a serial primary key &
-- 'player_name' as a text field.
CREATE TABLE players(
	player_id serial PRIMARY KEY UNIQUE,
	player_name text NOT NULL);

-- If 'matches' table exists, delete the table.
DROP TABLE IF EXISTS matches CASCADE;

-- Create 'matches' table with 'match_id' as a serial primary key &
-- 'winner_id' and 'loser_id' as integer fields 
-- referencing 'players.player_id'.
CREATE TABLE matches(
	match_id serial PRIMARY KEY UNIQUE,
	winner_id integer REFERENCES players (player_id) ON DELETE CASCADE,
	loser_id integer REFERENCES players (player_id) ON DELETE CASCADE);

-- Get players with their total wins
CREATE VIEW wins AS 
	SELECT p.player_id, COUNT(m.match_id) AS wins 
	FROM players AS p join matches AS m
	ON p.player_id = m.winner_id
	GROUP BY p.player_id;

-- Get players with their total matches
CREATE VIEW total_matches AS
	SELECT p.player_id, COUNT(m.match_id) AS total_matches
	FROM matches AS m join players AS p
	ON p.player_id = m.winner_id OR p.player_id = m.loser_id 
	GROUP BY p.player_id;

-- Get opponent players
CREATE VIEW opponent_player AS 
	SELECT * FROM (SELECT player_id, loser_id AS opponent
	FROM players
	LEFT JOIN matches ON (matches.winner_id = players.player_id)
    UNION
	SELECT player_id, winner_id AS opponent
	FROM players
	LEFT JOIN matches ON (matches.loser_id = players.player_id )
    ORDER BY player_id) AS subq WHERE opponent IS NOT NULL;
	
-- Get opponents' total wins
CREATE VIEW op_wins AS 
    SELECT op.player_id, SUM(COALESCE(wins,0)) AS op_wins 
    FROM opponent_player op
    LEFT JOIN wins w ON opponent = w.player_id 
    GROUP BY op.player_id;

-- Get players sorted by wins and in case of equal wins,
-- sorted by opponents' wins.
CREATE VIEW standings AS 
    SELECT 
	players.player_id AS id,
	players.player_name AS name,
	COALESCE(w.wins,0) AS wins,
    COALESCE(omw.op_wins,0) AS omw,
	COALESCE(tm.total_matches,0) AS matches
    FROM players 
	LEFT JOIN wins w ON players.player_id = w.player_id
	LEFT JOIN total_matches tm ON players.player_id = tm.player_id
    LEFT JOIN op_wins omw ON players.player_id = omw.player_id
	GROUP BY players.player_id, wins, omw, matches ORDER BY wins DESC, omw DESC;
