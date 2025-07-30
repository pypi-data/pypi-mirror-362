class SimpleEnv:
    """
    A simple environment with linear state space and two actions.
    
    This environment has 5 states (0-4) and 2 actions (left and right).
    The goal is to reach state 4 from the starting state 0.
    
    Attributes:
        state_space (int): Number of possible states (5).
        action_space (int): Number of possible actions (2).
        state (int): Current state of the agent.
        goal (int): Goal state (4).
    """
    def __init__(self):
        self.state_space = 5  # 5 possible states
        self.action_space = 2  # 2 actions: 0 (left), 1 (right)
        self.state = 0  # Start at state 0
        self.goal = 4   # Goal is state 4

    def reset(self):
        """
        Reset the environment to the initial state.
        
        Returns:
            int: The initial state.
        """
        self.state = 0
        return self.state

    def step(self, action):
        """
        Take a step in the environment based on the given action.
        
        Args:
            action (int): The action to take (0 for left, 1 for right).
            
        Returns:
            tuple: (next_state, reward, done) tuple.
        """
        # Track if the move was valid
        valid_move = False
        
        # Store the previous state to check if we moved
        prev_state = self.state
        
        # Action 0: move left, Action 1: move right
        if action == 0 and self.state > 0:
            self.state -= 1
            valid_move = True
        elif action == 1 and self.state < self.state_space - 1:
            self.state += 1
            valid_move = True

        # Reward: +10 for reaching the goal with a valid move, -1 otherwise
        reward = 10 if self.state == self.goal and valid_move else -1
        
        # Only consider the episode done if we reached the goal with a valid move
        # For invalid moves at the goal state, we're not done
        done = self.state == self.goal and valid_move
        
        return self.state, reward, done


class GridWorldEnv:
    """
    A 2D grid world environment for reinforcement learning.
    
    This environment represents a grid world where an agent can move in four directions.
    The grid may contain obstacles, rewards, and penalties.
    
    Args:
        width (int): Width of the grid.
        height (int): Height of the grid.
        start_pos (tuple): Starting position (x, y).
        goal_pos (tuple): Goal position (x, y).
        obstacles (list): List of obstacle positions [(x1, y1), (x2, y2), ...].
        reward_pos (dict): Dictionary mapping positions to rewards {(x, y): reward_value}.
        max_steps (int): Maximum number of steps before episode termination.
        
    Attributes:
        width (int): Width of the grid.
        height (int): Height of the grid.
        state (tuple): Current position (x, y).
        start_pos (tuple): Starting position (x, y).
        goal_pos (tuple): Goal position (x, y).
        obstacles (list): List of obstacle positions.
        reward_pos (dict): Dictionary mapping positions to rewards.
        action_space (int): Number of possible actions (4).
        state_space (int): Total number of possible states (width * height).
        steps (int): Current step count in the episode.
        max_steps (int): Maximum number of steps before episode termination.
    """
    
    def __init__(self, width=5, height=5, start_pos=(0, 0), goal_pos=(4, 4), 
                 obstacles=None, reward_pos=None, max_steps=100):
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacles = obstacles or []
        self.reward_pos = reward_pos or {goal_pos: 10}
        self.state = start_pos
        self.action_space = 4  # 0: up, 1: right, 2: down, 3: left
        self.state_space = width * height
        self.steps = 0
        self.max_steps = max_steps
        
    def reset(self):
        """
        Reset the environment to the initial state.
        
        Returns:
            tuple: The initial state (x, y).
        """
        self.state = self.start_pos
        self.steps = 0
        return self.state
    
    def step(self, action):
        """
        Take a step in the environment based on the given action.
        
        Args:
            action (int): The action to take (0: up, 1: right, 2: down, 3: left).
            
        Returns:
            tuple: (next_state, reward, done, info) tuple.
        """
        self.steps += 1
        x, y = self.state
        valid_move = True
        
        # Calculate new position based on action
        if action == 0:  # up
            new_pos = (x, max(0, y - 1))
        elif action == 1:  # right
            new_pos = (min(self.width - 1, x + 1), y)
        elif action == 2:  # down
            new_pos = (x, min(self.height - 1, y + 1))
        elif action == 3:  # left
            new_pos = (max(0, x - 1), y)
        else:
            raise ValueError(f"Invalid action: {action}")
        
        # Check if the move is valid (not into an obstacle)
        if new_pos in self.obstacles:
            new_pos = self.state  # Stay in the same position
            valid_move = False
        
        # Update state
        self.state = new_pos
        
        # Calculate reward
        reward = self.reward_pos.get(new_pos, -1)  # Default reward is -1
        
        # Check if done
        done = (new_pos == self.goal_pos and valid_move) or self.steps >= self.max_steps
        
        # Additional info
        info = {
            "steps": self.steps,
            "valid_move": valid_move,
            "max_steps_reached": self.steps >= self.max_steps
        }
        
        return self.state, reward, done, info
    
    def render(self):
        """
        Render the grid world as a string representation.
        
        Returns:
            str: String representation of the grid world.
        """
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Mark obstacles
        for x, y in self.obstacles:
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = '#'
        
        # Mark goal
        x, y = self.goal_pos
        if 0 <= x < self.width and 0 <= y < self.height:
            grid[y][x] = 'G'
        
        # Mark agent position
        x, y = self.state
        if 0 <= x < self.width and 0 <= y < self.height:
            grid[y][x] = 'A'
        
        # Convert grid to string
        return '\n'.join([''.join(row) for row in grid])


