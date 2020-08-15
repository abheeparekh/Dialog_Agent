#!/usr/bin/env python
# import math
# import numpy as np

# def	create_states(n):
# 	binlist=[]
# 	for i in range(2**n):
# 		temp = bin(i)[2:]
# 		temp_n = n - len(temp)
# 		for i in range(temp_n):
# 			temp='0'+temp
# 		binlist.append(temp)
# 	binlist.append('term')
# 	# print binlist
# 	return binlist
	

# def create_states_from_bin(n):
# 	binlist = create_states(n) 
# 	states= []

# 	for bi in binlist:
# 		if bi !='term':
# 			s=''
# 			for number in range(len(bi)):
# 				if bi[number]=='0':
# 					s+='not'+'s'+str(number)
# 				else:
# 					s+='s'+str(number)
# 				if number != (len(bi)-1):
# 					s+='_'
# 			states.append(s)
# 	states.append('term')
# 	return states

# def get_string_remainder(s,ind):

# 	if ind!= len(s)-1 and ind!=0:
# 		return s[:ind] + s[ind+1:]
# 	elif ind==0:
# 		return s[1:]
# 	elif ind== len(s)-1:
# 		return s[:ind]

# def update_trans_mat(n, trans_mat,action_acc):

# 	for a,action in enumerate(create_actions(n)):
# 		if 'express' in action:
# 			idx= int(action.split('_')[1][1])
# 			for i,init_state in enumerate(create_states(n)[:-1]):

# 				init_remainder=get_string_remainder(init_state,idx)

# 				for e, end_state in enumerate(create_states(n)[:-1]):
	
# 					end_remainder=get_string_remainder(end_state,idx)

					
# 					if idx==0:

# 						if init_state[idx]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=action_acc
# 						elif init_state[idx]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=1- action_acc
# 						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=1.0
# 					else:
# 						if init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=action_acc*0.2
# 						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=action_acc
# 						elif init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=1- action_acc*0.2
# 						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='0' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=1- action_acc
# 						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
# 							trans_mat[a,i,e]=1.0


# 		if 'confirm' in action:
# 			idx= int(action.split('_')[1][1])
# 			for i,init_state in enumerate(create_states(n)):
# 				for e, end_state in enumerate(create_states(n)):
# 					if init_state == end_state:
# 						trans_mat[a,i,e]=1.0

		
# 	trans_mat[:,len(create_states(n))-1,len(create_states(n))-1]=1.0

# 	trans_mat[len(create_actions(n))-1,:,len(create_states(n))-1]=1.0

# 	return trans_mat


# def update_obs_mat(n, obs_mat):
# 	for a,action in enumerate(create_actions(n)):
# 		if 'express' in action:
# 			idx= int(action.split('_')[1][1])
# 			for i,init_state in enumerate(create_states(n)[:-1]):

# 				if init_state[idx]=='0':
# 					obs_mat[a,i,0]=0.1
# 					obs_mat[a,i,1]=0.2
# 					obs_mat[a,i,2]=0.7
# 				elif init_state[idx]=='1':
# 					obs_mat[a,i,0]=0.2
# 					obs_mat[a,i,1]=0.1
# 					obs_mat[a,i,2]=0.7					

# 		if 'confirm' in action:
# 			idx= int(action.split('_')[1][1])
# 			for i,init_state in enumerate(create_states(n)[:-1]):
# 				if init_state[idx]=='0':
# 					obs_mat[a,i,0]=0.1
# 					obs_mat[a,i,1]=0.9
					
# 				elif init_state[idx]=='1':
# 					obs_mat[a,i,0]=0.9
# 					obs_mat[a,i,1]=0.1
						

		
# 	obs_mat[:,len(create_states(n))-1,2]=1.0

# 	obs_mat[len(create_actions(n))-1,:,2]=1.0

# 	return obs_mat

# def create_actions(n):

# 	actions=[]
# 	for action in range(n):
# 		actions.append('express_s'+str(action))
# 	for action in range(n):
# 		actions.append('confirm_s'+str(action))
# 	actions.append('terminate')

# 	return actions

# def write_trans_mat(Tr, s,n):

# 	for a,action in enumerate(create_actions(n)):
# 		s+='\nT: '+action+'\n'
# 		for i,init_state in enumerate(create_states(n)):
# 			for e, end_state in enumerate(create_states(n)):
# 				s+= str(Tr[a,i,e]) +' '
# 			s+='\n'

# 	return s

# def write_reward_mat(s,n,bonus,penalty,exp_cost,conf_cost):

