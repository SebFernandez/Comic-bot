#This code does web scraping, so urls are going to be dynamic.

import os, requests, time, random
from cred_T import *
from tweepy import *
from bs4 import BeautifulSoup

class comic:
	def __init__ (self, comicName, comicAuthor, url, hashtag):
		self.comicName = comicName
		self.comicAuthor = comicAuthor
		self.url = url 						#Link to fetch
		self.download = ''					#Link to download
		self.date = ''
		self.hashtag = hashtag

snoopy = comic ('Peanuts', 'Charles M. Schulz', 'https://www.gocomics.com/random/peanuts', '#Snoopy #CharlieBrown #Woodstock')
garfield = comic ('Garfield', 'Jim Davis', 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/', '#Garfield #Odie #Jon')
cyanide = comic ('Cyanide & happiness', 'author', 'http://explosm.net/comics/random/', '#CyanideAndHappiness')	#Cyanide has a group of authors, certain info is completed on ComicTweet ()
calvinHobbes = comic ('Calvin and Hobbes', 'Bill Watterson', 'https://www.gocomics.com/random/calvinandhobbes', '#CalvinAndHobbes')
foxtrot = comic ('Foxtrot', 'Bill Amend', 'https://www.gocomics.com/random/foxtrot', '#Foxtrot')
chickens = comic ('Savage Chickens', 'Doug Savage', 'https://www.gocomics.com/random/savage-chickens', '#SavageChickens')
horse = comic ('Dark side of the horse', 'Samson', 'https://www.gocomics.com/random/darksideofthehorse', '#DarkSideOfTheHorse')
longStoryShort = comic ('Long Story short', 'Daniel Beyer', 'https://www.gocomics.com/random/long-story-short', '#LongStoryShort')
fMinus = comic ('F Minus', 'Tony Carrillo', 'https://www.gocomics.com/random/fminus', '#FMinus')
dilbert = comic ('Dilbert', 'Scott Adams', 'https://www.gocomics.com/random/dilbert-classics', '#Dilbert')
offTheMark = comic ('Off the mark', 'Mark Parisi', 'https://www.gocomics.com/random/offthemark', '#OffTheMark')
bc = comic ('B.C', 'Mastrolanni and Hart', 'https://www.gocomics.com/random/bc', '#BC #AC #DC #Caveman')

popeye = comic ('Popeye', 'Elzie Crisler Segar', 'http://comicskingdom.com/popeye/', '#Popeye #OliveOyl #Spinach')

comicArray = [snoopy, garfield, cyanide, calvinHobbes, foxtrot, chickens, horse, longStoryShort, fMinus, dilbert, offTheMark, bc]

def botLogin ():																	#Log to Twitter
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)
	return api

def write (comicStrip):
	error = '>> ERROR! Requests -> '

	try:
		f = open ('comic.jpg', 'wb')
		f.write (requests.get (comicArray [comicStrip].download).content)												
		f.close 

	except requests.exceptions.ConnectionError as e:    							# This is the correct syntax
		print (error + str (e))
	except requests.exceptions.Timeout as e:
		print (error + str (e))
	    # Maybe set up for a retry, or continue in a retry loop
	except requests.exceptions.TooManyRedirects as e:
		print (error + str (e))
	    # Tell the user their URL was bad and try a different one
	except requests.exceptions.RequestException as e:
		    # catastrophic error. bail.
		print (error + str (e))

	except requests.exceptions.HTTPError as e:
		print (error + str (e)) 	

