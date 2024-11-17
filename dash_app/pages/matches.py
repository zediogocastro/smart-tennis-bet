# import dash
# from dash import html, dcc, dash_table, Dash, Output, Input, State
# import requests
# import plotly.graph_objs as go

# app = Dash(__name__, suppress_callback_exceptions=True)  # Allow callbacks for dynamically generated components

# dash.register_page(__name__)

# # Home page layout (your existing app content)
# layout = html.Div(
#     children=[
#         html.H1("🎾 Smart Tennis Bet 🎾", style={'textAlign': 'center'}),
#         html.Hr(),
#         html.H2("📡 Latest Match Results", style={'textAlign': 'left'}),

#         # DataTable to display the matches
#         dash_table.DataTable(
#             id="match-table",
#             columns=[
#                 {"name": "Match Date", "id": "match_date"},
#                 {"name": "Winner", "id": "winner_player"},
#                 {"name": "Winner Sets", "id": "winner_sets"},
#                 {"name": "Loser Sets", "id": "loser_sets"},
#                 {"name": "Loser", "id": "loser_player"},
#                 {"name": "Tournament", "id": "tournament_name"},
#                 {"name": "Round", "id": "match_round"},
#                 {"name": "Surface", "id": "surface"},
#                 {"name": "Court type", "id": "court_type"},
#                 {"name": "Comments", "id": "comments"},
#             ],
#             page_size=10,
#             page_current=0,
#             style_header={'backgroundColor': 'green', 'fontWeight': 'bold', 'textAlign': 'center'},
#             style_cell_conditional=[
#                 {'if': {'column_id': c}, 'fontWeight': 'bold'} for c in ['winner_player', 'winner_sets', 'loser_sets', 'loser_player']
#             ],
#             style_table={'overflowX': 'auto'},
#             style_data={'textAlign': 'center'},
#         ),
#         html.Hr(),

#         # Section for the Player Rank Evolution
#         html.H2("📈 Player Rank Evolution", style={'textAlign': 'left'}),
#         dcc.Graph(id="rank-evolution-graph"),
#     ]
# )

# # Define existing callbacks for your home page
# @app.callback(
#     Output('match-table', 'data'),
#     Input('match-table', 'id')
# )
# def update_table_on_load(_):
#     # Fetch data from the Flask API
#     response = requests.get("http://web:5000/all_matches", timeout=10)

#     # Check if the response is successful
#     if response.status_code == 200:
#         matches = response.json()
#         return matches
#     else:
#         return []

# @app.callback(
#     Output('rank-evolution-graph', 'figure'),
#     Input('match-table', 'active_cell'),
#     State('match-table', 'data'),
#     State('match-table', 'page_current'),
#     State('match-table', 'page_size')
# )
# def update_rank_evolution(active_cell, table_data, page_current, page_size):
#     if active_cell:
#         row_in_current_page = active_cell['row']
#         global_row_index = page_current * page_size + row_in_current_page
#         col = active_cell['column_id']

#         if col in ['winner_player', 'loser_player']:
#             selected_player = table_data[global_row_index][col]
#             response = requests.get(f"http://web:5000/historical_player_rank?name={selected_player}", timeout=10)

#             if response.status_code == 200:
#                 data = response.json()
#                 ranking_dates = [entry['ranking_date'] for entry in data]
#                 ranks = [entry['rank'] for entry in data]

#                 figure = go.Figure(
#                     data=[go.Scatter(x=ranking_dates, y=ranks, mode='lines+markers', line=dict(color='black'))],
#                     layout=go.Layout(
#                         title=f'Ranking Evolution of {selected_player}',
#                         xaxis={'title': 'Ranking Date', 'tickangle': -45},
#                         yaxis={'title': 'Rank', 'autorange': 'reversed', 'tickmode': 'linear', 'dtick': 1},
#                         plot_bgcolor='rgba(0, 255, 0, 0.1)',
#                         template='plotly_white'
#                     )
#                 )
#                 return figure
#     return go.Figure()

import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our Matches page'),
])