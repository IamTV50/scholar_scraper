# GOOGLE SCOLAR SCRAPER

Web scraper za pridobitev javnih člankov od ljudi navedenih v datoteki *names.txt* iz strani google scholar.

# OPOZORILO!!
**Uporaba na lastno odgovornost!!!!**

Koda izvaja nekatere operacije, ki so v [robots.txt](#robotstxt-952024) NEDOVOLJENE! To lahko vodi do tega, da Google uporabniku onemogoči dostop za nedoločen čas.
Program se temu poskuša izognit z uporabo pavze med vsakim zahtevkom.

**UPORABA SAMO ZA IZOBRAŽEVALNE IN RAZISKOVALNE NAMENE!**

## robots.txt (9.5.2024)
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