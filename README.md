# SECP Scrapper

A SECP Scraper which scrape the data from SECP registered companies with the keywords or Air or Technologies.


## Requirements
- Python3
- Selenium >= 4
- python-mysql-connector
- python-dotenv
- virtual-env


## Installation

### Step #01

clone the repo
```shell
https://github.com/MuhammadSaim/ch-secp-scrapper secp_scrapper
```

step into the directory
```shell
cd secp_scrapper
```

### Step #02

create and activate the virtualenv
```shell
virtualenv venv
```

now activate the venv
```shell
source venv/bin/activate
```

### Step #03

Install the requirements or dependencies of the project
```shell
pip install requirements.txt
```

### Step #04

Now before set up the Database you have to configure and run the [Laravel Project](https://github.com/MuhammadSaim/ch-secp-laravel) after setting the Database in laravel project and run the migration now please copy the <kbd>.env.example</kbd> to <kbd>.env</kbd> and set the environment variable.

```shell
cp .env.example .env
```

and set the Database credentials to this file.

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=YOUR_DB_NAME
DB_USERNAME=YOUR_DB_USERNAME
DB_PASSWORD=YOUR_DB_PASSWORD
```

after completing those steps it's time to run the project and scrape the data
```python
python main.py
```