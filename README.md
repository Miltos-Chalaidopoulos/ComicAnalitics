# Comic Analitics

## About 

A destop app build with **python** and **pyside6 (qt)** for managing comic book collections

## Features 

- *Multiple tabs based on database tables*
- *Search filters*
- *Add/Delete/Edit tuples*
- *CSV import*
- *CSV export*
- *Database backup/deletion*
- *Dark/Light theme support*

## Technologies used
- **Python 3.12 :** Programming Languege
- **PySide6 :** GUI framework
- **SQLite3 :** Embedded databse
- **Pytest :** Testing framework
- **PyInstaller :** Packaging to executable

## Src Stracture

1. *src/database/ :* Database + Database manipulation functions
2. *src/services/ :* Services for csv's and filters
3. *src/ui/ :* User interface
4. *tests/ :* Unit tests


## Installation instructions 

### Clone repository
```bash
git clone https://github.com/Miltos-Chalaidopoulos/ComicAnalitics.git

cd ComicAnalytics
```
### Create virtual Enviroment
```bash
python3 -m venv .venv

source .venv/bin/activate # for linux

# or 

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate  # for Windows
```
### Install dependancies
``` bash
pip install -r requirements.txt
```
### Run the application
``` bash
python -m src.main
```