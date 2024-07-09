import os
import logging
import collections
import configparser
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui

from constants import LOG_FOLDER, TR_FOLDER, BIN_FOLDER
from form_main import UiMainWindow


class SaveLoadConfig:
    def __init__(self):
        self.file_ini = os.path.join(BIN_FOLDER, "settings.ini")
        self.ex_config = configparser.ConfigParser()

    def save(self, exam_class):
        dict_class = {}
        for key, item in exam_class.__dict__.items():
            dict_class[key] = item

        self.ex_config[exam_class.__class__.__name__] = dict_class

        with open(self.file_ini, 'w') as configfile:
            self.ex_config.write(configfile)

    def load(self, exam_class):
        if os.path.exists(self.file_ini):
            self.ex_config.read(self.file_ini)
            for key, value in self.ex_config[exam_class.__class__.__name__].items():
                setattr(exam_class, key, value)
        else:
            self.save(exam_class)


class InitialValues:
    scope_values = ('aero', 'blps', 'btmn', 'lgst', 'lubr', 'mbun')
    type_values = ('dim', 'fct')
    columns = ('column_name', 'data_type', 'length', 'precision', 'scale', 'is_nullable',
               'is_key', 'default_value', 'source_name', 'description', 'comment')

    def __init__(self):
        self.scope_values = InitialValues.scope_values
        self.type_values = InitialValues.type_values
        self.columns = InitialValues.columns


class SQLObject:
    def __init__(self):
        self.scope = InitialValues.scope_values[0]
        self.object = ""
        self.type = InitialValues.type_values[0]
        self.source_system = ""
        self.source_type = ""
        self.domain = ""
        self.template = "base"
        self.dmt_view_source = "ods"
        self.comment = ""

    def get_scope(self):
        return InitialValues.scope_values

    def get_type(self):
        return InitialValues.type_values

    def get_name(self):
        return self.object

    def __str__(self):
        return str(self.__dict__)


class TableObject:
    def __init__(self):
        self.column_name = ""
        self.data_type = "bigint"
        self.length = ""
        self.precision = ""
        self.scale = ""
        self.is_nullable = 2
        self.is_key = 0
        self.default_value = ""
        self.source_name = ""
        self.description = ""
        self.comment = ""

    def __str__(self):
        return str(self.__dict__)


class DataType:
    def __init__(self):
        self.bigint = 'bigint'
        self.bit = 'bit'
        self.datetime2 = 'datetime2'
        self.decimal = 'decimal'
        self.int = 'int'
        self.nvarchar = 'nvarchar'
        self.time = 'time'
        self.uniqueidentifier = 'uniqueidentifier'

    @staticmethod
    def get_col_val_data(type_str):
        if type_str == 'bigint':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'bit':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'datetime2':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'decimal':
            return {'length': 'null', 'precision': '30', 'scale': '10', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'int':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'nvarchar':
            return {'length': '4000', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'time':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        elif type_str == 'uniqueidentifier':
            return {'length': 'null', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}
        else:
            return {'length': '4000', 'precision': 'null', 'scale': 'null', 'is_nullable': 2, 'is_key': 0,
                    'default_value': 'null'}


class AppDWHGeneratorSQL(QMainWindow):
    def __init__(self):
        super(AppDWHGeneratorSQL, self).__init__()
        self.sql_object = SQLObject()
        self.data_type = DataType()
        self.columns = InitialValues.columns
        self.table_object = TableObject

        self.ui = UiMainWindow(self)

    @staticmethod
    def create_folder_app():
        if not os.path.isdir(TR_FOLDER):
            os.mkdir(TR_FOLDER)
        if not os.path.isdir(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        if not os.path.isdir(BIN_FOLDER):
            os.mkdir(BIN_FOLDER)

    @staticmethod
    def load_logger():
        logging.basicConfig(filename=os.path.join(LOG_FOLDER, "_log.log"),
                            # filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO,
                            encoding='utf-8')
        logging.info("Starting program...")


if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
    else:
        print('running in a normal Python process')

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.ico"))
    window = AppDWHGeneratorSQL()
    window.create_folder_app()
    window.load_logger()
    window.ui.show()

    sys.exit(app.exec_())
