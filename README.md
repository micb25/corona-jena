[![License](https://img.shields.io/github/license/micb25/corona-jena.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/micb25/corona-jena.svg)](https://github.com/micb25/corona-jena/issues)

# corona-jena
A small webcrawler and gnuplot visualization that helps to track the number of Corona cases in Jena, Germany. Currently, the crawler runs every hour on my web server.

## Resources

The project uses the following official numbers as provided by the state of Thuringia or the local authorities:

| City / Province | URL                                                                                                                    |
|-----------------|------------------------------------------------------------------------------------------------------------------------|
| Jena            | [https://gesundheit.jena.de/de/coronavirus](https://gesundheit.jena.de/de/coronavirus)                                 |
| Weimar          | [https://stadt.weimar.de/aktuell/coronavirus](https://stadt.weimar.de/aktuell/coronavirus)                           |
| Thuringia       | [https://www.landesregierung-thueringen.de/corona-bulletin](https://www.landesregierung-thueringen.de/corona-bulletin) |

## Requirements 
- Python 3
- gnuplot (version >= 5.0)
- awk

## Miscellaneous
Bugs? Wishes? Suggestions? Please add them all to the [bug tracker](https://github.com/micb25/corona-jena/issues).
