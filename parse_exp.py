

class ParseExp:

	def __init__(self):
		pass


	def read_exp_oeg(self):

		f=open('sample_oeg.txt','r')
		#for line in f.readlines():
		oeg_list=[]
		oeg_ind = []
		actions =[]
		all_words = f.read().split('(1)')
		# print('all words ' + str(all_words))
		for index, item in enumerate(all_words):
			actions.append(item)
			if '[PRECONDITION]' in item:
				oeg_list.append(item.split('##')[1])
				oeg_ind.append(index)
				# print('OEG list '+str(oeg_list))
				# print('OEG index '+str(oeg_ind))
		oeg_dict={}
		for a in range(len(oeg_list)):
			oeg_dict[str(a)]=oeg_list[a]
		# print('oeg_dict ' + str(oeg_dict))
		# return preconditions dictionary, index of actions with preconditions, number of actions and all actions
		return oeg_dict, oeg_ind, len(all_words), actions

	def read_exp_peg(self):

		f=open('sample_peg.txt','r')
		#for line in f.readlines():
		peg_list=[]
		all_words = f.read().split('\n')
		peg_dict={}
		for a in range(len(all_words)):
			peg_dict[str(a)]=all_words[a]

		return peg_dict


	def read_exp_complete(self):

		f=open('sample_complete.txt','r')
		#for line in f.readlines():
		oeg_list=[]
		all_words = f.read().split('\n')
		#for item in all_words:
		#	if '[PRECONDITION]' in item:
		#		oeg_list.append(item.split('##')[1])
		#oeg_dict={}
		#for a in range(len(oeg_list)):
		#	oeg_dict[str(a)]=oeg_list[a]
		print all_words

		return all_words





def main():

	a=ParseExp()
	a.read_exp_complete()


if __name__=="__main__":
	main()


