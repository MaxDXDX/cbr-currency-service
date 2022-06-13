"""Service to retrieve currency data and save it to database.


.. moduleauthor:: Max Dubrovin <mihadxdx@gmail.com>

"""

import requests

import db_controller
from db_controller import DbController
from launch_args_parser import SysArgsParser
from logger import Logger
from pretty_table import print_pretty_table
from xml_parser import tag_content, tag_attribute, xml_date


class OnDateCurs:
    """Currency service main logic Class"""
    def __init__(self, db_file):
        self.logger = Logger('ondatecurs.log', show_time=True)
        self.logger.log('Service have been started')
        self.url = 'https://cbr.ru/DailyInfoWebServ/DailyInfo.asmx'
        self.request_template = 'soap-template.xml'
        self.args = SysArgsParser(require_args=['date', 'codes'], logger=self.logger)
        self.db_file = db_file

        self.main_routine()

    def stop(self):
        """Emergency stop the service"""
        self.logger.log('Service stopped')
        exit()

    def main_routine(self):
        """Main logic of service"""

        if self.args.error:  # check input arguments
            self.stop()
        else:
            self.logger.log(f'STEP 1 IS STARTED - RETRIEVING CURRENCY DATA')
            xml = self.data_request()

            if xml:
                data = self.db_payload(xml_data=xml)
                if data:
                    self.logger.log(f'STEP 2 IS STARTED - DATABASE UPDATING')
                    self.db_update(data)
            else:
                self.stop()

    def data_request(self):
        """Retrieve xml data from Web

        :return: response plain text or False if request exception is raised
        """
        date = self.args.args['date']

        headers = {
            'Content-Type': 'application/soap+xml; charset=utf-8',
            'Content-Length': '0',
        }
        with open('soap-template.xml', 'r') as f:
            data = f.read()
        data = data.replace('{ date }', xml_date(date))

        try:
            self.logger.log('Trying make data request...')
            response = requests.post(url=self.url, data=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as E:
            self.logger.log(f'ERROR: request error')
            return False
        else:
            self.logger.log(f'Response is got, code - {response.status_code}')
            xml_data = response.text
            return xml_data

    def db_payload(self, xml_data):
        """Parse response content, extract currency data and build data structure to save it into database using
        db_controller

        :param xml_data: Plain text of web service response. It would have XML format.
        :type xml_data: str
        :return: prepared Data block for saving it in database or False if there is no currency data in given xml.
            Data block format: {'date': 'YYYYMMDD', 'rows' : list of Currency data}.
            Each item of 'rows' list must be a dict with following keys: 'name', 'numeric_code', 'alphabetic_code',
            'scale' and 'rate'
        """
        date = tag_attribute(xml_data, 'ValuteData', 'OnDate')  # extract date of currency set in
        if not date:
            self.logger.log('No -ondate- attribute in response xml. Response data seems to be incorrect.')
            return False
        else:
            response_date = db_controller.human_date(date)
            request_date = self.args.args['date']
            self.logger.log(f'Ondate attribute in response: {date}')
            if response_date != request_date:
                # requested data is not equal response data
                self.logger.log(f'WARNING: response currency info date for {request_date} is {response_date}')

            # list of all 'ValuteCursOnDate' tags contents (each item is a one currency)
            currencies = tag_content(xml_data, 'ValuteCursOnDate', find_all=True)
            currencies_count = len(currencies)

            self.logger.log(f'Total currencies in response: {currencies_count}')

            requested_codes = self.args.args['codes'].replace(' ', '').split(',')  # specified codes at service launch

            if not currencies:
                return False
            else:
                cur_data = {'date': date, 'rows': []}  # main data structure for further saving into database

                left_codes = requested_codes.copy()  # codes that have not been founded in response codes yet
                for item in currencies:
                    numeric_code = tag_content(item, 'Vcode')
                    if requested_codes == ['*'] or (numeric_code in requested_codes):

                        if requested_codes != ['*']:
                            left_codes.remove(numeric_code)  # eject code from non-founded codes

                        data = {
                            'name': tag_content(item, 'Vname'),
                            'numeric_code': numeric_code,
                            'alphabetic_code': tag_content(item, 'VchCode'),
                            'scale': tag_content(item, 'Vnom'),
                            'rate': tag_content(item, 'Vcurs'),
                        }
                        cur_data['rows'].append(data)

                if requested_codes != ['*']:
                    for code in left_codes:
                        self.logger.log(f'WARNING: Requested currency code {code} is not founded in response currency list')

                return cur_data

    def db_update(self, payload):
        """Save prepared data structure into database and print result report

        :param payload: Data block to save into database. Format: {'date': 'YYYYMMDD', 'rows' : list of Currency data}.
            Each item of 'rows' list must be a dict with following keys: 'name', 'numeric_code', 'alphabetic_code',
            'scale' and 'rate'
        """
        db = DbController(self.db_file, self.logger, rewrite_mode=self.args.args['rewrite'])
        report = db.write_data(payload)
        db.close_db()

        report.insert(0, ['№ расп.', 'Дата', 'Валюта', 'Номинал', 'Курс'])
        print('\nDatabase update report:')
        print_pretty_table(report)
