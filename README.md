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

## Redis CLI

Redis is an open source (BSD licensed), in-memory data structure store used as a database, cache, message broker, and streaming engine.

In development mode we need to install Redis CLI to debug our code and do some test. We will use Redis Server on a Docker configuration, that will be explaned later.

**Downloading the source files:**
```bash
$promt> wget https://download.redis.io/redis-stable.tar.gz
```

**Compiling Redis CLI:**
```bash
$promt> tar -xzvf redis-stable.tar.gz
$promt> cd redis-stable/
$promt> make redis-cli
```

**Installing Redis CLI:**
```bash
$promt> sudo cp src/redis-cli /usr/local/bin/
```

**Connecting to the Redis server locally:**
```bash
$promt> redis-cli -h 0.0.0.0 -p 6379
```

## Redis Server

In development mode we are going to use a Docker container, to achieve that, we need just download the official Redis Docker Image, then we run a docker command to run a Redis Server container.

**Downloading the official Redis Docker image:**
```bash
$promt> docker pull redis:7-alpine
```

**Run Redis Server container:**
```bash
$promt> docker run --name tangara-redis -p 6379:6379 -d redis:7-alpine
```
s
**Connecting to the Redis server from container:**
```bash
$promt> docker exec -it tangara-redis redis-cli
```

Finally, we are ready to use a Redis Server in our project.

## How to run

> **Development Mode**

```bash
$promt> uvicorn app.main:app --reload
```

## Testing

**Run API tests**

```bash
$promt> pytest -v -s -W ignore::trio.TrioDeprecationWarning -W ignore::DeprecationWarning
```

**Run API integration tests**

> [Install Thunder Client Extension for VS Code](https://rangav.medium.com/thunder-client-alternative-to-postman-68ee0c9486d6)

Activate the checkbox ***Thunder-client: Save To Workspace*** in Thunder Client Extension **Settings**.

> [Install Thunder Client CLI:](https://rangav.medium.com/thunder-client-cli-a-new-way-to-test-apis-inside-vscode-d91eb5c71d8e)
```bash
# Install Thunder Client CLI as a global nodejs package
$promt> sudo npm i -g @thunderclient/cli
$promt> tc2 -v
$promt> tc2 -h
# Thunder Client CLI Documentation: https://medium.com/p/d91eb5c71d8e
```


---

***That's all for now ...***

---

#### License

[GPL-3.0 License](./LICENSE)

#### About me

[https://about.me/sebaxtian](https://about.me/sebaxtian)
