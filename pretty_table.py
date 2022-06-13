"""A primitive table (list of list, list of tuples and etc.) pretty console printer. It was also possible to use
ready to use modules (xml for example), but I have built this one from scratch to decrease count of third-party
modules (due to task recommendations).

.. moduleauthor:: Max Dubrovin <mihadxdx@gmail.com>

"""


def auto_widths(table):
    """Calculate and return optional columns width due to size of its contents

    :param table: A table which is a list/tuples of list/tuples
    :return: list of column widths
    """
    column_count = len(table[0])
    row_count = len(table)

    col_widths = []

    for col_index in range(column_count):
        width = max([len(table[row_index][col_index]) for row_index in range(row_count)])
        col_widths.append(width)
    return col_widths


def print_pretty_table(table, header=True):
    """Print pretty table in console

    :param table: A table which is a list/tuples of list/tuples
    :param header: If True dividing line is printed after upper row
    """
    widths = auto_widths(table)

    def divider():
        header_div = '--'
        for index, value in enumerate(table[0]):
            human_value = '-' * (widths[index] + 1)
            header_div += f'{human_value}--'
        print(header_div)

    divider()

    for row_index, row in enumerate(table):
        row_string = '| '
        for index, value in enumerate(row):
            human_value = value.rjust(widths[index] + 1)
            row_string += f'{human_value} |'
        print(row_string)
        if header and row_index == 0:
            divider()

    divider()
