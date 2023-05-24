# tangara-api-mvp
Basic MVP code that exposes a REST API for Tangara's air quality sensors, which are installed throughout Cali, Colombia.

## How to use

Please read and execute each step below:

### Step 1

Create and use Python virtual environment:

```bash
$promt> python -m venv .venv
$promt> source .venv/bin/activate
```

### Step 2

Install all Python requirements:

```bash
$promt> python -m pip install -U pip
$promt> pip install -r requirements.txt
```

### Optional

Generate a requirements file and then install from it in another environment:

```bash
$promt> pip freeze > requirements.txt
```

## Data Base SQLite

There is an SQLite database available to use out of the box.

All entities, relations and data are ready to use from the SQLite database file located in [./db/tangara-mvp.db](/db/tangara-mvp.db) and you don't need to change anything, because the API REST uses this SQLite database.

Optional, if you need to explore the database, I recommend you use:  [DB Browser for SQLite](https://sqlitebrowser.org/) because it is easy to use, all that you need to do is open the SQLite database file from DB Browser and that's all.

Also, there are JSON [./db/json/](./db/json/) and CSV [./db/csv/](./db/csv/) files for each entity on the database, therefore you can use the data for your own project, we support open knowledge that's important to the community open source.

Finally, we have exported an SQL file [./db/tangara-mvp.sql](./db/tangara-mvp.sql) to recreate all the entities of our database in another SQL engine, like PostgreSQL or MySQL.

## Notebooks

Jupyter Notebooks are helpful to explore some features and explain them to the team and easy to use before coding those features into the API, the purpose of the notebooks created in [./notebooks](./notebooks/) is only to explore, test, and explain those features to the team. You dont need change anything here.

## How to run

> **Development Mode**

```bash
$promt> uvicorn app.main:app --reload
```

## Testing

```bash
$promt> pytest -v -s -W ignore::trio.TrioDeprecationWarning
```

---

***That's all for now ...***

---

#### License

[GPL-3.0 License](./LICENSE)

#### About me

[https://about.me/sebaxtian](https://about.me/sebaxtian)
