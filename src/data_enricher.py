"""
Enriches the data by handling additional extractions and data transformations.
"""

import pandas as pd
import psycopg2
from db_values import HOST, DBNAME, USER, PASSWORD
from src.utils import extract_atp_players_data, append_player_info


class DataEnricher:
    """class to enrich the database with several external sources"""

    def __init__(self, online):
        self.atp_players_info = self.get_atp_players_data(online)

    def enrich_data(self):
        """INSERT external data into the main database.
        """
        with psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD) as conn:
            with conn.cursor() as cur:
                append_player_info(self.atp_players_info, cur)

    def get_atp_players_data(self, online: bool = False) -> pd.DataFrame:
        """Loads data either offline using cached dataframe or webscrapping offical ATP Ranking

        Returns:
            pd.Dataframe: A dataframe containing relevant ATP players information, i.e., rank, Nationality, image link, and others.

        """
        if not online:
            df = pd.read_csv("/workspaces/smart-tennis-bet/data/players_data.csv")
        else:
            df = extract_atp_players_data()

        return df

if __name__ == "__main__":
    data_enricher = DataEnricher(online=False)
    data_enricher.enrich_data()
    
