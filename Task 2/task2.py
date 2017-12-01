import sys
import operator



tag_list = {}
wordlist = []
dataset = []
wordset = []
utr = {}
rank = {}



def calculate_rank(sorted_utr):
	r=1
	global rank
	for word in sorted_utr:
		rank[word[0]] = r
		r+=1



def calculate_utr():
	global utr	
	for i in wordlist:
		try:
			utr[i] = float(0.800*tag_list[str(i +'HI:HI')] + 0.100*tag_list[str(i +'HI:CMH')] + 0.75*tag_list[str(i +'EN:CMH')] + 0.15*tag_list[str(i +'HI:CMEQ')]+0.10*tag_list[str(i +'EN:CMEQ')])/float(tag_list[str(i +'EN:EN')])
		except ZeroDivisionError:
			utr[i] = float(0.800*tag_list[str(i +'HI:HI')] + 0.100*tag_list[str(i +'HI:CMH')] + 0.75*tag_list[str(i +'EN:CMH')] + 0.15*tag_list[str(i +'HI:CMEQ')]+0.10*tag_list[str(i +'EN:CMEQ')])/0.01
	 


def create_outputfile():
	out_file = open("Rank_list.txt","w") 
	for word in wordlist:
		out_file.write(word + ", " + str(utr[word]) + ", " +str(rank[word])  + "\n")
	out_file.close()



def initialize_tags():
	for word in wordset:
		x = (word.strip('\n')).strip('\r')
		global wordlist
		global tag_list
		wordlist.append(x) 
		tag_list[str(x +'EN:EN')] = 0
		tag_list[str(x +'EN:HI')] = 0
		tag_list[str(x +'EN:CME')] = 0
		tag_list[str(x +'EN:CMH')] = 0
		tag_list[str(x +'EN:CMEQ')] = 0
		tag_list[str(x +'HI:EN')] = 0
		tag_list[str(x +'HI:HI')] = 0
		tag_list[str(x +'HI:CME')] = 0
		tag_list[str(x +'HI:CMH')] = 0
		tag_list[str(x +'HI:CMEQ')] = 0

  

def open_inputfile(): 
    	with open("dataset.txt",'r') as data_set:
		global dataset
		dataset = data_set.readlines()

	with open("wordset.txt",'r') as word_set:
		global wordset
		wordset = word_set.readlines()



def update_count():
	for i in range(0,len(dataset)):		
		tweet = dataset[i].strip('\n')	
		line = tweet.split('\t')
		tag = line[0].split("/")[0]
		sent = line[1].split(" ")	
		for j in range(0, len(sent)):
			try:		
				item = sent[j].split('/')
				if item[0] in wordlist:
					if item[1] == 'EN' or item[1] == 'HI':
						tag_list[str(item[0] + item[1] + ':' + tag)] += 1
			except IndexError:
				continue									
						


if __name__ == "__main__":		
	open_inputfile()
	initialize_tags()
	update_count()
	calculate_utr()
	sorted_utr = sorted(utr.items(), key=operator.itemgetter(1), reverse=True)
	calculate_rank(sorted_utr)
	create_outputfile()



