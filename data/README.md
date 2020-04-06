# Daten für Thüringen

In diesem [Verzeichnis](/data/) befinden sich die gesammelten Daten COVID-19 Daten für Thüringen als CSV-Tabellen.

| Region               | Datei                                                          |
|----------------------|----------------------------------------------------------------|
| Deutschland          | [cases_germany_total_rki.csv](cases_germany_total_rki.csv)     |
| Thüringen            | [cases_thuringia.csv](cases_thuringia.csv)                     |
|                      |                                                                |
| Eichsfeld            | [cases_eic.csv](cases_eic.csv)                                 |
| Erfurt               | [cases_erfurt.csv](cases_erfurt.csv)                           |
| Gera                 | [cases_gera.csv](cases_gera.csv)                               |
| Jena                 | [cases_jena_opendata.csv](cases_jena_opendata.csv)             |
| Landkreis Nordhausen | [cases_ndh.csv](cases_ndh.csv)                                 |
| Saale-Orla-Kreis     | [cases_sok.csv](cases_sok.csv)                                 |

Die folgenden Dateien sind momentan noch in einem älteren Format gespeichert und werden demnächst zum CSV-Format transformiert:

| Region               | Datei                                                          |
|----------------------|----------------------------------------------------------------|
| Thüringen            | [cases_thuringia_rki.dat](cases_thuringia_rki.dat)             |
| Thüringen            | [cases_thuringia_recovered.dat](cases_thuringia_recovered.dat) |
|                      |                                                                |
| Jena                 | [cases_jena.dat](cases_jena.dat)                               |
| Weimar               | [cases_weimar.dat](cases_weimar.dat)                           |
 	

# Format

Die CSV-Tabellen haben das folgende Format:

| Datum | bestätigte Fälle (Summe) | Genesungen (Summe) | Verstorbene (Summe) | stationäre Fälle (aktuell) | schwere Fälle (aktuell) | Quelle |
|-------|--------------------------|--------------------|---------------------|----------------------------|-------------------------|--------|
| ...   | ...                      | ...                | ...                 | ...                        | ...                     | ...    |

Das Datum wird dabei zur einfacheren Verarbeitung immer als [Unixzeit](https://de.wikipedia.org/wiki/Unixzeit) angegeben.

