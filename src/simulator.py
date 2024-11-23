import pandas as pd
from enum import Enum, auto
from src.strategies import bet_on_smaller_odd

class BetResult(Enum):
    """Result of the bet"""

    WIN = auto()
    LOSE = auto()

def evaluate_bet(winner: str, bet_decision: str) -> BetResult:
    if winner == bet_decision:
        return BetResult.WIN
    else:
        return BetResult.LOSE
    
def settleBet(bet_result: BetResult, bet_amount: float, winner_odd: float) -> float:
    if bet_result == BetResult.WIN:
        return (bet_amount * winner_odd) - bet_amount
    else:
        return - bet_amount
    
def simulate_bets(df, initial_value, bet_amount, strategy=bet_on_smaller_odd):
    results = list()
    running_total = initial_value
    df.loc[:, 'AvgW'] = df['AvgW'].astype(float)
    df.loc[:, 'AvgL'] = df['AvgL'].astype(float)


    for _, match in df.iterrows():
        #print(f"{match["Winner"] = }")
        intersting_columns = [x for x in df.columns if x not in ('ATP', 'Location', 'Tournament','Series', 'Court', 'Surface',
       'Best of', 'WRank', 'LRank', 'WPts', 'LPts',
       'W1', 'L1', 'W2', 'L2', 'W3', 'L3', 'W4', 'L4', 'W5', 'L5', 'Wsets',
       'Lsets', 'Comment', 'B365W', 'B365L', 'PSW', 'PSL', 'MaxW', 'MaxL')]
        match_dict = {col: match[col] for col in intersting_columns}

        # Check if AvgW and AvgL are valid numbers (not None or 0)
        if not match.get("AvgW") or not match.get("AvgL"):
            print(f"Skipping game {match["Winner"]} - {match["Loser"]} due to missing odds (AvgW: {match.get('AvgW')}, AvgL: {match.get('AvgL')})")
            continue

        # Bet Decision (The one I think will win)
        #print(match["Winner"], match["Loser"], match["AvgW"], match["AvgL"])
        #print(type(match["AvgW"]))
        bet_decision = strategy(match["Winner"], match["Loser"], match["AvgW"], match["AvgL"])
        #print(f"{bet_decision = }")
        if not bet_decision:
            #print(f"Skipping for {match_dict}")
            continue


        # Evaluate Bet
        bet_result = evaluate_bet(winner=match["Winner"], bet_decision=bet_decision)
        #print(f"{bet_result = }") 

        # Settling
        netResult = settleBet(bet_result= bet_result, bet_amount= bet_amount, winner_odd= match["AvgW"])
        #print(f"{match["AvgW"] = }")
        #print(f"{match["AvgL"] = }")
        #print(f"{netResult = }")

        # Add new values to the dictionary
        match_dict['bet_decision'] = bet_decision
        match_dict['bet_result'] = bet_result
        match_dict['netResult'] = netResult
        running_total += netResult
        match_dict['running_total'] = running_total

        results.append(match_dict)
        
    return results


def simulate_by_player(df, initial_value, bet_amount, strategy=bet_on_smaller_odd):
    # Get All players
    players = pd.concat([df["Winner"], df["Loser"]]).unique()

    results_summary = []
    for player in players:
        #print(player)
        # Create Player DataFrame
        df_player = df[
            (df["Winner"] == player) | (df["Loser"] == player)
        ]
        
        # Simulates bets
        res = simulate_bets(df_player, initial_value, bet_amount, strategy)
        df_r = pd.DataFrame.from_dict(res)

        # Generate Specific Columns
        fraction_win = round(df_r["bet_result"].value_counts(normalize=True).get(BetResult.WIN, 0) * 100, 2)
        final_amount = round(df_r.iloc[-1]["running_total"], 2)
        net_gain_loss = round(final_amount - initial_value, 3)
        net_gain_loss_percentage = round(net_gain_loss / initial_value * 100, 2)
        
        # Count wins and losses
        num_wins = df_r["bet_result"].value_counts().get(BetResult.WIN, 0)
        num_losses = df_r["bet_result"].value_counts().get(BetResult.LOSE, 0)

        # Count the total number of games played
        num_played_games = len(df_r)

        # Append results to the summary list
        results_summary.append({
            "Player": player,
            "Number of Bet Won": num_wins,
            "Number of Bet Lost": num_losses,
            "Win Percentage (%)": fraction_win,
            "Final Amount ($)": final_amount,
            "Net Gain/Loss ($)": net_gain_loss,
            "Net Gain/Loss Percentage (%)": net_gain_loss_percentage,
            "Number of Played Games": num_played_games
        })
    return pd.DataFrame(results_summary)