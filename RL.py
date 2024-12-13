import random

class AIPrefetcher:
    def __init__(self, state_size=4, action_space=16):
        """Initialize AI-based prefetcher."""
        self.state_size = state_size  # Number of recent addresses to track
        self.action_space = action_space  # Number of possible actions (e.g., offsets)
        self.q_table = {}  # Q-value table for reinforcement learning
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        self.history = []  # Address history for state representation
        self.name = "RL"

    def get_state(self):
        """Get the current state from the history."""
        if len(self.history) < self.state_size:
            return tuple([0] * (self.state_size - len(self.history)) + self.history)
        return tuple(self.history[-self.state_size:])

    def choose_action(self, state):
        """Choose an action using epsilon-greedy policy."""
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space - 1)
        if state not in self.q_table:
            self.q_table[state] = [0] * self.action_space
        return self.q_table[state].index(max(self.q_table[state]))

    def prefetch(self, address):
        """Make a prefetch decision."""
        self.history.append(address)
        state = self.get_state()
        action = self.choose_action(state)
        return [address + action]

    def update_q_value(self, address, reward):
        """Update Q-value based on reward."""
        state = self.get_state()
        action = self.history[-1] - address  # Calculate action as offset
        if state not in self.q_table:
            self.q_table[state] = [0] * self.action_space
        self.q_table[state][action] = (1 - self.alpha) * self.q_table[state][action] + self.alpha * (
            reward + self.gamma * max(self.q_table[state])
        )
