import math

def distancing_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_position = game.get_player_location(player)
    opponent_position = game.get_player_location(game.get_opponent(player))

    distance_between = math.sqrt(math.pow(player_position[0] - opponent_position[0] , 2) + math.pow( player_position[1] - opponent_position[1], 2))
    num_moves = float(len(game.get_legal_moves(player)))

    return distance_between + num_moves


def open_half_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    half = game.width/2

    if game.get_player_location(player)[0] <= half:
        blank_spaces = sum([x if x <= half else 0 for x in game.get_blank_spaces()[0]])
    else:
        blank_spaces = sum([x if x > half else 0 for x in game.get_blank_spaces()[0]])

    num_moves = float(len(game.get_legal_moves(player)))

    return blank_spaces*num_moves

def getting_closer_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_position = game.get_player_location(player)
    opponent_position = game.get_player_location(game.get_opponent(player))

    distance_between = math.sqrt(math.pow(player_position[0] - opponent_position[0] , 2) + math.pow( player_position[1] - opponent_position[1], 2))
    num_moves = float(len(game.get_legal_moves(player)))

    return  num_moves - distance_between