import random
import math

class QLearningAgent:
    """
    A Q-learning agent for reinforcement learning.

    This class implements a Q-learning algorithm to train an agent in a given environment.
    It maintains a Q-table to store action values and supports exploration-exploitation trade-off.

    Args:
        state_space (int or list): Number of possible states or list of possible states in the environment.
        action_space (int or list): Number of possible actions or list of possible actions in the environment.
        learning_rate (float, optional): Learning rate for Q-value updates. Defaults to 0.1.
        discount_factor (float, optional): Discount factor for future rewards. Defaults to 0.9.
        exploration_rate (float, optional): Initial rate for exploration. Defaults to 1.0.

    Attributes:
        q_table (dict or ndarray): Q-value table for state-action pairs.
        learning_rate (float): Learning rate for updates.
        discount_factor (float): Discount factor for future rewards.
        exploration_rate (float): Current exploration rate.
        action_space (int or list): Number or list of possible actions.
    """

    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.action_space = action_space
        
        # Handle different types of state_space and action_space
        if isinstance(state_space, int) and isinstance(action_space, int):
            # Original behavior for integer inputs
            # Create a 2D list instead of numpy array
            self.q_table = [[0.0 for _ in range(action_space)] for _ in range(state_space)]
        else:
            # Dictionary-based Q-table for non-integer state/action spaces
            self.q_table = {}
            self.state_space = state_space
            
            # Initialize Q-table with zeros
            if isinstance(state_space, list):
                for state in state_space:
                    self.q_table[state] = {}
                    for action in action_space:
                        self.q_table[state][action] = 0.0

    def _ensure_state_exists(self, state):
        """
        Ensure that a state exists in the Q-table.
        
        Args:
            state: The state to check/add.
        """
        if isinstance(self.q_table, dict) and state not in self.q_table:
            self.q_table[state] = {}
            for action in self.action_space:
                self.q_table[state][action] = 0.0

    def choose_action(self, state, explore=True):
        """
        Choose an action based on the current state using epsilon-greedy policy.

        Args:
            state (int or any): Current state index or state representation.
            explore (bool, optional): Whether to use exploration or not. Defaults to True.

        Returns:
            int or any: Selected action index or action representation.
        """
        # Check if we're using the dictionary-based Q-table
        if isinstance(self.q_table, dict):
            # Initialize state if not in Q-table
            self._ensure_state_exists(state)
                    
            if explore and random.random() < self.exploration_rate:
                return random.choice(self.action_space)  # Explore
            else:
                # Find action with maximum Q-value
                return max(self.q_table[state].items(), key=lambda x: x[1])[0]  # Exploit
        else:
            # Original behavior for list-based Q-table
            if explore and random.random() < self.exploration_rate:
                return random.randint(0, len(self.action_space)-1) if isinstance(self.action_space, list) else random.randint(0, self.action_space-1)  # Explore
            # Find index of max value in the row
            return self.q_table[state].index(max(self.q_table[state]))  # Exploit

    def learn(self, state, action, reward, next_state):
        """
        Update the Q-table based on the Q-learning update rule.

        Args:
            state (int or any): Current state index or state representation.
            action (int or any): Action taken in current state.
            reward (float): Reward received after taking the action.
            next_state (int or any): Next state index or state representation.
        """
        # Check if we're using the dictionary-based Q-table
        if isinstance(self.q_table, dict):
            # Initialize states if not in Q-table
            self._ensure_state_exists(state)
            self._ensure_state_exists(next_state)
            
            # Get the current Q-value
            current_q = self.q_table[state][action]
            
            # Find the maximum Q-value for the next state
            best_next_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
            
            # Calculate the new Q-value
            new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_next_q - current_q)
            
            # Update the Q-table
            self.q_table[state][action] = new_q
        else:
            # Original behavior for list-based Q-table
            current_q = self.q_table[state][action]
            best_next_q = max(self.q_table[next_state])
            new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_next_q - current_q)
            self.q_table[state][action] = new_q

    def decay_exploration(self, decay_rate=0.99):
        """
        Decay the exploration rate to gradually shift from exploration to exploitation.

        Args:
            decay_rate (float, optional): Rate at which to decay exploration. Defaults to 0.99.
        """
        self.exploration_rate *= decay_rate


