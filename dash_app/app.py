import dash
from dash import Dash, html, dcc, Output, Input
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
        ]
    )

def my_button_navigation():
    """Create navigation buttons for the pages in a single row"""
    return html.Div(
        style={
            "display": "flex",
            "justifyContent": "center", 
            "alignItems": "center",
        },
        children=[
            dcc.Location(id="url", refresh=False),
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        " 🚀  Players Rank",
                        id="players-rank-button",
                        href="/",
                        color="success",
                        #className="me-1",
                        active=True,
                        style={
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "color":"black",
                        },
                    ),
                    dbc.Button(
                        " 📡 Matches",
                        id="matches-button",
                        href="/matches",
                        color="success",
                        active=False,
                        style={
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "color":"black",
                        },
                    ),
                    dbc.Button(
                        " 📈 Profits (Soon)",
                        id="profits-button",
                        href="/matches",
                        color="success",
                        active=False,
                        disabled=True,
                        style={
                            "fontSize": "20px",
                            "fontWeight": "bold",
                            "color":"black",
                        },
                    ),
                ],
                style={"width": "100%",
                       #"height": "5px"
                       }
            )
        ]
    )

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    my_banner(),
    my_button_navigation(),
    dash.page_container  # Placeholder for dynamic page content
])

# Callback to update button styles based on active page
@app.callback(
    [
        Output("players-rank-button", "active"),
        Output("matches-button", "active"),
        Output("profits-button", "active"),
    ],
    Input("url", "pathname"),
)
def update_button_styles(pathname):
    """Makes the button darker when is active by setting active to true"""
    if pathname == "/":
        return True, False, False  
    elif pathname == "/matches":
        return False, True, False  
    else:
        return False, False 
    
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