# 	for action in create_actions(n):
# 		if 'express' in action:
# 			for state in create_states_from_bin(n):
# 				if state =='term':
# 					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
# 				else:
# 					s+='\nR:'+action+' : '+state+' : * :* '+ str(exp_cost)
# 		elif 'confirm' in action:
# 			for state in create_states_from_bin(n):
# 				if state =='term':
# 					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
# 				else:
# 					s+='\nR:'+action+' : '+state+' : * :* '+ str(conf_cost)
# 		else:
# 			for state in create_states_from_bin(n):
# 				if state =='term':
# 					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
# 				elif state ==create_states_from_bin(n)[-2]:
# 					s+='\nR:'+action+' : '+state+' : * :* '+ str(bonus)
# 				else:
# 					s+='\nR:'+action+' : '+state+' : * :* '+ str(penalty)

# 	return s


# def write_obs_mat(Ob, s,n):

# 	for a,action in enumerate(create_actions(n)):
# 		s+='\nO: '+action+'\n'
# 		for i,init_state in enumerate(create_states(n)):
# 			for o, obs in enumerate(['pos','neg','na']):
# 				s+= str(Ob[a,i,o]) +' '
# 			s+='\n'

# 	return s

def writeToFile(s,filename):

	f = open(str(filename)+".pomdp",'w')
	f.write(s)	
	f.close()

def generate_states(n):
	states = []
	state_index = {}
	offset=2**n
	for i in range(2**n, 2**(n+1)):
		bitmask = bin(i)[3:]
		state = []
		for j in range(len(bitmask)):
			if bitmask[j] == '1':
				state.append('s' + str(j))
			else:
				state.append('nots' + str(j))
		state_string = '_'.join(state)
		states.append(state_string)
		state_index[state_string] = i-offset
	states.append('term')
	state_index['term'] = i-offset + 1
	return states, state_index

def generate_actions(n):
	actions = []
	for i in range(n):
		actions.append('express_s{0}'.format(i))
		actions.append('confirm_s{0}'.format(i))
		actions.append('behavior_s{0}'.format(i))
	actions.append('terminate')
	return actions
	

def generate_observations():
	observations = []
	observations.append('pos')
	observations.append('neg')
	observations.append('na')
	observations.append('why')
	return observations

def generate_transition_matrix(states, state_index, actions, prerequisite_dict):
	matrices = []
	for action in actions:	
		matrix = transition_matrix_action(states, state_index, action, prerequisite_dict)
		matrices.append(matrix)
	return matrices

def transition_matrix_action(states, state_index, action, prerequisite_dict):
	m = len(states)
	matrix = []
	action_accuracy = 0.9
	if 'confirm' in action:
		row = [0.0 for _ in range(m)] 
		row[0] = 1.0
		for i in range(m):
			matrix.append(row)
			row = [0.0] + row[:-1]
		return matrix
	elif 'express' in action or 'behavior' in action:
		
		action_attribute = action.split('_')[1]
		# iterate over the column by building matrix row by row
		for init in states:
			init_state_attributes = init.split('_')
			row = [0.0]*(len(states))
			prerequisite_fail = False
			
			# check for prerequsites if action is behavior
			if 'behavior' in action:
				if 'not' + prerequisite_dict[action_attribute] in init_state_attributes:
					prerequisite_fail = True
			
			# if the state is not know initially, then after the action make the state know with some probability
			if 'not' + action_attribute in init and not prerequisite_fail:
				row[state_index[init]] = 1-action_accuracy
				final = []
				for st in init_state_attributes:
					if action_attribute in st:
						final.append(action_attribute)
					else:
						final.append(st)
				final_state = '_'.join(final)
				row[state_index[final_state]] = action_accuracy
			else:
				row[state_index[init]] = 1.0

			matrix.append(row)	
		return matrix
	else:
		# terminate
		row = [0.0 for _ in range(m)] 
		row[-1] = 1.0
		return [row]*m
	return 

def generate_observation_matrix(states, actions):
	matrices = []
	for action in actions:	
		matrix = observation_matrix_action(states, action)
		matrices.append(matrix)
	return matrices 

def observation_matrix_action(states, action):
	m = len(states)
	matrix = []
	# pos, neg, na, why
	express_known = [0.2, 0.1, 0.7, 0.0]
	express_unknown = [0.1, 0.2, 0.7, 0.0]
	confirm_known = [0.9, 0.1, 0.0, 0.0]
	confirm_unknown = [0.1, 0.9, 0.0, 0.0]
	behavior_known = [0.7, 0.1, 0.1, 0.1]
	behavior_unknown = [0.1, 0.5, 0.1, 0.3]
	terminate = [0.0, 0.0, 1.0, 0.0]
	if 'terminate' in action:
		return [terminate]*m
	
	action_attribute = action.split('_')[1]
	for state in states:
		if 'not'+action_attribute in state:
			if 'express' in action:
				matrix.append(express_unknown)
			elif 'confirm' in action:
				matrix.append(confirm_unknown)
			elif 'behavior' in action:
				matrix.append(behavior_unknown)
		elif 'term' in state:
			matrix.append(terminate)
		else:
			if 'express' in action:
				matrix.append(express_known)
			elif 'confirm' in action:
				matrix.append(confirm_known)
			elif 'behavior' in action:
				matrix.append(behavior_known)
	return matrix

