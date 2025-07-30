import pytest
import random
from QAgentLib.agent import TargetedQLearningAgent
from QAgentLib.environment import GridWorldEnv, MultiObjectiveEnv

def test_targeted_agent_init():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    assert agent.learning_rate == 0.1
    assert agent.discount_factor == 0.9
    assert agent.exploration_rate == 1.0
    assert agent.target_domain == "general"
    assert agent.min_learning_rate == 0.01
    assert isinstance(agent.experience_buffer, list)
    assert isinstance(agent.state_visit_counts, dict)
    assert isinstance(agent.performance_history, list)

def test_track_state():
    agent = TargetedQLearningAgent(state_space=['s1', 's2'], action_space=['a1', 'a2'])
    agent.track_state('s1')
    assert agent.state_visit_counts['s1'] == 1
    agent.track_state('s1')
    assert agent.state_visit_counts['s1'] == 2
    assert 's2' not in agent.state_visit_counts

def test_add_experience():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    agent.add_experience(0, 1, 1.0, 1, False)
    assert len(agent.experience_buffer) == 1
    assert agent.experience_buffer[0] == (0, 1, 1.0, 1, False)

def test_replay_experience():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    # Add some experiences
    for _ in range(20):
        agent.add_experience(0, 1, 1.0, 1, False)
    
    # Track initial Q-value
    initial_q = agent.q_table[0][1]
    
    # Replay experiences
    agent.replay_experience(batch_size=10)
    
    # Q-value should have changed after replay
    assert agent.q_table[0][1] != initial_q

def test_targeted_choose_action():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    state = 0
    action = agent.choose_action(state)
    assert state in agent.state_visit_counts
    assert action in [0, 1]

def test_targeted_learn():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    agent.learn(0, 1, 1.0, 1)
    assert len(agent.performance_history) == 1
    assert agent.performance_history[0] == 1.0
    assert len(agent.experience_buffer) == 1

def test_get_performance_metrics():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    # Add some rewards to history
    rewards = [-1, 0, 1, 2, 3]
    for r in rewards:
        agent.performance_history.append(r)
    
    metrics = agent.get_performance_metrics()
    assert metrics['avg_reward'] == sum(rewards) / len(rewards)
    assert metrics['max_reward'] == max(rewards)
    assert metrics['min_reward'] == min(rewards)
    assert metrics['total_reward'] == sum(rewards)
    assert metrics['episodes'] == len(rewards)

def test_adaptive_learning_rate():
    agent = TargetedQLearningAgent(state_space=5, action_space=2)
    initial_lr = agent.learning_rate
    
    # Add good performance history
    for _ in range(10):
        agent.performance_history.append(1.0)
    
    new_lr = agent.adaptive_learning_rate(performance_threshold=0.7)
    assert new_lr < initial_lr  # Should decrease for good performance

    # Add poor performance history
    agent.performance_history.clear()
    for _ in range(10):
        agent.performance_history.append(0.0)
    
    new_lr = agent.adaptive_learning_rate(performance_threshold=0.7)
    assert new_lr > agent.min_learning_rate  # Should increase for poor performance

def test_gridworld_env():
    env = GridWorldEnv(width=3, height=3, start_pos=(0,0), goal_pos=(2,2),
                      obstacles=[(1,1)], reward_pos={(2,2): 10})
    
    # Test initialization
    assert env.width == 3
    assert env.height == 3
    assert env.state == (0,0)
    
    # Test reset
    env.state = (1,1)
    assert env.reset() == (0,0)
    
    # Test valid move
    state, reward, done, info = env.step(1)  # Move right
    assert state == (1,0)
    assert reward == -1
    assert not done
    assert info['valid_move']
    
    # Test obstacle collision
    env.state = (0,1)
    state, reward, done, info = env.step(1)  # Try to move into obstacle
    assert state == (0,1)  # Should stay in place
    assert not info['valid_move']

def test_multiobjective_env():
    env = MultiObjectiveEnv(num_objectives=2, state_space_size=5, action_space_size=3)
    
    # Test initialization
    assert env.num_objectives == 2
    assert env.state_space == 5
    assert env.action_space == 3
    
    # Test reset
    initial_state = env.reset()
    assert initial_state == (0, [0, 0])
    
    # Test step
    state, reward, done, info = env.step(1)
    assert isinstance(state, tuple)
    assert len(state[1]) == 2  # Two objective values
    assert isinstance(reward, (int, float))
    assert isinstance(done, bool)
    assert 'objective_values' in info