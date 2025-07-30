import pytest
import random
from QAgentLib.agent import QLearningAgent
from QAgentLib.environment import SimpleEnv

def test_q_learning_agent_init():
    agent = QLearningAgent(state_space=5, action_space=2)
    assert agent.learning_rate == 0.1
    assert agent.discount_factor == 0.9
    assert agent.exploration_rate == 1.0
    assert len(agent.q_table) == 5
    assert len(agent.q_table[0]) == 2

def test_q_learning_agent_init_dict_space():
    state_space = ['s1', 's2', 's3']
    action_space = ['a1', 'a2']
    agent = QLearningAgent(state_space=state_space, action_space=action_space)
    assert isinstance(agent.q_table, dict)
    assert 's1' in agent.q_table
    assert 'a1' in agent.q_table['s1']
    assert agent.q_table['s1']['a1'] == 0.0

def test_choose_action_explore():
    agent = QLearningAgent(state_space=5, action_space=2, exploration_rate=1.0)
    # With exploration_rate = 1.0, it should always explore (choose random action)
    actions = [agent.choose_action(0) for _ in range(100)]
    # Check that we get at least one of each action (0 and 1) in our samples
    assert 0 in actions and 1 in actions

def test_choose_action_exploit():
    agent = QLearningAgent(state_space=5, action_space=2, exploration_rate=0.0)
    agent.q_table[0][0] = 10 # Make action 0 the best for state 0
    agent.q_table[0][1] = 1
    assert agent.choose_action(0) == 0

def test_learn_ndarray():
    agent = QLearningAgent(state_space=5, action_space=2, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.0)
    initial_q = agent.q_table[0][0]
    agent.learn(0, 0, 1, 1) # state, action, reward, next_state
    # Expected Q-value update: Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s',a')) - Q(s,a))
    # Here, max(Q(s',a')) is max(agent.q_table[1]) which is 0 initially
    expected_q = initial_q + 0.1 * (1 + 0.9 * 0 - initial_q)
    assert agent.q_table[0][0] == pytest.approx(expected_q)

def test_learn_dict():
    state_space = ['s1', 's2']
    action_space = ['a1', 'a2']
    agent = QLearningAgent(state_space=state_space, action_space=action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.0)
    agent.q_table['s1']['a1'] = 0.0
    agent.q_table['s2']['a1'] = 5.0 # Make s2, a1 have a value
    agent.q_table['s2']['a2'] = 10.0 # Make s2, a2 have a higher value

    initial_q = agent.q_table['s1']['a1']
    agent.learn('s1', 'a1', 1, 's2') # state, action, reward, next_state
    # Expected Q-value update: Q(s,a) = Q(s,a) + alpha * (reward + gamma * max(Q(s',a')) - Q(s,a))
    # Here, max(Q(s',a')) is max(agent.q_table['s2'].values()) which is 10.0
    expected_q = initial_q + 0.1 * (1 + 0.9 * 10.0 - initial_q)
    assert agent.q_table['s1']['a1'] == pytest.approx(expected_q)

def test_decay_exploration():
    agent = QLearningAgent(state_space=5, action_space=2, exploration_rate=1.0)
    agent.decay_exploration(0.5)
    assert agent.exploration_rate == 0.5
    agent.decay_exploration(0.5)
    assert agent.exploration_rate == 0.25

def test_simple_env_init():
    env = SimpleEnv()
    assert env.state_space == 5
    assert env.action_space == 2
    assert env.state == 0
    assert env.goal == 4

def test_simple_env_reset():
    env = SimpleEnv()
    env.state = 3
    assert env.reset() == 0

def test_simple_env_step_move_right():
    env = SimpleEnv()
    initial_state = env.state
    next_state, reward, done = env.step(1) # Move right
    assert next_state == initial_state + 1
    assert reward == -1
    assert not done

def test_simple_env_step_move_left():
    env = SimpleEnv()
    env.state = 2
    initial_state = env.state
    next_state, reward, done = env.step(0) # Move left
    assert next_state == initial_state - 1
    assert reward == -1
    assert not done

def test_simple_env_step_reach_goal():
    env = SimpleEnv()
    env.state = 3
    next_state, reward, done = env.step(1) # Move right to goal
    assert next_state == env.goal
    assert reward == 10
    assert done

def test_simple_env_step_invalid_move_left():
    env = SimpleEnv()
    env.state = 0
    next_state, reward, done = env.step(0) # Try to move left from state 0
    assert next_state == 0 # Should not move
    assert reward == -1
    assert not done

def test_simple_env_step_invalid_move_right():
    env = SimpleEnv()
    env.state = env.state_space - 1 # At max state
    next_state, reward, done = env.step(1) # Try to move right from max state
    assert next_state == env.state_space - 1 # Should not move
    assert reward == -1
    assert not done