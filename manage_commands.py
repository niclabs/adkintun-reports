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


# todavia no se como funciona este
class Test(Command):
    def run(self):
        import unittest
        testmodules = [
            "test",
        ]

        suite = unittest.TestSuite()

        for t in testmodules:
            try:
                # If the module defines a suite() function, call it to get the suite.
                mod = __import__(t, globals(), locals(), ["suite"])
                suitefn = getattr(mod, "suite")
                suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

        unittest.TextTestRunner(verbosity=2).run(suite)
