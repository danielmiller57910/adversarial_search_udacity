
from sample_players import DataPlayer


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
        for action in state.actions():
            optimal_value = max(float("-inf"), self.max_action(state.result(action), self.player_id))
            print("OPTIMAL VALUE")
        self.queue.put(optimal_value)

    def min_action(self, state, player_id):
        if state.terminal_test():
            print("TERMINAL TEST MIN", state.utility(player_id))
            return state.utility(player_id)

        for a in state.actions():
            value = min(float("inf"), self.max_action(state.result(a), player_id))
        return value

    def max_action(self, state, player_id):
        if state.terminal_test():
            print("TERMINAL TEST MAX", state.utility(player_id))
            return state.utility(player_id)
        for a in state.actions():
            value = max(float("-inf"), self.min_action(state.result(a), player_id))
        return value