class TargetedQLearningAgent(QLearningAgent):
    """
    A specialized Q-learning agent with targeted features for specific domains.
    
    This agent extends the base QLearningAgent with additional capabilities:
    - Prioritized experience replay
    - Dynamic learning rate adjustment
    - State importance weighting
    - Performance metrics tracking
    
    Args:
        state_space (int or list): Number of possible states or list of possible states in the environment.
        action_space (int or list): Number of possible actions or list of possible actions in the environment.
        learning_rate (float, optional): Learning rate for Q-value updates. Defaults to 0.1.
        discount_factor (float, optional): Discount factor for future rewards. Defaults to 0.9.
        exploration_rate (float, optional): Initial rate for exploration. Defaults to 1.0.
        target_domain (str, optional): Specific domain this agent is targeting. Defaults to "general".
        min_learning_rate (float, optional): Minimum learning rate after decay. Defaults to 0.01.
    
    Attributes:
        experience_buffer (list): Buffer to store past experiences for replay.
        state_visit_counts (dict): Tracks how often each state has been visited.
        performance_history (list): Tracks rewards over time for performance analysis.
        target_domain (str): The specific domain this agent is targeting.
    """
    
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, 
                 exploration_rate=1.0, target_domain="general", min_learning_rate=0.01):
        super().__init__(state_space, action_space, learning_rate, discount_factor, exploration_rate)
        self.experience_buffer = []
        self.state_visit_counts = {}
        self.performance_history = []
        self.target_domain = target_domain
        self.min_learning_rate = min_learning_rate
        
    def track_state(self, state):
        """
        Track state visits for importance weighting.
        
        Args:
            state: The state being visited.
        """
        if isinstance(self.state_visit_counts, dict):
            if state not in self.state_visit_counts:
                self.state_visit_counts[state] = 0
            self.state_visit_counts[state] += 1
    
    def add_experience(self, state, action, reward, next_state, done):
        """
        Add an experience to the replay buffer.
        
        Args:
            state: Current state.
            action: Action taken.
            reward: Reward received.
            next_state: Next state.
            done: Whether the episode is done.
        """
        self.experience_buffer.append((state, action, reward, next_state, done))
        # Limit buffer size to prevent memory issues
        if len(self.experience_buffer) > 1000:
            self.experience_buffer.pop(0)
    
    def replay_experience(self, batch_size=10):
        """
        Learn from past experiences using prioritized replay.
        
        Args:
            batch_size (int): Number of experiences to replay.
        """
        if len(self.experience_buffer) < batch_size:
            return
            
        # Select random batch of experiences
        batch = random.sample(self.experience_buffer, batch_size)
        
        for state, action, reward, next_state, done in batch:
            # Apply importance weighting based on state visit frequency
            importance = 1.0
            if state in self.state_visit_counts and self.state_visit_counts[state] > 0:
                importance = 1.0 / math.sqrt(self.state_visit_counts[state])
                
            # Adjust learning rate based on importance
            effective_lr = max(self.min_learning_rate, self.learning_rate * importance)
            
            # Store original learning rate
            original_lr = self.learning_rate
            
            # Temporarily set adjusted learning rate
            self.learning_rate = effective_lr
            
            # Learn from this experience
            self.learn(state, action, reward, next_state)
            
            # Restore original learning rate
            self.learning_rate = original_lr
    
    def choose_action(self, state, explore=True):
        """
        Choose action with domain-specific adjustments.
        
        Args:
            state: Current state.
            explore (bool): Whether to use exploration.
            
        Returns:
            The chosen action.
        """
        # Track state visit for importance calculations
        self.track_state(state)
        
        # Use parent class implementation
        return super().choose_action(state, explore)
    
    def learn(self, state, action, reward, next_state):
        """
        Enhanced learning with performance tracking.
        
        Args:
            state: Current state.
            action: Action taken.
            reward: Reward received.
            next_state: Next state.
        """
        # Track performance
        self.performance_history.append(reward)
        
        # Add to experience buffer
        self.add_experience(state, action, reward, next_state, False)
        
        # Use parent class implementation for basic learning
        super().learn(state, action, reward, next_state)
        
    def get_performance_metrics(self):
        """
        Calculate performance metrics based on reward history.
        
        Returns:
            dict: Dictionary containing performance metrics.
        """
        if not self.performance_history:
            return {"avg_reward": 0, "max_reward": 0, "min_reward": 0, "total_reward": 0}
            
        return {
            "avg_reward": sum(self.performance_history) / len(self.performance_history),
            "max_reward": max(self.performance_history),
            "min_reward": min(self.performance_history),
            "total_reward": sum(self.performance_history),
            "episodes": len(self.performance_history)
        }
        
    def adaptive_learning_rate(self, performance_threshold=0.7):
        """
        Adjust learning rate based on recent performance.
        
        Args:
            performance_threshold (float): Threshold to determine adjustment.
            
        Returns:
            float: The new learning rate.
        """
        if len(self.performance_history) < 10:
            return self.learning_rate
            
        # Calculate recent performance trend
        recent_rewards = self.performance_history[-10:]
        avg_recent_reward = sum(recent_rewards) / len(recent_rewards)
        
        # If recent performance is good, reduce learning rate to fine-tune
        if avg_recent_reward > performance_threshold:
            self.learning_rate = max(self.min_learning_rate, self.learning_rate * 0.95)
        # If recent performance is poor, increase learning rate to explore more
        else:
            self.learning_rate = min(1.0, self.learning_rate * 1.05)
            
        return self.learning_rate