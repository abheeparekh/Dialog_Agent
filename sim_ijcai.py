#!/usr/bin/env python
from parser1 import Policy,Solver
from pomdp_parser import Model
import numpy as np
from scipy.stats import entropy
import parse_exp
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import simulator
from itertools import chain, combinations
from updatehuman import Update
from PDDLhelp import read_state_from_domain_file
from PDDLhelp import write_domain_file_from_state

np.set_printoptions(suppress=True)

class IJCAI(simulator.Simulator):
	def __init__(self, filename='pomdp.pomdp', output='policy.policy'):
		self.model = Model(filename, parsing_print_flag=False)
		self.policy = Policy(len(self.model.states),len(self.model.actions) ,output)
		# self.robot_state = read_state_from_domain_file('domainRobot.pddl', 'problemRobot.pddl')
		# self.human_state = read_state_from_domain_file('domainHuman.pddl', 'problemHuman.pddl')
		# self.domain_template = 'domain_template.pddl' 
		# self.problem_template = 'prob_template.pddl'
		self.attribute_dict = {'s0' : 'Robot has left leg', 's1' : 'Robot has right leg', 's2' : 'Robot can listen'}
		self.behavior_dict = {'s0s1s2': 'Robot is dancing', 's0s1':'Robot is walking'}
		self.known_attributes=[]
		
	# def powerset(self,iterable):
	#     """
	#     powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
	#     note we return an iterator rather than a list
	# 	"""
	#     xs = list(iterable)
	#     return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

	def init_belief(self, int_prob = 1.0):
		"""
		initialize the beliefs of the states with index=0 evenly
		"""
		num_states = len(self.model.states)
		b = np.zeros(num_states)
		init_belief=[]
		for i in range(num_states):
			if i == 0:
				init_belief.append(1.0)
			else:
				init_belief.append(0)	 
		b = np.zeros(num_states)
		for i in range(num_states):
				b[i] = init_belief[i]/sum(init_belief)
		return b
	
	def updateBelief(self, action_idx,obs_idx,belief ):
		belief = np.dot(belief, self.model.trans_mat[action_idx, :]) 
		belief = [belief[i] * self.model.obs_mat[action_idx, i, obs_idx] for i in range(len(self.model.states))]
		belief = belief / sum(belief)
		return belief

	def robot_nlg(self,action):
		print ''
		if action=='terminate':
			print'Conversation terminated'
		else:
			fluent = action.split('_')[1]
			if 'confirm' in action:
				print 'Robot is confirming that human understands the attribute: ' + str(self.attribute_dict[fluent])
			elif 'express' in action:
				print 'Robot is expressing the attribute: ' + str(self.attribute_dict[fluent])
			elif 'behavior' in action:
				print str(self.behavior_dict[fluent])
			else:
				pass

	def human_nlg(self,obs, action):
		'''
		Based on the observation made by the human model, this function generates
		the natural language for the observation made
		'''
		if action=='terminate':
			return
		fluent = action.split('_')[1]
		attributes = ['s' + i for i in fluent.split('s')[1:]]
		if 'behavior' in action:
			if obs=='pos':
				for attribute in attributes:
					print 'Human is inferring that ' + str(self.attribute_dict[attribute]) 
			elif obs=='neg':
				print 'Human: Not able to infer anything from the action'
			elif obs == 'why':
				print 'Why ' + str(self.behavior_dict[fluent])
		else:
			if obs=='pos':
				print'Human: I understand that ' + str(self.attribute_dict[fluent])
			elif obs=='neg':
				print'Human: Sorry, I didn\'t catch what you said'
			else:
				pass
	
	def sample (self, alist, distribution):
		return np.random.choice(alist, p=distribution)
	
	def get_obs_index(self, obs):
		return self.model.observations.index(obs)

	def get_action_index(self, action):
		return self.model.actions.index(action)

	def observe(self, action):
		if action == 'terminate':
			obs='na'
		elif 'confirm' in action:
			obs=self.sample(['pos','neg'],[0.9,0.1])
		elif 'express' in action:
			obs=self.sample(['pos','neg','na'],[0.20,0.10,0.70])
		else:
			obs=self.sample(['pos','neg','na', 'why'],[0.5,0.10,0.10, 0.3])
		obs_idx=self.get_obs_index(obs)
		return obs_idx
	
	def explain_neg(self, action):
		'''
		This function is called when human gives a negative observation. This will explain all parameters
		of the given action
		'''
		fluent = action.split('_')[1]
		attributes = ['s' + i for i in fluent.split('s')[1:]]
		if 'behavior' in action:
			print '\nRobot: I will explain....'
			for attribute in attributes:
				print 'Explanation >> ' + str(self.attribute_dict[attribute]) 
			print('Human: I see')

			# human_params = []
			
			# for param in self.human_state:
			# 	if action in param:
			# 		human_params.append(param)

			# for param in self.robot_state:
			# 	if action in param:
			# 		print('Explanation >> ' + param)
			# 		if param not in human_params:
			# 			self.human_state.append(param)

	# def check_action(self, action):
	# 	'''
	# 	to check whether the given action in human model is same as that in robot model
	# 	'''
	# 	human_params = []
		
	# 	for param in self.human_state:
	# 		if str(action) in param:
	# 			human_params.append(param)

	# 	for param in self.robot_state:
	# 		if str(action) in param:
	# 			if param not in human_params:
	# 				return False
	# 	return True			

	# def update_human_model(self, action):
	# 	'''
	# 	update the human model with the robot model for a given action 
	# 	'''
	# 	human_params = []
	# 	fluent = action.split('_')[1]
	# 	for param in self.human_state:
	# 		if str('express_'+ fluent) in param:
	# 			human_params.append(param)

	# 	for param in self.robot_state:
	# 		if str('express_'+ fluent) in param:
	# 			if param not in human_params:
	# 				self.human_state.append(param)
			
	# def execute_plan_no_exp(self,plan_cnt):
	# 	plan_cnt+=1

	# def replan(self, a):
	# 	explaind_sofar_ind = self.exp_ind_list[:len(self.confirmed_sofar)]
	# 	explaind_sofar_pred=[]
	# 	print('Explantion index list:' + str(self.exp_ind_list))
	# 	print('Confirmed so far:' + str(self.confirmed_sofar) )
	# 	print('Explained ID so far' + str(explaind_sofar_ind))
	# 	print('Precondition dict' + str(self.expdict))
	# 	for i in explaind_sofar_ind:
	# 		# explaind_sofar_pred.append(self.expdict[i]) 
	# 		explaind_sofar_pred.append(self.expdict.get('%{0}'.format(i))) 
	# 	print('Explained so far:' + str(explaind_sofar_pred))
	# 	subsets_of_explained = self.powerset(explaind_sofar_pred)
	# 	print('Subset of explained ' + str(list(subsets_of_explained)))
	# 	tempdict = {}
	# 	plans = {}
	# 	print('update human: ' + str(self.updatehuman()))

	# 	for i,each_subset in enumerate(subsets_of_explained):
	# 		tempdiff =list(set(Update.updatehuman()) - set(each_subset))
	# 		plans[each_subset]= (Update.updatedomainH(tempdiff))
	# 	print('re plan ' + str(plans))
	# 	return plans

	def run(self, verbose = False):
		curr_belief = self.init_belief()
		dialog_cnt=0
		state_idx,init_state = self.init_state()
		
		print '\nConversation begins....'		
		if verbose:
			print('State index: '+ str(state_idx))
			print('Init state: ' + str(init_state))

		while True :
			action_idx=self.policy.select_action(curr_belief)
			action = self.model.actions[action_idx]
			self.robot_nlg(action)      
			obs_idx = self.observe(action)
			obs = self.model.observations[obs_idx]
			self.human_nlg(obs, action)

			if 'terminate' in action:
				print 'Dialog length', dialog_cnt
				print ('Conversation ends......\n')
				# temp_domain, temp_problem = write_domain_file_from_state(self.human_state, self.domain_template, self.problem_template)
				break

			dialog_cnt+=1
			curr_belief =self.updateBelief(action_idx,obs_idx, curr_belief)
			
			if verbose:
				print('get index of action: ' + str(action_idx))
				print('get action: ' + str(action))
				print('current belief: ' + str(curr_belief))
				print('observation index: ' + str(obs_idx))
				print('observation ' + str(obs))
			if obs =='pos':
				pass
				# self.update_human_model(action)
				# if'confirm' in action:
				# self.confirmed_sofar.append(action)
			elif obs =='neg':
				self.explain_neg(action)
				obs_idx = self.get_obs_index('pos')
				fluent = action.split('_')[1]
				# update_action = 'confirm_' + fluent
				update_action = action
				action_idx = self.get_action_index(update_action)
				curr_belief = self.updateBelief(action_idx,obs_idx, curr_belief)
				dialog_cnt+=1
		return dialog_cnt,curr_belief[-2]
	
	def run_n_trials(self,numbers=1):
		
		average_belief = 0
		average_dialog_cnt = 0
		
		for i in range(numbers):
			dialog_cnt,belief=self.run()
			average_dialog_cnt+=dialog_cnt
			average_belief+=belief

		average_dialog_cnt= average_dialog_cnt/float(numbers)
		average_belief= average_belief/float(numbers)
		result=[]
		result.append(average_belief)
		result.append(average_dialog_cnt)
		return result

def main():
		n = 'prj1_3a'
		b=IJCAI(filename='out.pomdp', output='out.policy')
		# b=IJCAI(filename=n+'.pomdp', output=n+'.policy')
		result = b.run_n_trials()


if __name__=="__main__":

	main()

