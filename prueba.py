#This code does web scraping, so urls are going to be dynamic.

import os, requests, time, random
from cred_T import *
from tweepy import *
from bs4 import BeautifulSoup

class comic:
	def __init__ (self, comicName, comicAuthor, url, hashtag):
		self.comicName = comicName
		self.comicAuthor = comicAuthor
		self.url = url
		self.date = ''
		self.hashtag = hashtag

snoopy = comic ('Peanuts', 'Charles M. Schulz', 'https://www.peanuts.com/comics/#', '#Snoopy #CharlieBrown #Woodstock')
garfield = comic ('Garfield', 'Jim Davis', 'https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/', '#Garfield #Odie #Jon')
cyanide = comic ('Cyanide & happiness', 'author', 'http://explosm.net/comics/random/', '#CyanideAndHappiness')								#Cyanide has a group of authors, certain info is completed on ComicTweet ()

comicArray = [snoopy, garfield, cyanide]

def botLoggin ():											#Log to Twitter
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)
	return api

def write (comicStrip):
	error = '>> ERROR! Requests -> '

	try:
		f = open ('comic.jpg', 'wb')
		f.write (requests.get (comicArray [comicStrip].url).content)												#Requests code for Snoopy! (!)									#Peanuts web has some issues with URLs
		f.close 

	except requests.exceptions.ConnectionError as e:    # This is the correct syntax
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

def comicTweet (comicStrip):										#Here decides which comic strip will tweet
	if (comicStrip == 0):
		url = snoopy (fecha)
	elif (comicStrip == 1 ):
		YY = random.randrange (2000, time.localtime(time.time()).tm_year) #To have the years up to date.
		MM = random.randrange (1,12)
		if (MM % 2 == 0):
			DD = random.randrange (1, 30)
		else:
			DD = random.randrange (1,31)

		garfield.date = str (DD) + '/' + str (MM) + '/' + str (YY)

		if (DD < 10 and MM < 10):						#Format to access at the URL picture.
			garfield.url = garfield.url + str (YY) + '/' + str (YY) + '-0' + str (MM) + '-0' + str (DD) + '.gif'
		elif (DD < 10):
			garfield.url = garfield.url + str (YY) + '/' + str (YY) + '-' + str (MM) + '-0' + str (DD) + '.gif'
		elif (MM < 10):
			garfield.url = garfield.url + str (YY) + '/' + str (YY) + '-0' + str (MM) + '-' + str (DD) + '.gif'
		else:
			garfield.url = garfield.url + str (YY) + '/' + str (YY) + str (MM) + str (DD) + '.gif'

	elif (comicStrip == 2):
		URL = requests.get (cyanide.url)

		soup = BeautifulSoup (URL.content, 'html.parser')
		img = soup.find_all (id = 'main-comic')
		cyanide.url = 'http:' + img[0].get ('src')
		
		auxString = soup.find_all (class_ = 'author-credit-name')
		auxString = auxString [0].get_text ()
		cyanide.comicAuthor = auxString [3: len (auxString)]

		auxString = soup.find_all (class_ = 'zeta small-bottom-margin past-week-comic-title')
		cyanide.date = auxString [0].get_text ()
		cyanide.date = cyanide.date.replace ('.', '/')

def log (comicStrip):
	print (">> Comic: \t" + comicArray [comicStrip].comicName)
	print (">> URL: \t" + comicArray [comicStrip].url)
	print (">> Date: \t" + comicArray [comicStrip].date) 
	print (">> AUTOR: \t" + comicArray [comicStrip].comicAuthor)
	print (">> Time: \t" + str (time.localtime (time.time()).tm_hour) + ":" + str (time.localtime (time.time()).tm_min))
	print (">> Tweet!\n\t---------------------------------------------------------------")

def upload ():
	bot = botLoggin ()
	comicStrip = random.randrange (0,2) + 1
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