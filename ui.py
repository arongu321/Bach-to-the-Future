# Later on auto install required libraries shown below
# pip install PyQt5
# pip install pyqt-tools
# pip install qdarkgraystyle
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGroupBox
import sys
import qdarkgraystyle

class mainWindow(QDialog):
    
    def __init__(self):
        super(mainWindow, self).__init__()
        # Determines the properties of the application.
        # screen = QtWidgets.QDesktopWidget().screenGeometry(-1) # use screen.width() and screen.height()
        # (0,0) is the top left corner of screen
        # .setGeometry(xpos, ypos, width, height)
        # self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle("UI test in a grid")
        self.setGeometry(400, 400, 400, 400)
        self.initUI()


    def initUI(self):
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        #.adjustSize() when clicked (updating)

    def createGridLayout(self):
        # Widgets that we want in the window (labels, etc)
        self.horizontalGroupBox = QGroupBox("Web Scraper 3000")
        layout = QGridLayout(self)

        layout.addWidget(QLineEdit('What would you like to look for?'), 0, 0)

        self.horizontalGroupBox.setLayout(layout)
        

def window(): # Defines application called window
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    win = mainWindow()
    win.show() # Shows the window
    sys.exit(app.exec_()) # Closes application when you hit "X"

if __name__ == "__main__":
    window()