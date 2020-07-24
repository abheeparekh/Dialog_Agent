import os
import sys
import re
from itertools import chain, combinations

def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def get_subset():


	Rpath="/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/domain.pddl"
	Hpath= "/home/saeid/software/DIRNAME/misc/tests/benchmarks/rovers/rovers/human/domain-H.pddl"

	assert os.path.exists(Rpath), 'File does not exist: %s' % Rpath
	assert os.path.exists(Hpath), 'File does not exist: %s' % Hpath

	with open(Rpath) as f:

		Rlines=f.readlines()
	with open(Hpath) as f:

		Hlines=f.readlines()

	# create predicates list
	Rpredicates ={}
	Hpredicates ={}
	# initialize predicates

	#for i in range(4,30):

	#	predicate = Rlines[i].split("(")[1].split(" ")[0]
	#	if predicate == ':predicates':
	#		predicate = 'at'
	#	Rpredicates[predicate] =[]
	#	Hpredicates[predicate] =[]


		
	#print Rpredicates

	for l,line in enumerate(Rlines):
		if 'action' in line:
			action_name = line.split(" ")[1].split("\n")[0]
			#print action_name
			#get the preconditions
			for pre in Rlines[l+2][18:].split("(")[1:-1]:
				for pre2 in Rlines[l+2][18:].split(")")[1:-1]:
					
					if pre.split(")")[0] ==pre2.split("(")[1]:
						key = pre.split(")")[0]
						if key in Rpredicates:

							Rpredicates[key].append((key,action_name,0))
						else:
							Rpredicates[key] = [(key,action_name,0)]

			for post in Rlines[l+5][12:].split("(")[1:-1]:
				for post2 in Rlines[l+2][18:].split(")")[1:-1]:

					if 'not' not in post:
						if post.split(")")[0] == post2.split("(")[1]:
							key = post.split(")")[0]
							if key in Rpredicates:
								Rpredicates[key].append((key,action_name,1))
							else:
								Rpredicates[key] = [(key,action_name,1)]
				
	for ll,lline in enumerate(Hlines):
		if 'action' in lline:
			action_name = lline.split(" ")[1].split("\n")[0]
			#print action_name
			#get the preconditions
			#print Hlines[ll+2][18:].split("(")[1:]
			for pre in Hlines[ll+2][18:].split("(")[1:-1]:
				#print Hlines[ll+2][18:].split(")")[1:]
				for pre2 in Hlines[ll+2][18:].split(")")[1:-1]:
					#print 'Hi'
					#print pre.split(")")[0]
					#print pre2.split("(")[1]
					#print 'Bye\n' 
					if pre.split(")")[0] ==pre2.split("(")[1]:
					#	print 'HI'
						#key = pre.split(" ")[0]
						key = pre.split(")")[0]
						#print key
						if key in Hpredicates:
							Hpredicates[key].append((key,action_name,0))
						else:
							Hpredicates[key] =[(key,action_name,0)]
				
			for post in Hlines[ll+4][12:].split("(")[1:-1]:
				for post2 in Hlines[ll+2][18:].split(")")[1:-1]:
				#print post
					if 'not' not in post:
						if post.split(")")[0] == post2.split("(")[1]:
							key = post
							if key in Hpredicates:
								Hpredicates[key].append((key, action_name,1))
							else:
								Hpredicates[key] = [(key, action_name,1)]
	
	diff = {}

	for key in Rpredicates.keys():
	
		if key in Hpredicates.keys():	
			if len(list(set(Rpredicates[key]) - set(Hpredicates[key])))!=0:
				diff[key] = list(set(Rpredicates[key]) - set(Hpredicates[key])) 			
		else:
			diff[key] = Rpredicates[key]
			
	return diff, Hpredicates



def main():

	get_subset()




if __name__=="__main__":

	main()