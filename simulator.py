#!/usr/bin/env python
from parser1 import Policy,Solver
from pomdp_parser import Model
import numpy as np
from scipy.stats import entropy
import parse_exp
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)

class Simulator:
	def __init__(self, filename='pomdp.pomdp', output='policy.policy'):
		self.model = Model(filename, parsing_print_flag=False)
		#self.policy = Policy(len(self.model.states),len(self.model.actions) ,output)
		
		self.policy = Policy(len(self.model.states),len(self.model.actions) ,output)
		self.expdict = parse_exp.ParseExp().read_exp_oeg()
		print self.expdict
		self.explist = parse_exp.ParseExp().read_exp_complete()
		
		self.policy = Policy(len(self.model.states),len(self.model.actions) ,output)
		self.expdictpeg = parse_exp.ParseExp().read_exp_peg()
	def init_belief(self, int_prob):

		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		init_belief=[]
		#if int_prob >0.5:
		for i in range(len(self.model.states)):
			if i == 0:
				init_belief.append(1.0)
			else:
				init_belief.append(0)	 
		#else:
		#	init_belief = [0.1,0.1,0.7,0.1, 0]	 
		#int_prob =float(int_prob)
		
		b = np.zeros(len(self.model.states))
		for i in range(len(self.model.states)):
				b[i] = init_belief[i]/sum(init_belief)
		#print 'The initial belief where human knows nothing about the explanations would be:'
#raw_input()
		return b

	def sample (self, alist, distribution):
  
		return np.random.choice(alist, p=distribution)

	def get_state_index(self,state):

		return self.model.states.index(state)


	def robot_nlg(self,strategy,a,d_cnt):
		print 'action is: ',a
		print d_cnt
		if strategy =='oeg':
			if a=='terminate':
				print'Conversation terminated'
			elif 'confirm' in a:
				print str(d_cnt)+'-Robot confirms: '#+self.expdict[a.split('_')[1][1]]
			else:
				print str(d_cnt)+'-Robot: ' #+ self.expdict[a.split('_')[1][1]] 
		elif strategy =='peg':
			if a=='terminate':
				print'Conversation terminated'
			elif 'confirm' in a:
				print  str(d_cnt)+'-Robot confirms: '+self.expdictpeg[a.split('_')[1][1]]
			else:
				print str(d_cnt)+'-Robot: ' + self.expdictpeg[a.split('_')[1][1]] 
		elif strategy == 'complete':
			if 'confirm' in a:
				print  str(d_cnt)+'-Robot confirms: '+ self.explist[self.model.actions.index(a) - len(self.explist)]
			else:
				print str(d_cnt)+'-Robot: ' + self.explist[self.model.actions.index(a)]
		
			
	def human_nlg(self,o):

		if o=='pos':
			print'JPL: I see'
		elif o=='neg':
			print'JPL: Sorry, I didn\'t catch what you said'
		else:
			pass


	def init_state(self):
	#print self.model.states[0]
		state= self.model.states[0] #change it later
		#print '\nRandomly selected state from [not_forward_not_interested,not_forward_interested] =',state
		s_idx = self.get_state_index(state)
		#print s_idx
		return s_idx, state

	def get_obs_index(self, obs):

		return self.model.observations.index(obs)
	def observe(self, a_idx):

				
		p =0.2
		if self.model.actions[a_idx] == 'terminate':
			obs='na'
		elif 'confirm' in self.model.actions[a_idx]:
			obs=self.sample(['pos','neg'],[1-p,p])
		elif 'express' in self.model.actions[a_idx]:
			obs=self.sample(['pos','neg','na'],[0.20,0.1,0.7])

		#if self.model.actions[a_idx] == 'terminate' or 'express' in self.model.actions[a_idx] :
		#	obs='na'
		#else:
		#	obs=self.sample(['pos','neg'],[1-p,p])
		
		#obs = 'na'
		#l=len(self.model.observations)-1
		#o_idx=randint(0,l)
		o_idx=self.get_obs_index(obs)
		print ('observation: ',self.model.observations[o_idx])
		return o_idx

		

	def update(self, a_idx,o_idx,b ):
		b = np.dot(b, self.model.trans_mat[a_idx, :]) 

		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
			
		b = b / sum(b)
		#raw_input()
		return b



	def run(self,strategy):
		print 'Conversation begins'
		#s_idx,temp = self.init_state()
		prob = 0.75
		b = self.init_belief(prob)
		C=0	
		R= 0
		s_idx,temp = self.init_state()
		if strategy =='oeg' or strategy == 'peg':
			d_cnt=0
			express_actions = self.model.actions[0:(len(self.model.actions)-1)/2 + 1]
			while True:
				print '\n'
				a_idx=self.policy.select_action(b)
				a = self.model.actions[a_idx]
				d_cnt+=1
				self.robot_nlg(strategy,a,d_cnt)      
				o_idx = self.observe(a_idx)
				o = self.model.observations[o_idx]
				self.human_nlg(o)
				#b =self.update(a_idx,o_idx, b)
				#print b
				
				if 'terminate' in a:
					print 'Normalized dialog length', d_cnt/9
					print ('Conversation ends\n ')

					break
				C = C + self.model.reward_mat[a_idx,s_idx]
				print C
				b =self.update(a_idx,o_idx, b)
		elif strategy == 'complete':
			d_cnt=0
			express_actions = self.model.actions[0:(len(self.model.actions)-1)/2 + 1]
			confirm_actions = self.model.actions[(len(self.model.actions)-1)/2:]
			while True:
				
				if len(express_actions)==0:
					print ('Conversation ends\n ')
					print 'Normalized dialog length', d_cnt/len(self.model.actions[0:(len(self.model.actions)-1)/2 + 1])
					break
				a = random.choice(express_actions)
				d_cnt+=1
				a_idx = self.model.actions.index(a)
				self.robot_nlg(strategy,a,d_cnt)
				#express_actions.remove(a)
				o_idx = self.observe(a_idx)
				o = self.model.observations[o_idx]
				self.human_nlg(o)
				b =self.update(a_idx,o_idx, b)
				a_c= 'confirm_'+a.split('_')[1]
				a_c_idx = self.model.actions.index(a_c)
				d_cnt+=1
				self.robot_nlg(strategy, a_c,d_cnt)			
				o_idx = self.observe(a_c_idx)
				o = self.model.observations[o_idx]
				self.human_nlg(o)
				b =self.update(a_c_idx,o_idx, b)
				if o =='pos':
					express_actions.remove(a)
					
				print b[-2]
				C = C + self.model.reward_mat[a_idx,s_idx]
				print C

		return d_cnt/len(self.model.actions[0:(len(self.model.actions)-1)/2 + 1]),b[-2],C
	
	def run_n_trials(self,strategylist,numbers):

		average_dcnt = {}
		average_belief = {}
		average_cost={}
		average_belief['peg'] = 0
		average_belief['oeg'] = 0
		average_dcnt['peg'] = 0
		average_dcnt['oeg'] = 0
		average_dcnt['complete'] = 0
		average_belief['complete'] = 0
		for strategy in strategylist:

			for i in range(numbers):
				d,b=self.run(strategy)

				average_dcnt[strategy]+=d
				average_belief[strategy]+=b


			average_dcnt[strategy]= average_dcnt[strategy]/float(numbers)
			average_belief[strategy]= average_belief[strategy]/float(numbers)

		result=[]
		#result.append(average_dcnt)
		for item in strategylist:
			result.append(average_belief[item])
		#self.print_result(result)
		return result



