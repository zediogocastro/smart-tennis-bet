# from dash import Dash, html, dcc, dash_table, Output, Input, State
# import requests
# import plotly.graph_objs as go

# app = Dash(__name__, suppress_callback_exceptions=True)  # Allow callbacks for dynamically generated components

# # Set up layout with navigation buttons and placeholder for page content
# app.layout = html.Div(
#     style={'background-color': '#f0f0f0', 'padding': '50px', 'border': 'none'},
#     children=[
#         # Navigation buttons
#         html.Div([
#             html.Button("Home", id="home-button", n_clicks=0),
#             html.Button("Player", id="player-button", n_clicks=0),
#         ], style={'textAlign': 'center', 'margin-bottom': '20px'}),

#         # Placeholder for page content
#         html.Div(id="page-content")
#     ]
# )


# # Player card page layout for Jannik Sinner
# player_layout = html.Div(
#     children=[
#         html.H1("Player Profile: Jannik Sinner", style={'textAlign': 'center'}),
#         html.Div(
#             style={
#                 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'padding': '20px',
#                 'border': '1px solid #ddd', 'border-radius': '10px', 'backgroundColor': '#fff', 'width': '300px',
#                 'margin': '0 auto'
#             },
#             children=[
#                 html.Img(src="https://www.atptour.com/-/media/alias/player-gladiator-headshot/s0ag",
#                          style={'width': '100%', 'border-radius': '10px'}),
#                 html.H2("Jannik Sinner", style={'margin-top': '10px'}),
#                 html.P("ATP Tour Tennis Player"),
#                 html.P("Country: Italy"),
#                 # Add any other player stats you want here
#             ]
#         ),
#     ]
# )

# # Callback to control page navigation
# @app.callback(
#     Output('page-content', 'children'),
#     [Input('home-button', 'n_clicks'), Input('player-button', 'n_clicks')]
# )
# def display_page(home_clicks, player_clicks):
#     # Check which button was clicked most recently
#     if player_clicks > home_clicks:
#         return player_layout  # Show player card page if "Player" button clicked more times
#     else:
#         return home_layout   # Show home page otherwise



# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")


import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")