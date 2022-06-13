"""Module included SQLite table structures. It is used in DbController class of db_controller.py module.

.. moduleauthor:: Max Dubrovin <mihadxdx@gmail.com>

"""


currency_order_structure = {
    'human_name': 'Распоряжения о загрузке курсов',
    'name': 'CURRENCY_ORDER',
    'columns': [
        {
            'human_name': 'Номер распоряжения',
            'name': 'id',
            'type': 'INTEGER',
            'primary_key': True,
        },
        {
            'human_name': 'Дата установки курсов ЦБ РФ',
            'name': 'ondate',
            'type': 'TEXT',
            'unique': 'IGNORE',
            'not_null': '',
        },
    ]
}

currency_rates_structure = {
    'name': 'CURRENCY_RATES',
    'human_name': 'Курсы валют',
    'columns': [
        {
            'name': 'order_id',
            'type': 'INT',
            'human_name': 'Номер распоряжения',
            'foreign_key': 'CURRENCY_ORDER(id)'
        },
        {
            'name': 'name',
            'type': 'TEXT',
            'human_name': 'Наименование валюты',
            'not_null': '',
        },
        {
            'name': 'numeric_code',
            'type': 'TEXT',
            'human_name': 'Цифровой код валюты',
            'not_null': '',
        },
        {
            'name': 'alphabetic_code',
            'type': 'TEXT',
            'human_name': 'Буквенный код валюты',
            'not_null': '',
        },
        {
            'name': 'scale',
            'type': 'INT',
            'human_name': 'Номинал курса',
            'not_null': '',
        },
        {
            'name': 'rate',
            'type': 'TEXT',
            'human_name': 'Значение курса',
            'not_null': '',
        },
    ]
}
