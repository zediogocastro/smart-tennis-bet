"""
Exports the data from postgres into a master table.
"""

import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('HOST'),
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
}   

QUERY = """
    WITH set_scores AS (
        SELECT 
            match_id,
            MAX(CASE WHEN set_number = 1 THEN winner_score END) as w1,
            MAX(CASE WHEN set_number = 1 THEN loser_score END) as l1,
            MAX(CASE WHEN set_number = 2 THEN winner_score END) as w2,
            MAX(CASE WHEN set_number = 2 THEN loser_score END) as l2,
            MAX(CASE WHEN set_number = 3 THEN winner_score END) as w3,
            MAX(CASE WHEN set_number = 3 THEN loser_score END) as l3,
            MAX(CASE WHEN set_number = 4 THEN winner_score END) as w4,
            MAX(CASE WHEN set_number = 4 THEN loser_score END) as l4,
            MAX(CASE WHEN set_number = 5 THEN winner_score END) as w5,
            MAX(CASE WHEN set_number = 5 THEN loser_score END) as l5
        FROM match_scores
        GROUP BY match_id
    ),
    bookmaker_odds AS (
        SELECT 
            match_id,
            MAX(CASE WHEN bookmaker = 'Bet365' THEN winner_odds END) as B365W,
            MAX(CASE WHEN bookmaker = 'Bet365' THEN loser_odds END) as B365L,
            MAX(CASE WHEN bookmaker = 'Pinnacle' THEN winner_odds END) as PSW,
            MAX(CASE WHEN bookmaker = 'Pinnacle' THEN loser_odds END) as PSL,
            MAX(CASE WHEN bookmaker = 'Max' THEN winner_odds END) as MaxW,
            MAX(CASE WHEN bookmaker = 'Max' THEN loser_odds END) as MaxL,
            MAX(CASE WHEN bookmaker = 'Avg' THEN winner_odds END) as AvgW,
            MAX(CASE WHEN bookmaker = 'Avg' THEN loser_odds END) as AvgL
        FROM betting_odds
        GROUP BY match_id
    )
    SELECT 
        m.match_id,
        m.date,
        m.best_of,
        t.tournament_ATP AS atp_tournament,
        t.name as tournament,
        t.series as series,
        t.surface,
        t.court,
        m.round,
        w.name as winner,
        l.name as loser,
        m.winner_rank,
        m.loser_rank,
        m.winner_pts,
        m.loser_pts,
        m.winner_sets,
        m.loser_sets,
        s.w1, s.l1,
        s.w2, s.l2,
        s.w3, s.l3,
        s.w4, s.l4,
        s.w5, s.l5,
        bo.B365W, bo.B365L,
        bo.PSW, bo.PSL,
        bo.MaxW, bo.MaxL,
        bo.AvgW, bo.AvgL,
        m.comments
    FROM matches m
    JOIN tournaments t ON m.tournament_id = t.tournament_id
    JOIN players w ON m.winner_id = w.player_id
    JOIN players l ON m.loser_id = l.player_id
    LEFT JOIN set_scores s ON m.match_id = s.match_id
    LEFT JOIN bookmaker_odds bo ON m.match_id = bo.match_id
    ORDER BY m.date DESC;
"""

def create_master_data(output_dir: str = "data/output", query: str = QUERY) -> None:
    """Export the master data from the database into a CSV file."""    
    try:
        # Connect to the database
        with psycopg2.connect(**DB_CONFIG) as conn:
            # Execute query and load ito DataFrame
            df = pd.read_sql(query, conn)

            # Generate output filename with timestamp
            os.makedirs(output_dir, exist_ok=True)
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"matches_export_{timestamp}.csv")

            # Save the data to a CSV file
            df.to_csv(output_file, index=False)
            print(f"Data exported successfully to {output_file}")
            print(f"Total matches exported: {len(df)}")

    except Exception as e:
        print(f"Error exporting data: {str(e)}")

if __name__ == "__main__":
    create_master_data()
