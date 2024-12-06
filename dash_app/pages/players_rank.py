import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import requests  # To fetch data from the API

dash.register_page(__name__, path='/')

# Layout
layout = html.Div(
    [
        dcc.Store(id="players-data-store"),  # To store fetched players data
        html.Div(id="players-container"),  # Container for dynamically created player cards
    ],
    style={"padding": "20px"},
)


def create_player_card(player):
    return dbc.Card(
        [
            dbc.CardImg(
                src= player.get("picture_url", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMk7FTSymH9RlilziJurJVXkjxCGaozolJcQ&s"),  # Replace with player's image URL
                top=True,
                style={"height": "330px", "objectFit": "contain", "opacity": 0.99, "borderRadius": "10px"},
            ),
            dbc.CardImgOverlay(    
                dbc.CardBody(
                    [
                       # Position the player ID (top-left corner)
                    html.Div(
                        f"{player.get('amount_rank', 'N/A')}",
                        style={
                            "position": "absolute",
                            "top": "10px",
                            "left": "10px",
                            "color": "black",
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "text-decoration": "underline",
                        }), 

                        # Position the player name (center)
                        html.H4(f"{player.get('name', 'Unknown')}", className="card-title",
                            style={
                            "position": "absolute",
                            "top": "50%",
                            "left": "50%",
                            "transform": "translate(-50%, -50%)",  # Center align
                            "color": "black",
                            "fontSize": "24px",
                            "fontWeight": "bold",
                            "textAlign": "center",
                            "backgroundColor": "rgba(0, 68, 7, 0.7)",
                        }),

                        # Position the country and flag (top-right corner)
                        html.H6(f"{player.get('country', 'Unknown')} {player.get('flag', '')}",
                                style={
                            "position": "absolute",
                            "top": "10px",
                            "right": "10px",
                            "color": "black",
                            "fontSize": "16px",
                            "fontWeight": "bold",
                        }),

                        # Position the stats (bottom-left corner)
                        html.P(f"ATP RANK: {player.get('rank', 'Unknown')}", 
                               style={
                            "position": "absolute",
                            "bottom": "10px",
                            "left": "10px",
                            "color": "black",
                            "fontSize": "14px",
                        }),

                        # Position the rating (bottom-right corner)
                        html.Div(
                            f"Returns: {player.get('Net Gain/Loss Percentage (%)', 'N/A')}% 🤑",
                            style={
                            "position": "absolute",
                            "bottom": "10px",
                            "right": "10px",
                            "color": "green",
                            "fontSize": "14px",
                            "fontWeight": "bold",
                        },
                        ),
                    ]
                ),
            )
        ],
        style={
            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "borderRadius": "10px",
        },
    )

# Callback to fetch data and populate the layout
@dash.callback(
    Output("players-data-store", "data"),
    Input("players-container", "id"),  # Trigger fetching on page load
)
def fetch_players_data(_):
    try:
        response = requests.get("http://web:5000/amount_after_simulation")  # Replace with your API endpoint
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()  # Assuming the API returns a JSON list of players
        return data
    except Exception as e:
        print(f"Error fetching players data: {e}")
        return []
    

@dash.callback(
    Output("players-container", "children"),
    Input("players-data-store", "data"),
)
def populate_players_container(players_data):
    if not players_data:
        return html.Div("No player data available.", style={"textAlign": "center", "marginTop": "50px"})
    return dbc.Row(
        [dbc.Col(create_player_card(player), xs=12, sm=6, md=4, lg=3) for player in players_data],
        className="g-4",  # Gutters between rows and columns
    )
    