def print_result (results):

	objects = ['PEG','Complete','OEG']
	y_pos = np.arange(1,1+len(objects))
	barlist = plt.bar(y_pos, results, align='center', alpha=0.5)
	barlist[0].set_color('g')
	barlist[1].set_color('b')
	barlist[2].set_color('r')


	plt.xticks(y_pos, objects, fontsize= 16)
	plt.ylabel('Human belief', fontsize= 16)
	plt.title('Explanation strategy', fontsize=16)
	#plt.show()
	plt.savefig('Belief.pdf')




def main():
		
		
#		n = FLAGS_n

		n = '9'
		#a=Simulator(filename=n+'.pomdp', output=n+'.policy')
		#result = a.run_n_trials(['peg','complete'],300)
		#print result
		n = '3'
		b=Simulator(filename=n+'.pomdp', output=n+'.policy')
		result2 = b.run_n_trials(['oeg'],1)
		#result = result +result2
		print_result(result2)
		#n = '9'
		#a=Simulator('peg',filename=n+'.pomdp', output=n+'.policy')
		#a.run('peg')


	   

if __name__=="__main__":
#	import argparse
#	parser = argparse.ArgumentParser()
#	parser.add_argument('--n', type=str, required=True, default=3,
#						help="The number of statements of an explanation")
#	args = parser.parse_args()
#	for k, v in vars(args).items():
#		globals()['FLAGS_%s' % k] = v
	main()

