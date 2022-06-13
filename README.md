# Currency rate service

Project for completing hh.ru employer task 

## Downloading currency rates to local database


### Main capabilities:

* #### Downloading currency rates from cbr.ru
* #### Save results to SQLite database
* #### Logging process to .log file and to console
* #### Using previous database at repeated launches
* #### Checks for existing data in database and ignoring duplicate records
* #### Print report about inserted currency data

## Usage

`python start.py --date==dd.mm.yyyy --codes=code1,code2,... [--rewrite]`

* `--date=dd.mm.yyyy` - date of currency set
* `--codes=code1, code2, ...` - requested currency codes (separated by comma). Use `*` instead to get all available codes.
* `--rewrite` - clear current database before saving data (optional)

## Examples
`python start.py --date=10.03.2022 --codes=840,978,156`

`python start.py --date=01.06.2020 --codes=* --rewrite`


## Files overview

- `start.py` - two-lines script for creating and launch app
- `currency_service.py` - main logic of project
- `db_controller.py` - plain SQL based controller
- `logger.py` - primitive log module
- `xml_parser.py` - tag content extractor
- `tables.py` - database tables structures
- `soap-template.xml` - request template for [Central bank of Russia web service](https://cbr.ru/DailyInfoWebServ/DailyInfo.asmx?op=GetCursOnDateXML) service
- `pretty_table.py` - simple table decorator
- `launch_args_parser.py` - primitive command-line arguments handler
- `currency.db` - default SQLite database
- `ondatecurs.log` - default log file

######(C) Max Dubrovin 2022





