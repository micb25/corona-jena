# Daten für Thüringen

In diesem [Verzeichnis](/data/) befinden sich die gesammelten Daten COVID-19 Daten für Thüringen als CSV-Tabellen.

| Region               | Datei                                                          |
|----------------------|----------------------------------------------------------------|
| Deutschland          | [cases_germany_total_rki.csv](cases_germany_total_rki.csv)     |
| Thüringen            | [cases_thuringia.csv](cases_thuringia.csv)                     |
| Thüringen (RKI)      | [cases_rki_db_th.csv](cases_rki_db_th.csv)                     |
|                      |                                                                |
| Eisenach             | [cases_ea.csv](cases_ea.csv)                                   |
| Eichsfeld            | [cases_eic.csv](cases_eic.csv)                                 |
| Erfurt               | [cases_erfurt.csv](cases_erfurt.csv)                           |
| Gera                 | [cases_gera.csv](cases_gera.csv)                               |
| Greiz                | [cases_grz.csv](cases_grz.csv)                                 |
| Jena                 | [cases_jena_opendata.csv](cases_jena_opendata.csv)             |
| Landkreis Nordhausen | [cases_ndh.csv](cases_ndh.csv)                                 |
| Saale-Orla-Kreis     | [cases_sok.csv](cases_sok.csv)                                 |
| Wartburgkreis        | [cases_wak.csv](cases_wak.csv)                                 |

Sonstige Formate:

| Region                 | Format | lokaler Github-Link                                            | Link auf Webserver (wahrscheinlich aktueller)                        |
|------------------------|--------|----------------------------------------------------------------|----------------------------------------------------------------------|
| Thüringen (DIVI)       | CSV    | [Dokumentenordner](divi_db_th/)                                | [Dokumentenordner](https://michael-böhme.de/corona/data/divi_db_th/) |
|                        |        |                                                                |                                                                      |
| Saalfeld-Rudolstadt    | JPG    | [Bilderordner](cases_slf/)                                     | [Bilderordner](https://michael-böhme.de/corona/data/cases_slf/)      |
| Schmalkalden-Meiningen | PDF    | [Dokumentenordner](cases_sm/)                                  | [Dokumentenordner](https://michael-böhme.de/corona/data/cases_sm/)   |

Die folgenden Dateien sind momentan noch in einem älteren Format gespeichert und werden demnächst zum CSV-Format transformiert:

| Region               | Datei                                                          |
|----------------------|----------------------------------------------------------------|
| Thüringen            | [cases_thuringia_rki.dat](cases_thuringia_rki.dat)             |
| Thüringen            | [cases_thuringia_recovered.dat](cases_thuringia_recovered.dat) |
|                      |                                                                |
| Jena                 | [cases_jena.dat](cases_jena.dat)                               |
| Weimar               | [cases_weimar.dat](cases_weimar.dat)                           |


# Format

Die CSV-Tabellen (außer [cases_rki_db_th.csv](cases_rki_db_th.csv)) haben das folgende Format:

| Datum | bestätigte Fälle (Summe) | Genesungen (Summe) | Verstorbene (Summe) | stationäre Fälle (aktuell) | schwere Fälle (aktuell) | Quelle |
|-------|--------------------------|--------------------|---------------------|----------------------------|-------------------------|--------|
| ...   | ...                      | ...                | ...                 | ...                        | ...                     | ...    |

Der Umfang der Daten ist unterschiedlich und von der Quelle abhängig. Zahlenwerte von '-1' sind so zu verstehen, dass diese Information von der Quelle nicht verfügbar ist.

Das Datum wird zur einfacheren elektronischen Verarbeitung als [Unixzeit](https://de.wikipedia.org/wiki/Unixzeit) angegeben. 
