# Currency rate service

## Project is a result of completing a task given by hh.ru employer. The script downloads currency rates from Central Bank of Russia to local database.


### Features:

* #### Downloading currency rates from [Central Bank of Russia](cbr.ru) service
* #### Save results to SQLite database
* #### Logging to file and console
* #### Using previous database at repeated launches
* #### Check for existing data in database with ignoring duplicate records
* #### Print report about inserted currency data
* #### Test example included
* #### Documented code

### Usage

#### A) From command-line

`python start.py --date==dd.mm.yyyy --codes=code1,code2,... [--rewrite]`

* `python` - python 3.8+ interpreter (it can be `python3` in your system)
* `--date=dd.mm.yyyy` - date of currency set
* `--codes=code1, code2, ...` - requested currency codes (separated by comma). Use `*` instead to get all available codes.
* `--rewrite` - clear current database before saving data (optional)

###### Examples
```commandline
python start.py --date=10.03.2022 --codes=840,978,156

python start.py --date=01.06.2020 --codes=* --rewrite
```

#### B) From python code:
You have to create object by `OnDateCurs` class from `currecy_service.py`

###### Example
```python
from currency_service import OnDateCurs

OnDateCurs('currency.db', options=['--date=11.05.2011', '--codes=840,978,156'])
```


### Files overview

File | Description 
---|---
`start.py` | Two-lines script for creating and launch app
`currency_service.py` | Main logic of project
`db_controller.py` | Plain SQL based controller
`logger.py` | Primitive log module
`xml_parser.py` | Tag content extractor
`tables.py` | Database tables structures
`soap-template.xml` | Request template for [Central bank of Russia web service](https://cbr.ru/DailyInfoWebServ/DailyInfo.asmx?op=GetCursOnDateXML) service
`pretty_table.py` | Simple table decorator
`launch_args_parser.py` | Primitive command-line arguments handler
`test.py` | Tests
`currency.db` | Default SQLite database (created by service)
`ondatecurs.log` | Default log file (created by service)

### Requirements
#### Python 3.8+ interpreter with built-in modules and libraries
- `sqlite3`
- `os.path`
- `sys`
- `datetime`
- `re`
- `urllib.request` and `urllib.error`

#### No any third-party packages required

P.S. For testing purposes a principle of using minimal ready-to-use modules is used in this project.





