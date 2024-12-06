"""Module providig sql queries"""

table_names = (
    "players",
    "player_rankings",  
    "matches",
    "tournaments", 
    "match_scores", 
    "betting_odds"
)

# CREATE TABLES

PLAYERS_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS players (
  player_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);
"""

PLAYER_RANKINGS_TABLE_CREATE= """
CREATE TABLE IF NOT EXISTS player_rankings (
  ranking_id SERIAL PRIMARY KEY,
  player_id INT REFERENCES players(player_id),
  ranking_date DATE NOT NULL,
  rank INT NULL,
  points INT NULL,
  UNIQUE(player_id, ranking_date),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

MATCHES_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS matches (
  match_id SERIAL PRIMARY KEY,
  tournament_id INT REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
  date DATE NOT NULL,
  round VARCHAR(50),
  best_of INT,
  winner_id INT REFERENCES players(player_id) ON DELETE CASCADE,
  loser_id INT REFERENCES players(player_id) ON DELETE CASCADE,
  winner_rank INT NULL,
  loser_rank INT NULL,
  winner_pts INT NULL,
  loser_pts INT NULL,
  winner_sets INT CHECK (winner_sets >= 0 OR winner_sets IS NULL),
  loser_sets INT CHECK (loser_sets >= 0 OR loser_sets IS NULL),
  comments TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (tournament_id, date, round, winner_id, loser_id)
);
"""

TOURNAMENTS_TABLE_CREATE= """
CREATE TABLE IF NOT EXISTS tournaments (
  tournament_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  location VARCHAR(100),
  surface VARCHAR(50),
  series VARCHAR(50),
  court VARCHAR(50)
);
"""

MATCH_SCORES_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS match_scores (
  score_id SERIAL PRIMARY KEY,
  match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
  set_number INT CHECK (set_number > 0),
  winner_score INT,
  loser_score INT
);
"""

BETTING_ODDS_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS betting_odds (
  odds_id SERIAL PRIMARY KEY,
  match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
  bookmaker VARCHAR(50),
  winner_odds DECIMAL(5, 2),
  loser_odds DECIMAL(5, 2),
  UNIQUE (match_id, bookmaker)
);
"""

# INSERT RECORDS
PLAYER_INSERT = """
INSERT INTO players (name)
VALUES (%s)
ON CONFLICT (name) DO NOTHING;
"""

TOURNAMENT_INSERT = """
INSERT INTO tournaments (name, location, surface, series, court)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (name) DO NOTHING;
"""

MATCH_INSERT = """
INSERT INTO matches (
    tournament_id, date, round, best_of, winner_id, loser_id, 
    winner_rank, loser_rank, winner_pts, loser_pts, winner_sets, loser_sets, comments
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (tournament_id, date, round, winner_id, loser_id)  -- Conflict on unique match identifier
DO UPDATE SET
    winner_rank = EXCLUDED.winner_rank,
    loser_rank = EXCLUDED.loser_rank,
    winner_pts = EXCLUDED.winner_pts,
    loser_pts = EXCLUDED.loser_pts,
    winner_sets = EXCLUDED.winner_sets,
    loser_sets = EXCLUDED.loser_sets,
    comments = EXCLUDED.comments,
    updated_at = CURRENT_TIMESTAMP  -- Automatically update the 'updated_at' field on conflict
RETURNING match_id;
"""

PLAYER_RANKING_INSERT = """
INSERT INTO player_rankings (player_id, ranking_date, rank, points)
VALUES (%s, %s, %s, %s)
ON CONFLICT (player_id, ranking_date)
DO UPDATE SET
    rank = EXCLUDED.rank,
    points = EXCLUDED.points;
"""

MATCH_SCORES_INSERT = """
INSERT INTO match_scores (match_id, set_number, winner_score, loser_score)
VALUES (%s, %s, %s, %s)
"""

BETTING_ODDS_INSERT = """
INSERT INTO betting_odds (match_id, bookmaker, winner_odds, loser_odds)
VALUES (%s, %s, %s, %s)
ON CONFLICT (match_id, bookmaker) DO UPDATE SET
    winner_odds = EXCLUDED.winner_odds,
    loser_odds = EXCLUDED.loser_odds;
"""

# QUERY LISTS
CREATE_TABLE_QUERIES = [
    PLAYERS_TABLE_CREATE,
    PLAYER_RANKINGS_TABLE_CREATE,
    TOURNAMENTS_TABLE_CREATE,
    MATCHES_TABLE_CREATE,
    MATCH_SCORES_TABLE_CREATE,
    BETTING_ODDS_TABLE_CREATE
]

DROP_TABLE_QUERIES = [f"DROP TABLE IF EXISTS {table}" for table in table_names]

# Trigger Fuctions on Update
TRIGGER_FUNCTION_CREATE = """
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

TRIGGER_CREATE = """
CREATE TRIGGER trigger_update_timestamp
BEFORE UPDATE ON player_rankings
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
"""

# Analytics Queries
AVG_POINTS_BY_PLAYER_QUERY = """
SELECT p.player_id, p.name, AVG(pr.points) AS avg_points
FROM players p
JOIN player_rankings pr ON p.player_id = pr.player_id
GROUP BY p.player_id, p.name
ORDER BY avg_points DESC;
"""

COUNT_GAMES_PER_TOURNAMENT_QUERY = """
SELECT t.tournament_id, t.name, COUNT(m.match_id) AS total_games
FROM tournaments t
JOIN matches m ON t.tournament_id = m.tournament_id
GROUP BY t.tournament_id, t.name
ORDER BY total_games DESC
LIMIT 10
"""

CURRENT_PRE_MATCH_ATP_RANKINGS_QUERY = """
WITH latest_rankings AS (
    SELECT
        player_id,
        rank,
        points,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY ranking_date DESC) AS rn
    FROM player_rankings
)
SELECT
    p.player_id,
    p.name,
    lr.rank AS current_rank,
    lr.points AS total_points
FROM players p
JOIN latest_rankings lr ON p.player_id = lr.player_id
WHERE lr.rn = 1
ORDER BY current_rank;
"""



WINS_PER_SURFACE_QUERY = """
SELECT 
  p.player_id, 
  p.name, 
  t.surface, 
  COUNT(m.winner_id) AS total_wins
FROM players p
JOIN matches m ON p.player_id = m.winner_id
JOIN tournaments t ON m.tournament_id = t.tournament_id
GROUP BY p.player_id, p.name, t.surface
ORDER BY total_wins DESC
LIMIT 10;
"""

PLAYER_DETAILS_QUERY = """
SELECT *
FROM players p
JOIN player_rankings pr ON p.player_id = pr.player_id
WHERE p.name ILIKE %s
ORDER BY pr.ranking_date DESC
LIMIT 1;
"""

PLAYER_RANKING_HISTORY_QUERY = """
SELECT 
  TO_CHAR(pr.ranking_date, 'DD-MM-YYYY') AS ranking_date,
  pr.rank
FROM players p
JOIN player_rankings pr ON p.player_id = pr.player_id
WHERE p.name = %s
ORDER BY pr.ranking_date ASC;
"""

ALL_MATCHES_QUERY = """
SELECT 
  TO_CHAR(m.date, 'DD-MM-YYYY') AS match_date,
  tr.surface AS surface,
  tr.court AS court_type,
  tr.name AS tournament_name,
  m.round AS match_round,
  p_winner.name AS winner_player,
  m.winner_sets AS winner_sets,
  p_loser.name AS loser_player,
  m.loser_sets AS loser_sets,
  m.comments
FROM matches m
JOIN
  tournaments tr ON m.tournament_id = tr.tournament_id
JOIN
  players p_winner ON m.winner_id = p_winner.player_id
JOIN
  players p_loser ON m.loser_id = p_loser.player_id
ORDER BY m.date DESC
"""

ODDS = """
SELECT 
    m.match_id,
    m.date AS match_date,
    CASE 
        WHEN m.winner_id = p.player_id THEN 'Won'
        ELSE 'Lost'
    END AS result,
    CASE 
        WHEN m.winner_id = p.player_id THEN (SELECT p2.name FROM players p2 WHERE p2.player_id = m.loser_id)
        ELSE (SELECT p2.name FROM players p2 WHERE p2.player_id = m.winner_id)
    END AS opponent,
    bo.winner_odds AS winner_odds,
    bo.loser_odds AS loser_odds
FROM 
    matches m
JOIN 
    players p ON p.player_id = m.winner_id OR p.player_id = m.loser_id
LEFT JOIN 
    betting_odds bo ON bo.match_id = m.match_id
WHERE 
    p.name = (%s);  
"""

DATA_TO_SIMULATE = """
SELECT
    m.*,
    p_winner.name AS "Winner",
    p_loser.name AS "Loser",
    bo.winner_odds AS "AvgW",
    bo.loser_odds AS "AvgL"
FROM
    matches m
JOIN
    players p_winner ON m.winner_id = p_winner.player_id
JOIN
    players p_loser ON m.loser_id = p_loser.player_id
LEFT JOIN
    betting_odds bo ON m.match_id = bo.match_id AND bo.bookmaker = 'Avg'
"""
