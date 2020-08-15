#!/usr/bin/env python
import math
import numpy as np

def	create_states(n):
	binlist=[]
	for i in range(2**n):
		temp = bin(i)[2:]
		temp_n = n - len(temp)
		for i in range(temp_n):
			temp='0'+temp
		binlist.append(temp)
	binlist.append('term')
	# print binlist
	return binlist
	

def create_states_from_bin(n):
	binlist = create_states(n) 
	states= []

	for bi in binlist:
		if bi !='term':
			s=''
			for number in range(len(bi)):
				if bi[number]=='0':
					s+='not'+'s'+str(number)
				else:
					s+='s'+str(number)
				if number != (len(bi)-1):
					s+='_'
			states.append(s)
	states.append('term')
	return states

def get_string_remainder(s,ind):

	if ind!= len(s)-1 and ind!=0:
		return s[:ind] + s[ind+1:]
	elif ind==0:
		return s[1:]
	elif ind== len(s)-1:
		return s[:ind]

def update_trans_mat(n, trans_mat,action_acc):

	for a,action in enumerate(create_actions(n)):
		if 'express' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):

				init_remainder=get_string_remainder(init_state,idx)

				for e, end_state in enumerate(create_states(n)[:-1]):
	
					end_remainder=get_string_remainder(end_state,idx)

					
					if idx==0:

						if init_state[idx]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc
						elif init_state[idx]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc
						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1.0
					else:
						if init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc*0.2
						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc
						elif init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc*0.2
						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc
						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1.0


		if 'confirm' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)):
				for e, end_state in enumerate(create_states(n)):
					if init_state == end_state:
						trans_mat[a,i,e]=1.0

		
	trans_mat[:,len(create_states(n))-1,len(create_states(n))-1]=1.0

	trans_mat[len(create_actions(n))-1,:,len(create_states(n))-1]=1.0

	return trans_mat


def update_obs_mat(n, obs_mat):
	for a,action in enumerate(create_actions(n)):
		if 'express' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):

				if init_state[idx]=='0':
					obs_mat[a,i,0]=0.1
					obs_mat[a,i,1]=0.2
					obs_mat[a,i,2]=0.7
				elif init_state[idx]=='1':
					obs_mat[a,i,0]=0.2
					obs_mat[a,i,1]=0.1
					obs_mat[a,i,2]=0.7					

		if 'confirm' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):
				if init_state[idx]=='0':
					obs_mat[a,i,0]=0.1
					obs_mat[a,i,1]=0.9
					
				elif init_state[idx]=='1':
					obs_mat[a,i,0]=0.9
					obs_mat[a,i,1]=0.1
						

		
	obs_mat[:,len(create_states(n))-1,2]=1.0

	obs_mat[len(create_actions(n))-1,:,2]=1.0

	return obs_mat

def create_actions(n):

	actions=[]
	for action in range(n):
		actions.append('express_s'+str(action))
	for action in range(n):
		actions.append('confirm_s'+str(action))
	actions.append('terminate')

	return actions

def write_trans_mat(Tr, s,n):

	for a,action in enumerate(create_actions(n)):
		s+='\nT: '+action+'\n'
		for i,init_state in enumerate(create_states(n)):
			for e, end_state in enumerate(create_states(n)):
				s+= str(Tr[a,i,e]) +' '
			s+='\n'

	return s

def write_reward_mat(s,n,bonus,penalty,exp_cost,conf_cost):

	for action in create_actions(n):
		if 'express' in action:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(exp_cost)
		elif 'confirm' in action:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(conf_cost)
		else:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				elif state ==create_states_from_bin(n)[-2]:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(bonus)
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(penalty)

	return s


def write_obs_mat(Ob, s,n):

	for a,action in enumerate(create_actions(n)):
		s+='\nO: '+action+'\n'
		for i,init_state in enumerate(create_states(n)):
			for o, obs in enumerate(['pos','neg','na']):
				s+= str(Ob[a,i,o]) +' '
			s+='\n'

	return s

def writeToFile(s,n):

	f = open(str(n)+".pomdp",'w')
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
	return 'observations: pos neg na why'


def generate_transition_matrix(states, state_index, actions, n):
	matrices = []
	for action in actions:	
		matrix = transition_matrix_action(states, state_index, action, n)
		matrices.append(matrix)
	return matrices

def transition_matrix_action(states, state_index, action, n):
	m = len(states)
	matrix = []
	if 'confirm' in action:
		row = [0.0 for _ in range(m)] 
		row[0] = 1.0
		for i in range(m):
			matrix.append(row)
			row = [0.0] + row[:-1]
		return matrix
	if 'express' in action:
		action_attribute = action.split('_')[1]
		# iterate over the column by building matrix row by row
		for init in states:
			row = [0.0]*(len(states))
			# if the state is not know initially, then after the action make the state know with some probability
			if 'not' + action_attribute in init:
				row[state_index[init]] = 0.1
				# split the initial state into attributed. Make the attribute corresponding to the action known and build the final state
				attribute = init.split('_')
				final = []
				for st in attribute:
					if action_attribute in st:
						final.append(action_attribute)
					else:
						final.append(st)
				final_state = '_'.join(final)
				print(init, final_state)
				row[state_index[final_state]] = 0.9
			else:
				row[state_index[init]] = 1.0

			matrix.append(row)	
		print(action_attribute)
		return matrix
	
	
	# elif 'express' in action:
	# 	fluent = action.split('_')[1]
	# 	num = int(fluent[1])
	# 	row[0] = 0.1
	# 	row[half-num-1] = 0.9
	# matrix = []
	# for i in range(m//2):
	# 	matrix.append(row)
	# 	row = [0.0] + row[:-1]
	# row = [0.0 for _ in range(m)]
	# row[i+1] = 1.0 
	# for i in range(m//2+1):
	# 	matrix.append(row)
	# 	row = [0.0] + row[:-1]
	# return matrix
	
	# half = 2**(n-1)
	# matrix = [[0.0]*(m) for _ in range(m)]
	# for i in range(m):
	# 	for j in range(m):
	# 		if 'confirm' in action:
	# 			if i ==j:
	# 				matrix[i][j] = 1.0
			
				
				


				
				
	return matrix

def print_matrix(matrix):
	for i in range (len(matrix)):
		for j in range(len(matrix)):
			print matrix[i][j],
		print'\n',

def main():
	n=3
	s = ''
	s += 'discount : 0.99\n\nvalues: reward\n'

	states, state_index = generate_states(n)
	s	+=  'states: ' +  ' '.join(states) + '\n'
	actions = generate_actions(n)
	s	+=  'actions: ' +  ' '.join(actions) + '\n'
	observations = generate_observations()
	s	+=  'observations: ' +  ' '.join(observations) + '\n'
	# print(s)
	s+='\nstart: uniform\n'
	# print(state_index)
	# matrix = generate_transition_matrix(states, actions, n)
	matrix = transition_matrix_action(states, state_index, 'express_s1', 3)
	print_matrix(matrix)
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