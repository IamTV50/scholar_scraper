from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import requests

#NAMES_FILE = 'profiles.json'
NAMES_FILE = 'profiles_test.json' # shorter profiles.json
ARTICLES_FILE = 'atricles.json'

def formArticleObject(title, articleUrl, releaseYear) -> list:
	articleObject = {}
	articleObject['title'] = title
	articleObject['url'] = articleUrl
	articleObject['year'] = releaseYear

	return articleObject

def getScholarArticlesLinks(trArticles) -> list:
	articleLinks = []
	aClass = 'gsc_a_at'

	for el in trArticles:
		aTag = el.find('a', {'class':aClass})

		tmpTitle = aTag.text
		tmpUrl = 'https://scholar.google.com' + aTag.attrs['href']
		tmpYear = el.find('span', {'class': 'gsc_a_h gsc_a_hc gs_ibl'}).text

		articleLinks.append(formArticleObject(tmpTitle, tmpUrl, tmpYear))

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

def getResearchGateAtricleLinks(articleCards) -> list:
	articlesLinks = []
	aClass = 'nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare'
	yearLiClass = 'nova-legacy-e-list__item nova-legacy-v-publication-item__meta-data-item'

	for el in articleCards:
		aTag = el.find('a', {'class': aClass})
		year = el.find('li', {'class': yearLiClass}).text.split()[1] if el.find('li', {'class': yearLiClass}) else None

		tmpTitle = aTag.text
		tmpUrl = aTag.attrs['href']
		tmpYear = year

		articlesLinks.append(formArticleObject(tmpTitle, tmpUrl, tmpYear))

	return articlesLinks


def parseResearchGaetProfile(profilePageUrl) -> list:
	researchItemsDivId = 'research-items'
	publicationCardClass = 'nova-legacy-o-stack__item'

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36"
	}

	articleLinks = []
	pageNum = 1
	while True:
		if pageNum == 1:
			response = requests.get(profilePageUrl, headers=headers)
		else:
			response = requests.get(profilePageUrl + '/' + str(pageNum), headers=headers)

		research = BeautifulSoup(response.text, 'html.parser')
		cardsBody = research.find('div', {'id': researchItemsDivId})

		if cardsBody == None:
			break

		researchCards = cardsBody.find_all('div', {'class': publicationCardClass})
		articleLinks.extend(getResearchGateAtricleLinks(researchCards))

		pageNum += 1
		time.sleep(0.5)

	return articleLinks

def main():
	try:
		with open(NAMES_FILE, 'r', encoding='utf-8') as f:
			researchers = json.load(f)
			f.close()
	except FileNotFoundError:
		print(f'file {NAMES_FILE} not found')
		exit()

	profilesWithArticles = []
	for researcher in researchers:
		profileUrl = researcher['profileUrl']

		if profileUrl == "":
			print(f"missing profileUrl for {researcher['fullName']}")
			continue

		fullProfile = {}
		fullProfile['fullName'] = researcher['fullName']
		fullProfile['profileUrl'] = profileUrl

		if profileUrl.startswith('https://scholar.google.com/'):
			fullProfile['articles'] = parseScholarPage(profileUrl)
			time.sleep(5)  # Sleep between each requests to (hopefully) avoid google ip ban...
		elif profileUrl.startswith('https://www.researchgate.net/'):
			fullProfile['articles'] = parseResearchGaetProfile(profileUrl)
			time.sleep(2)
		else:
			print(f"unsuported profile {researcher['fullName']} ({profileUrl})")
			print("profile need to be either 'https://scholar.google.com/...' or 'https://www.researchgate.net/...'")
			print()

		profilesWithArticles.extend(fullProfile)


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
