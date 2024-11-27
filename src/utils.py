"""
Utilities related to the project. 
"""

from typing import Union
import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import URL_ATP



def build_atp_url(top_x: int) -> str:
    """
    Build a dynamic ATP rankings URL.

    Args:
        top_x (int): Number of top players to include in the rankings.

    Returns:
        str: The complete URL.
    """
    return URL_ATP + f"?rankRange=0-{top_x}"


def request_data(URL: str) -> Union[BeautifulSoup, None]:
    """Send an HTTP request to the URL"""
    response = requests.get(URL, headers={"User-Agent": ""})
    if response.status_code != 200:
        raise Exception(f"Failed to load page {URL}: {response.status_code}")

    return BeautifulSoup(response.content, "html.parser")


def preprocessing_players_data(soup: BeautifulSoup):
    # Initialize a list to store player data
    players_data = []

    # Iterate over all rows with class 'lower-row'
    for row in soup.find_all("tr"):
        # Extract the rank
        rank_cell = row.find("td", class_="rank bold heavy tiny-cell")
        rank = rank_cell.text.strip() if rank_cell else None

        # Extract the player name
        name_li = row.find("li", class_="name center")
        name = name_li.find("span").text.strip() if name_li else None

        # Extract the nationality
        flag_svg = row.find("svg", class_="atp-flag")
        if flag_svg and flag_svg.find("use"):
            flag_code = (
                flag_svg.find("use")["href"].split("#")[-1].split("-")[-1].lower()
            )
            nationality = flag_code.upper()  # Map this to a country name if needed
        else:
            nationality = None

        # Extract the ATP code from the player's link
        player_link = (
            name_li.find("a")["href"] if name_li and name_li.find("a") else None
        )
        atp_code = player_link.split("/")[-2] if player_link else None

        # Extract the age
        age_cell = row.find("td", class_="age small-cell")
        age = age_cell.text.strip() if age_cell else None

        # Extract the points and remove commas before converting to an integer
        points_cell = row.find("td", class_="points center bold extrabold small-cell")
        points = points_cell.text.strip() if points_cell else None
        if points:
            points = points.replace(",", "")  # Remove commas
            points = int(points)

        # Append player data to the list
        if rank and name and age and points:
            players_data.append(
                {
                    "rank": int(rank),
                    "name": name,
                    "age": int(age),
                    "points": points,
                    "nationality": nationality,
                    "atp_code": atp_code,
                }
            )

    # Convert the list of players to a Pandas DataFrame
    return pd.DataFrame(players_data)


def extract_atp_players_data(top_players: int = 500):
    """This function wescrapes the ATP rank website, process the relevant information and retrieve a panda Dataframe"""
    URL = build_atp_url(top_players)
    soup = request_data(URL)
    players_df = preprocessing_players_data(soup)
    return players_df
