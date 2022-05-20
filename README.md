# Energie Prijzen Bot 2.0

Een Telegram bot die de dagelijkse actuele inkoop energie prijzen verwerkt en toont. Dit is versie 2 van de Bot. Op een gegeven moment kreeg ik zoveel aanvragen van nieuwe features dat ik echt opnieuw moest beginnen omdat de eerste versie niet was gebouwd op het invoeren van extra features.

Op moment van Livegang van 2.0 zal de eerste versie gearchiveerd gaan worden. De Bot blijft werken zoals hij eerder werkte.

## Omschrijving
Een Telegram bot die de dagelijkse actuele inkoop energie prijzen verwerkt en toont die gebruikt worden door Frank Energie, ANWB, EnergieZero, EasyEnergy, Tibber, Nieuwestroom, LeasePlan Energy, MijnDomein Energie.

Blijf up to date met de laagste stroom en gas tarieven.

Je hoeft zelf dit script niet te draaien als je nu al informatie wilt ontvangen. Open telegram en meld je aan bij de telegram [@EnergiePrijzen_bot](https://t.me/EnergiePrijzen_bot)

**Vergeet niet te doneren!**
[Doneer voor een kop koffie](https://donorbox.org/tvdsluijs-github)

## Opstarten
Als je dit script wilt draaien kan dat direct via python
`src/python main.py`

of via de docker file
`docker build -t energie-prijzen-bot .`

ga daarna in de data folder staan en
`docker run -d energie-prijzen-bot -v $(pwd)/data:/src/data`

Vergeet niet dat je een Telegram bot moet aanmaken en daar de HTTP API Token moet kopiëren.

Een Telegram bot maak je via de @BotFather

De Token plaats je in `./config/config.conf` een voorbeeld van de config vind je in config.sample

###  Afhankelijkheden
- Python 3.8 (minimum)
- Telegram bot token
- Docker

#### Docker extra's
**Lijstje van al je docker containers**
`docker ps -a`

**Lijstje van alle container ids**
`docker ps -aq`

**Vind het pad naar de data**
`docker volume inspect <dockerid>`

**Data staat in**
/var/lib/docker/volumes/<dockerid>/_data

**Stop and verwijder container**
docker stop CONTAINER_ID
docker rm CONTATINER_ID

**Docker log files**
docker container logs CONTATINER_ID

### Installeren

Voordat je main.py kan draaien moet je eerst een environment maken

`python -m venv .venv`

Daarna (als je env is opgestart) draai je pip install

`pip  install  --no-cache-dir  -r  /src/requirements.txt`

En daarna kan je het script draaien!

`python main.py`

Je kan natuurlijk de docker draaien
 `docker build -t energie-prijzen-bot .`

en daarna
`docker run -d energie-prijzen-bot`

Deze doet alles voor je automatisch.

## Help

Heb je hulp nodig in de Bot?

`/help`

Heb je problemen bij dit script? Stuur dan een berichtje aan
info@itheo.tech

## Auteurs

[Theo van der Sluijs](https://itheo.tech)

## Versiegeschiedenis

20th mei, 2022 - versie: 2.0.3 
- Bug fixes, verbetering systeem info, onderhoudsmode ingebouwd 

18th mei, 2022 - versie: 2.0.2 
- Wat kleine bugfixes en verbetering van DEV ACC PROD 

17th mei, 2022 - versie: 2.0.1 
- Bugfixes van nieuwe versie, test klaar om op digital ocean te zetten 

03th mei, 2022 - versie: 1.2.0
- Koppeling gemaakt met entsoe voor 3 cijfers achter komma prijzen, meer system informatie en wat kleine layout aanpassingen.

Mei 1 2022 - versie: 1.1.1
- Paar kleine verbeteringe, system time toegevoegd in /system, wanneer de bot je niet snapt krijg je de bruikbare commandos te zien, in git_push_tag verandert hij nu ook de readme met versie gegevens

Apr 30 2022
- Docker slim anders ingericht met Europe/Amsterdam timezone
- Andere docker python image ivm problemen alpine en pandas
- diverse layout en aanpassingen, monofont aanpassing en kleine bugfixes

Apr 28 2022
- Aanpassing aanvraag via mdvmine altijd 2 cijfers achter de komma 0,2 > 0,20
- Aanpassing aanvraag via mdvmine €. > €

Apr 25 2022
- bug fix mbt morgen gaan de prijzen lager

Apr 23  2022
- Small bugfix for showing minus pricing next hour

Apr 22 2022
- Betere next hour minus prices, kleine verbeteringen
- New way run_repeating every minuut & run def every hour

Apr 21 2022
- datum dagen weekdagen enz

Apr 20 2022
- Kleine aanpassingen ivm int admin_ids
- Kleine aanpassing aan telegram key verwijzing
- Dockerfile improvements, volume for easier database placement -

Apr 18 2022
- Minor bugfixes
- Kleine update

Apr 16 2022
- Fixed hourly updates, and some minor fixes

Apr 15 2022
- Bug fix, sqlite external
- Bugfixes

Apr 13 2022
- Initial commit


## MIT License

Copyright (c) 2022 Theo van der Sluijs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



##  Dankbetuigingen

* [Github photo by Daniel Reche via Pexels](https://www.pexels.com/@daniel-reche-718241)

* [Python Telegram Bot]([https://python-telegram-bot.org](https://python-telegram-bot.org/))

* [dynamische-energieprijzen.nl](https://www.dynamische-energieprijzen.nl/actuele-energieprijzen/)

* [mdvmine](https://tweakers.net/gallery/78806/) heeft diverse verbeteringen en verbeteringen gestuurd.

## Informatie (API's, koppelingen, sites enz)

* [Day Ahead entsoe](https://transparency.entsoe.eu/load-domain/r2/totalLoadR2/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=04.05.2022+00:00|CET|DAY&biddingZone.values=CTY|10YNL----------L!BZN|10YNL----------L&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2))
* [Natural Gas prices](https://tradingeconomics.com/commodity/eu-natural-gas)
* [dynamische-energieprijzen.nl](https://www.dynamische-energieprijzen.nl/actuele-energieprijzen/)
* [Frank Marktprijzen-API](https://reversed.notion.site/Marktprijzen-API-89ce600a88ac4abe8c2ad89d3167a83e)

