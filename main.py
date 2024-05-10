from bs4 import BeautifulSoup
import requests
import time
import json

NAMES_FILE = 'profiles.json'

def getSoupPage(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36"
	}
	responsePage = requests.get(url, headers=headers)

	soup = BeautifulSoup(responsePage.text, 'html.parser')
	return soup

def parseScholarPage(profilePage):
	pass

def parseResearchGaetProfile(profilePage):
	pass

def main():
	with open(NAMES_FILE, 'r', encoding='utf-8') as f:
		researchers = json.load(f)
		f.close()

	for researcher in researchers:
		print(researcher)
		profileUrl = researcher['profileUrl']

		if profileUrl == "":
			print(f"missing profileUrl for {researcher['fullName']}")
			continue

		htmlProfile = getSoupPage(profileUrl)

		if profileUrl.startswith('https://scholar.google.com/'):
			parseScholarPage(htmlProfile)
		elif profileUrl.startswith('https://www.researchgate.net/'):
			parseResearchGaetProfile(htmlProfile)
		else:
			print(f"unsuported profile {researcher['fullName']} ({profileUrl})")
			print("profile need to be either 'https://scholar.google.com/...' or 'https://www.researchgate.net/'")
			print()


		time.sleep(5)  # Sleep between each requests to (hopefully) avoid google ip ban...

def create_jsonNames(input_file, output_file):
	researchers = []
	with open(input_file, 'r', encoding='utf-8') as file:
		for line in file:
			if line == "\n" or line == "":
				continue

			name = line.strip()
			researcher = {"fullName": name, "profileUrl": ""}
			researchers.append(researcher)

	with open(output_file, 'w', encoding='utf-8') as json_file:
		json.dump(researchers, json_file, ensure_ascii=False, indent=4)



# 1. run this and fill profile url by hand (google scholar or https://www.researchgate.net/ profile)
# 			OR
# create whole profiles.json by hand
#create_jsonNames('imena.txt', NAMES_FILE)

# 2. run main
main()
