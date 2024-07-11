import pyperclip
import logging
import pandas
from transliterator import Transliterator, Translate
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox

import resources
from func import get_text_null, get_length, get_state, to_camel_case
from dialog_prefix_postfix import UiDialogPrefixPostfix
from dialog_view_sql import UiDialogViewText


class UiQComboBox(QtWidgets.QComboBox):
    def __init__(self, main_app, items_data=(), type_style=''):
        super(UiQComboBox, self).__init__()
        self.main_app = main_app
        self.index_row = 0
        self.key = ''

        self._load_data(items_data)
        self._load_style(type_style)

    def set_index_row(self, row):
        self.index_row = row

    def get_index_row(self):
        return self.index_row

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def _load_data(self, items_data):
        collection_data_type = tuple(items_data)
        for i_cb, val_cb in enumerate(collection_data_type):
            self.addItem(val_cb)
            self.setItemData(i_cb + 1, val_cb)

    def _load_style(self, type_style):
        if type_style == 'object':
            self.setStyleSheet("QComboBox{\n"
                               "background-color: rgb(254, 255, 170);\n"
                               "border: 0px solid rgb(204, 204, 204);\n"
                               "}\n"
                               "\n"
                               "QComboBox::drop-down{\n"
                               "border:0;\n"
                               "}\n"
                               "\n"
                               "QComboBox::down-arrow{\n"
                               "image: url(:/icon/img/expand_more.png);\n"
                               "width: 20px;\n"
                               "height: 20px;\n"
                               "margin-right: 10px;\n"
                               "}\n"
                               "\n"
                               "\n"
                               "QComboBox:on{\n"
                               "background-color: none;\n"
                               "}\n"
                               "\n"
                               "QListView{\n"
                               "background-color: rgba(236, 236, 236, 128);\n"
                               "selection-color: rgb(0, 0, 0);\n"
                               "font-size: 14px;\n"
                               "outline: 0;\n"
                               "padding: 5px;\n"
                               "}")
        elif type_style == 'columns':
            self.setStyleSheet("QComboBox{\n"
                               "background-color: rgb(206, 255, 211);\n"
                               "border: 0px solid rgb(204, 204, 204);\n"
                               "}\n"
                               "\n"
                               "QComboBox::drop-down{\n"
                               "border:0;\n"
                               "}\n"
                               "\n"
                               "QComboBox::down-arrow{\n"
                               "image: url(:/icon/img/expand_more.png);\n"
                               "width: 20px;\n"
                               "height: 20px;\n"
                               "margin-right: 10px;\n"
                               "}\n"
                               "\n"
                               "\n"
                               "QComboBox:on{\n"
                               "background-color: none;\n"
                               "}\n"
                               "\n"
                               "QListView{\n"
                               "background-color: rgba(236, 236, 236, 128);\n"
                               "selection-color: rgb(0, 0, 0);\n"
                               "font-size: 14px;\n"
                               "outline: 0;\n"
                               "padding: 5px;\n"
                               "}")
        else:
            self.setStyleSheet("QComboBox{\n"
                               "border: 0px solid rgb(204, 204, 204);\n"
                               "}\n"
                               "\n"
                               "QComboBox::drop-down{\n"
                               "border:0;\n"
                               "}\n"
                               "\n"
                               "QComboBox::down-arrow{\n"
                               "image: url(:/icon/img/expand_more.png);\n"
                               "width: 20px;\n"
                               "height: 20px;\n"
                               "margin-right: 10px;\n"
                               "}\n"
                               "\n"
                               "\n"
                               "QComboBox:on{\n"
                               "background-color: none;\n"
                               "}\n"
                               "\n"
                               "QListView{\n"
                               "selection-color: rgb(0, 0, 0);\n"
                               "font-size: 14px;\n"
                               "outline: 0;\n"
                               "padding: 5px;\n"
                               "}")


class UiQTableWidgetItemRow(QtWidgets.QTableWidgetItem):
    def __init__(self, value):
        super(UiQTableWidgetItemRow, self).__init__(value)

        self.key = ''
        self.data_item = None

    def set_item_data(self, data_item):
        self.data_item = data_item

    def get_item_data(self):
        return self.data_item

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key


class UiAbsQTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(UiAbsQTableWidget, self).__init__(parent=parent)

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setRowCount(0)
        self.setColumnCount(2)
        self.setSortingEnabled(False)

        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setCascadingSectionResizes(False)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setMinimumSectionSize(150)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(23)
        self.verticalHeader().setMinimumSectionSize(23)

        self._add_header()

    def _add_header(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/img/property.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/img/value.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        item = QtWidgets.QTableWidgetItem()
        item.setIcon(icon)
        item.setText("Свойство")
        self.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setIcon(icon1)
        item.setText("Значение")
        self.setHorizontalHeaderItem(1, item)

    def _add_rows(self):
        pass

    def _connect_event(self):
        pass

    def _change_item(self, item: QtWidgets.QTableWidgetItem):
        pass

    def create_widget_combo_box(self, name, collection):
        pass

    def clear_items(self):
        pass


class UiTableWidgetObject(UiAbsQTableWidget):
    def __init__(self, parent=None, main_app=None):
        super(UiTableWidgetObject, self).__init__(parent)
        self.sql_object = None
        self.main_app = main_app

        self.setObjectName("tableWidget_OBJECT")
        self.setStyleSheet("#tableWidget_OBJECT{\n"
                           "    alternate-background-color: rgb(255, 255, 210);\n"
                           "    background-color: rgb(254, 255, 170);\n"
                           "}")

        self._add_rows()
        self._connect_event()

    def _add_rows(self):
        for key in enumerate(self.main_app.sql_object.__dict__.keys()):
            row = self.rowCount()
            self.insertRow(row)

            index, name_prop = key[0], key[1]
            value = self.main_app.sql_object.__dict__[name_prop]

            item_prop0 = QtWidgets.QTableWidgetItem(name_prop)
            item_prop0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
            self.setItem(row, 0, item_prop0)

            if name_prop == "scope":
                collection_scope = self.main_app.sql_object.get_scope()
                combo_box = self.create_widget_combo_box("cb_scope", collection_scope)
                self.setCellWidget(row, 1, combo_box)
            elif name_prop == "type":
                collection_type = self.main_app.sql_object.get_type()
                combo_box = self.create_widget_combo_box("cb_type", collection_type)
                self.setCellWidget(row, 1, combo_box)
            else:
                item_value1 = QtWidgets.QTableWidgetItem(value)
                if name_prop == "template" or name_prop == "dmt_view_source":
                    item_value1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
                self.setItem(row, 1, item_value1)

    def _connect_event(self):
        self.itemChanged.connect(self._change_item)

    def _change_item(self, item: QtWidgets.QTableWidgetItem):
        item_prop0 = self.item(item.row(), 0)
        item_value1 = item
        setattr(self.main_app.sql_object, item_prop0.text(), item_value1.text())

    def create_widget_combo_box(self, name, collection):
        combo_box = UiQComboBox(main_app=self.main_app, items_data=collection, type_style='object')
        combo_box.setObjectName(name)
        combo_box.currentIndexChanged.connect(lambda: self._cb_current_index_change(name, combo_box))
        return combo_box

    def _cb_current_index_change(self, object_name, combo_box):
        if object_name == "cb_scope":
            self.main_app.sql_object.scope = combo_box.itemText(combo_box.currentIndex())
        if object_name == "cb_type":
            self.main_app.sql_object.type = combo_box.itemText(combo_box.currentIndex())

    def clear_items(self):
        self.setRowCount(0)
        self._add_rows()


class UiTableWidgetColumns(UiAbsQTableWidget):
    def __init__(self, parent=None, main_app=None, main_form=None):
        super(UiTableWidgetColumns, self).__init__(parent=parent)

        self.table_object = None
        self.main_app = main_app
        self.main_form = main_form

        self.set_table_object()

        self.setObjectName("tableWidget_COLUMNS")
        self.setStyleSheet("#tableWidget_COLUMNS{\n"
                           "    alternate-background-color: rgb(206, 255, 211);\n"
                           "    background-color: rgb(160, 255, 171);\n"
                           "}")

        self._add_rows()
        self._connect_event()
        self._set_values_columns('bigint')

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            self.select_next_row()

    def select_next_row(self):
        self.setCurrentCell(self.currentRow() + 1, self.currentColumn())
        self.edit(self.currentIndex())

    def set_table_object(self):
        self.table_object = self.main_app.table_object()

    def _add_rows(self):
        for tuple_value in enumerate(self.table_object.__dict__.keys()):
            row = self.rowCount()
            self.insertRow(row)

            index_prop, name_prop = tuple_value[0], tuple_value[1]
            value = self.table_object.__dict__[name_prop]

            item_prop0 = QtWidgets.QTableWidgetItem(name_prop)
            item_prop0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
            self.setItem(row, 0, item_prop0)

            if name_prop == "data_type":
                items_data = tuple(self.main_app.data_type.__dict__)
                combo_box = self.create_widget_combo_box("cb_data_type", items_data)
                self.setCellWidget(row, 1, combo_box)
            elif name_prop == "is_nullable" or name_prop == "is_key":
                item_value1 = QtWidgets.QTableWidgetItem()
                item_value1.setCheckState(int(value))
                self.setItem(row, 1, item_value1)
            else:
                item_value1 = QtWidgets.QTableWidgetItem(value)
                self.setItem(row, 1, item_value1)

    def _connect_event(self):
        self.itemChanged.connect(self._change_item)

    def _change_item(self, item: QtWidgets.QTableWidgetItem):
        item_prop0 = self.item(item.row(), 0)
        item_value1 = item
        if item_prop0.text() == "is_nullable" or item_prop0.text() == "is_key":
            setattr(self.table_object, item_prop0.text(), item_value1.checkState())
        else:
            setattr(self.table_object, item_prop0.text(), item_value1.text())

    def create_widget_combo_box(self, name, collection):
        combo_box = UiQComboBox(main_app=self.main_app, items_data=collection, type_style='columns')
        combo_box.setObjectName(name)
        combo_box.currentIndexChanged.connect(lambda: self._cb_current_index_change(name, combo_box))
        return combo_box

    def _cb_current_index_change(self, object_name, combo_box):
        if object_name == "cb_data_type":
            self._set_values_columns(combo_box.itemText(combo_box.currentIndex()))

    def _set_values_columns(self, name_data_type):
        values_data_type = self.main_app.data_type.get_col_val_data(name_data_type)

        setattr(self.table_object, 'data_type', name_data_type)
        for key, value in values_data_type.items():
            setattr(self.table_object, key, value)

        for i in range(2, self.rowCount()):
            item_prop = self.item(i, 0)
            item_value = self.item(i, 1)
            try:
                if type(values_data_type[item_prop.text()]) == int:
                    item_value.setCheckState(values_data_type[item_prop.text()])
                else:
                    item_value.setText(values_data_type[item_prop.text()])
            except KeyError:
                continue

    def clear_items(self):
        self.setRowCount(0)
        self.set_table_object()
        self._add_rows()
        self._set_values_columns('bigint')


class UiTableWidgetData(QtWidgets.QTableWidget):
    def __init__(self, parent=None, main_app=None, main_window=None):
        super(UiTableWidgetData, self).__init__(parent=parent)

        self.main_app = main_app
        self.main_window = main_window
        self._create_widget_combo_box = main_window.create_widget_combo_box

        self.setObjectName("tableWidget_DATA")
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setColumnCount(11)
        self.setRowCount(0)
        self.setSortingEnabled(False)
        self.horizontalHeader().setStretchLastSection(True)

        self._add_header()
        self._connect_event()

    def _connect_event(self):
        self.itemChanged.connect(self._change_item)

    def _add_header(self):
        for index, column in enumerate(self.main_app.columns):
            item = QtWidgets.QTableWidgetItem()
            item.setText(column)
            if column == "column_name":
                item.setBackground(QtGui.QColor(151, 183, 214))
            if column == "source_name":
                item.setBackground(QtGui.QColor(183, 159, 130))
            self.setHorizontalHeaderItem(index, item)

    def keyPressEvent(self, event):
        clipboard = QtWidgets.QApplication.clipboard()
        if event.matches(QKeySequence.Paste):

            try:
                row, column, column_count = self.currentRow(), self.currentColumn(), self.columnCount()
            except Exception as e:
                logging.exception(e)
                return None

            data_clipboard = clipboard.text()
            logging.info(data_clipboard)
            data_frame = pandas.read_clipboard(sep=r'[\t]|[\n]', header=None)
            array_data_clipboard = data_frame.values.tolist()
            len_array_data = len(array_data_clipboard)
            rows_table_data = self.rowCount()
            if len_array_data > rows_table_data - row:
                _start_row = rows_table_data - row
                _difference = len_array_data - _start_row
                for i in range(_difference):
                    self.add_row(self.main_app.table_object())

            for index, value in enumerate(array_data_clipboard):
                item_0 = self.item(row + index, 0)
                data_item = item_0.get_item_data()
                if len(value) == 1:
                    item_column = self.item(row + index, column)
                    key_item = item_column.get_key()
                    setattr(data_item, key_item, value[0])
                    item_column.setText(value[0])
                else:
                    for index_column, value_column in enumerate(value):
                        start_index_column = column + index_column
                        if start_index_column > column_count-1:
                            continue
                        item_column = self.item(row + index, start_index_column)
                        key_item = item_column.get_key()
                        setattr(data_item, key_item, value_column)
                        item_column.setText(value_column)

    def _change_item(self, item: QtWidgets.QTableWidgetItem):
        key_item = item.get_key()

        item_0 = self.item(item.row(), 0)
        data_item_0 = item_0.get_item_data()
        if key_item in ["is_nullable", "is_key"]:
            setattr(data_item_0, key_item, item.checkState())
        elif key_item in ["column_name"]:
            setattr(data_item_0, key_item, item.text().lower())
        else:
            setattr(data_item_0, key_item, item.text())

        # print(data_item_0)

    def cb_current_index_change(self, combo_box):
        row = combo_box.get_index_row()
        item_0 = self.item(row, 0)
        item_0_data = item_0.get_item_data()

        cb_text = combo_box.itemText(combo_box.currentIndex())
        values_data_type = self.main_app.data_type.get_col_val_data(cb_text)

        setattr(item_0_data, "data_type", cb_text)
        for key, value in values_data_type.items():
            setattr(item_0_data, key, value)

        for index_col, value_col in enumerate(item_0_data.__dict__.items()):
            if index_col < 2:
                continue
            item = self.item(row, index_col)
            if value_col[0] in ["is_nullable", "is_key"]:
                item.setCheckState(value_col[1])
            elif value_col[0] in ["source_name"]:
                if item_0.text() and not item.text():
                    item.setText(item_0.text())
                else:
                    item.setText(value_col[1])
            else:
                item.setText(value_col[1])

    def add_row(self, data_item):
        row = self.rowCount()
        self.insertRow(row)

        current_index_cb = tuple(self.main_app.data_type.__dict__.keys()).index(data_item.data_type)
        combo_box = self._create_widget_combo_box(f"cb_data_type_row_{row}", row, current_index_cb)

        for index_col, value_col in enumerate(data_item.__dict__.items()):
            if index_col == 0:
                item_0 = UiQTableWidgetItemRow(value_col[1])
                item_0.set_item_data(data_item)
                item_0.set_key(value_col[0])
                self.setItem(row, index_col, item_0)
            elif value_col[0] == "data_type":
                combo_box.set_key(value_col[0])
                self.setCellWidget(row, 1, combo_box)
            elif value_col[0] in ["is_nullable", "is_key"]:
                item = UiQTableWidgetItemRow("")
                item.setCheckState(value_col[1])
                item.set_key(value_col[0])
                self.setItem(row, index_col, item)
            else:
                item = UiQTableWidgetItemRow(value_col[1])
                item.set_key(value_col[0])
                self.setItem(row, index_col, item)

        self.cb_current_index_change(combo_box)

    def del_row(self):
        row = self.currentRow()
        self.removeRow(row)

        for row in range(self.rowCount()):
            combo_box = self.cellWidget(row, 1)
            combo_box.set_index_row(row)

    def translit_rows(self):
        try:
            for i in range(self.rowCount()):
                item_0 = self.item(i, 0)
                data_item = item_0.get_item_data()
                item_0.setText(self.main_window.transliterator.get_tranlit(data_item.source_name.lower()))
        except Exception as e:
            logging.exception(e)
            self.main_window.statusBar.showMessage(f"Не удалось транслитеровать текст", 5000)

    def translate_rows(self):
        for i in range(self.rowCount()):
            item_0 = self.item(i, 0)
            data_item = item_0.get_item_data()
            translation = self.main_window.translate.translate(data_item.source_name)
            item_0.setText(translation.lower())

    def format_column_name_rows(self):
        for i in range(self.rowCount()):
            item_0 = self.item(i, 0)
            data_item = item_0.get_item_data()
            item_0.setText(data_item.column_name.replace(" ", "_"))

    def format_source_name_rows(self):
        for i in range(self.rowCount()):
            item_8 = self.item(i, 8)
            item_8.setText(to_camel_case(item_8.text()))

    def add_prefix(self, prefix: str):
        for i in range(self.rowCount()):
            item_0 = self.item(i, 0)
            data_item = item_0.get_item_data()
            if data_item.column_name:
                item_0.setText(f"{prefix}_{data_item.column_name}")

    def add_postfix(self, postfix: str):
        for i in range(self.rowCount()):
            item_0 = self.item(i, 0)
            data_item = item_0.get_item_data()
            if data_item.column_name:
                item_0.setText(f"{data_item.column_name}_{postfix}")


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_app):
        super(UiMainWindow, self).__init__()
        self.transliterator = Transliterator()
        self.translate = Translate(only_offline=True)
        self.main_app = main_app

        self._setupUi()
        self.actions = ActionMainWindow(self)
        self.clicked = ClickedMainWindow(self)

        self._setup_Action_MenuBar()
        self._setup_Action_ToolBar()

        self._connect_event()
        self._test_connect_translate()
        self._disable_element()

    def _setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1200, 800)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_DATA = UiTableWidgetData(self.centralwidget, self.main_app, self)
        self.gridLayout_3.addWidget(self.tableWidget_DATA, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 40))
        self.toolBar.setMovable(True)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget_OBJECT = QtWidgets.QDockWidget(self)
        self.dockWidget_OBJECT.setMinimumSize(QtCore.QSize(320, 320))
        self.dockWidget_OBJECT.setMaximumSize(QtCore.QSize(524287, 350))
        self.dockWidget_OBJECT.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_OBJECT.setObjectName("dockWidget_OBJECT")
        self.dockWidgetContents_OBJECT = QtWidgets.QWidget()
        self.dockWidgetContents_OBJECT.setObjectName("dockWidgetContents_OBJECT")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_OBJECT)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget_OBJECT = UiTableWidgetObject(self.dockWidgetContents_OBJECT, self.main_app)
        self.gridLayout.addWidget(self.tableWidget_OBJECT, 1, 0, 1, 1)
        self.btn_clear_OBJECT = QtWidgets.QPushButton(self.dockWidgetContents_OBJECT)
        self.btn_clear_OBJECT.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_OBJECT.setStyleSheet("QPushButton{\n"
                                            "background-color: rgba(232, 232, 232, 128);\n"
                                            "border: 1px solid rgb(204, 204, 204);\n"
                                            "border-top: none;\n"
                                            "border-radius: 0px;\n"
                                            "padding: 7px;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "background-color: rgb(255, 255, 210);\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed{\n"
                                            "background-color: rgba(255, 255, 255, 128);\n"
                                            "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/img/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear_OBJECT.setIcon(icon2)
        self.btn_clear_OBJECT.setObjectName("btn_clear_OBJECT")
        self.gridLayout.addWidget(self.btn_clear_OBJECT, 2, 0, 1, 1)
        self.dockWidget_OBJECT.setWidget(self.dockWidgetContents_OBJECT)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_OBJECT)
        self.dockWidget_COLUMNS = QtWidgets.QDockWidget(self)
        self.dockWidget_COLUMNS.setMinimumSize(QtCore.QSize(320, 428))
        self.dockWidget_COLUMNS.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_COLUMNS.setObjectName("dockWidget_COLUMNS")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget_COLUMNS = UiTableWidgetColumns(self.dockWidgetContents, self.main_app, self)
        self.gridLayout_2.addWidget(self.tableWidget_COLUMNS, 0, 0, 1, 1)
        self.frame_btn_translition = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame_btn_translition.setMinimumSize(QtCore.QSize(0, 32))
        self.frame_btn_translition.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame_btn_translition.setStyleSheet("#frame_btn_translition{\n"
                                                 "    border: 1px solid rgb(151, 153, 153);\n"
                                                 "    border-radius: 0px;\n"
                                                 "}")
        self.frame_btn_translition.setObjectName("frame_btn_translition")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_btn_translition)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_translit_PROPS = QtWidgets.QPushButton(self.frame_btn_translition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_translit_PROPS.sizePolicy().hasHeightForWidth())
        self.btn_translit_PROPS.setSizePolicy(sizePolicy)
        self.btn_translit_PROPS.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_translit_PROPS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_translit_PROPS.setStyleSheet("QPushButton{\n"
                                              "background-color: rgba(232, 232, 232, 128);\n"
                                              "border: 0px solid rgb(204, 204, 204);\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:hover{\n"
                                              "background-color: rgba(200, 200, 200, 128);\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed{\n"
                                              "background-color: rgba(255, 255, 255, 128);\n"
                                              "}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/img/tranlit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_translit_PROPS.setIcon(icon3)
        self.btn_translit_PROPS.setObjectName("btn_translit_PROPS")
        self.horizontalLayout.addWidget(self.btn_translit_PROPS)
        self.btn_translation_PROPS = QtWidgets.QPushButton(self.frame_btn_translition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_translation_PROPS.sizePolicy().hasHeightForWidth())
        self.btn_translation_PROPS.setSizePolicy(sizePolicy)
        self.btn_translation_PROPS.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_translation_PROPS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_translation_PROPS.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgba(232, 232, 232, 128);\n"
                                                 "border: 0px solid rgb(204, 204, 204);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgba(200, 200, 200, 128);\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:pressed{\n"
                                                 "background-color: rgba(255, 255, 255, 128);\n"
                                                 "}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/img/translate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_translation_PROPS.setIcon(icon4)
        self.btn_translation_PROPS.setObjectName("btn_translation_PROPS")
        self.horizontalLayout.addWidget(self.btn_translation_PROPS)
        self.gridLayout_2.addWidget(self.frame_btn_translition, 2, 0, 1, 1)
        self.frame_btn_rows = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame_btn_rows.setMinimumSize(QtCore.QSize(0, 32))
        self.frame_btn_rows.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame_btn_rows.setStyleSheet("#frame_btn_rows{\n"
                                          "    border: 1px solid rgb(151, 153, 153);\n"
                                          "    border-radius: 0px;\n"
                                          "}")
        self.frame_btn_rows.setObjectName("frame_btn_rows")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_btn_rows)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_add_row_DATA = QtWidgets.QPushButton(self.frame_btn_rows)
        self.btn_add_row_DATA.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_add_row_DATA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_row_DATA.setStyleSheet("QPushButton{\n"
                                            "background-color: rgba(232, 232, 232, 128);\n"
                                            "border: 0px solid rgb(204, 204, 204);\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "background-color: rgba(200, 200, 200, 128);\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed{\n"
                                            "background-color: rgba(255, 255, 255, 128);\n"
                                            "}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/img/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_row_DATA.setIcon(icon5)
        self.btn_add_row_DATA.setObjectName("btn_add_row_DATA")
        self.horizontalLayout_2.addWidget(self.btn_add_row_DATA)
        self.btn_clear_COLUMN = QtWidgets.QPushButton(self.frame_btn_rows)
        self.btn_clear_COLUMN.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_COLUMN.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_COLUMN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_COLUMN.setStyleSheet("QPushButton{\n"
                                            "background-color: rgba(232, 232, 232, 128);\n"
                                            "border: 0px solid rgb(204, 204, 204);\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "background-color: rgba(200, 200, 200, 128);\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed{\n"
                                            "background-color: rgba(255, 255, 255, 128);\n"
                                            "}")
        self.btn_clear_COLUMN.setIcon(icon2)
        self.btn_clear_COLUMN.setObjectName("btn_clear_COLUMN")
        self.horizontalLayout_2.addWidget(self.btn_clear_COLUMN)
        self.gridLayout_2.addWidget(self.frame_btn_rows, 1, 0, 1, 1)
        self.dockWidget_COLUMNS.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_COLUMNS)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Генератор SQL скрипта"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_OBJECT.setWindowTitle(_translate("MainWindow", "Object"))
        self.btn_clear_OBJECT.setText(_translate("MainWindow", "Очистить"))
        self.dockWidget_COLUMNS.setWindowTitle(_translate("MainWindow", "Колонки"))
        self.btn_translit_PROPS.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Транслит значение source_name</p></body></html>"))
        self.btn_translit_PROPS.setText(_translate("MainWindow", "Транслит"))
        self.btn_translation_PROPS.setToolTip(
            _translate("MainWindow", "<html><head/><body><p>Перевести значение source_name</p></body></html>"))
        self.btn_translation_PROPS.setText(_translate("MainWindow", "Перевод"))
        self.btn_add_row_DATA.setText(_translate("MainWindow", "Добавить"))
        self.btn_clear_COLUMN.setText(_translate("MainWindow", ""))

    def _setup_Action_ToolBar(self):
        self.action_tb_add_row = QAction(QIcon(":/icon_30/img/add_30.png"), "", self)
        self.action_tb_add_row.setStatusTip("Добавить новую строку.")
        self.action_tb_add_row.triggered.connect(lambda: self.actions.add_row(None))

        self.action_tb_del_row = QAction(QIcon(":/icon_30/img/del_30.png"), "", self)
        self.action_tb_del_row.setStatusTip("Удалить текущую строку.")
        self.action_tb_del_row.triggered.connect(self.actions.delete_row)

        self.action_tb_clear_table = QAction(QIcon(":/icon_30/img/clear_30.png"), "", self)
        self.action_tb_clear_table.setStatusTip("Очистить таблицу.")
        self.action_tb_clear_table.triggered.connect(self.actions.clear_table)

        if not self.translate.is_active():
            self.action_tb_translate = QAction(QIcon(":/icon_30/img/translate_30.png"), "", self)
        else:
            if self.translate.is_online():
                self.action_tb_translate = QAction(QIcon(":/icon_30/img/translate_online_30.png"), "", self)
            else:
                self.action_tb_translate = QAction(QIcon(":/icon_30/img/translate_offline_30.png"), "", self)

        self.action_tb_translate.setStatusTip("Перевод source_name в column_name.")
        self.action_tb_translate.triggered.connect(self.actions.translate)

        self.action_tb_translit = QAction(QIcon(":/icon_30/img/tranlit_30.png"), "", self)
        self.action_tb_translit.setStatusTip("Транслитерация source_name в column_name.")
        self.action_tb_translit.triggered.connect(self.actions.translit)

        self.action_tb_format_column_name = QAction(QIcon(":/icon_30/img/format_30.png"), "", self)
        self.action_tb_format_column_name.setStatusTip(
            "Форматировать колонку column_name. Пример: Text example -> text_example")
        self.action_tb_format_column_name.triggered.connect(self.actions.format_column_name)

        self.action_tb_format_source_name = QAction(QIcon(":/icon_30/img/format_1_30.png"), "", self)
        self.action_tb_format_source_name.setStatusTip(
            "Форматировать колонку source_name. Пример: text example -> TextExample")
        self.action_tb_format_source_name.triggered.connect(self.actions.format_source_name)

        self.action_tb_add_prefix = QAction(QIcon(":/icon_30/img/prefix_30.png"), "", self)
        self.action_tb_add_prefix.setStatusTip("Добавить префикс_ в колонку column_name. Пример: text -> prefix_text")
        self.action_tb_add_prefix.triggered.connect(self.actions.add_prefix)

        self.action_tb_add_postfix = QAction(QIcon(":/icon_30/img/postfix_30"), "", self)
        self.action_tb_add_postfix.setStatusTip(
            "Добавить _постфикс в колонку column_name. Пример: text -> text_postfix")
        self.action_tb_add_postfix.triggered.connect(self.actions.add_postfix)

        self.action_tb_sql_save = QAction(QIcon(":/icon_30/img/sql_save_30.png"), "", self)
        self.action_tb_sql_save.setStatusTip("Сохранить SQL-скрипт")
        self.action_tb_sql_save.triggered.connect(self.actions.sql_save)

        self.action_tb_sql_view = QAction(QIcon(":/icon_30/img/sql_view_30.png"), "", self)
        self.action_tb_sql_view.setStatusTip("Показать SQL-скрипт")
        self.action_tb_sql_view.triggered.connect(self.actions.sql_view)

        self.action_tb_md5_view = QAction(QIcon(":/icon_30/img/md5_30.png"), "", self)
        self.action_tb_md5_view.setStatusTip("Показать строку MD5")
        self.action_tb_md5_view.triggered.connect(self.actions.md5_view)

        self.toolBar.addAction(self.action_tb_add_row)
        self.toolBar.addAction(self.action_tb_del_row)
        self.toolBar.addAction(self.action_tb_clear_table)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.action_tb_format_column_name)
        self.toolBar.addAction(self.action_tb_add_prefix)
        self.toolBar.addAction(self.action_tb_add_postfix)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.action_tb_translate)
        self.toolBar.addAction(self.action_tb_translit)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.action_tb_format_source_name)

        self.toolBar.addSeparator()
        self.toolBar.addWidget(QtWidgets.QLabel("SQL"))
        self.toolBar.addAction(self.action_tb_sql_save)
        self.toolBar.addAction(self.action_tb_sql_view)

        self.toolBar.addSeparator()

        self.toolBar.addWidget(QtWidgets.QLabel("MD5"))
        self.toolBar.addAction(self.action_tb_md5_view)

    def _setup_Action_MenuBar(self):
        self.action_mb_close = QtWidgets.QAction(self)
        self.action_mb_close.setObjectName("action_mb_close")
        self.action_mb_close.setText("Закрыть")
        self.action_mb_close.triggered.connect(self.actions.close)

        self.action_mb_sql_save = QtWidgets.QAction(self)
        self.action_mb_sql_save.setObjectName("action_mb_sql_save")
        self.action_mb_sql_save.setText("Сохранить SQL")
        self.action_mb_sql_save.triggered.connect(self.actions.sql_save)

        self.action_mb_sql_view = QtWidgets.QAction(self)
        self.action_mb_sql_view.setObjectName("action_mb_sql_view")
        self.action_mb_sql_view.setText("Просмотр SQL")
        self.action_mb_sql_view.triggered.connect(self.actions.sql_view)

        self.action_mb_md5_view = QtWidgets.QAction(self)
        self.action_mb_md5_view.setObjectName("action_mb_md5_view")
        self.action_mb_md5_view.setText("Просмотр MD5")
        self.action_mb_md5_view.triggered.connect(self.actions.md5_view)

        self.action_mb_view_object = QtWidgets.QAction(self)
        self.action_mb_view_object.setObjectName("action_mb_view_object")
        self.action_mb_view_object.setText("Панель Object")
        self.action_mb_view_object.triggered.connect(self.actions.view_panel_object)

        self.action_mb_view_column = QtWidgets.QAction(self)
        self.action_mb_view_column.setObjectName("action_mb_view_column")
        self.action_mb_view_column.setText("Панель Колонки")
        self.action_mb_view_object.triggered.connect(self.actions.view_panel_column)

        self.action_mb_add_row = QtWidgets.QAction(self)
        self.action_mb_add_row.setObjectName("action_mb_add_row")
        self.action_mb_add_row.setText("Добавить строку")
        self.action_mb_add_row.triggered.connect(lambda: self.actions.add_row(None))

        self.action_mb_del_row = QtWidgets.QAction(self)
        self.action_mb_del_row.setObjectName("action_mb_del_row")
        self.action_mb_del_row.setText("Удалить строку")
        self.action_mb_del_row.triggered.connect(self.actions.delete_row)

        self.action_mb_clear_table = QtWidgets.QAction(self)
        self.action_mb_clear_table.setObjectName("action_mb_del_row")
        self.action_mb_clear_table.setText("Очистить таблицу")
        self.action_mb_clear_table.triggered.connect(self.actions.clear_table)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 24))
        self.menubar.setObjectName("menubar")

        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_file.setTitle("Файл")

        self.menu_view = QtWidgets.QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        self.menu_view.setTitle("Вид")

        self.menu_data = QtWidgets.QMenu(self.menubar)
        self.menu_data.setObjectName("menu_data")
        self.menu_data.setTitle("Данные")

        self.menu_info = QtWidgets.QMenu(self.menubar)
        self.menu_info.setObjectName("menu_info")
        self.menu_info.setTitle("Справка")
        self.setMenuBar(self.menubar)

        #
        # self.action_view_COLUMNS = QtWidgets.QAction(self)
        # self.action_view_COLUMNS.setObjectName("action_view_COLUMNS")
        # self.action_view_COLUMNS.setText("Показать заполнение")
        #
        # self.action_save_SQL = QtWidgets.QAction(self)
        # self.action_save_SQL.setObjectName("action_save_SQL")
        # self.action_save_SQL.setText("Сохранить SQL")
        #
        # self.action_view_SQL = QtWidgets.QAction(self)
        # self.action_view_SQL.setObjectName("action_view_SQL")
        # self.action_view_SQL.setText("Показать SQL")
        #
        # self.action_MD5 = QtWidgets.QAction(self)
        # self.action_MD5.setObjectName("action_MD5")
        # self.action_MD5.setText("XML-схема")
        #
        # self.action_clear_TABLE = QtWidgets.QAction(self)
        # self.action_clear_TABLE.setObjectName("action_clear_TABLE")
        # self.action_clear_TABLE.setText("Очистить таблицу")
        #
        # self.action_clear_DATA = QtWidgets.QAction(self)
        # self.action_clear_DATA.setObjectName("action_clear_DATA")
        # self.action_clear_DATA.setText("Очистить данные")
        #
        # self.action_INFO = QtWidgets.QAction(self)
        # self.action_INFO.setObjectName("action_INFO")
        # self.action_INFO.setText("О программе")
        #
        self.menu_file.addAction(self.action_mb_sql_save)
        self.menu_file.addAction(self.action_mb_sql_view)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_mb_md5_view)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_mb_close)

        self.menu_view.addAction(self.action_mb_view_object)
        self.menu_view.addAction(self.action_mb_view_column)

        # self.menu_data.addAction(self.action_mb_add_row)
        # self.menu_data.addAction(self.action_mb_del_row)
        self.menu_data.addAction(self.action_mb_clear_table)
        self.menu_data.addSeparator()

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_data.menuAction())
        self.menubar.addAction(self.menu_info.menuAction())

    def _connect_event(self):
        self.btn_add_row_DATA.clicked.connect(self.clicked.add_row)
        self.btn_clear_OBJECT.clicked.connect(self.clicked.clear_panel_object)
        self.btn_clear_COLUMN.clicked.connect(self.clicked.clear_panel_column)
        self.btn_translit_PROPS.clicked.connect(lambda: self.clicked.translation_panel_column("transliteration"))
        self.btn_translation_PROPS.clicked.connect(lambda: self.clicked.translation_panel_column("translate"))

    def _test_connect_translate(self):
        self.btn_translation_PROPS.setEnabled(self.translate.is_active())
        self.action_tb_translate.setEnabled(self.translate.is_active())
        self.action_tb_translate.setStatusTip(self.translate.get_state())

    def _disable_element(self):
        # self.action_tb_translit.setEnabled(False)
        # self.btn_translit_PROPS.setEnabled(False)
        pass

    def create_widget_combo_box(self, object_name, index_row, current_index=0):
        collection = tuple(self.main_app.data_type.__dict__.keys())
        combo_box = UiQComboBox(main_app=self.main_app, items_data=collection)
        combo_box.set_index_row(index_row)
        combo_box.setObjectName(object_name)
        combo_box.setCurrentIndex(current_index)
        combo_box.currentIndexChanged.connect(lambda: self.tableWidget_DATA.cb_current_index_change(combo_box))
        return combo_box

    def get_sql_text(self):
        sql_object = self.main_app.sql_object
        scope = get_text_null(sql_object.scope)
        object_s = get_text_null(sql_object.object)
        source_system = get_text_null(sql_object.source_system)
        source_type = get_text_null(sql_object.source_type)
        domain = get_text_null(sql_object.domain)
        template = get_text_null(sql_object.template)
        type_s = get_text_null(sql_object.type)
        dmt_view_source = get_text_null(sql_object.dmt_view_source)
        comment = get_text_null(sql_object.comment)

        sql_text_object = (
            f"INSERT INTO [data].[object] ([scope], [object], [source_system], [source_type], [domain], [template], [type], [dmt_view_source], [comment])"
            f"\n"
            f"VALUES ({scope}, {object_s}, {source_system}, {source_type}, {domain}, {template}, {type_s}, {dmt_view_source}, {comment});")

        sql_text_object_column = f"INSERT INTO [data].[object_column] ([scope], [object], [source_system], [column_name], [data_type], [length], [precision],[scale],[is_nullable],[is_key],[default_value],[source_name],[description],[comment]) VALUES"

        for row in range(self.tableWidget_DATA.rowCount()):
            item = self.tableWidget_DATA.item(row, 0)
            item_data = item.get_item_data()
            column_name = get_text_null(item_data.column_name)
            data_type = get_text_null(item_data.data_type)
            length = get_length(item_data.length)
            precision = get_text_null(item_data.precision)
            scale = get_text_null(item_data.scale)
            is_nullable = get_state(item_data.is_nullable)
            is_key = get_state(item_data.is_key)
            default_value = get_text_null(item_data.default_value)
            source_name = get_text_null(item_data.source_name)
            description = get_text_null(item_data.description)
            comment = get_text_null(item_data.comment)
            sql_text_object_column += f"\n({scope},{object_s},{source_system},{column_name},{data_type},{length},{precision},{scale},{is_nullable},{is_key},{default_value},{source_name},{description},{comment}),"

        sql_text_object_column = sql_text_object_column[:-1] + ';'
        sql_text_exec = f"EXEC [core_metadata].[exec].[create_dwh_objects] @object = '{sql_object.object}', @source_system = '{sql_object.source_system}', @scope = '{sql_object.scope}';"

        sql_text = f"{sql_text_object}\n\n{sql_text_object_column}\n\n{sql_text_exec}"
        return sql_text

    def get_md5_text(self):
        field_text = ""
        for row in range(self.tableWidget_DATA.rowCount()):
            item = self.tableWidget_DATA.item(row, 0)
            item_data = item.get_item_data()
            field_text += f"{item_data.source_name}||"
        field_text = field_text[:-2]
        return f"MD5({field_text})"


