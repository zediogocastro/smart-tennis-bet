import dash
from dash import html, Input, Output, dash_table
import requests

dash.register_page(__name__)

def generate_table():
    return dash_table.DataTable(
            id="match-table",
            columns=[
                {"name": "Match Date", "id": "match_date"},
                {"name": "Winner", "id": "winner_player"},
                {"name": "Winner Sets", "id": "winner_sets"},
                {"name": "Loser Sets", "id": "loser_sets"},
                {"name": "Loser", "id": "loser_player"},
                {"name": "Tournament", "id": "tournament_name"},
                {"name": "Round", "id": "match_round"},
                {"name": "Surface", "id": "surface"},
                {"name": "Court type", "id": "court_type"},
                {"name": "Comments", "id": "comments"},
            ],
            page_size=10,
            page_current=0,
            style_header={'backgroundColor': 'green', 'fontWeight': 'bold', 'textAlign': 'center'},
            style_cell_conditional=[
                {'if': {'column_id': c}, 'fontWeight': 'bold'} for c in ['winner_player', 'winner_sets', 'loser_sets', 'loser_player']
            ],
            style_table={'overflowX': 'auto'},
            style_data={'textAlign': 'center'},
        )

# Define existing callbacks for your home page
@dash.callback(
    Output('match-table', 'data'),
    Input('match-table', 'id')
)
def update_table_on_load(_):
    # Fetch data from the Flask API
    response = requests.get("http://web:5000/all_matches", timeout=10)

    # Check if the response is successful
    if response.status_code == 200:
        matches = response.json()
        return matches
    else:
        return []

layout = html.Div(
    children=[
        html.H1('This is our Matches page!'),
        generate_table(),
    ]
)