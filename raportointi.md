# Seminaarityö: Task → Calendar -sovellus (task2cal)

## 1. Johdanto

Tämän seminaarityön tavoitteena oli kehittää sovellus, joka muuntaa luonnollisella kielellä kirjoitetut tehtävänannot automaattisesti kalenterimerkinnöiksi (.ics-muotoon). 

Sovellus on suunniteltu erityisesti (itselle) helpottamaan opiskelutehtävien hallintaa, jolloin tehtävänannot voidaan kopioida suoraan esimerkiksi oppimisympäristöstä ja muuntaa kalenteritapahtumiksi ilman manuaalista syöttöä.

---

## 2. Tavoitteet

Työn keskeiset tavoitteet:

- Tunnistaa tehtävänantojen keskeinen sisältö
- Poimia tehtävän nimi, kuvaus ja deadline
- Tukea suomenkielistä luonnollista kieltä
- Tuottaa toimiva .ics-tiedosto kalenterikäyttöön
- Mahdollistaa sekä paikallisen että pilvipohjaisen kielimallin käyttö

---

## 3. Toteutus

Sovellus toteutettiin Pythonilla käyttäen Streamlit-kirjastoa web-käyttöliittymänä.

### Arkkitehtuuri

1. Käyttäjä syöttää tekstin
2. Teksti analysoidaan kielimallilla (paikallinen tai pilvi)
3. Tuloksesta parsitaan JSON-data
4. Päivämäärät normalisoidaan
5. Luodaan .ics-kalenteritiedosto

### Keskeiset komponentit

- LLM-integraatio (paikallinen + pilvi)
- JSON-parsinta
- Päivämäärien käsittely
- ICS-tiedoston generointi

---

## 4. Käytetyt teknologiat

- Python
- Streamlit
- dateparser
- ICS (kalenterikirjasto)
- paikallinen LLM: Ollamaa käyttäen
- pilvimalli: Gemini

---

## 5. Keskeiset haasteet

### Päivämäärien tulkinta

Suurin tekninen haaste oli suomenkielisten päivämäärien käsittely, esimerkiksi:

- "27.04.2026, 22.00"
- "maanantaina 27. huhtikuuta 2026"

Ratkaisuna toteutettiin:
- esiprosessointi (preprocess)
- formaatin normalisointi (ISO-muotoon)
- tässä käytetty eri tekoälyjä toteutuksen parantamiseen

---

### LLM:n epäluotettavuus

Kielimallit eivät aina tuota validia JSONia tai oikeita päivämääriä.

Ratkaisut:
- regex fallback
- useampi parsing-vaihe
- validointi ennen käyttöä

---

## 6. Oppiminen

Työn aikana opittiin:

- miten kielimalleja käytetään ohjelmallisesti
- miten luonnollista kieltä käsitellään ohjelmallisesti
- ohjelmiston toimintavarmuuden suunnittelua (fallbackit, validointi)
- API-integraatioiden toteuttaminen
- käytännön ongelmia LLM-mallien käytössä
- Eri kielimallien erot tuloksissa ja nopeudessa
- Paikallisen kielimallin "keveys" sopivan pienissä tehtävissä yllätti

---

## 7. Jatkokehitys

Mahdollisia jatkokehitysideoita:

- bugien korjaaminen
- kuvasta tekstin tunnistus (OCR)
- useiden tehtävien parempi erottelu
- deadline-priorisointi (“viimeistään”)
- muut vastaavat toteutukset paikalliseen käyttöön

---

## 8. Lähteet

- dateparser-dokumentaatio
- Streamlit-dokumentaatio
- Ollama-dokumentaatio
- Gemini API -dokumentaatio
- ChatGPT, Gemini ja Copilot

---

## 9. Repository

https://github.com/bhu574/task2cal

---

## 10. Video

https://youtu.be/XQAF3wX_7yg