class ActionMainWindow:
    def __init__(self, main: UiMainWindow):
        self.main = main

    def add_postfix(self):
        dialog = UiDialogPrefixPostfix(self.main)
        dialog.setModal(True)
        result = dialog.exec()
        if result == 1:
            self.main.tableWidget_DATA.add_postfix(dialog.value_text)

    def add_prefix(self):
        dialog = UiDialogPrefixPostfix(self.main)
        dialog.setModal(True)
        result = dialog.exec()
        if result == 1:
            self.main.tableWidget_DATA.add_prefix(dialog.value_text)

    def add_row(self, table_object):
        if table_object is None:
            table_object = self.main.main_app.table_object()
        self.main.tableWidget_DATA.add_row(table_object)

    def clear_table(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Очистить таблицу?")
        msg.setWindowTitle("Информация")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            self.main.tableWidget_DATA.setRowCount(0)

    def close(self):
        self.main.close()

    def delete_row(self):
        self.main.tableWidget_DATA.del_row()

    def format_column_name(self):
        self.main.tableWidget_DATA.format_column_name_rows()

    def format_source_name(self):
        self.main.tableWidget_DATA.format_source_name_rows()

    def md5_view(self):
        md5_text = self.main.get_md5_text()
        dialog = UiDialogViewText(self.main, md5_text)
        dialog.setWindowTitle("Просмотр MD5")
        dialog.setModal(True)
        result = dialog.exec()
        if result == 1:
            pyperclip.copy(md5_text)
            self.main.statusBar.showMessage(f"MD5 - скопирован", 5000)

    def sql_save(self):
        sql_text = self.main.get_sql_text()
        default_filename = f"{self.main.main_app.sql_object.get_name()}.sql"

        filename, _ = QFileDialog.getSaveFileName(self.main, "Сохранить SQL-скрипт", default_filename,
                                                  "SQL-script (*.sql);;All Files (*)")

        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(sql_text)
                self.main.statusBar.showMessage(f"SQL - сохранен. {filename}", 5000)
                logging.info(f"Сохранен SQL. {filename}")
            except Exception as e:
                logging.exception(f"Save file error: {e}")

    def sql_view(self):
        sql_text = self.main.get_sql_text()
        dialog = UiDialogViewText(self.main, sql_text)
        dialog.setWindowTitle("Просмотр SQL")
        dialog.setModal(True)
        result = dialog.exec()
        if result == 1:
            pyperclip.copy(sql_text)
            self.main.statusBar.showMessage(f"SQL - скопирован", 5000)

    def translate(self):
        self.main.tableWidget_DATA.translate_rows()

    def translit(self):
        self.main.tableWidget_DATA.translit_rows()

    def view_panel_column(self):
        self.main.dockWidget_COLUMNS.show()

    def view_panel_object(self):
        self.main.dockWidget_OBJECT.show()


class ClickedMainWindow:
    def __init__(self, main: UiMainWindow):
        self.main = main

    def add_row(self):
        self.main.tableWidget_COLUMNS.select_next_row()
        self.main.actions.add_row(self.main.tableWidget_COLUMNS.table_object)

    def clear_panel_object(self):
        self.main.tableWidget_OBJECT.clear_items()

    def clear_panel_column(self):
        self.main.tableWidget_COLUMNS.clear_items()

    def translation_panel_column(self, type_translation):
        self.main.tableWidget_COLUMNS.select_next_row()
        item_source_name = self.main.tableWidget_COLUMNS.item(self.main.main_app.columns.index("source_name"), 1)
        item_column_name = self.main.tableWidget_COLUMNS.item(self.main.main_app.columns.index("column_name"), 1)
        text_source_name = item_source_name.text()

        if type_translation == "translate":
            translation = self.main.translate.translate(text_source_name)
            item_column_name.setText(translation)
        elif type_translation == "transliteration":
            text_translit = self.main.transliterator.get_tranlit(text_source_name)
            item_column_name.setText(text_translit)
        else:
            item_column_name.setText("")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    ui = UiMainWindow(None)
    ui.show()
    sys.exit(app.exec_())
