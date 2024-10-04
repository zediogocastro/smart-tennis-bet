from dash import Dash, html, dcc, dash_table, Output, Input, callback, State
import requests

app = Dash()

app.layout = html.Div(
    [
        html.H1("Tennis Dashboard 🎾", style={'textAlign': 'center'}),
        html.Hr(),
        html.H2("Latest Match Results", style={'textAlign': 'left'}),

        # DataTable to display the matches
        dash_table.DataTable(
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
            style_header={
                'backgroundColor': 'green',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'fontWeight': 'bold'
                } for c in ['winner_player', 'winner_sets', 'loser_sets', 'loser_player']
            ],
            style_table={'overflowX': 'auto'},
            style_data={'textAlign': 'center'},
        ),
        html.Hr(),
    ]
)


# Define a callback to populate the table when the app loads
@app.callback(
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
