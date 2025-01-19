"""
Module providing an ETL process for tenis data
"""

import pandas as pd
import psycopg2
from psycopg2.extensions import cursor
from db_values import HOST, DBNAME, USER, PASSWORD
from aux import convert_nan_to_none
from sql_queries import (
    PLAYER_INSERT, TOURNAMENT_INSERT, MATCH_INSERT, 
    PLAYER_RANKING_INSERT, MATCH_SCORES_INSERT, BETTING_ODDS_INSERT)

def extract_data_from_excel(url: str) -> pd.DataFrame:
    """Extract data from an Excel file at the given URL and return a pandas DataFrame"""
    return pd.read_excel(url)

def validate_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate that essential columns ('Winner' and 'Loser') are not missing.
    Returns a cleaned DataFrame with only valid rows.
    """
    initial_row_count = len(df)
    df_cleaned = df.dropna(subset=['Winner', 'Loser'])
    final_row_count = len(df_cleaned)
    
    rows_removed = initial_row_count - final_row_count
    if rows_removed > 0:
        print(f"Removed {rows_removed} rows due to missing 'Winner' or 'Loser'.")
    
    return df_cleaned

def insert_players(df: pd.DataFrame, cur: cursor) -> None:
    """Insert players from the DataFrame into the database."""
    players = pd.concat([df['Winner'], df['Loser']]).unique()
    for player in players:
        cur.execute(PLAYER_INSERT, (player,))

def insert_tournaments(df: pd.DataFrame, cur: cursor) -> None:
    """Insert unique tournaments from the DataFrame into the database."""
    tournaments = df[["ATP", "Tournament","Location", "Surface", "Series", "Court"]].drop_duplicates()
    for _, row in tournaments.iterrows():
        cur.execute(TOURNAMENT_INSERT, (row["ATP"], row["Tournament"], row["Location"], row["Surface"], row["Series"], row["Court"]))

def insert_match_scores(match_id: int, row: pd.Series, cur: cursor) -> None:
    """Insert match scores for each set into the database."""
    for set_number in range(1, 6):  # 5 possible sets
        winner_score = row.get(f'W{set_number}')
        loser_score = row.get(f'L{set_number}')
        if pd.notna(winner_score) and pd.notna(loser_score):
            cur.execute(MATCH_SCORES_INSERT, (match_id, set_number, winner_score, loser_score))

def insert_betting_odds(match_id: int, row: pd.Series, cur: cursor) -> None:
    """Insert betting odds for each bookmaker into the database."""
    bookmakers = {
        "Bet365": (row['B365W'], row['B365L']),
        "Pinnacle": (row['PSW'], row['PSL']),
        "Max": (row['MaxW'], row['MaxL']),
        "Avg": (row['AvgW'], row['AvgL'])
    }
    for bookmaker, odds in bookmakers.items():
        winner_odds, loser_odds = odds
        cur.execute(BETTING_ODDS_INSERT, (match_id, bookmaker, winner_odds, loser_odds))

def insert_player_rankings(winner_id: int, loser_id: int, row: pd.Series, cur: cursor) -> None:
    """Insert player rankings for both winner and loser into the database."""
    cur.execute(PLAYER_RANKING_INSERT, (winner_id, row['Date'], convert_nan_to_none(row['WRank']), convert_nan_to_none(row['WPts'])))
    cur.execute(PLAYER_RANKING_INSERT, (loser_id, row['Date'], convert_nan_to_none(row['LRank']), convert_nan_to_none(row['LPts'])))


def transform_and_insert_data(df: pd.DataFrame, cur: cursor) -> None:
    """Transform raw tennis data and insert it into the database."""
    # Insert players and tournaments first
    insert_players(df, cur)
    insert_tournaments(df, cur)

    # Process each match in the DataFrame
    for _, row in df.iterrows():
        # Get player IDs for winner and loser
        cur.execute("SELECT player_id FROM players WHERE name = %s", (row['Winner'],))
        winner_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM players WHERE name = %s", (row['Loser'],))
        loser_id = cur.fetchone()[0]

        # Get tournament ID
        cur.execute("SELECT tournament_id FROM tournaments WHERE name = %s", (row['Tournament'],))
        tournament_id = cur.fetchone()[0]

        # Insert match data
        match_data = (
            tournament_id, 
            row['Date'], 
            row['Round'], 
            row['Best of'],
            winner_id, 
            loser_id, 
            convert_nan_to_none(row['WRank']), 
            convert_nan_to_none(row['LRank']), 
            convert_nan_to_none(row['WPts']), 
            convert_nan_to_none(row['LPts']), 
            convert_nan_to_none(row['Wsets']), 
            convert_nan_to_none(row['Lsets']), 
            row['Comment']
        )
        #print(match_data)
            
        cur.execute(MATCH_INSERT, match_data)
        match_id = cur.fetchone()[0]  # Get the match_id of the inserted match

        # Insert match scores, betting odds, and player rankings
        insert_match_scores(match_id, row, cur)
        insert_betting_odds(match_id, row, cur)
        insert_player_rankings(winner_id, loser_id, row, cur)

def load_data_to_db(url: str) -> None:
    """Extract, transform, and load data from the given URL into the database."""
    df = extract_data_from_excel(url)
    with psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            # Pre-process and clean the DataFrame
            df_cleaned = validate_and_clean_data(df)
            # Process the DataFrame
            transform_and_insert_data(df_cleaned, cur)
    print("Data inserted!")

def main():
    """Main ETL process entry point."""
    URL = "http://tennis-data.co.uk/2024/20234.xlsx"
    load_data_to_db(URL)

if __name__ == "__main__":
    main()
