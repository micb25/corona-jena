[![License](https://img.shields.io/github/license/micb25/corona-jena.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/micb25/corona-jena.svg)](https://github.com/micb25/corona-jena/issues)

# corona-jena
A small webcrawler and gnuplot visualization that helps to track the number of Corona cases in Thuringia. Currently, the crawler runs every hour on my web server.

Official numbers of confirmed COVID19 patients from federal authorities like the Robert Koch institute are unfortunately connected with a certain delay. Therefore, a main idea of this project is to obtain case numbers on a local level in order to have a more accurate picture of the situation as well as plotting the data as a function over time. From my point of view, this might be much more useful for people and easier to understand things like exponential growth than large tables with a lot of numbers.

## Resources

The project uses the following official numbers as provided by the state of Thuringia or the local authorities:

| City / Province | URL                                                                                                                                                          |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Jena            | [https://gesundheit.jena.de/de/coronavirus](https://gesundheit.jena.de/de/coronavirus) |
| Jena            | [https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv](https://opendata.jena.de/dataset/2cc7773d-beba-43ad-9808-a420a67ffcb3/resource/d3ba07b6-fb19-451b-b902-5b18d8e8cbad/download/corona_erkrankungen_jena.csv)                                                                       |
| Erfurt (manually) | [https://www.erfurt.de/ef/de/service/aktuelles/am/index.itl](https://www.erfurt.de/ef/de/service/aktuelles/am/index.itl) |
| Gera            | [https://corona.gera.de/](https://corona.gera.de/)                                                                                                           |
| Weimar          | [https://stadt.weimar.de/aktuell/coronavirus](https://stadt.weimar.de/aktuell/coronavirus)                                                                   |
| Thuringia       | [https://www.landesregierung-thueringen.de/corona-bulletin](https://www.landesregierung-thueringen.de/corona-bulletin)                                       |
| Thuringia (RKI) | [https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html) |

## Requirements 
- Python 3
- gnuplot (version >= 5.0)
- awk

## Miscellaneous
Bugs? Wishes? Suggestions? Please let me know and add them all to the [bug tracker](https://github.com/micb25/corona-jena/issues).
