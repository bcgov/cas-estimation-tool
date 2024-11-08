# cas-estimation-tool

DDS hackathon 2024: An async github estimation tool

## Installation instructions

Prereqs: a python 3.12 + pip available a global install

Only once:

```
python -m venv ./env/
pip install -r requirements.txt
```

Then, every time we start developing:

```
source ./env/bin/activate
```

Database: a local Postgres 14+ available

Run the app:
```
cd estimation
python manage.py runserver
```
