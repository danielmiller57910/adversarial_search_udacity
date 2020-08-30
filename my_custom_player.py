
from sample_players import DataPlayer
import random
import pdb
from isolation import DebugState
import time
MAXIMIZER = True
ALPHA_DEFAULT=float("-inf")
BETA_DEFAULT=float("+inf")

class CustomPlayer(DataPlayer):

    def get_action(self, state):
        alpha_value = ALPHA_DEFAULT
        if state.ply_count < 2:
            # random state required due to large depth of tree at initial state
            self.queue.put(random.choice(state.actions()))
        else:
            optimal_action = None
            optimal_value = float("-inf")
            for action in state.actions():
                candidate = self.min_value(state.result(action), 4, MAXIMIZER, alpha_value, BETA_DEFAULT)
                if candidate > optimal_value:
                    optimal_action = action
                alpha_value = max(alpha_value, candidate)
            if optimal_action:
                self.queue.put(optimal_action)
            else:
                self.queue.put(random.choice(state.actions()))

    def min_value(self, state, depth, is_alpha, alpha_value, beta_value):
        if state.terminal_test(): 
            return state.utility(self.player_id)

        if depth <= 0: 
            return self.score(state)

        value = float("inf")
        for action in state.actions():
            value = min(value, self.max_value(state.result(action), depth - 1, not is_alpha, alpha_value, beta_value))
            if value <= alpha_value:
                return value
            beta_value = min(beta_value, value)
     
        return value

    def max_value(self, state, depth, is_alpha, alpha_value, beta_value):
        if state.terminal_test(): 
            return state.utility(self.player_id)

        if depth <= 0: 
            return self.score(state)

        value = float("-inf")
        for action in state.actions():
            value = max(value, self.min_value(state.result(action), depth - 1, not is_alpha, alpha_value, beta_value))
            if value >= beta_value:
                return value
            alpha_value = max(alpha_value, value)
         
        return value
        

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - (len(opp_liberties) * 4)