def comicTweet (comicStrip):													#Here decides which comic strip will tweet
	try:
		if (comicStrip == 0):
			fetchData (comicStrip)

		elif (comicStrip == 1 ):
			YY = random.randrange (2000, time.localtime(time.time()).tm_year) 						#To have the years up to date.
			MM = random.randrange (1,12)
			if (MM % 2 == 0):
				DD = random.randrange (1, 30)
			else:
				DD = random.randrange (1,31)

			garfield.date = str (DD) + '/' + str (MM) + '/' + str (YY)

			if (DD < 10 and MM < 10):													#Format to access at the URL picture.
				garfield.download = garfield.url + str (YY) + '/' + str (YY) + '-0' + str (MM) + '-0' + str (DD) + '.gif'
			elif (DD < 10):
				garfield.download = garfield.url + str (YY) + '/' + str (YY) + '-' + str (MM) + '-0' + str (DD) + '.gif'
			elif (MM < 10):
				garfield.download = garfield.url + str (YY) + '/' + str (YY) + '-0' + str (MM) + '-' + str (DD) + '.gif'
			else:
				garfield.download = garfield.url + str (YY) + '/' + str (YY) + str (MM) + str (DD) + '.gif'

		elif (comicStrip == 2):
			URL = requests.get (cyanide.url)

			soup = BeautifulSoup (URL.content, 'html.parser')
			img = soup.find_all (id = 'main-comic')
			cyanide.download = 'http:' + img[0].get ('src')
			
			auxString = soup.find_all (class_ = 'author-credit-name')
			auxString = auxString [0].get_text ()
			cyanide.comicAuthor = auxString [3: len (auxString)]

			auxString = soup.find_all (class_ = 'zeta small-bottom-margin past-week-comic-title')
			cyanide.date = auxString [0].get_text ()
			cyanide.date = cyanide.date.replace ('.', '/')

		elif (comicStrip == 3):
			fetchData (comicStrip)
		
		elif (comicStrip == 4):
			fetchData (comicStrip)

		elif (comicStrip == 5):
			fetchData (comicStrip)

		elif (comicStrip == 6):
			fetchData (comicStrip)

		elif (comicStrip == 7):
			fetchData (comicStrip)
		
		elif (comicStrip == 8):
			fetchData (comicStrip)
	
		elif (comicStrip == 9):
			fetchData (comicStrip)
	
		elif (comicStrip == 10):
			fetchData (comicStrip)

		elif (comicStrip == 11):
			fetchData (comicStrip)

	except:
		print ('\n\t\t-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-\n')
		pass

def fetchData (comicStrip):										#This function fetchs data from the same source for different comic strips.
	URL = requests.get (comicArray [comicStrip].url)

	soup = BeautifulSoup (URL.content, 'html.parser')
	img = soup.find_all ('picture')
	auxString = img [1]
	auxString = auxString.find_all ('img')
	comicArray [comicStrip].download = auxString [0].get ('src')
	
	auxString = soup.find_all (class_="btn-calendar-nav item-control gc-calendar-wrapper js-calendar-wrapper")
	auxString = auxString [0].get ('data-date')
	YY = auxString [0:4]
	MM = auxString [5:7]
	DD = auxString [8:11]
	comicArray [comicStrip].date = DD + '/' + MM + '/' + YY

def log (comicStrip):
	print (">> Comic: \t" + comicArray [comicStrip].comicName)
	print (">> URL: \t" + comicArray [comicStrip].download)
	print (">> Date: \t" + comicArray [comicStrip].date) 
	print (">> AUTOR: \t" + comicArray [comicStrip].comicAuthor)
	print (">> Time: \t" + str (time.localtime (time.time()).tm_hour) + ":" + str (time.localtime (time.time()).tm_min))
	print (">> Tweet!\n\t---------------------------------------------------------------")

def upload ():
	bot = botLogin ()
	comicStrip = random.randrange (0,12)
	comicTweet (comicStrip)
	write (comicStrip)
	tweetLine = comicArray [comicStrip].comicName + ', made by: ' + comicArray [comicStrip].comicAuthor + '.\nDate: ' + comicArray [comicStrip].date + '\n\n#Comics ' + comicArray [comicStrip].hashtag
	bot.update_with_media (filename = 'comic.jpg', status = tweetLine)
	log (comicStrip)

while True:
	try:
		upload ()
		time.sleep (7200)

	except TweepError as e:
		print (">> ERROR!\n>>" + e.reason + "\n\t---------------------------------------------------------------")
		pass
