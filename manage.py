from flask_script import Manager
from app import application
from manage_commands import Test, ReportsGeneration, ReportsImportation

manager = Manager(application)

manager.add_command('test', Test())
manager.add_command('generate_reports', ReportsGeneration())
manager.add_command('generate_and_import_reports', ReportsImportation())

if __name__ == '__main__':
    manager.run()