def generate_reward_matrix(states, actions):
	matrices = []
	for action in actions:	
		matrix = reward_matrix_action(states, action)
		matrices.append(matrix)
	return matrices 

def reward_matrix_action(states, action):
	matrix = []
	communication_cost = -4.0
	terminate_cost = 0.0
	final_reward = 100.0
	behavior_cost_dict = {'s0': -2.0, 's1': -2.0, 's2': -2.0, 's3': -2.0, 's4': -2.0}
	for state in states:
		if 'term' in state:
			row = 'R:{0} : {1} : * :* {2}'.format(action, state, terminate_cost)
		elif 'express' in action or 'confirm' in action:
			row = 'R:{0} : {1} : * :* {2}'.format(action, state, communication_cost)
		elif 'behavior' in action:
			action_attribute = action.split('_')[1]
			row = 'R:{0} : {1} : * :* {2}'.format(action, state, behavior_cost_dict[action_attribute])
		elif 'terminate' in action:
			if 'not' in state:
				row = 'R:{0} : {1} : * :* {2}'.format(action, state, -final_reward)
			else:
				row = 'R:{0} : {1} : * :* {2}'.format(action, state, final_reward)

		matrix.append(row)
	return matrix
		

def print_matrix(matrix):
	# display the matrix on the terminal
	for i in range (len(matrix)):
		for j in range(len(matrix[0])):
			print matrix[i][j],
		print'\n',

def get_matrix_string(matrix):
	# get string representation from a matrix 
	s = ''
	for i in range (len(matrix)):
		for j in range(len(matrix[0])):
			s += str(matrix[i][j]) + ' '
		s += '\n'
	return s

def main():
	n=3
	prerequisite_dict = {'s0': '#', 's1': '#', 's2': 's1', 's3': '#', 's4': '#'}
	s = ''
	s += 'discount : 0.99\n\nvalues: reward\n'

	states, state_index = generate_states(n)
	s	+=  'states: ' +  ' '.join(states) + '\n'
	actions = generate_actions(n)
	s	+=  'actions: ' +  ' '.join(actions) + '\n'
	observations = generate_observations()
	s	+=  'observations: ' +  ' '.join(observations) + '\n'
	s+='\nstart: uniform\n'

	# Transition Matrix
	matrices = generate_transition_matrix(states, state_index, actions, prerequisite_dict)
	for i in range(len(actions)):
		s += '\nT: {0}\n'.format(actions[i])
		matrix_string = get_matrix_string(matrices[i])
		s += matrix_string

	# Observation Matrix
	matrices = generate_observation_matrix(states, actions)
	for i in range(len(actions)):
		s += '\nO: {0}\n'.format(actions[i])
		matrix_string = get_matrix_string(matrices[i])
		s += matrix_string

	# Reward Matrix
	matrices = generate_reward_matrix(states, actions)
	for matrix in matrices:
		for row in matrix:
		# s += '\nO: {0}\n'.format(actions[i])
		# matrix_string = get_matrix_string(matrices[i])
			s += row + '\n'
	
	filename = 'temp'
	writeToFile(s,filename)
	
	# print(s)


	# matrix  = observation_matrix_action(states, 'express_s0')
	# print_matrix(matrix)

	
	# matrix = transition_matrix_action(states, state_index, 'behavior_s2', prerequisite_dict)
	# print_matrix(matrix)
	# for state in create_states_from_bin(n):
	# 	s += state + ' '

	# s+='\nactions:'
	# for action in create_actions(n):
	# 	s+=action + ' '

	# observations=['pos','neg','na']

	# s+='\nobservations: pos neg na'

	# s+='\nstart: uniform\n'

	# trans_mat = np.zeros((len(create_actions(n)),len(create_states_from_bin(n)),len(create_states_from_bin(n))))

	# trans_mat = update_trans_mat(n, trans_mat,0.8)	
	# s= write_trans_mat(trans_mat, s,n)

	# obs_mat = np.zeros((len(create_actions(n)),len(create_states_from_bin(n)),len(observations)))

	# obs_mat = update_obs_mat(n, obs_mat)

	# s= write_obs_mat(obs_mat, s,n)

	# s=write_reward_mat(s,n,100.0,-100.0,-4.0,-2.0)

	# writeToFile(s,n)

if __name__ == '__main__':
	main()