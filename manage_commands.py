from flask_script import Command, Option

from app import application


class ReportsGeneration(Command):
    option_list = (
        Option('--month', '-m', dest='month'),
        Option('--year', '-y', dest='year'),
    )

    def run(self, month=None, year=None):
        # parameters validation
        if month:
            try:
                month = int(month)
            except:
                print("Month must be a number")
                return

        if year:
            try:
                year = int(year)
            except:
                print("Year must be a number")
                return

        from app.automatization.monthly_update import monthly_reports_generation

        monthly_reports_generation(month, year)
        application.logger.info("Reports have been generated")
        print("Reports have been generated")


class ReportsImportation(Command):
    option_list = (
        Option('--month', '-m', dest='month'),
        Option('--year', '-y', dest='year'),
    )

    def run(self, month=None, year=None):
        # parameters validation
        if month:
            try:
                month = int(month)
            except:
                print("Month must be a number")
                return

        if year:
            try:
                year = int(year)
            except:
                print("Year must be a number")
                return

        from app.automatization.monthly_update import monthly_update

        monthly_update(month, year)
        application.logger.info("Reports have been generated")
        print("Reports have been generated")


class Test(Command):
    def run(self):
        import unittest
        tests = unittest.TestLoader().discover('tests', pattern='test*.py')
        unittest.TextTestRunner(verbosity=2).run(tests)
