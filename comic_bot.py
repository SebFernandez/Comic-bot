import praw, config, os, requests, time, random
from cred_T import *
from tweepy import *
from bs4 import BeautifulSoup

def bot_loggin_R ():										#Log to Reddit
	r = praw.Reddit (username = config.username,
				 password = config.password, 
				 client_id = config.client_id, 
				 client_secret = config.client_secret, 
				 user_agent = 'Bot that downloads comics from Reddit.')
	print ('>> Logged in Reddit\n')
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


	return comic_name, comic_author, URL_D			#image/link = [name, author, url] ---> Info of the comic strip

def cyanide ():													# (!) Attention with this function, returns more variables than the others
	URL = requests.get ('http://explosm.net/comics/random/')
	comic_name = 'Cyanide & happiness'

	soup = BeautifulSoup (URL.content, "html.parser")
	img = soup.find_all (id = 'main-comic')

	author = soup.find_all (class_ = 'author-credit-name')
	comic_author = author [0].get_text()
	comic_author = comic_author [3:len (comic_author)]

	date = soup.find_all (class_ = 'zeta small-bottom-margin past-week-comic-title')
	r_date = date[0].get_text()
	DD = r_date [8:10]
	MM = r_date [5:7]
	YY = r_date [0:4]

	URL_D = 'http:' + img[0].get ('src')

	return comic_name, comic_author, URL_D, DD, MM, YY			#image/link = [name, author, url, DD, MM, YY] ---> Info of the comic strip

def comic_tweet (fecha):							#Here decides which comic strip will tweet
	c_t = random.randrange (0,3)
	if (c_t == 0):
		url = snoopy (fecha)
	elif (c_t == 1 ):
		url = garfield (fecha)
	elif (c_t == 2):
		url = cyanide ()

	return url

def tweet_text (fecha, image):						#Status of the tweet
	line = image [0] + ', made by: ' + image [1] + '.\nDate: ' + str (fecha [0]) + '/' + str (fecha [1]) + '/' + str (fecha [2]) + '\n\n' + '#Comics '

	if (len (image) == 3):
		if (image [0] == 'Peanuts'):
			line += '#Snoopy #CharlieBrown #Woodstock'
		elif (image [0] == 'Garfield'):
			line += '#Garfield #Odie #Jon'
	else:		
		if (image [0] == 'Cyanide & happiness'):
			line = image [0] + ', made by: ' + image [1] + '.\nDate: ' + str (image [3]) + '/' + str (image [4]) + '/' + str (image [5]) + '\n\n' + '#Comics #CyanideAndHappiness'

	return line

def log (fecha, image):
	print (">> Comic: \t" + image [0])
	print (">> URL: \t" + image [2])
	
	if (image [0] == 'Peanuts' or image [0] == 'Garfield'):
		print (">> Date: \t" + str (fecha [0]) + '/' + str (fecha [1]) + '/' + str (fecha [2]))
	else:
		print (">> Date: \t" + str (image [3]) + '/' + str (image [4]) + '/' + str (image [5]))

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
		log (date, link)
		upload (date, link)
		print (">> Tweet!")
		print ("\n\t---------------------------------------------------------------")
		time.sleep (7200)				#2 hour

	except TweepError as e:
		if (e.api_code == 187):			#Code error --> Status duplicate
			print (">> ERROR!\n>> " + e.reason)
			pass

	except TweepError as e:
		api = bot_loggin_T ()
		api.update_status (status = 'heyyeyaaeyaaaeyaeyaa! @Zeby95')
		print (">> ERROR!\n>> " + e.reason)
		time.sleep (120)