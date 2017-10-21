import sys
import webbrowser

from bs4 import BeautifulSoup
import requests
import time


'''
	Script for opening up a tv show and incrementing the count

	Run with the name of the television show(with spaces replaced with "_") and the csv file.  After the video loads
	it prompts the user if it worked, typing "yes" will increase the count in the show, aware of seasons.  If there are
	no more shows it will record the date date finished.  Saying "no" will show the next website link it found until it 
	runs out.

	TV Shows stored in a csv file using the format:
	showName, showURL, startDate, Season, Episode, DateFinished

	Append sites to APPROVED_SITES to allow more websites to be parsed

	@author Brett Levenson
'''

# Approved sites to stream from in order of prefrence
APPROVED_SITES = ["lolzor.com"]

def openWebBrowser(url, season, episode):
	# webbrowser.open(url)

	r  = requests.get(url)

	data = r.text

	soup = BeautifulSoup(data, "html.parser")

	websiteLink = ""
	checkFor = ("season-" + season + "-episode-" + episode + "-s")
	for link in soup.find_all('a'):
		# print "Link: " + link.get('href')
		if(checkFor in link.get('href', '')):
			websiteLink = link.get('href', '')

	# We have the link to go to, go there
	soup = BeautifulSoup(requests.get(websiteLink).text, "html.parser")
	# webbrowser.open(websiteLink)

	# Collect the links to all the approved websites
	watchLinks = []
	for link in soup.find_all('a'):
		for approvedSite in APPROVED_SITES:
			try:
				if(approvedSite in link.string):
					watchLinks.append(link.get('href', ''))
			except TypeError:
				pass

	# Navigate to each site, if that doesn't work, launch the next
	for newSite in watchLinks:
		soup = BeautifulSoup(requests.get(watchLinks[0]).text, "html.parser")

		for link in soup.findAll("a", {"class" : "watch-button actWatched", "rel" : "nofollow"}):
			webbrowser.open(link.get('href', ''))

		if("y" in raw_input("Did that work? ")):
			return True
	return False


def incrementTheEpisode(fileName, fullFile, showData):
	allShowsData = fullFile.splitlines(True)
	showIndex = allShowsData.index(','.join(showData))

	f = open(fileName, "w+")
	f.write(''.join(allShowsData[ : showIndex]))

	if(doesEpisodeExist(showData[1], showData[3], (int(showData[4]) + 1))):
		# Increment episode
		f.write(showData[0] + "," + showData[1] + "," + showData[2] + "," + showData[3] + "," + str(int(showData[4]) + 1) + "," + showData[5])
	elif(doesEpisodeExist(showData[1], (int(showData[3]) + 1), 1)):
		# Increment season and reset episode
		f.write(showData[0] + "," + showData[1] + "," + showData[2] + "," + str(int(showData[3]) + 1) + ",1," + showData[5])
	else:
		# Done with show
		print("I'm sorry, but I think you are done with this show! :(")
		f.write(showData[0] + "," + showData[1] + "," + showData[2] + "," + showData[3] + "," + showData[4] + "," + (time.strftime("%m/%d/%Y")))

	f.write(''.join(allShowsData[showIndex + 1 : ]))
	f.close()

def doesEpisodeExist(url, season, episode):
	soup = BeautifulSoup(requests.get(url).text, "html.parser")
	for link in soup.find_all('a'):
		try:
			if(("season-" + str(season) + "-episode-" + str(episode) + "-s") in link.get('href', '')):
				return True
		except TypeError:
			pass
	return False


def getTVURL(tvShow):
	# Make the string formatted.  No special marks
	return "http://www.watchepisodeseries.com/" + tvShow.replace(" ", "-").lower().replace("'", "")

def createNewCSVFile(fileName):
	f = open(fileName,"w+")
	f.write("")
	f.close()

def addShowToFile(tvShow, fileName):
	f = open(fileName, "a+")
	saving = tvShow + "," + getTVURL(tvShow) + "," + (time.strftime("%m/%d/%Y")) + ",1,1,NA\n"
	f.write(saving)
	f.close()
	return saving

def main():
	tvShow = ""
	fileName = ""

	# Ask user for parameters
	if(len(sys.argv) == 1):
		print("Welcome to the TV binge watching tool")
		tvShow = raw_input("TV Show: ")
		fileName = raw_input("TV Show file: ")

	# Paramaters: tvShow, fileName
	elif(len(sys.argv) == 3):
		tvShow = sys.argv[1].replace("_", " ")
		fileName = sys.argv[2]

	# Read parameters from terminal, using default fileName
	else:
		fileName = "tvShows.csv"
		tvShow = sys.argv[1].replace("_", " ")

	# Check that they are using a cpp file
	if(".csv" not in fileName):
		sys.exit("ERROR:\tAll the TV shows should be saved using a csv file format")

	#Check whether the filename was passed in with an unnessary closing slash ("/")
	if(fileName.endswith('/')):
		print("Warning:\tthe parameters should be files, not directories.  Don't worry, I'll take care of it...this time.")
		fileName = fileName[:-1]


	# Ready to parse file
	data = ""
	fullFileData = ""
	try:
		with open(fileName, 'rU') as myFile:
			for line in myFile:
				if(tvShow.lower() in line.lower()):
					data = line
				fullFileData += line
	except IOError:
		# If the file doesn't exist, show the user the other options
		if("y" in raw_input("Warning:\t" + fileName + " does not exist.  Would you like me to create a new file?")):
			createNewCSVFile(fileName)
		else:
			return

	# TV Show not in data base
	if(data == ""):
		print("Warning:\tFailed to find " + tvShow + " in the database.")
		checkURLStatus = requests.get(getTVURL(tvShow))

		if(checkURLStatus.status_code != 200):
			sys.exit("ERROR:\tTV Show name not recognized.  Please check the spelling")

		if("y" in raw_input("Would you like me to add it to the file?")):
			data = addShowToFile(tvShow, fileName)
		else:
			return

	dataList = data.split(",")

	url = dataList[1]
	season = dataList[3]
	episode = dataList[4]

	print "Now streaming: " + dataList[0] + " Season: " + season + " Episode: " + episode
	
	if(openWebBrowser(url, season, episode)):
		print("Thank you, enjoy the show!")
		incrementTheEpisode(fileName, fullFileData, dataList)
	else:
		print("I'm sorry, better luck next time")


if __name__ == "__main__":
    main()