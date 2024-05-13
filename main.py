from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

#NAMES_FILE = 'profiles.json'
NAMES_FILE = 'profiles_test.json' # shorter profiles.json
ARTICLES_FILE = 'atricles.json'

def getScholarArticlesLinks(trArticles) -> list:
	articleLinks = []
	aClass = 'gsc_a_at'

	for el in trArticles:
		aTag = el.find('a', {'class':aClass})

		articleObject = {}
		articleObject['title'] = aTag.text
		articleObject['url'] = 'https://scholar.google.com' + aTag.attrs['href']
		articleObject['year'] = el.find('span', {'class': 'gsc_a_h gsc_a_hc gs_ibl'}).text

		articleLinks.append(articleObject)

	return articleLinks

def parseScholarPage(profilePageUrl) -> list:
	loadMoreBtnId = 'gsc_bpf_more'
	articleTrElemClass = 'gsc_a_tr'

	# use headless browser (without gui)
	options = ChromeOptions()
	options.add_argument('--headless=new')
	driver = webdriver.Chrome(options=options)

	# make initial get request
	driver.get(profilePageUrl)

	# Get session cookies
	cookies = driver.get_cookies()
	time.sleep(0.5)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	loadMoreBtn = soup.find('button', {'id': loadMoreBtnId})

	while 'disabled' not in loadMoreBtn.attrs:
		moreBtn = driver.find_element(By.ID, loadMoreBtnId)
		moreBtn.click()

		time.sleep(2)  # DON'T DELETE!!!

		# Add session cookies to the browser session
		for cookie in cookies:
			driver.add_cookie(cookie)

		soup = BeautifulSoup(driver.page_source, 'html.parser')
		loadMoreBtn = soup.find('button', {"id": loadMoreBtnId})
		trs = soup.find_all('tr', {"class": articleTrElemClass})

		time.sleep(1)

	# close "browser" to save resources
	driver.quit()

	if trs == None:
		return []

	return getScholarArticlesLinks(trs)


def parseResearchGaetProfile(profilePageUrl) -> list:
	pass

def main():
	try:
		with open(NAMES_FILE, 'r', encoding='utf-8') as f:
			researchers = json.load(f)
			f.close()
	except FileNotFoundError:
		print(f'file {NAMES_FILE} not found')
		exit()

	profilesWithArticles = {}
	for researcher in researchers:
		profileUrl = researcher['profileUrl']

		if profileUrl == "":
			print(f"missing profileUrl for {researcher['fullName']}")
			continue

		profilesWithArticles['fullName'] = researcher['fullName']
		profilesWithArticles['profileUrl'] = profileUrl

		if profileUrl.startswith('https://scholar.google.com/'):
			profilesWithArticles['articles'] = parseScholarPage(profileUrl)
		elif profileUrl.startswith('https://www.researchgate.net/'):
			continue
			#profilesWithArticles['articles'] = parseResearchGaetProfile(profileUrl)
		else:
			print(f"unsuported profile {researcher['fullName']} ({profileUrl})")
			print("profile need to be either 'https://scholar.google.com/...' or 'https://www.researchgate.net/...'")
			print()

		time.sleep(5)  # Sleep between each requests to (hopefully) avoid google ip ban...

	with open(ARTICLES_FILE, 'w', encoding='utf-8') as json_file:
		json.dump(profilesWithArticles, json_file, ensure_ascii=False, indent=4)

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
