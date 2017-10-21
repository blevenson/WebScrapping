import sys
import webbrowser

from bs4 import BeautifulSoup
import requests


'''
	Script for opening up a tv show and incrementing the count

	Run with the file name of the tv show

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
	checkFor = ("season-" + season + "-episode-" + episode)
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


def incrementTheEpisode():
	pass

def main():
	fileName = ""

	# Ask user for parameters
	if(len(sys.argv) == 1):
		print("Welcome to the TV binge watching tool")
		fileName = "/Users/Blevenson/Desktop/Other/TV Shows/" + raw_input("TV show name: ").replace(" ", "") + ".rtf"

	# Read parameters from terminal
	else:
		fileName = sys.argv[1]

	# Check that they are using a cpp file
	if(".rtf" not in fileName):
		print("Warning:\tAll the TV shows are saved using textEdit's rich text format(rtf)")

	#Check whether the filename was passed in with an unnessary closing slash ("/")
	if(fileName.endswith('/')):
		print("Warning:\tthe parameters should be files, not directories.  Don't worry, I'll take care of it...this time.")
		fileName = fileName[:-1]


	# Ready to parse file
	try:
		with open(fileName, 'r') as myFile:
			data = myFile.read()
	except IOError:
		# If the file doesn't exist, show the user the other options
		webbrowser.open("file:///Users/Blevenson/Desktop/Other/TV%20Shows/")
		sys.exit(fileName + " does not exist")

	url = data[data.index("HYPERLINK") + 11 : data.index("\"}}")]

	# Remove used data
	data = data[data.index("Season:") : ]
	season = data[8 : data.index("\\")]

	data = data[data.index("Episode:") : ]
	episode = data[9 : data.index("\\")]

	if(openWebBrowser(url, season, episode)):
		print("Thank you, enjoy the show!")
		incrementTheEpisode()
	else:
		print("I'm sorry, better luck next time")


if __name__ == "__main__":
    main()