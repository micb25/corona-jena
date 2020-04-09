# corona-jena

<img align="right" src="logo.jpg">

Erfassung und Visualisierung der Corona-Fallzahlen für Thüringen und ausgewählte Kommunen. Aktuell läuft eine stündliche Aktualisierung der Fallzahlen auf meinem Webserver. Die Daten werden bis auf wenige Ausnahmen automatisiert abgerufen und die entsprechenden Abbildungen aktualisiert.

Zahlen von bestätigten COVID19-Fällen von offiziellen Stellen wie dem Land Thüringen oder Bundesstellen wie etwa dem Robert Koch-Institut sind leider mit einer gewissen Meldeverzögerung verbunden. Dies ist mit der Meldekette zu begründen, kann aber abseits dessen auch andere Gründe haben, wie etwa einer kurzfristigen Überlastung der meldenden Gesundheitsämter vor Ort. Daher war es eine initiale Idee dieses Projekts die bestätigten Coronavirus-Fallzahlen auf der kommunalen Ebene möglichst automatisiert zu erfassen, um ein genaueres Bild über die Gesamtsituation vor Ort zu haben. Zusätzlich werden diese Daten visuell aufbereitet, getreu dem Sprichwort "ein Bild sagt mehr als 1000 Worte". Dies soll helfen die regionalen Unterschiede zu erfassen und darzustellen sowie das exponentielle Wachstum einer Pandemie leichter verständlich zu machen. An ausgewählten Daten werden exponentielle Anpassungsfunktionen ("Fits") angewandt, um damit Parameter wie die Fallzahl-Dopplungsrate zu bestimmen. Daraus können im Nachhinein gegebenenfalls Rückschlüsse auf die Wirksamkeit verordneter Maßnahmen geschlossen werden.

Dieses Repository dient neben der Bereitstellung des Projekt-Quelltextes für Interessenten auch der Zurverfügungstellung der gesammelten [Daten](/data/).

## Coronavirus-Datenquellen

Dieses Projekt verwendet einige der folgenden offiziellen Quellen der Kommunen und des Freistaats Thüringen:

| #  | kreisfreie Stadt / Landkreis     | Abruf der Daten?                       | Art der Datenerhebung auf Homepage | Webseite                                                                                                                                                                                                                                               |
|----|----------------------------------|----------------------------------------|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    | Thüringen                        | [ja](data/cases_thuringia.csv)         | T                                  | [https://www.landesregierung-thueringen.de](https://www.landesregierung-thueringen.de/corona-bulletin)                                                                                                                                                 |
|    | Thüringen (RKI)                  | [ja](data/cases_rki_db_th.csv)         | T                                  | [https://www.rki.de](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html), [https://corona.rki.de/](https://corona.rki.de/)                                                                                                   |
|    | Deutschland (RKI)                | [ja](data/cases_germany_total_rki.csv) | T                                  | [https://www.rki.de](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)                                                                                                                                                     |
|    |                                  |                                        |                                    |                                                                                                                                                                                                                                                        |
| 1  | Altenburger Land                 | -                                      | -                                  | [https://www.altenburgerland.de](https://www.altenburgerland.de/sixcms/detail.php?&_nav_id1=2508&_lang=de&id=371691)                                                                                                                                   |
| 2  | Eichsfeld                        | [ja](data/cases_eic.csv)               | T                                  | [https://www.kreis-eic.de](https://www.kreis-eic.de/aktuelle-fallzahlen-im-landkreis-eichsfeld.html)                                                                                                                                                   |
| 3  | Eisenach                         | [ja](data/cases_ea.csv)                | T                                  | [https://www.wartburgkreis.de](https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus)                                                                                                                 |
| 4  | Erfurt                           | [ja](data/cases_erfurt.csv)            | T                                  | [https://www.erfurt.de](https://www.erfurt.de/ef/de/service/aktuelles/topthemen/2020/134840.html)                                                                                                                                                      |
| 5  | Gera                             | [ja](data/cases_gera.csv)              | T                                  | [https://corona.gera.de](https://corona.gera.de/)                                                                                                                                                                                                      |
| 6  | Landkreis Gotha                  | -                                      | I                                  | [https://www.landkreis-gotha.de](https://www.landkreis-gotha.de/)                                                                                                                                                                                      |
| 7  | Landkreis Greiz                  | [ja](data/cases_grz.csv)               | T                                  | [https://www.landkreis-greiz.de](https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/?tx_ttnews%5Btt_news%5D=224&cHash=74595518f951c32f22d04b7591d643fe)                                                                        |
| 8  | Landkreis Hildburghausen         | -                                      | P                                  | [https://www.landkreis-hildburghausen.de](https://www.landkreis-hildburghausen.de/Aktuelles-Covid-19/Aktuelles-zu-Covid-19-im-Landkreis/Aktuelle-Meldungen-aus-dem-Landkreis)                                                                          |
| 9  | Ilm-Kreis                        | -                                      | P                                  | [https://www.ilm-kreis.de](https://www.ilm-kreis.de/Landkreis/Ver%C3%B6ffentlichungen/Pressearchiv/index.php?ModID=255&NavID=2778.25&text=Coronavirus)                                                                                                 |
| 10 | Jena                             | [ja](data/cases_jena_opendata.csv)     | O, T                               | [https://gesundheit.jena.de](https://gesundheit.jena.de/de/coronavirus), [OpenData Tabelle](https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv) |
| 11 | Kyffhäuserkreis                  | -                                      | -                                  | [https://www.kyffhaeuser.de](https://www.kyffhaeuser.de/kyf/index.php/landkreis.html)                                                                                                                                                                  |
| 12 | Landkreis Nordhausen             | [ja](data/cases_ndh.csv)               | T                                  | [https://www.landratsamt-nordhausen.de](https://www.landratsamt-nordhausen.de/informationen-coronavirus.html)                                                                                                                                          |
| 13 | Saale-Holzland-Kreis             | [manuell](data/cases_shk.csv)          | T, G                               | [https://www.saaleholzlandkreis.de](https://www.saaleholzlandkreis.de/corona-virus/diagramm-fall-zahlen/)                                                                                                                                              |
| 14 | Saale-Orla-Kreis                 | [ja](data/cases_sok.csv)               | T                                  | [https://www.saale-orla-kreis.de](https://www.saale-orla-kreis.de/sok/)                                                                                                                                                                                |
| 15 | Landkreis Saalfeld-Rudolstadt    | [ja](data/cases_slf/)                  | G                                  | [http://www.kreis-slf.de](http://www.kreis-slf.de/landratsamt/)                                                                                                                                                                                        |
| 16 | Landkreis Schmalkalden-Meiningen | [ja](data/cases_sm/)                   | P, D                               | [https://www.lra-sm.de](https://www.lra-sm.de/?p=22632)                                                                                                                                                                                                |
| 17 | Suhl                             | -                                      | T, A                               | [https://www.suhltrifft.de](https://www.suhltrifft.de/content/blogsection/41/2246/)                                                                                                                                                                    |
| 18 | Landkreis Sömmerda               | -                                      | P, D                               | [https://www.lra-soemmerda.de](https://www.lra-soemmerda.de/)                                                                                                                                                                                          |
| 19 | Landkreis Sonneberg              | -                                      | P                                  | [https://www.kreis-sonneberg.de](https://www.kreis-sonneberg.de/news/information-zum-infektionsgeschehen-im-landkreis-sonneberg)                                                                                                                       |
| 20 | Unstrut-Hainich-Kreis            | [ja](data/cases_uh.csv)                | T                                  | [https://www.unstrut-hainich-kreis.de](https://www.unstrut-hainich-kreis.de/index.php/informationen-zum-neuartigen-coronavirus)                                                                                                                        |
| 21 | Wartburgkreis                    | [ja](data/cases_wak.csv)               | T                                  | [https://www.wartburgkreis.de](https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus)                                                                                                                 |
| 22 | Weimar                           | [ja](data/cases_weimar.dat)            | T                                  | [https://stadt.weimar.de](https://stadt.weimar.de/aktuell/coronavirus)                                                                                                                                                                                 |
| 23 | Weimarer Land                    | -                                      | -                                  | [https://weimarerland.de](https://weimarerland.de/index_lra.html)                                                                                                                                                                                      |
|    | <strong>Gesamt</strong>          | <strong>14/23</strong>                 |                                    |                                                                                                                                                                                                                                                        |

Art der Datenerhebung auf Homepage (Legende):
 - A: veraltete Daten
 - D: Dokument (PDF)
 - G: Grafik (JPG)
 - I: interaktive Grafik
 - J: JSON
 - O: OpenData (CSV)
 - P: Pressemitteilungen
 - T: Text

## benötigte Software
- Python 3
- gnuplot (Version >= 5.0)
- awk
- ImageMagick

## weitere Projekte

Eine Liste weiterer ähnlicher Github-Projekte, die COVID19-Daten für Deutschland erfassen und auswerten:

| Region        | Link                                                                                                                                      |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Deutschland   | [micgro42/COVID-19-DE](https://github.com/micgro42/COVID-19-DE)<br /> [HoffmannP/coronaZahlen](https://github.com/HoffmannP/coronaZahlen) |
| Bayern        | [koepferl/COVID19Dahoam](https://github.com/koepferl/COVID19Dahoam)                                                                       |
| Niedersachsen | [codeforosnabrueck/COVID-19-NDS](https://github.com/codeforosnabrueck/COVID-19-NDS)                                                       |
| Jena          | [HoffmannP/jenaCorona](https://github.com/HoffmannP/jenaCorona)                                                                           |

## Sonstiges
Fehler? Wünsche? Verbesserungsvorschläge? Dann lasst sie uns wissen und fügt sie dem [Bug-Tracker](https://github.com/micb25/corona-jena/issues) hinzu.

[![License](https://img.shields.io/github/license/micb25/corona-jena.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/micb25/corona-jena.svg)](https://github.com/micb25/corona-jena/issues)
