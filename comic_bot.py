import praw, config, os, requests, time, random
from cred_T import *
from tweepy import *

def bot_loggin_R ():										#Log to Reddit
	r = praw.Reddit (username = config.username,
				 password = config.password, 
				 client_id = config.client_id, 
				 client_secret = config.client_secret, 
				 user_agent = 'Bot that downloads comics from Reddit.')
	print ('Logged in Reddit')
	return r

def bot_loggin_T ():										#Log to Twitter
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)
	return api

def comic_date ():													  #Picks a random date to choose the comic strip
	YY = random.randrange (2000, time.localtime(time.time()).tm_year) #To have the years up to date.
	MM = random.randrange (1,12)
	if (MM % 2 == 0):
		DD = random.randrange (1, 30)
	else:
		DD = random.randrange (1,31)

	print ('\n\n>> ' + str (DD) + '/' + str (MM) + '/' + str (YY))	

	return DD, MM, YY 				#date/fecha = [DD, MM, YY]

def write (direc):					
	f = open ('comic.jpg', 'wb')
	f.write (requests.get (direc).content)
	f.close

def snoopy (fecha):
	URL = 'http://www.peanuts.com/wp-content/comic-strip/color-low-resolution/desktop/'				
	comic_name = 'Peanuts'
	comic_author = 'Charles M. Schulz'

	if (fecha [0] < 10 and fecha [1] < 10 and (fecha [2]-2000) < 10):	#Format to access at the URL picture.
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + '0' + str (fecha [2]-2000) + '0' + str (fecha [1]) + '0' + str (fecha [0]) + '.jpg'
	elif ((fecha [2]-2000) < 10 and fecha [1] < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + '0' + str (fecha [2]-2000) + '0' + str (fecha [1]) + str (fecha [0]) + '.jpg'
	elif ((fecha [2]-2000) < 10 and fecha [0] < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + '0' + str (fecha [2]-2000) + str (fecha [1]) + '0' + str (fecha [0]) + '.jpg'
	elif (fecha [1] < 10 and fecha [0] < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + str (fecha [2]-2000) + '0' + str (fecha [1]) + '0' + str (fecha [0]) + '.jpg'
	elif (fecha [0] < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + str (fecha [2]-2000) + str (fecha [1]) + '0' + str (fecha [0]) + '.jpg'
	elif (fecha [1] < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + str (fecha [2]-2000) + '0' + str (fecha [1]) + str (fecha [0]) + '.jpg'
	elif ((fecha [2]-2000) < 10):
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + '0' + str (fecha [2]-2000) + str (fecha [1]) + str (fecha [0]) + '.jpg'
	else:
		URL_D = URL + str (fecha [2]) + '/daily/pe_c' + str (fecha [2]-2000) + str (fecha [1]) + str (fecha [0]) + '.jpg'

	print ('>> Peanuts: ' + URL_D)

	return comic_name, comic_author, URL_D			#image/link = [name, author, url] ---> Info of the comic strip

def garfield (fecha):
	URL = 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/' #2017/2017-07-13.gif'
	comic_name = 'Garfield'
	comic_author = 	'Jim Davis'

	if (fecha [0] < 10 and fecha [1] < 10):	#Format to access at the URL picture.
		URL_D = URL + str (fecha [2]) + '/' + str (fecha [2]) + '-0' + str (fecha [1]) + '-0' + str (fecha [0]) + '.gif'
	elif (fecha [0] < 10):
		URL_D = URL + str (fecha [2]) + '/' + str (fecha [2]) + '-' + str (fecha [1]) + '-0' + str (fecha [0]) + '.gif'
	elif (fecha [1] < 10):
		URL_D = URL + str (fecha [2]) + '/' + str (fecha [2]) + '-0' + str (fecha [1]) + '-' + str (fecha [0]) + '.gif'
	else:
		URL_D = URL + str (fecha [2]) + '/' + str (fecha [2]) + str (fecha [1]) + str (fecha [0]) + '.gif'

	print ('>> Garfield: ' + URL_D)

	return comic_name, comic_author, URL_D			#image/link = [name, author, url] ---> Info of the comic strip

def comic_tweet (fecha):							#Here decides which comic strip will tweet
	if (random.randrange (0,2) == 0):
		url = snoopy (fecha)
	else:
		url = garfield (fecha)	

	return url

def tweet_text (fecha, image):						#Status of the tweet
	if (image [0] == 'Peanuts'):
		tweet = image [0] + ', made by: ' + image [1] + '.\nDate: ' + str (fecha [0]) + '/' + str (fecha [1]) + '/' + str (fecha [2]) + '\n\n' + '#Comics #Snoopy #CharlieBrown #Woodstock'
	else:
		tweet = image [0] + ', made by: ' + image [1] + '.\nDate: ' + str (fecha [0]) + '/' + str (fecha [1]) + '/' + str (fecha [2]) + '\n\n' + '#Comics #Garfield #Odie #Jon'

	return tweet

def upload (fecha, image):
	app = bot_loggin_T ()
	text = tweet_text (fecha, image)
	write (image [2])
	fn = os.getcwd () + '/comic.jpg'
	app.update_with_media (filename = 'comic.jpg', status = text)

bot_loggin_R ()

while True: 
	try:
		date = comic_date ()
		link = comic_tweet (date)
		upload (date, link)
		print (">>Tweet!")
		print ("\t---------------------------------------------------------------")
		time.sleep (7200)				#2 hour

	except:
		api = bot_loggin_T ()
		api.update_status (status = 'heyyeyaaeyaaaeyaeyaa! @Zeby95')
		print (">>ERROR!")
		time.sleep (120)