# WEB SCRAPER

Web scraper for resarch.

# OPOZORILO!!
**Uporaba na lastno odgovornost!!!!**

Koda izvaja nekatere operacije, ki so v [robots.txt](#robotstxt) NEDOVOLJENE! To lahko vodi do tega, da Google uporabniku onemogoči dostop za nedoločen čas.
Program se temu poskuša izognit z uporabo pavze med vsakim zahtevkom.

**UPORABA SAMO ZA IZOBRAŽEVALNE IN RAZISKOVALNE NAMENE!**

# uporaba
V datoteko *profiles.json* je potrebno ROČNO vnesti polno ime in povezavo do profila raziskovalca/ke (https://scholar.google.com/ ali https://www.researchgate.net/).

V kolikor že imamo datoteko z imeni (1 ime v 1 vrsti), lahko to datoteko preimenujemo v `imena.txt` in v `main.py` zakomentiramo klic *main()* in odkomentiramo klic *create_jsonNames('imena.txt', NAMES_FILE)*.
Ta funkcija bo delno ustvarila json datoteko v pričakovanem formatu, vendar je še vedno potrebno ročno vnesti povezavo do uporabnikovega profila.

json datoteka po klicu *create_jsonNames('imena.txt', NAMES_FILE)*:
```json
[
	{"fullName": "John Doe", "scholarUrl": ""}, 
]
```

pričakovan format končni:
```json
[
	{"fullName": "John Doe", "scholarUrl": "https://scholar.google.com/citations?user=<profile id>"},
    {"fullName": "John2 Doe2", "scholarUrl": "https://www.researchgate.net/profile/John-Doe"},
    ...
]
```

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