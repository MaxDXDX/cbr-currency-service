import sqlite3
from table_structures import currency_order_structure
from table_structures import currency_rates_structure
from os.path import exists


def create_table_stmt(table_structure: dict):
    """Build SQL statement for creating a new table in SQLite database

    :param Table_structure: dictionary describing table structure and other options
    :type table_structure: dict
    :return: Ready to use SQL statement for creating a table
    :rtype: str
    """
    cols_def = list()
    for col in table_structure['columns']:
        col_stmt = f'{col["name"]} {col["type"]}'

        foreign_key = col.get('foreign_key')
        if foreign_key:
            col_stmt += ' REFERENCES ' + foreign_key

        primary_key = col.get('primary_key')
        if primary_key:
            col_stmt += ' PRIMARY KEY'

        unique = col.get('unique')
        if unique:
            col_stmt += ' UNIQUE'
            if unique != '':
                col_stmt += ' ON CONFLICT ' + unique

        not_null = col.get('not_null')
        if not_null is not None:
            col_stmt += ' NOT NULL'
            if not_null != '':
                col_stmt += ' ON CONFLICT ' + not_null
        cols_def.append(col_stmt)

    columns_def = ', '.join(cols_def)
    statement = f'CREATE TABLE IF NOT EXISTS {table_structure["name"]} ({columns_def});'
    # print(statement)
    return statement


def human_date(db_date: str):
    """Convert YYYYMMDD date format to DD.MM.YYYY format

    :param db_date: YYYYMMDD string (for example '19811020')
    :return: DD.MM.YYYYY string ('20.10.1981' for example)
    :rtype: str
    """

    day = db_date[-2:]
    month = db_date[4:6]
    year = db_date[:4]
    hum_date = f'{day}.{month}.{year}'
    return hum_date


def insert_order_stmt(date, order_id):
    """Build SQL statement for inserting a new record into CURRENCY_ORDER table.
    You can specify order-id exactly by order_id parameter.
    If order_id is omitted then record will inserted with autoincrement id.

    :param date: Value of 'ondate' column
    :type date: str
    :param order_id: Value of 'id' column
    :type order_id: str or int, optional
    :return: Ready to use SQL statement for inserting a record into CURRENCY_ORDER table
    """
    if order_id:
        stmt = f"INSERT INTO CURRENCY_ORDER VALUES ({str(order_id)}, '{date}');"
    else:
        stmt = f"INSERT INTO CURRENCY_ORDER (ondate) VALUES ('{date}');"
    # print(stmt)
    return stmt


def insert_rows_stmt(table_name, rows: list):
    """ Build SQL statement for inserting a list of records into SQLite table.

    :param table_name: A target table into which records will be inserted
    :param table_name: str
    :param rows: A list of records to insert. Each item of this list must be a dict with structure:
                 {first_column: value, second_column: value, ...} and specify all of the table columns
    :type rows: List
    :return: Ready to use SQL statement for inserting a multiple records into target table
    :rtype: str
    """
    values_stmt = ', '.join([f"""({', '.join([f"'{value}'" for value in row.values()])})""" for row in rows])
    stmt = f"INSERT INTO {table_name} VALUES {values_stmt};"
    return stmt


