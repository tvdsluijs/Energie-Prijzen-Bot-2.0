import os
import logging

import telegram
from telegram.utils.helpers import escape_markdown

PY_ENV = os.getenv('PY_ENV', 'dev')
log = logging.getLogger(PY_ENV)

class Help:
    def __init__(self) -> None:
        pass

    @staticmethod
    def start_text(update: telegram.Update)->str:

        first_name = update.message.chat.first_name
        username = update.message.chat.username

        if first_name is None or first_name == "":
            name = username
        else:
            name = first_name
        return f"""
Hoi {name} welkom op deze energie prijzen bot!

Als je je snel wilt aanmelden doe dan
/a

Wil je meer informatie of hulp?

/help
"""

    @staticmethod
    def help_text(update: telegram.Update)->str:

        first_name = update.message.chat.first_name
        username = update.message.chat.username

        if first_name is None or first_name == "":
            name = username
        else:
            name = first_name

        msg = f"""
Hoi {name}, hier is hulp

💡 Stroom prijzen
🔥 Gas prijzen

Handmatige berichten
/nu → huidige prijzen
/vandaag → Alle prijzen vandaag
/morgen → Alle prijzen morgen*

* prijzen pas na 15u (soms eerder)

Voor automatische berichten:
/a → aanmelden
/i → jouw instellingen
/o 9 → ochtend melding 9 uur
/m 15 → middag melding 15 uur

Gegevens verwijderen?
/verwijder

Wil je meer hulp? Zet er help achter
/a help
/i help
enz.
"""
        msg = escape_markdown(msg, version=2)

        msg = msg + """
[Doneren? Ja graag](https://donorbox.org/tvdsluijs-github)

Vragen? @tvdsluijs of ga naar mijn [Github pagina](https://github.com/tvdsluijs/Energie-Prijzen-Bot-2.0)

"""
        return msg

    @staticmethod
    def systeem_help()->str:
        return """
Wil je meer informatie over dit systeem?

/s

en je krijg wat info te zien!
"""

    @staticmethod
    def ochtend_instellen_help()->str:
        return """
Wil je een hoog laag melding in de ochtend voor die dag?
Zet hem aan via

/o [uur]

Wil je een melding om 8 uur

/o 8

Een melding om 10 uur
/o 10

Ochtend meldingen uitzetten
/o uit

Je kan maar 1 ochtend melding instellen!
"""

    @staticmethod
    def ld_instellen_help()->str:
        return """
Melding wanneer de prijs lager of gelijk is dan x?

/ld 0,001

of iets als
/ld 0,09

Alle getallen zijn mogelijk, systeem gaat nu nog van inkoop prijs uit.

Uitzetten?
/ld uit
"""

    @staticmethod
    def hd_instellen_help()->str:
        return """
Melding wanneer de prijs hoger of gelijk is dan x?

/hd 0,05

of iets als
/ld 0,10

Alle getallen zijn mogelijk, systeem gaat nu nog van inkoop prijs uit.

Uitzetten?
/ld uit"""

    @staticmethod
    def middag_instellen_help()->str:
        return """
Wil je automatisch een melding van de prijzen van morgen?
Zet hem aan via

/m [uur]

Wil je een melding om 15 uur

/m 15

Een melding om 17 uur
/m 17

Je kan maar 1 middag melding instellen!
"""

    @staticmethod
    def get_instellingen_help()->str:
        return """
Instellingen hulp
/ochtend 8  →  update om 8 uur [1-12]
/ochtend uit → update uit
/middag 16 → prijzen morgen [16-23]
/middag uit → prijzen morgen uit
/lager -0.001 → melding prijs lager 0.001
/lager uit → melding lager uit
/hoger 0.10 → melding prijs hoger 0,10
/hoger uit → hoger dan uit
/verwijder → verwijder gebruiker
"""

    @staticmethod
    def afmelden_help()->str:
        return """
Als je je afmeldt dan worden je gegevens verwijderd
Je krijgt geen automatische meldingen meer
Je kan de bot nog wel steeds gebruiken
"""

    @staticmethod
    def aanmelden_help()->str:
        return """
Als je je aanmeldt krijg je automatisch:
Een ochtend melding met hoogste en laagste prijs van de dag
De middag melding met de prijzen voor morgen
Een melding wanneer de prijs 0 of lager wordt
"""

    @staticmethod
    def donatie_help():
        return """
Het heeft me best wat tijd gekost om deze Bot te bouwen

Ook steek ik tijd in het fixen van Bugs en het bouwen van nieuwe zaken

Daarnaast draait het op een server die ook niet gratis is

Iedere donatie is dus van harte welkom

/donatie"""