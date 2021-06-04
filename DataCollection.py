
import tweepy as tw
import csv 
from decouple import config # keys are stored in .env

CONSUMER_KEY = config("CONSUMER_KEY") 
CONSUMER_SECRET = config("CONSUMER_SECRET") 
ACCESS_TOKEN = config("ACCESS_TOKEN") 
ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET") 

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

SEP = ';'
csv = open('clippersVSmavs.csv','a')

#setup top of CSV file
csv.write('ID' + SEP + 'Date' + SEP + 'Text' + SEP + 'Place' + SEP + 'Location' + SEP + 'Number of Followers' + SEP + 'UserName' + SEP + 'Friends Count\n')

class StreamListener(tw.StreamListener):
	def on_status(self, status):

		if status.lang != 'en': # only collect English tweets
			return



		# get the full text of the tweet
		text = ''
		if hasattr(status, "retweeted_status"):  # Check if Retweet due to different structure
			try:
				print(status.retweeted_status.extended_tweet["full_text"])
				text = status.retweeted_status.extended_tweet["full_text"]
			except AttributeError:
				print(status.retweeted_status.text)
				text =  status.retweeted_status.text
		else:
			try:
				print(status.extended_tweet["full_text"])
				text = status.extended_tweet["full_text"]
			except AttributeError:	
				print(status.text)
				text =  status.text
			

		text = text.replace('\n', ' ').replace('\r', '').replace(SEP, ' ') #clean text
		
		unique_id = status.id_str #tweet ID
		created = status.created_at.strftime("%Y-%m-%d-%H:%M:%S") #created at

		place = '' # place 
		if status.place is not None:
			Place = status.place.full_name

		location = '' #location
		if status.coordinates is not None:
			lon = status.coordinates['coordinates'][0]
			lat = status.coordinates['coordinates'][1]
			location = str(lat) + ',' + str(lon)     

		followers = str(status.user.followers_count)
		name = status.user.screen_name
		friends = str(status.user.friends_count)

		csv.write(unique_id + SEP + created + SEP + text + SEP + place + SEP + location + SEP + followers + SEP + name + SEP + friends + '\n')


# set up streamer
stream_listener = StreamListener()
stream = tw.Stream(auth = api.auth, listener = stream_listener)

filters = ['DALvLAC', 'Mavericks', 'Mavs', 'Clippers', 'Luka', 'Kawhi', 'PG13', 'Paul George', 'Fluka', 'The Claw', 'KP', 'Porzingis', 'Rondo']
langs = ["en"]

# start streaming tweets
stream.filter(languages=langs, track=filters)



