from dash import Dash, html, dcc, dash_table, Output, Input, State
import requests
import plotly.graph_objs as go

app = Dash()

app.layout = html.Div(
    style={'background-color': '#f0f0f0', 'padding': '50px', 'border': 'none'}, 
    children=[
        html.H1("🎾 Smart Tennis Bet 🎾", style={'textAlign': 'center'}),
        html.Hr(),
        html.H2("📡 Latest Match Results", style={'textAlign': 'left'}),

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
            page_size=10,  # Limit the number of rows per page
            page_current=0,  # Track current page
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
        
        # Section for the Player Rank Evolution
        html.H2("📈 Player Rank Evolution", style={'textAlign': 'left'}),
        dcc.Graph(id="rank-evolution-graph"),  # Line plot for ranking evolution
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

# Callback to handle clicks on player names and update the ranking evolution graph
@app.callback(
    Output('rank-evolution-graph', 'figure'),
    Input('match-table', 'active_cell'),  # Detect clicks on table cells
    State('match-table', 'data'),  # Get the table data
    State('match-table', 'page_current'),  # Get the current page of the table
    State('match-table', 'page_size')  # Get the number of rows per page
)
def update_rank_evolution(active_cell, table_data, page_current, page_size):
    if active_cell:
        # Calculate the correct row index across pages
        row_in_current_page = active_cell['row']
        global_row_index = page_current * page_size + row_in_current_page  # Adjust for pagination

        # Get the clicked player name (either from 'winner_player' or 'loser_player')
        col = active_cell['column_id']

        # Only proceed if the clicked column is either winner or loser player
        if col in ['winner_player', 'loser_player']:
            selected_player = table_data[global_row_index][col]  # Use global row index

            # Fetch historical ranking data for the selected player
            response = requests.get(f"http://web:5000/historical_player_rank?name={selected_player}", timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extract ranking_date and rank for the line plot
                ranking_dates = [entry['ranking_date'] for entry in data]
                ranks = [entry['rank'] for entry in data]

                # Create a line plot using Plotly
                figure = go.Figure(
                    data=[go.Scatter(
                        x=ranking_dates, 
                        y=ranks, 
                        mode='lines+markers', 
                        line=dict(color='black'),  # Line color set to black
                        name=f'Ranking of {selected_player}'
                    )],
                    layout=go.Layout(
                        title=f'Ranking Evolution of {selected_player}',
                        xaxis={'title': 'Ranking Date', 'tickangle': -45},  # Rotate x-axis labels for better readability
                        yaxis={
                            'title': 'Rank', 
                            'autorange': 'reversed',  # To show lower ranks (better positions) at the top
                            'tickmode': 'linear',  # Ensure only integers on the y-axis
                            'dtick': 1  # Set tick step to 1 for integers only
                        },
                        plot_bgcolor='rgba(0, 255, 0, 0.1)',  # Light green background with low opacity
                        template='plotly_white'
                    )
                )
                return figure
    # If no player is clicked or selected, return an empty graph
    return go.Figure()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
