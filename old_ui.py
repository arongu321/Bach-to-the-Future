# Later on auto install required libraries shown below
# pip install PyQt5
# pip install pyqt-tools
# pip install qdarkgraystyle

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
import sys
import qdarkgraystyle
from time import sleep

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        # Determines the properties of the application.
        # screen = QtWidgets.QDesktopWidget().screenGeometry(-1) # use screen.width() and screen.height()
        # (0,0) is the top left corner of screen
        # .setGeometry(xpos, ypos, width, height)
        # self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle("Listing Scraper 3000")
        self.setGeometry(1000,1000, 400, 400)
        self.initUI()


    def initUI(self):
        # Widgets that we want in the window (labels, etc)

        # Label
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Type something into the box, and\ncheck at least one of the boxes below!')
        self.label.adjustSize()
        self.label.move(25,85)


        # Search button
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText('Search')
        # self.button.adjustSize()
        self.button1.move(250,25)
        self.button1.setDisabled(True)
        self.button1.clicked.connect(self.start_search)
        self.button1.setDisabled(True)


        # Input line
        self.input = QtWidgets.QLineEdit(self)
        self.input.setDragEnabled(True) # Can drag text within text box, as well as copy and paste
        self.input.setPlaceholderText('What are you looking for?')
        self.input.resize(200,30)
        self.input.move(25,25)
        #FIXME When you enter text, and then empty self.input, button1 is not disabled.
        self.input.textChanged.connect(self.checkdisableButton)
        if not self.input.text():
            self.button1.setDisabled(True)


        # Amazon checkbox
        self.check1 = QtWidgets.QCheckBox(self)
        self.check1.setText('Amazon')
        self.check1.adjustSize()
        self.check1.move(25,125)
        self.check1.stateChanged.connect(self.checkdisableButton)

        # eBay checkbox
        self.check2 = QtWidgets.QCheckBox(self)
        self.check2.setText('eBay')
        self.check2.adjustSize()
        self.check2.move(25,165)
        self.check2.stateChanged.connect(self.checkdisableButton)

        # FB Marketplace checkbox
        self.check3 = QtWidgets.QCheckBox(self)
        self.check3.setText('Facebook Marketplace')
        self.check3.adjustSize()
        self.check3.move(25,205)
        self.check3.stateChanged.connect(self.checkdisableButton)

        # Kijiji checkbox
        self.check4 = QtWidgets.QCheckBox(self)
        self.check4.setText('Kijiji')
        self.check4.adjustSize()
        self.check4.move(25,245)
        self.check4.stateChanged.connect(self.checkdisableButton)

        # I could make a button group with QButtonGroup, however I don't have the time.

        # # Super secret debug checkbox
        # self.check5 = QtWidgets.QCheckBox(self)
        # self.check5.setText('Super Top Secret Debug')
        # self.check5.adjustSize()
        # self.check5.move(250,85)


    def start_search(self):
        self.button1.setText('Searching...')
        self.search()

    def search(self):
        # sleep(3) # Temporary, call to main.py
        # self.input.text() is the text of the input box
        # self.check1.isChecked() - if Amazon checked
        # self.check2.isChecked() - if eBay checked
        # self.check3.isChecked() - if FB Marketplace checked
        # self.check4.isChecked() - if Kijiji checked
        self.finished_search()

    def finished_search(self):
        self.button1.setDisabled(False)
        self.button1.setText('Search again...')
        pass

    def checkdisableButton(self):
        if (self.input.text() != '') and (self.check1.isChecked() or self.check2.isChecked() or self.check3.isChecked() or self.check4.isChecked()):
            self.button1.setDisabled(False)
        else:
            self.button1.setDisabled(True)
            


def window(): # Defines application called window
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    win = mainWindow()
    win.show() # Shows the window
    sys.exit(app.exec_()) # Closes application when you hit "X"

if __name__ == "__main__":
    window()