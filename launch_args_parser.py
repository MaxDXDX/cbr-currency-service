import sys


class SysArgsParser:
    """
    Custom primitive class for processing command-line arguments which have specified at service launch.
    P.S. It was also possible to use standard <argparse> module. But I have built this one from scratch to decrease
    count of third-party libraries.
    """

    def __init__(self, require_args: list, init_args, logger):
        self.logger = logger
        self.error = False
        if len(sys.argv) > 1:
            self.init_args = sys.argv
        else:
            self.init_args = init_args
        self.args = self.args()
        self.check_require_args(require_args)
        if not self.error:
            self.check_codes()

    def args(self):
        """Extract arguments from command line

        :return: dictionary (keys are argument names, values - related values)
        """
        args = {'rewrite': False}
        for arg in self.init_args:
            if '--' in str(arg) and '=' in str(arg):
                args[arg.partition('--')[2].partition('=')[0]] = arg.partition('--')[2].partition('=')[2]
            if '--rewrite' in str(arg):
                args['rewrite'] = True
        return args

    def check_require_args(self, require_args: list):
        """ Check args list for containing required arguments.
        If test not passed .error attribute of Class is set to False.

        :param require_args: list of required arguments
        """
        for arg in require_args:
            if arg not in self.args:
                self.logger.log(f'ERROR: Missing require argument: --{arg}')
                self.error = True

    def check_codes(self):
        """Some checks for currency codes"""
        arg_value = self.args['codes']

        if arg_value != '*':
            codes = arg_value.split(',')

            error = False
            if len(codes) > 0:
                for code in codes:
                    try:
                        int(code)
                    except ValueError:
                        error = True
            else:
                error = True

            if error:
                print(f'Ошибка: неверно указаны коды валют')
                self.logger.log(f'ERROR: Currency codes are invalid')
                self.error = True