import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QKeyEvent
from PyQt5.QtCore import Qt, QRect
from api.data_dragon import *

class App(QWidget):
    #init
    def __init__(self):
        super().__init__()
        self.initUI()
    #create all widgets
    def initUI(self):
        #selection label
        self.type_selection_label = QLabel(self)
        self.type_selection_label.setText("<h3>"
                                          "选择<i><u>英雄</u></i>或<i><u>装备</u></i>."
                                          "<h2>")
        self.type_selection_label.move(50, 50)
        #selection
        self.type_selection = QComboBox(self)
        self.type_selection.addItem("英雄")
        self.type_selection.addItem("装备")
        self.type_selection.move(50, 80)
        #input label
        self.input_label = QLabel(self)
        self.input_label.setText("<h3>"
                                 "输入<i><u>英雄</u></i>或<i><u>装备</u></i>的英文名称"
                                 "</h2>")
        self.input_label.move(50, 170)
        #input
        self.input = QLineEdit(self)
        self.input.move(50, 200)
        #search button
        self.search_button = QPushButton("搜索🔍", self)
        self.search_button.move(50, 250)
        self.search_button.clicked.connect(self.search)

        self.output = QTextBrowser(self)
        self.output.setGeometry(QRect(400, 50, 750, 900))
        self.output.setText("<h1>"
                            "咕咕咕~"
                            "</h1>")
        #window
        self.resize(1200, 1000)
        self.center()
        self.setWindowTitle('PBE Translate en->zh --- by cocdeshijie')
        self.show()

    def search(self):
        selection = self.type_selection.currentText()
        input = self.input.text()
        if selection == "英雄":
            self.output.setText(zh_CN(selection=selection, input=input).champion_data())
        if selection == "装备":
            self.output.setText(zh_CN(selection=selection, input=input).item_data())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Enter:
                self.search()


def main():
    app = QApplication(sys.argv)
    #dark mode
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    main = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()