from PyQt5 import QtCore, QtGui, QtWidgets


class UiDialogPrefixPostfix(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UiDialogPrefixPostfix, self).__init__(parent)
        self.value_text = ""
        self._setupUi()
        self._connect_event()

    def _setupUi(self):
        self.setObjectName("DialogPrefixPostfix")
        self.resize(300, 75)
        self.setMinimumSize(QtCore.QSize(300, 75))
        self.setMaximumSize(QtCore.QSize(300, 75))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.lineEdit.setStyleSheet("QLineEdit{\n"
                                    "    padding-left: 5px;\n"
                                    "    border: 1px solid rgb(205, 205, 205);\n"
                                    "    border-radius: 3px;\n"
                                    "}")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self._retranslateUi()
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DialogPrefixPostfix", "Добавить префикс/постфикс"))

    def _connect_event(self):
        self.lineEdit.textEdited.connect(self._edited_text)

    def _edited_text(self):
        self.value_text = self.lineEdit.text()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = UiDialogPrefixPostfix()
    ui.show()
    sys.exit(app.exec_())
