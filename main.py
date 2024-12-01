"""Main Module to call the Flask App"""

import pandas as pd
from src.simulator import simulate_by_player
from flask import Flask, request, jsonify
from aux import execute_query_with_params
from sql_queries import (
    AVG_POINTS_BY_PLAYER_QUERY, COUNT_GAMES_PER_TOURNAMENT_QUERY, 
    WINS_PER_SURFACE_QUERY, CURRENT_PRE_MATCH_ATP_RANKINGS_QUERY,
    PLAYER_DETAILS_QUERY, PLAYER_RANKING_HISTORY_QUERY, ALL_MATCHES_QUERY,
    ODDS,
    DATA_TO_SIMULATE
)

app = Flask(__name__)

@app.route('/all_matches', methods=['GET'])
def get_all_matches():
    matches = execute_query_with_params(ALL_MATCHES_QUERY) 
    # Get filtering parameters
    surface = request.args.get('surface')
    court = request.args.get('court')

    # Filter matches in Python
    if surface:
        matches = [match for match in matches if match['surface'] == surface]
    if court:
        matches = [match for match in matches if match['court_type'] == court]

    return jsonify(matches)

@app.route('/avg_points_by_playerzzz', methods=['GET'])
def get_avg_points_by_player():
    print("Here!!!!!!!!!!!!!!!!!!")
    results = execute_query_with_params(AVG_POINTS_BY_PLAYER_QUERY)
    return jsonify(results)

@app.route('/amount_after_simulation', methods=['GET'])
def get_amount_after_simulation():
    # Gather data
    results = execute_query_with_params(DATA_TO_SIMULATE)
    df = pd.DataFrame(results)

    # Simulate bet
    INITIAL_VALUE = 100
    BET_AMOUNT = 10
    res = simulate_by_player(df, INITIAL_VALUE, BET_AMOUNT)
    
    # Format output
    res["amount_rank"] = res["Net Gain/Loss ($)"].rank(method="dense", ascending=False)
    res.sort_values("amount_rank", ascending=True, inplace=True)
    #print(res.head(2))

    # Get Players info
    players_info = execute_query_with_params("SELECT * FROM players")
    df_players_info = pd.DataFrame(players_info)
    #print(df_players_info.columns)

    # Merge players info with the results
    merged_df = res.merge(
        df_players_info,
        how='left',
        left_on='Player',
        right_on='name',
    )
    #print(merged_df.head())

    return jsonify(merged_df.to_dict(orient="records"))

@app.route('/tournament_matches', methods=["GET"])
def get_tournament_matches():
    results = execute_query_with_params(COUNT_GAMES_PER_TOURNAMENT_QUERY)
    return jsonify(results)

@app.route('/wins_per_surface', methods=["GET"])
def get_wins_per_surface():
    results = execute_query_with_params(WINS_PER_SURFACE_QUERY)
    return jsonify(results)

@app.route('/pre_match_atp_rank', methods=["GET"])
def get_pre_match_atp_rank():
    results = execute_query_with_params(CURRENT_PRE_MATCH_ATP_RANKINGS_QUERY)
    return jsonify(results)

@app.route('/player_details_get', methods=['GET'])
def get_player_details():
    player_name = request.args.get('name')  
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    results = execute_query_with_params(PLAYER_DETAILS_QUERY, (player_name,))
    return jsonify(results), 200

@app.route("/historical_player_rank", methods=['GET'])
def get_historical_player_rank():
    player_name = request.args.get('name')
    print(player_name)
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    results = execute_query_with_params(PLAYER_RANKING_HISTORY_QUERY, (player_name,))
    return jsonify(results), 200

@app.route('/historical_odds_matches', methods=['GET'])
def historical_matches():
    player_name = request.args.get('name')
    print(player_name)
    results_q = execute_query_with_params(ODDS, (player_name,))
    print(results_q)

    # Format the data into a list of dictionaries
    """results = []
    for row in results_q:
        results.append({
            "match_id": row[0],
            "match_date": row[1],
            "opponent": row[3],
            "odds": row[4],
            "result": row[2]
        })
    """
    return jsonify(results_q)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
