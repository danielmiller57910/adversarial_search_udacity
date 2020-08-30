
from sample_players import DataPlayer
import random
import pdb
from isolation import DebugState
import time
# https://github.com/alex-modyil/Udacity-AIND/blob/master/3.%20Build%20a%20Game%20Playing%20Agent/my_custom_player.py -> compare

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************

        randomly select a move as player 1 or 2 on an empty board, otherwise
        return the optimal minimax move at a fixed search depth of 3 plies"""
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            optimal_value = float("-inf")
            for action in state.actions():
                candidate = self.min_value(state, 3)
                if candidate > optimal_value:
                    optimal_action = action
            
            self.queue.put(optimal_action)

    def min_value(self, state, depth):
        if state.terminal_test(): return state.utility(self.player_id)
        if depth <= 0: return self.score(state)
        value = float("inf")
        for action in state.actions():
            value = min(value, self.max_value(state.result(action), depth - 1))
        return value

    def max_value(self, state, depth):
        if state.terminal_test(): return state.utility(self.player_id)
        if depth <= 0: return self.score(state)
        value = float("-inf")
        for action in state.actions():
            value = max(value, self.min_value(state.result(action), depth - 1))
        return value
        

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
