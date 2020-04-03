[![License](https://img.shields.io/github/license/micb25/corona-jena.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/micb25/corona-jena.svg)](https://github.com/micb25/corona-jena/issues)

*Read this in English: [README.en.md](README.en.md)*

# corona-jena
Ein kleiner Webcrawler and entsprechende Visualisierung der Corona-Fallzahlen für Thüringen und ausgewählte Thüringer Kommunen. Aktuell läuft eine stündliche Aktualisierung der Fallzahlen auf meinem Webserver.

Offizielle Zahlen von bestätigten COVID19-Fällen von Stelle des Landes oder Bundes, wie etwa dem Robert Koch-Institut, sind leider mit einer gewissen Meldeverzögerung verbunden. Daher ist es eine Hauptidee dieses Projekts diese Fallzahlen auf der kommunalen Ebene zu erfassen, um ein genaueres Bild über die Gesamtsituation zu haben. Zusätzlich werden diese Daten visuell aufbereitet, was für Leute besser verständlich sein sollte als große Daten-Tabellen, um Dinge wie exponentielles Wachstum zu verstehen.

## Quellen

Dieses Projekt verwendet folgdende offizielle Zahlen von Kommunen und dem Freistaat Thüringen:

| Stadt / Landkreis | URL                                                                                                                                                                                                                                                                                                                    |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Jena              | [https://gesundheit.jena.de/de/coronavirus](https://gesundheit.jena.de/de/coronavirus)                                                                                                                                                                                                                                 |
|                   | [https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv](https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv) |
| Erfurt (manuell)  | [https://www.erfurt.de/ef/de/service/aktuelles/am/index.itl](https://www.erfurt.de/ef/de/service/aktuelles/am/index.itl)                                                                                                                                                                                               |
| Gera              | [https://corona.gera.de/](https://corona.gera.de/)                                                                                                                                                                                                                                                                     |
| Weimar            | [https://stadt.weimar.de/aktuell/coronavirus](https://stadt.weimar.de/aktuell/coronavirus)                                                                                                                                                                                                                             |
| Thuringia         | [https://www.landesregierung-thueringen.de/corona-bulletin](https://www.landesregierung-thueringen.de/corona-bulletin)                                                                                                                                                                                                 |
| Thuringia (RKI)   | [https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)                                                                                                                                                           |

## Weitere Quellen (momentan nicht verwendet)

| Stadt / Landkreis              | Zahlenerhebung? | URL                                                                                                                                                                                                                                                                                            |
|--------------------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Altenburger Land               | T, A            | [https://www.altenburgerland.de](https://www.altenburgerland.de/sixcms/detail.php?&_nav_id1=2508&_lang=de&id=371691)                                                            |
| Eichsfeld                      | T               | [https://www.kreis-eic.de](https://www.kreis-eic.de/aktuelle-fallzahlen-im-landkreis-eichsfeld.html)                                                                            |
| Eisenach                       | T               | [https://www.wartburgkreis.de](https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus)                                          |
| Landkreis Greiz                | T               | [https://www.landkreis-greiz.de](https://www.landkreis-greiz.de/landkreis-greiz/aktuell/nachrichten-details/?tx_ttnews%5Btt_news%5D=224&cHash=74595518f951c32f22d04b7591d643fe) |
| Landkreis Gotha                | I               | [https://www.landkreis-gotha.de](https://www.landkreis-gotha.de/)                                                                                                               |
| Landkreis Hildburghausen       | P               | [https://www.landkreis-hildburghausen.de](https://www.landkreis-hildburghausen.de/Aktuelles-Corona-Virus)                                                                       |
| Ilm-Kreis                      | P               | [https://www.ilm-kreis.de](https://www.ilm-kreis.de/Landkreis/Ver%C3%B6ffentlichungen/Pressearchiv/index.php?ModID=255&NavID=2778.25&text=Coronavirus)                          |
| Kyffhäuserkreis                | -               | [https://www.kyffhaeuser.de](https://www.kyffhaeuser.de/kyf/index.php/landkreis.html)                                                                                           |
| Landkreis Nordhausen           | T               | [https://www.landratsamt-nordhausen.de](https://www.landratsamt-nordhausen.de/informationen-coronavirus.html)                                                                   |
| Saale-Holzland-Kreis           | T, P?           | [https://www.saaleholzlandkreis.de](https://www.saaleholzlandkreis.de/corona-virus/aktuelle-infos/)                                                                             |
| Saale-Orla-Kreis               | T               | [https://www.saale-orla-kreis.de](https://www.saale-orla-kreis.de/sok/)                                                                                                         |
| Suhl                           | T, A            | [https://www.suhltrifft.de](https://www.suhltrifft.de/content/blogsection/41/2246/)                                                                                             |
| Saalfeld-Rudolstadt            | G               | [http://www.kreis-slf.de](http://www.kreis-slf.de/landratsamt/)                                                                                                                 |
| Schmalkalden-Meiningen         | P, D            | [https://www.lra-sm.de](https://www.lra-sm.de/?p=22632)                                                                                                                         |
| Landkreis Sömmerda             | P, D            | [https://www.lra-soemmerda.de](https://www.lra-soemmerda.de/)                                                                                                                   |
| Landkreis Sonneberg            | P               | [https://www.kreis-sonneberg.de](https://www.kreis-sonneberg.de/)                                                                                                               |
| Unstrut-Hainich-Kreis          | T               | [https://www.unstrut-hainich-kreis.de](https://www.unstrut-hainich-kreis.de/index.php/informationen-zum-neuartigen-coronavirus)                                                 |
| Weimarer Land                  | -               | [https://weimarerland.de](https://weimarerland.de/index_lra.html)                                                                                                               |
| Wartburgkreis                  | T               | [https://www.wartburgkreis.de](https://www.wartburgkreis.de/leben-im-wartburgkreis/gesundheit/aktuelle-informationen-zum-corona-virus)                                          |

Zahlenerhebung:
 - A: veraltete Daten
 - D: Dokument (PDF)
 - G: Grafik (JPG)
 - I: interaktive Grafik
 - P: Pressemitteilungen
 - T: Text

## Voraussetzungen 
- Python 3
- gnuplot (version >= 5.0)
- awk

## Sonstiges
Fehler? Wünsche? Verbesserungsvorschläge? Dann lasst sie uns wissen und fügt sie dem [Bug-Tracker](https://github.com/micb25/corona-jena/issues) hinzu.
