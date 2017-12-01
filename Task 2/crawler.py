# NLP Shared Task 2 - Group8
#!/user/bin/python
import tweepy
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


with open("Datasheet.csv","r") as d:
	source_tweets = d.readlines()

target_tweets = open("dataset.txt", "w")


consumer_token = "V4uOcxRwzfBufeD8RZc6uM7N8"
consumer_secret = "eMQqZ6uNau0QMR1XxqiDkeNqNi9o3F5rx8MM7gCIan81AMRHMy"
oauth_token = "441958665-Cj3Qe98W41WhEONWvJlN88gvT7QtuyGMwbg4zFTa"
oauth_token_secret = "BZmm9n9qnodUtOsIaMv7ivRTmpGN2KL3jaVC6nnZoU3lz"

oauth = tweepy.OAuthHandler(consumer_token, consumer_secret)
oauth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(oauth)


for t in source_tweets:
	temp = []
	w_type = []
 	t_list = []

	tweet_id = t.split(',')
	for i in range(1,len(tweet_id)):
		temp = tweet_id[i].split(":")
		w_type.append(temp[2])	

	try:
		tweet_content = api.get_status(tweet_id[0])
		
	except tweepy.error.TweepError:
		print "err"
		continue

	t_list = re.findall('#\w+|@\w+|\w+', tweet_content.text)

	h_count = 0
	e_count = 0
	for w in w_type:
		if w == 'HI':
			h_count+=1
		elif w == 'EN':
			e_count+=1

	percent_hin = h_count*100/len(w_type)
	percent_eng = e_count*100/len(w_type)

	if  percent_hin > 90:
		target_tweets.write("EN/")
	elif percent_eng > 90:
		target_tweets.write("HIN/")
	elif percent_eng == 0:
		target_tweets.write("HI/")
	elif percent_hin == 0:
		target_tweets.write("EN/")
	elif percent_eng > 50:
		target_tweets.write("CME/")
	elif percent_hin > 50:
		target_tweets.write("CMH/")
	elif percent_hin == e_count:
		target_tweets.write("CMEQ/")	
	elif percent_hin > percent_eng:
		target_tweets.write("CMH/")
	else:
		target_tweets.write("CME/")

	target_tweets.write(tweet_id[0]+"\t")
	
	for i in range(0,len(w_type)):
		target_tweets.write(str(t_list[i]))
		target_tweets.write("/")
		target_tweets.write(w_type[i])
		target_tweets.write(" ")

	target_tweets.write("\n")


