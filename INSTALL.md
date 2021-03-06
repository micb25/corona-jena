# Installation on Linux

To install all dependencies, follow this small guide.
This guide is uses apt as package manager.

Update and upgrade your system (optional):
```bash
sudo apt-get update 
sudo apt-get upgrade
```

## Dependencies

* Python 3 (with additional modules)
* GnuPlot
* awk
* Magick

## Python 3 + Modules

Python 3 should be installed. Check with:

```bash
python3 --version
```

If not, install it and also virtual environments:

```bash
sudo apt-get install python3 python-venv
```

Create virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
Everytime you use this application, activate
the virtual environment via
```bash
source .venv/bin/activate
```
A virtual environment makes sure, that the 
python installation (and modules) installed for this software are independent of your global python
installation.


Install Python dependencies (already provided
by .txt-file in this repository) with activated
environment:

```bash
pip install -r python-dependencies.txt
```

## gnu plot
For the creation of all plots, we use gnuplot.
We need only the cli:

```bash
sudo apt-get install gnuplot
```

## ImageMagick
For image manipulation we use ImageMagick.
Installation with:
```bash
sudo apt-get install imagemagick
```

