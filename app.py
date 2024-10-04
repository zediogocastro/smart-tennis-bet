from dash import Dash, html, dcc, dash_table, Output, Input, callback, State
import requests

def determine_surface(grass_clicks, clay_clicks, hard_clicks):
    """Helper function to determine which surface was clicked."""
    if grass_clicks > 0:
        return 'Grass'
    elif clay_clicks > 0:
        return 'Clay'
    elif hard_clicks > 0:
        return 'Hard'
    return None

def determine_court(indoor_clicks, outdoor_clicks):
    """Helper function to determine which court type was clicked."""
    if indoor_clicks > 0:
        return 'Indoor'
    elif outdoor_clicks > 0:
        return 'Outdoor'
    return None


def build_api_url(surface, court=None):
    """Helper function to build the Flask API URL for fetching matches."""
    url = 'http://127.0.0.1:5001/all_matches'
    filters = []
    if surface:
        filters.append(f'surface={surface}')
    if court:
        filters.append(f'court={court}')
    if filters:
        url += '?' + '&'.join(filters)
    return url

app = Dash()

app.layout = html.Div(
    [
        html.H1("Tenis Dashboard 🎾"),
        html.Hr(),

        # Buttons to filter by surface
        html.Div([
            html.Button('Grass', id='grass-btn', n_clicks=0),
            html.Button('Clay', id='clay-btn', n_clicks=0),
            html.Button('Hard', id='hard-btn', n_clicks=0),
            html.Button('Show All Surfaces', id='show-all-btn', n_clicks=0)  # Button to reset surface filters
        ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '50%'}),

        html.Hr(),

        # DataTable to display the matches
        dash_table.DataTable(
            id="match-table",
            columns=[
                {"name": "Match Date", "id": "match_date"},
                {"name": "Surface", "id": "surface"},
                {"name": "Court type", "id": "court_type"},
                {"name": "Tournament", "id": "tournament_name"},
                {"name": "Round", "id": "match_round"},
                {"name": "Winner", "id": "winner_player"},
                {"name": "Winner Sets", "id": "winner_sets"},
                {"name": "Loser Sets", "id": "loser_sets"},
                {"name": "Loser", "id": "loser_player"},
                {"name": "Comments", "id": "comments"},
            ],
            page_size=10,
        ),
    ]
)


# Callback to update the table when the button is clicked
@callback(
    Output(component_id="match-table", component_property="data"),
    Input('grass-btn', 'n_clicks'),
    Input('clay-btn', 'n_clicks'),
    Input('hard-btn', 'n_clicks'),
    Input('show-all-btn', 'n_clicks')
)
def update_table(grass_clicks, clay_clicks, hard_clicks, show_all_surface_clicks):
    # Determine the surface filter
    surface = determine_surface(grass_clicks, clay_clicks, hard_clicks)
    if show_all_surface_clicks > 0:
        surface = None  # Reset surface filter when 'Show All Surfaces' is clicked

    # Build the API URL and fetch the data
    url = build_api_url(surface)
    response = requests.get(url)
    data = response.json()
    
    return data


if __name__ == "__main__":
    app.run(debug=True)
