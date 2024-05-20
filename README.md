# scholar_scraper 

Web scraper za pridobivanje vseh javnih clankov navedenih na profilu raziskovalca/ke ([google scholar](https://scholar.google.com/) ali [research gate](https://www.researchgate.net/)).

# OPOZORILO!!
**Uporaba na lastno odgovornost!**

**UPORABA SAMO ZA IZOBRAŽEVALNE IN RAZISKOVALNE NAMENE!**

# uporaba
V datoteko *profiles.json* je potrebno ROČNO vnesti polno ime,povezavo do profila raziskovalca/ke ([google scholar](https://scholar.google.com/) ali [research gate](https://www.researchgate.net/)) in ustanovo, kjer delajo.

V kolikor že imamo datoteko z imeni (1 ime v 1 vrsti), lahko to datoteko preimenujemo v `imena.txt` in v `main.py` zakomentiramo klic *main()* in odkomentiramo klic *create_jsonNames('imena.txt', NAMES_FILE)*.
Ta funkcija bo delno ustvarila json datoteko v pričakovanem formatu, vendar je še vedno potrebno ročno vnesti povezavo do uporabnikovega profila("profileUrl") in delavno mesto("researchFacility").

json datoteka po klicu *create_jsonNames('imena.txt', NAMES_FILE)*:
```json
[
	{"fullName": "John Doe", "profileUrl": "", "researchFacility": ""}, 
]
```

pričakovan končni format za *profiles.json*:
```json
[
	{"fullName": "John Doe", "profileUrl": "https://scholar.google.com/citations?user=<profile id>", "researchFacility": "UM"},
    {"fullName": "John2 Doe2", "profileUrl": "https://www.researchgate.net/profile/John-Doe", "researchFacility": "uni-lj"},
    ...
]
```

Ko smo v celoti izpolnili *profiles.json*, lahko zaženemo main.py, kot rezultat dobimo *articles.json*.

*articles.json* format
```json
[{
	"fullName": "John Doe",
	"profileUrl": "<url to user profile>",
    "researchFacility": "<work>",
    "interestTags": ["<ai or something>", ],
	"atricles": [
			{
				"title": "<title>",
				"url": "<article page url>",
				"year": "<published year>"
			},
		]
}, ]
```

# articles.json spletni pregled

zagon serverja: `python -m http.server`

dostop do spletne strani: `http://localhost:8000/frontend/index.html`


# ROBOTS.TXT

## https://scholar.google.com/robots.txt - 9.5.2024
```
User-agent: *
Disallow: /search
Disallow: /index.html
Disallow: /scholar
Disallow: /citations?
Allow: /citations?user=
Disallow: /citations?*cstart=
Disallow: /citations?user=*%40
Disallow: /citations?user=*@
Allow: /citations?view_op=list_classic_articles
Allow: /citations?view_op=metrics_intro
Allow: /citations?view_op=new_profile
Allow: /citations?view_op=sitemap
Allow: /citations?view_op=top_venues

User-agent: Twitterbot
Disallow:

User-agent: facebookexternalhit
Disallow:

User-agent: PetalBot
Disallow: /
```

## https://www.researchgate.net/robots.txt - 10.5.2024
```
User-agent: *
Allow: /
Disallow: /cdn-cgi/
Disallow: /connector/
Disallow: /plugins.
Disallow: /firststeps.
Disallow: /publicliterature.PublicLiterature.search.html
Disallow: /lite.publication.PublicationRequestFulltextPromo.requestFulltext.html
Disallow: /amp/authorize
Allow: /signup.SignUp.html$
Disallow: /signup.
```