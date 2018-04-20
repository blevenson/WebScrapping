import sys
import webbrowser

from bs4 import BeautifulSoup
import requests

tor_path = 'open -a /Applications/TorBrowser.app %s'

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

	# Collect the links to all the websites
	watchLinks = []
	for link in soup.findAll("div", {"class": "ll-item"}):
		watchLinks.append(link.find('a', {"class": "watch-button"}, href=True).get('href', ''))

	# Navigate to each site, if that doesn't work, launch the next
	try:
		for newSite in watchLinks:
			req = requests.get(newSite)
			soup = BeautifulSoup(req.text, "html.parser")

			link = soup.find("a", {"class" : "watch-button actWatched", "rel" : "nofollow"})
			
			reqWatch = requests.get(link.get('href', ''))	
			soup = BeautifulSoup(reqWatch.text, "html.parser")


			# If video not there, skip it
			failedKeys = ("not found", "deleted", "404", "expired", "sorry", "403", "forbidden")
			if any(s in soup.text.lower() for s in failedKeys):
				print "Failed: ", link.get('href', '')
				continue
				
			webbrowser.get(tor_path).open(link.get('href', ''))

	except (KeyboardInterrupt, SystemExit):
		sys.exit()



# Call with arugments: python TVParser3.0.py [TV-Show-Name] [season #] [episode #]
def main():
	link = "http://www.watchepisodeseries.com/" + sys.argv[1].lower()
	season = sys.argv[2]
	episode = sys.argv[3]
	openWebBrowser(link, season, episode)



if __name__ == "__main__":
    main()