import readmodel
from itertools import chain, combinations
import sys
import subprocess
from collections import Counter


class Update:

	def __init__(self):

		self.problem_file = "/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/pfile01"
		self.domain = "/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/human/domain-Hsaeid.pddl"
		self.solver_path = "/home/saeid/software/DIRNAME/fast-downward.py"
		self.newHpath = "/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/human/domain-Hsaeid.pddl"
		self.origHpath = "/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/human/domain-H.pddl"
		self.Hlines = None
	def getplan(self):
		plan =subprocess.check_output([self.solver_path, self.domain, self.problem_file, "--search", "astar(lmcut())" ])#.splitlines()
		return plan


	def powerset(self,iterable):
	    """
	    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
	    """
	    xs = list(iterable)
	    # note we return an iterator rather than a list
	    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

	def updatehuman(self):
		diff, Hpredicates = readmodel.get_subset()
		all_subsets = list(self.powerset(diff.keys()))
		predicates = diff.keys()

		with open(self.origHpath) as f:
			self.Hlines=f.readlines()
			#print type(Hlines)
			f.close()
		#all_plans={}
		tempdiff ={}
		temppredlist =[]
		for s,subset in enumerate(all_subsets):
			temppredlist.append( list(set(diff.keys()) - set(subset)))
		return temppredlist, diff


	def updatedomainH(self, temppredlist,diff):
		tempdiff ={}
		all_plans ={}
		action_of_plans = []
		for s,temppred in enumerate(temppredlist):
			#print temppredlist
			for pred in temppred:
				tempdiff[pred] = diff[pred]

				for key in tempdiff.values():
					#print 'key is' , key
					for l,line in enumerate(self.Hlines[34:]):   # From line 34 , actions are written
					#line[:-2] +' '+'\n'

						if 'action' in line:
						     # get predicate
							if key[0][1] in line:        # if action is in that line
												        # if it's a precondition
								if key[0][2] ==0:
									#print 'l: ', l 
									#rint 'line is:',line
									self.Hlines[34+l+2]=self.Hlines[34+l+2][:-1]+' '+'('+key[0][0]+')'+'\n'
									#print Hlines[l+2]
								elif key[0][2] ==1:
									self.Hlines[34+l+4]= self.Hlines[34+l+4][:-1]+' '+'('+key[0][0]+')'+'\n'
			#print type(self.Hlines)
			with open(self.newHpath,'w') as g:
				for line in self.Hlines:
					g.write(line)
				g.close()

			all_plans[s] = self.getplan() 
		
			for line in all_plans[s].splitlines():
				if '(1)' in line:
					action_of_plans.append(line)

		print self.getplan()
		return action_of_plans
	


	def get_similarity(self,all_plans, index):
		Bestplan = all_plans[0]
		length_of_most_similar =100
		current_plan = all_plans[0][0:index]
		
		counter_b = Counter(current_plan)
		for ind, singleplan in enumerate(all_plans[0:index]):
			counter_a = Counter(singleplan)
			if len(Counter(counter_a - counter_b))< length_of_most_similar:
				length_of_most_similar = len(Counter(counter_a - counter_b))
				Bestplan = singleplan
	
		return ind

def main():

	a= Update()
	temppred, diff = a.updatehuman()
	all_plans = a.updatedomainH(temppred, diff)
	print a.get_similarity(all_plans,6)
	#print action_of_plan

if __name__ == "__main__":

	main()