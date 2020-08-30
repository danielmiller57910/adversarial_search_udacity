
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
        current = float("-inf")
        optimal_action = None
        for action in state.actions():
            print(action, state.liberties(action))
        print(DebugState.from_state(state))
        self.queue.put(random.choice(state.actions()))

    
          
    def min_action(self, state, depth):
        # print("MIN ACTION")
        # print([a for a in state.actions()])
        # print(random.choice(state.actions()))
        value = float("inf")
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0:
            return self.score(state)
        for a in state.actions():
            value = min(value, self.max_action(state.result(a), depth-1))
        return value

    def max_action(self, state, depth):
        # print("MAX ACTION")
        # print([a for a in state.actions()])
        # print(random.choice(state.actions()))
        value = float("-inf")
        if state.terminal_test():
            return state.utility(self.player_id)
        if depth <= 0:
            return self.score(state)
        for a in state.actions():
            value = max(value, self.min_action(state.result(a), depth-1))
        return value

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
