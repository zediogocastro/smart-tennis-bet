from typing import Optional

def bet_on_smaller_odd(player_A: str, player_B: str, odd_A: str, odd_B: str) -> Optional[str]:
    if odd_A < odd_B:
        return player_A
    elif odd_A > odd_B:
        return player_B
    else: 
        return None
    
def bet_on_smaller_odd_criteria(player_A: str, player_B: str, odd_A: str, odd_B: str) -> Optional[str]:
    if (odd_A <= 1.2) or (odd_B <= 1.2):
        return None
    if odd_A < odd_B:
        return player_A
    elif odd_A > odd_B:
        return player_B
    else: 
        return None