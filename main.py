from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

NAMES_FILE = 'profiles.json'
#NAMES_FILE = 'profiles_test.json' # shorter profiles.json
ARTICLES_FILE = 'articles.json'
INTEREST_TAGS = ['Recommender systems', 'natural language processing', 'language technologies', 'data mining', 'text mining']

"""
If USE_INTEREST_TAGS is set to True:
- Articles are retrieved only for users whose profile includes at least one interest tag 
  listed in the INTEREST_TAGS array.
- Case-insensitive comparisons are used for tag matching.
- If a user has no interest tags listed, articles from their profile are still retrieved.

If USE_INTEREST_TAGS is set to False:
- Articles are retrieved from all user profiles, regardless of their interest tags.
"""
USE_INTEREST_TAGS = True

INTEREST_TAGS = [tag.lower() for tag in INTEREST_TAGS]

def formArticleObject(title, articleUrl, releaseYear) -> list:
	articleObject = {}
	articleObject['title'] = title
	articleObject['url'] = articleUrl
	articleObject['year'] = releaseYear

	return articleObject

def checkIfUserTagsAreInteresting(userTags: list) -> bool:
	for tag in userTags:
		if tag.lower() in INTEREST_TAGS:
			return True

	return False

def getScholarArticlesLinks(trArticles) -> list:
	articleLinks = []
	aClass = 'gsc_a_at'
	yearClass = 'gsc_a_h gsc_a_hc gs_ibl'

	for el in trArticles:
		aTag = el.find('a', {'class':aClass})

		tmpTitle = aTag.text
		tmpUrl = 'https://scholar.google.com' + aTag.attrs['href']
		tmpYear = el.find('span', {'class': yearClass}).text if el.find('span', {'class': yearClass}).text != "" else None

		articleLinks.append(formArticleObject(tmpTitle, tmpUrl, tmpYear))

	return articleLinks

def getScholarProfileTags(profileBs4) -> list:
	tagsDivId = 'gsc_prf_int'
	tagClass = 'gsc_prf_inta gs_ibl'
	tags = []

	tagsContainger = profileBs4.find('div', {'id': tagsDivId})
	if tagsContainger == None:
		return tags

	for tag in tagsContainger.find_all('a', {'class':tagClass}):
		tags.append(tag.text)

	return tags

def parseScholarPage(profilePageUrl) -> dict:
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
	userInterestTags = getScholarProfileTags(soup)

	if USE_INTEREST_TAGS and len(userInterestTags) > 0 and checkIfUserTagsAreInteresting(userInterestTags) == False:
		driver.quit()
		return {'urls': [],'tags': []}

	loadMoreBtn = soup.find('button', {'id': loadMoreBtnId})

	if 'disabled' in loadMoreBtn.attrs:
		trs = soup.find_all('tr', {"class": articleTrElemClass})
	else:
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

	return {'urls': getScholarArticlesLinks(trs) if trs != None else [], 'tags': userInterestTags if userInterestTags != None else []}

def getResearchGateArticleLinks(articleCards) -> list:
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

def getResearchGateProfileTags(profileBs4) -> list:
	tagsDivContainerClass = 'nova-legacy-l-flex__item nova-legacy-l-flex nova-legacy-l-flex--gutter-xs nova-legacy-l-flex--direction-row@s-up nova-legacy-l-flex--align-items-stretch@s-up nova-legacy-l-flex--justify-content-flex-start@s-up nova-legacy-l-flex--wrap-wrap@s-up js-target-skills'
	tagClass = 'nova-legacy-l-flex__item'
	tags = []

	tagsContainger = profileBs4.find('div', {'class': tagsDivContainerClass})
	if tagsContainger == None:
		return tags

	for tag in tagsContainger.find_all('div', {'class': tagClass}):
		tags.append(tag.a.text)

	return tags

def parseResearchGateProfile(profilePageUrl) -> dict:
	researchItemsDivId = 'research-items'
	publicationCardClass = 'nova-legacy-o-stack__item'

	options = ChromeOptions()
	# options.add_argument("--headless")  # Run the browser in headless mode
	driver = webdriver.Chrome(options=options)  # Path to your ChromeDriver

	articleLinks = []
	pageNum = 1
	while True:
		profileUrl = profilePageUrl if pageNum == 1 else f'{profilePageUrl}/{str(pageNum)}'
		driver.minimize_window()
		driver.get(profileUrl)
		time.sleep(2)  # Add a delay to allow the page to load

		# Now, grab the page source
		page_source = driver.page_source
		research = BeautifulSoup(page_source, 'html.parser')

		if pageNum == 1:
			userInterestTags = getResearchGateProfileTags(research)
			if USE_INTEREST_TAGS and len(userInterestTags) > 0 and not checkIfUserTagsAreInteresting(userInterestTags):
				break

		cardsBody = research.find('div', {'id': researchItemsDivId})

		if cardsBody is None:
			break

		researchCards = cardsBody.find_all('div', {'class': publicationCardClass})
		articleLinks.extend(getResearchGateArticleLinks(researchCards))

		pageNum += 1
		time.sleep(0.5)  # Add a small delay between page loads

	driver.quit()  # Close the browser

	return {'urls': articleLinks, 'tags': userInterestTags if userInterestTags != None else []}

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
			print(f"MISSING profileUrl for {researcher['fullName']}")
			continue

		parsed = {}
		if profileUrl.startswith('https://scholar.google.com/'):
			parsed = parseScholarPage(profileUrl)
			time.sleep(5)  # Sleep between each requests to (hopefully) avoid google ip ban...
		elif profileUrl.startswith('https://www.researchgate.net/'):
			parsed = parseResearchGateProfile(profileUrl)
			time.sleep(3)
		else:
			print(f"unsuported profile {researcher['fullName']} ({profileUrl})")
			print("profile need to be either 'https://scholar.google.com/...' or 'https://www.researchgate.net/...'")
			print()

		# only add profiles with at least 1 article
		if len(parsed['urls']) == 0:
			print(f'SKIPPED {researcher["fullName"]}')
			continue

		print(f'parsing {researcher["fullName"]}')

		fullProfile = {}
		fullProfile['fullName'] = researcher['fullName']
		fullProfile['profileUrl'] = profileUrl
		fullProfile['researchFacility'] = researcher['researchFacility'] if researcher['researchFacility'] != '' else None
		fullProfile['interestTags'] = parsed['tags']
		fullProfile['articles'] = parsed['urls']

		profilesWithArticles.append(fullProfile)

	with open(ARTICLES_FILE, 'w', encoding='utf-8') as json_file:
		json.dump(profilesWithArticles, json_file, ensure_ascii=False, indent=4)

def create_jsonNames(input_file, output_file):
	researchers = []
	encountered_names = set()

	with open(input_file, 'r', encoding='utf-8') as file:
		for line in file:
			if line.strip() == "":
				continue

			name = line.strip().lower()  # Convert name to lowercase for case-insensitive comparison
			if name in encountered_names:
				continue  # Skip duplicate name
			else:
				encountered_names.add(name)

			researcher = {"fullName": line.strip(), "profileUrl": ""}
			researchers.append(researcher)

	with open(output_file, 'w', encoding='utf-8') as json_file:
		json.dump(researchers, json_file, ensure_ascii=False, indent=4)



# 1. run this and fill profile url by hand (google scholar or https://www.researchgate.net/ profile)
# 			OR
# create whole profiles.json by hand
#create_jsonNames('imena.txt', NAMES_FILE)

# 2. run main
main()
