"""Main Module to call the Flask App"""

from flask import Flask, request, jsonify
from aux import execute_query_with_params
from sql_queries import (
    AVG_POINTS_BY_PLAYER_QUERY, COUNT_GAMES_PER_TOURNAMENT_QUERY, 
    WINS_PER_SURFACE_QUERY, CURRENT_PRE_MATCH_ATP_RANKINGS_QUERY,
    PLAYER_DETAILS_QUERY, PLAYER_RANKING_HISTORY_QUERY
)

app = Flask(__name__)

@app.route('/avg_points_by_player', methods=['GET'])
def get_avg_points_by_player():
    results = execute_query_with_params(AVG_POINTS_BY_PLAYER_QUERY)
    return jsonify(results)

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


# Experiment with post, it requires body data
@app.route('/player_details', methods=["POST"])
def post_player_details():
    data = request.get_json()
    player_name = data.get('name')

    if not player_name:
        return jsonify({"error": "Player name is required"}), 400

    results = execute_query_with_params(PLAYER_DETAILS_QUERY, (player_name,))
    return jsonify(results)

@app.route("/historical_player_rank", methods=['GET'])
def get_historical_player_rank():
    player_name = request.args.get('name')
    print(player_name)
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    results = execute_query_with_params(PLAYER_RANKING_HISTORY_QUERY, (player_name,))
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)
