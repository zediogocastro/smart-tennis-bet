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
import dash_bootstrap_components as dbc

def banner():
    """Build the banner at the top of the page."""
    return html.Div(
        id="banner",
        style={
            "backgroundColor": "#f4f4f4",
            "padding": "10px",
            "textAlign": "left",
            "position": "fixed",
            "top": "0",
            "width": "100%",
            "zIndex": "1000",
            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
        },
        children=[
            html.H1(
                "Smart Tennis Bet 🎾",
                style={"margin": "0", "fontSize": "24px"}
            ),
            html.H5(
                "Navigate through the pages using the buttons below!",
                style={"margin": "0", "color": "gray", "fontSize": "16px"}
            )
        ]
    )

def my_banner():
    """My personal header at the top of the page"""
    return html.Div(style={
                'display': 'flex',
                'justify-content': 'space-between',
                'align-items': 'center',
                'padding': '20px'
        }, children=[
            html.H1(" 🎾 Smart Tennis Bet"),
            html.H6("Legal")
        ])

def button_navigation():
    """Create navigation buttons for Matches and Players Rank in a single row."""
    return html.Div(
        style={
            #"paddingTop": "80px",  # Space for the fixed header
            "display": "flex",
            "justifyContent": "space-between",  # Spread buttons across the row
            "alignItems": "center",  # Center vertically
            "width": "100%",
            #"gap": "10px",  # Space between buttons
            #"boxSizing": "border-box",  # Ensure padding doesn't affect width
        },
        children=[
            dcc.Location(id="url", refresh=False),  # URL manager
            dbc.Button(
                " 📡 Matches",
                id="matches-button",
                href="/",
                color="primary",
                outline=False,
                style={
                    "flex": "1",  # Equal width for all buttons
                #     "height": "60px",
                #     "fontSize": "20px",
                #     "fontWeight": "bold",
                #     "textAlign": "center",
                #     "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
                },
            ),
            dbc.Button(
                "🚀 Players Rank",
                id="players-rank-button",
                href="/players-rank",
                color="primary",
                outline=False,
                style={
                    "flex": "1",  # Equal width for all buttons
                #     "height": "60px",
                #     "fontSize": "20px",
                #     "fontWeight": "bold",
                #     "textAlign": "center",
                #     "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
                },
            )
        ]
    )

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    my_banner(),
    button_navigation(),
    dash.page_container  # Placeholder for dynamic page content
])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


