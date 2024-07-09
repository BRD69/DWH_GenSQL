from PyQt5 import QtCore, QtGui, QtWidgets


class UiDialogViewText(QtWidgets.QDialog):
    def __init__(self, parent=None, text=""):
        super(UiDialogViewText, self).__init__(parent)
        self.text = text
        self._setupUi()
        self._load_data()
    def _setupUi(self):
        self.setObjectName("DialogViewSQL")
        self.resize(600, 350)
        self.setBaseSize(QtCore.QSize(600, 350))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

        self._retranslateUi()
        self.buttonBox.accepted.connect(self.accept) # type: ignore
        self.buttonBox.rejected.connect(self.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DialogViewSQL", "Dialog"))

    def _load_data(self):
        self.textEdit.setText(self.text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = UiDialogViewText()
    ui.show()
    sys.exit(app.exec_())
