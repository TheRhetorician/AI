from itertools import combinations

def take_action(num_soldiers_west, num_soldiers_east, direction, action, stack):
	'''
	Appends the action to stack, modifies state
	'''

	if direction == 0:  # west-east
		stack.append(action)
		num_soldiers_west[action[0]] -= 1
		if num_soldiers_west[action[0]] == 0:
			del(num_soldiers_west[action[0]])

		num_soldiers_west[action[1]] -= 1
		if num_soldiers_west[action[1]] == 0:
			del(num_soldiers_west[action[1]])

		num_soldiers_east[action[0]] = num_soldiers_east.get(action[0], 0)+1
		num_soldiers_east[action[1]] = num_soldiers_east.get(action[1], 0)+1

	elif direction == 1:  # east-west
		stack.append(action)
		num_soldiers_east[action[0]] -= 1
		if num_soldiers_east[action[0]] == 0:
			del(num_soldiers_east[action[0]])

		num_soldiers_west[action[0]] = num_soldiers_west.get(action[0], 0)+1

	return None


def dfs(num_soldiers_west, num_soldiers_east, direction, stack, parent_action):
	if len(num_soldiers_west) == 0:  # All soldiers transferred
		return True, parent_action+1

	if direction == 0:  # west-east
		if len(num_soldiers_west.keys()) < 2:  # No solution
			if stack:
				stack.pop()
			# Returns no solution, action that should be taken
			return False, parent_action+1

		action_num = 0
		solved = False
		while not solved:
			# Not storing, generating everytime
			actions = list(combinations(num_soldiers_west.keys(), 2))
			len_actions = len(actions)
			copy_num_soldiers_west = num_soldiers_west.copy()
			copy_num_soldiers_east = num_soldiers_east.copy()
			take_action(copy_num_soldiers_west, copy_num_soldiers_east,
						direction, actions[action_num], stack)
			actions.clear()  # Memory cleared
			solved, action_num = dfs(
				copy_num_soldiers_west, copy_num_soldiers_east, 1, stack, action_num)
			if not solved and action_num >= len_actions:  # No solution
				if stack:
					stack.pop()
				break

		return solved, parent_action+1

	if direction == 1:  # east-west
		action_num = 0
		solved = False
		while not solved:
			# Not storing, generating everytime
			actions = list(combinations(num_soldiers_east.keys(), 1))
			len_actions = len(actions)
			copy_num_soldiers_west = num_soldiers_west.copy()
			copy_num_soldiers_east = num_soldiers_east.copy()
			take_action(copy_num_soldiers_west, copy_num_soldiers_east,
						direction, actions[action_num], stack)
			actions.clear()  # Memory cleared
			solved, action_num = dfs(
				copy_num_soldiers_west, copy_num_soldiers_east, 0, stack, action_num)
			if not solved and action_num >= len_actions:  # No solution
				if stack:
					stack.pop()
				break

		return solved, parent_action+1


# if __name__ == '__main__':
def cal(n,num_west):
	# flag = True if input('Do you want custom input?[y/n]: ') == 'y' else False
	# if flag:
	# 	num_colours = int(input('Enter the number of colours(>1): '))
	# 	num_soldiers_west = {}
	# 	for i in range(num_colours):
	# 		colour = input('Enter colour name: ')
	# 		num_soldiers_west[colour] = int(
	# 			input('Enter the number of soldiers of that colour: '))
	# else:
	# 	num_soldiers_west = {'blue': 3, 'green': 3, 'red': 3}
	num_soldiers_west = num_west
	print(num_west)
	print(num_soldiers_west)
	num_soldiers_east = {}
	stack = []

	solved, _ = dfs(num_soldiers_west, num_soldiers_east, 0, stack, 0)

	if solved:
		print(stack)

	else:
		print('Not solved')
	return stack
	# print(list(combinations(num_soldiers_west.keys(), 2)))
