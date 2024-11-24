import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path='/')

# Sample data for players
players = [
    {
        "id": 1,
        "name": "Player 1",
        "country": "USA",
        "flag": "🇺🇸",
        "stats": "50 Wins / 10 Losses",
        "rating": "⭐⭐⭐⭐⭐",
    },
    {
        "id": 2,
        "name": "Player 2",
        "country": "Japan",
        "flag": "🇯🇵",
        "stats": "40 Wins / 20 Losses",
        "rating": "⭐⭐⭐⭐",
    },
    {
        "id": 3,
        "name": "Player 3",
        "country": "France",
        "flag": "🇫🇷",
        "stats": "60 Wins / 5 Losses",
        "rating": "⭐⭐⭐⭐⭐",
    },
    {
        "id": 4,
        "name": "Player 4",
        "country": "Germany",
        "flag": "🇩🇪",
        "stats": "30 Wins / 15 Losses",
        "rating": "⭐⭐⭐",
    },
    {
        "id": 5,
        "name": "Player 5",
        "country": "Germany",
        "flag": "🇩🇪",
        "stats": "30 Wins / 15 Losses",
        "rating": "⭐⭐⭐",
    },
]



def create_player_card(player):
    return dbc.Card(
        [
            dbc.CardImg(
                src="https://upload.wikimedia.org/wikipedia/commons/7/77/Jannik_Sinner_%282024_US_Open%29_04.jpg",  # Replace with player's image URL
                top=True,
                style={"height": "330px", "objectFit": "cover", "opacity": 0.8, "borderRadius": "10px"},
            ),
            dbc.CardImgOverlay(    
                dbc.CardBody(
                    [
                       # Position the player ID (top-left corner)
                    html.Div(
                        f"{player['id']}",
                        style={
                            "position": "absolute",
                            "top": "10px",
                            "left": "10px",
                            "color": "white",
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "text-decoration": "underline",
                        }), 

                        # Position the player name (center)
                        html.H4(f"{player['name']}", className="card-title",
                            style={
                            "position": "absolute",
                            "top": "50%",
                            "left": "50%",
                            "transform": "translate(-50%, -50%)",  # Center align
                            "color": "white",
                            "fontSize": "24px",
                            "fontWeight": "bold",
                            "textAlign": "center",
                        }),

                        # Position the country and flag (top-right corner)
                        html.H6(f"{player['flag']} {player['country']}",
                                style={
                            "position": "absolute",
                            "top": "10px",
                            "right": "10px",
                            "color": "white",
                            "fontSize": "16px",
                            "fontWeight": "bold",
                        }),

                        # Position the stats (bottom-left corner)
                        html.P(player["stats"], 
                               style={
                            "position": "absolute",
                            "bottom": "10px",
                            "left": "10px",
                            "color": "white",
                            "fontSize": "14px",
                        }),

                        # Position the rating (bottom-right corner)
                        html.Div(
                            f"Rating: {player['rating']}",
                            style={
                            "position": "absolute",
                            "bottom": "10px",
                            "right": "10px",
                            "color": "#FFD700",
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
            "borderRadius": "100px",
        },
    )



layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(create_player_card(player), xs=12, sm=6, md=4, lg=3)
                for player in players
            ],
            className="g-4",  # Gutters between rows and columns
        )
    ],
    style={"padding": "20px"},
)