class MultiObjectiveEnv:
    """
    An environment with multiple competing objectives for the agent to balance.
    
    This environment simulates scenarios where the agent must balance multiple
    objectives, such as maximizing performance while minimizing resource usage.
    
    Args:
        num_objectives (int): Number of objectives to balance.
        state_space_size (int): Size of the state space.
        action_space_size (int): Size of the action space.
        objective_weights (list): Weights for each objective in the reward calculation.
        max_steps (int): Maximum number of steps before episode termination.
        
    Attributes:
        num_objectives (int): Number of objectives to balance.
        state_space (int): Size of the state space.
        action_space (int): Size of the action space.
        state (int): Current state.
        objective_values (list): Current values for each objective.
        objective_weights (list): Weights for each objective in the reward calculation.
        steps (int): Current step count in the episode.
        max_steps (int): Maximum number of steps before episode termination.
    """
    
    def __init__(self, num_objectives=3, state_space_size=10, action_space_size=4, 
                 objective_weights=None, max_steps=100):
        self.num_objectives = num_objectives
        self.state_space = state_space_size
        self.action_space = action_space_size
        self.state = 0
        self.objective_values = [0] * num_objectives
        self.objective_weights = objective_weights or [1.0 / num_objectives] * num_objectives
        self.steps = 0
        self.max_steps = max_steps
        
    def reset(self):
        """
        Reset the environment to the initial state.
        
        Returns:
            tuple: The initial state and objective values.
        """
        self.state = 0
        self.objective_values = [0] * self.num_objectives
        self.steps = 0
        return (self.state, self.objective_values)
    
    def step(self, action):
        """
        Take a step in the environment based on the given action.
        
        Args:
            action (int): The action to take.
            
        Returns:
            tuple: (next_state, reward, done, info) tuple.
        """
        self.steps += 1
        
        # Update state based on action
        self.state = (self.state + action) % self.state_space
        
        # Update objective values based on action and state
        for i in range(self.num_objectives):
            # Different objectives respond differently to actions
            if i == 0:  # First objective (e.g., performance)
                self.objective_values[i] += (action + 1) * 0.1
            elif i == 1:  # Second objective (e.g., resource usage - lower is better)
                self.objective_values[i] += action * 0.2
            else:  # Other objectives
                self.objective_values[i] += (action % (i + 1)) * 0.15
        
        # Calculate weighted reward
        reward = 0
        for i in range(self.num_objectives):
            # For some objectives, lower values are better
            if i == 1:  # Resource usage - lower is better
                reward -= self.objective_values[i] * self.objective_weights[i]
            else:  # Higher values are better
                reward += self.objective_values[i] * self.objective_weights[i]
        
        # Check if done
        done = self.steps >= self.max_steps
        
        # Additional info
        info = {
            "steps": self.steps,
            "objective_values": self.objective_values,
            "max_steps_reached": done
        }
        
        return (self.state, self.objective_values), reward, done, info