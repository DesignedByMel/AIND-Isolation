"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math
from random import randint

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
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

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # TODO: optimiazation, opening/closing books and symetry
        best_move = (-1,-1)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if self.iterative == True:
                # Fixed search depth on appropriate method

                ply = 1     # Book keeping for the ply

                # While there are moves left
                while game.get_legal_moves() != 0:

                    # Go one ply deeper and save the best move
                    if self.method == 'minimax':
                        _, best_move = self.minimax(game, ply)
                    elif self.method == 'alphabeta':
                        _, best_move = self.minimax(game, ply)

                    ply = ply + 1
            else:
                # Fixed search depth on appropriate method
                if self.method == 'minimax':
                    _, best_move = self.minimax(game,self.search_depth)
                elif self.method == 'alphabeta':
                    _, best_move = self.minimax(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            # If it runs out of time just return the best move.
            return best_move

        # Return the best move from the last completed search iteration
        # this returns a tuple for the location
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        # Raises timeout exception when time is up
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Termination Function, if we are at the depth we wanted we score the "leaf" and go back up the tree
        if depth == 0:
            return self.score(game, self), None

        # Get the legal moves, if none then return (-1,-1)
        next_moves = game.get_legal_moves()
        if len(next_moves) == 0:
            return self.score(game, self), (-1,-1)

        if maximizing_player == True:
            # If a max player, find the max of the score of all legal moves on the next level. Return a tuple of max score and the move that got there
            best_score, best_move = max([(self.minimax( game.forecast_move(potential_move), depth-1, False)[0], potential_move) for potential_move in next_moves])
        else:
            # If a min player, find the min of the score of all legal moves on the next level. Return a tuple of min score and the move that got there
            best_score, best_move = min([(self.minimax( game.forecast_move(potential_move), depth-1, True)[0], potential_move) for potential_move in next_moves])

        return best_score, best_move


    # This will be the same as mini max, but with more terminating conditions, and updating alpha and beta
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        # Raises timeout exception when time is up
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Termination Function, if we are at the depth we wanted we score the "leaf" and go back up the tree
        if depth == 0:
            return self.score(game, self), None

        # Get the legal moves, if none then return (-1,-1)
        next_moves = game.get_legal_moves()
        if len(next_moves) == 0:
            return self.score(game, self), (-1, -1)

        # Found out that this wasn't a good idea in the list comphrension...
        if maximizing_player == True:
            # For a Max Player
            # Initialize the score for the children
            best_score = float("-inf")
            best_move = None

            for potential_move in next_moves:
                # Find the max of the score of all legal moves on the next level, store the score for that state and the move that got to it
                curr_score, curr_move = (self.alphabeta(game.forecast_move(potential_move), depth-1, alpha, beta, False)[0], potential_move)
                best_score, best_move = max((best_score, best_move), (curr_score, curr_move))

                # Prune any branch you can by terminating the DFS
                if best_score >= beta:
                    return best_score, best_move

                # Update the alpha if needed
                alpha = max(alpha, best_score)
        else:
            # For a Min Player
            # Initialize the score for the children
            best_score = float("inf")
            best_move = None

            for potential_move in next_moves:
                # Find the min of the score of all legal moves on the next level, store the score for that state and the move that got to it
                curr_score, curr_move = (self.alphabeta(game.forecast_move(potential_move), depth - 1, alpha, beta, True)[0], potential_move)
                best_score, best_move = min((best_score, best_move), (curr_score, curr_move))

                # Prune any branch you can
                if best_score <= alpha:
                    return best_score, best_move

                # Update the beta if needed
                beta = min(beta, best_score)

        # Return the score and move
        return best_score, best_move