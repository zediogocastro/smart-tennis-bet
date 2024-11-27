"""
Enriches the data by handling additional extractions and data transformations.
"""

import pandas as pd
from src.utils import extract_atp_players_data


class DataEnricher:
    """class to enrich the database with several external sources"""

    def __init__(self, online):
        self.atp_players_info = self.get_atp_players_data(online)

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
    atp_data = data_enricher.atp_players_info
    