class DbController:
    """This is my custom class for working on the test task by plain SQL statements. P.S. It was also possible to use
    object relational mappers, 'SQLAlchemy' for example. But I have choose plain SQL to decrease count of third-party
    libraries  (due to task recommendations).
    """
    def __init__(self, db_file, logger, rewrite_mode=False):
        self.logger = logger
        self.db_file = db_file
        db_is_exist = self.check_db()
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        if not db_is_exist:
            self.create_tables()
        elif rewrite_mode:
            self.drop_tables()
            self.create_tables()
            self.logger.log('Rewrite mode is set by --rewrite option. Current DB is cleared.')

    def drop_tables(self):
        """ Remove CURRENCY_ORDER and CURRENCY_RATES tables """
        self.cur.execute('DROP TABLE IF EXISTS CURRENCY_ORDER')
        self.cur.execute('DROP TABLE IF EXISTS CURRENCY_RATES')

    def create_tables(self):
        """ Create CURRENCY_ORDER and CURRENCY_RATES tables """
        self.cur.execute(create_table_stmt(currency_rates_structure))
        self.cur.execute(create_table_stmt(currency_order_structure))

    def check_db(self):
        """ Check database existence on local drive
        :return: True if database file exists or False if not
        :rtype: bool
        """

        existence = exists(self.db_file)
        if existence:
            bd_exist = True
            self.logger.log('Existing database is found and connected.')
        else:
            bd_exist = False
            self.logger.log(f'WARNING: Database {self.db_file} does not exist. New database will be created.')
        return bd_exist

    def values_exist(self, table, values: dict, mode='and'):
        """ Check if some values are already present in table

        :param table: Table name
        :type table: str
        :param values: Dictionary for representing searching values.
            Its format is {column_name_1: value, column_name_2: value, ... }.
            This dict can include from one to all of table columns.
        :type values: dict
        :param mode: A logic operator to use by searching in a record of table - 'or' or 'and'.
            Defaults to 'and'
        :type mode: str
        :return: True if values are already in table, False if not
        :rtype: bool
        """

        expr_list = []
        for column, value in values.items():
            expr = f"{column}='{value}'"
            expr_list.append(expr)
        where_stmt = f' {mode} '.join(expr_list)
        stmt = f"SELECT EXISTS (SELECT * FROM {table} WHERE {where_stmt});"
        self.cur.execute(stmt)
        result = self.cur.fetchone()[0]
        return result == 1

    def date_exist_order_id(self, date):
        """ Return value of CURRENCY_ORDER 'id' column by specified order date

        :param date: Date of order in format 'YYYYMMDD'
        :return: 'Id' value of order date if one exists. 'False' if there is not this date in table.
        """
        stmt = f"SELECT id FROM CURRENCY_ORDER WHERE ondate='{date}';"
        # print(stmt)
        self.cur.execute(stmt)
        f = self.cur.fetchone()
        if f:
            order_id = f[0]
        else:
            order_id = False
        return order_id

    def insert_order(self, date, order=None):
        """Insert one record in  CURRENCY_ORDER table

        :param date: Date or order
        :param order: Order ID
        :type order: str or int, optional
        :return: Value of 'id' column for inserted record
        :rtype: str
        """
        if order:
            db_rows = [{'id': order, 'date': date}]
            stmt = insert_rows_stmt('CURRENCY_ORDER', db_rows)
            self.cur.execute(stmt)
            order_id = order
        else:
            stmt = f"INSERT INTO CURRENCY_ORDER (ondate) VALUES ('{date}') RETURNING id;"
            self.cur.execute(stmt)
            order_id = str(self.cur.fetchone()[0])
        return order_id

    def insert_order_cur_data(self, order_id: str, order_cur_data: list):
        """
        Insert new data in CURRENCY_RATES table. Existing rows are ignored.

        :param order_id: order ID from CURRENCY_ORDERS table
        :param order_cur_data: List or dicts. Each dict is a map of inserted row (without <order_id> column).
            Dict pattern is {'name': value, 'numeric_code': value, 'alphabetic_code': value, 'scale': value,
            'rate': value}
        :type order_cur_data: list

        :returns: A list of inserted (non-ignored) rows (dicts). Order_id values are included.
        """

        db_rows = []
        for data in order_cur_data:
            row = {'order_id': str(order_id)}
            row.update(data)

            values_for_exist_check = {
                'order_id': row['order_id'],
                'numeric_code': row['numeric_code']
            }

            if self.values_exist('CURRENCY_RATES', values_for_exist_check):
                self.logger.log(f'WARNING: Currency with code {row["numeric_code"]} is already existed in db. Insert ignored.')
            else:
                db_rows.append(row)

        if len(db_rows) > 0:
            stmt = insert_rows_stmt('CURRENCY_RATES', db_rows)
            self.cur.execute(stmt)
            self.con.commit()

        return db_rows

    def write_data(self, data, order=None):
        """Save prepared Currency data block to database and prepare data for update report. Already existing records
        are ignored. Currency data block must be represented by dictionary of specific format (data parameter).

        :param data: Currency data block in below format: {'date': 'YYYYMMDD', 'rows' : list of Currency data}.
            Each item of included list must be a dict with following keys: 'name', 'numeric_code', 'alphabetic_code',
            'scale' and 'rate'
        :param order: If of order. If order_id is omitted then record will inserted with autoincrement order id.
        :type order: str or int, optional
        :return: info about rows which ones have been really inserted. Each item of list is a tuple of values
            in following order: id of order, date of currency rate set, name of currency, scale, rate.
        :rtype: list
        """
        date = data['date']
        cur_data = data['rows']
        exist_date_order = self.date_exist_order_id(date)

        if exist_date_order:
            self.logger.log(f'WARNING: Order for date {human_date(date)} is already existed with id {exist_date_order}. Insert ignored.')
            order_id = exist_date_order
        else:
            order_id = self.insert_order(date, order)
            self.logger.log(f'Order of date {date} with id {order_id} is inserted into db.')

        inserted_rows = self.insert_order_cur_data(order_id, cur_data)

        inserted_rows_count = len(inserted_rows)
        if inserted_rows_count:
            self.logger.log(f'Database successfully updated by {inserted_rows_count} rows')
        else:
            self.logger.log(f'There is no data to insert into database')

        report = [
            (
                row['order_id'],
                human_date(date),
                row['name'] + f' ({row["numeric_code"].rjust(3)})',
                row['scale'],
                row['rate'],
            )
            for row in inserted_rows
        ]

        return report

        # self.date_exist_order_id(date)

    def close_db(self):
        """Close connection to database"""
        self.con.close()
        self.logger.log('Database closed')




