from typing import List, Union, Optional


def find_player(players: List[str], name: str) -> Optional[str]:
    """
    Searches for a player by name in the given list of players.
    
    Args:
        players (List[str]): A list of player names.
        name (str): The name of the player to search for.
    
    Returns:
        Optional[str]: The name of the player if found, otherwise None.
    """  
    return name if name in players else None


def calculate_average_score(scores: List[Union[int, float]]) -> float:
    """
    Calculates the average score from a list of scores.
    
    Args:
        scores (List[Union[int, float]]): A list of scores from players.
    
    Returns:
        float: The average score, or 0.0 if no scores are provided.
    """  
    return sum(scores) / len(scores) if scores else 0.0


def is_player_active(active_players: List[str], name: str) -> bool:
    """
    Checks if a player is currently active.
    
    Args:
        active_players (List[str]): A list of currently active player names.
        name (str): The name of the player to check.
    
    Returns:
        bool: True if the player is active, otherwise False.
    """  
    return name in active_players


def get_player_statistics(player: str, stats: dict) -> dict:
    """
    Retrieves statistics for a specific player.
    
    Args:
        player (str): The name of the player.
        stats (dict): A dictionary containing player statistics.
    
    Returns:
        dict: A dictionary containing the player's statistics or an empty dict if not found.
    """  
    return stats.get(player, {})