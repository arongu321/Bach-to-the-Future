# Later on auto install required libraries

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        # screen = QtWidgets.QDesktopWidget().screenGeometry(-1) # use screen.width() and screen.height()
        # self.setGeometry(0, 0, screen.width(), screen.height()) 
        # .setGeometry(xpos, ypos, width, height)
        # (0,0) is the top left corner of screen
        # self.showMaximized()
        self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle("TEST UI WINDOW LOLOLOLOLOLOLOL")
        self.initUI()

    def initUI(self):
        # Put all the stuff we want here in the window
        # Widgets that we want in the window
        self.label = QtWidgets.QLabel(self)
        self.label.setText("TEST LABEL LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOL")
        self.label.move(50,50)
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("TEST BUTTON LOLOLOLOLOL")
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("CLICKED LOLOLOLOLOLOLOL")

    def update(self):
        self.label.adjustSize()

def window(): # Defines application called window
    app = QApplication(sys.argv)
    win = myWindow()
    win.show() # Shows the window
    sys.exit(app.exec_()) # Closes application when you hit "X"


if __name__ == "__main__":
    window()