### MDP Value Iteration and Policy Iteratoin
# You might not need to use all parameters

import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

def policy_evaluation(P, nS, nA, policy, gamma=0.9, max_iteration=1000, tol=1e-3):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	policy: np.array
		The policy to evaluate. Maps states to actions.
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returns
	-------
	value function: np.ndarray
		The value function from the given policy.
	"""
	############################
	# YOUR IMPLEMENTATION HERE #
	############################
	V = np.zeros(nS)

	for i in range(max_iteration):
		delta = 0
		for s in range(nS):
			v = 0
			a = policy[s]
			for p, next_s, r, term in P[s][a]:
				v += p * (r + gamma * V[next_s])
			delta = max(delta, np.abs(v - V[s]))
			V[s] = v

		print("Value delta: %.3f" % delta)
		if delta < tol:
			break

	return V

def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new policy: np.ndarray
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""
	############################
	# YOUR IMPLEMENTATION HERE #
	############################
	new_policy = np.zeros(nS, dtype='int')

	for s in range(nS):
		v_values = np.zeros(nA)
		for a in range(nA):
			for p, next_s, r, term in P[s][a]:
				v_values[a] =  p * (r + gamma * value_from_policy[next_s])
		new_policy[s] = np.argmax(v_values)

	return new_policy

def policy_iteration(P, nS, nA, gamma=0.9, max_iteration=20, tol=1e-3):
	"""Runs policy iteration.

	You should use the policy_evaluation and policy_improvement methods to
	implement this method.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returns:
	----------
	value function: np.ndarray
	policy: np.ndarray
	"""
	V = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	############################
	# YOUR IMPLEMENTATION HERE #
	############################
	for i in range(max_iteration):
		old_policy = np.copy(policy)

		V = policy_evaluation(P, nS, nA, policy, gamma, max_iteration, tol)
		policy = policy_improvement(P, nS, nA, V, policy, gamma)

		delta = np.linalg.norm(policy, ord=1) - np.linalg.norm(old_policy, ord=1)   # L1-norm
		print("Policy delta: %.3f" % delta)
		if (delta < tol):
			print("Policy has converged after %d iterations!" % (i+1))
			break

	return V, policy

def value_iteration(P, nS, nA, gamma=0.9, max_iteration=20, tol=1e-3):
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returns:
	----------
	value function: np.ndarray
	policy: np.ndarray
	"""
	V = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	############################
	# YOUR IMPLEMENTATION HERE #
	############################
	for i in range(max_iteration):
		delta = 0
		for s in range(nS):
			v = 0
			v_values = np.zeros(nA)
			for a in range(nA):                     # The max to be taken over all possible actions.
				for p, next_s, r, term in P[s][a]:
					v = p * (r + gamma * V[next_s])
				v_values[a] = v
			v = np.max(v_values)                    # The max v-value of the state.
			policy[s] = np.argmax(v_values)         # Identical to policy improvement.
			delta = max(delta, np.abs(v - V[s]))
			V[s] = v

		print("Value iteration delta: %.3f" % delta)
		if delta < tol:
			print("Policy has converged after %d iterations!" % (i+1))
			break

	return V, policy

def example(env):
	"""Show an example of gym
	Parameters
		----------
		env: gym.core.Environment
			Environment to play on. Must have nS, nA, and P as
			attributes.
	"""
	env.seed(0);
	from gym.spaces import prng; prng.seed(10) # for print the location
	# Generate the episode
	ob = env.reset()
	for t in range(100):
		env.render()
		a = env.action_space.sample()
		ob, rew, done, _ = env.step(a)
		if done:
			break
	assert done
	env.render();

def render_single(env, policy):
	"""Renders policy once on environment. Watch your agent play!

		Parameters
		----------
		env: gym.core.Environment
			Environment to play on. Must have nS, nA, and P as
			attributes.
		Policy: np.array of shape [env.nS]
			The action to take at a given state
	"""

	episode_reward = 0
	ob = env.reset()
	for t in range(100):
		env.render()
		time.sleep(0.5) # Seconds between frames. Modify as you wish.
		a = policy[ob]
		ob, rew, done, _ = env.step(a)
		episode_reward += rew
		if done:
			break
	assert done
	env.render();
	print "Episode reward: %f" % episode_reward


# Feel free to run your own debug code in main!
# Play around with these hyperparameters.
if __name__ == "__main__":
	env = gym.make("Deterministic-4x4-FrozenLake-v0")
	print env.__doc__
	print "Here is an example of state, action, reward, and next state"
	example(env)
	t1 = time.time()
	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration=20, tol=1e-3)
	t2 = time.time()
	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration=20, tol=1e-3)
	t3 = time.time()
	render_single(env, p_pi)
	render_single(env, p_vi)
	print("Value Iteration took %fs" % (t2-t1))
	print("Policy Iteration took %fs" % (t3-t2))
