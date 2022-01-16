# Later on auto install required libraries

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        # Determines the properties of the application.
        # screen = QtWidgets.QDesktopWidget().screenGeometry(-1) # use screen.width() and screen.height()
        # (0,0) is the top left corner of screen
        # .setGeometry(xpos, ypos, width, height)
        self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle("Super basic UI test with widgets")
        self.initUI()

    def initUI(self):
        # Widgets that we want in the window (labels, etc)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Type something into the box!')
        self.label.adjustSize()
        self.label.move(50,50)
        
        # Input line
        self.input = QtWidgets.QLineEdit(self)
        self.input.setDragEnabled(True) # Can drag text within text box, as well as copy and paste
        self.input.setPlaceholderText("What are you looking for?")
        self.input.resize(250,30)
        self.input.move(200,200)
        self.input.returnPressed.connect(self.update_text) # Hit enter
        # Call main or something on this line

        # Reset text button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Press me to reset the label!')
        self.button.adjustSize()
        self.button.move(300,50)
        self.button.clicked.connect(self.reset_text) # Reset

    
    #def clicked(self):
    #    self.label.setText("THIS LABEL IS NOW CLICKED OR ENTERED (not being used right now)")
    #    self.update()

    def reset_text(self):
        self.label.setText('Type something into the box!')
        self.update()

    def update_text(self):
        self.label.setText(self.input.text()) # Gets text and updates label after pressing enter
        self.update()

    def update(self):
        self.label.adjustSize()

def window(): # Defines application called window
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = mainWindow()
    win.show() # Shows the window
    sys.exit(app.exec_()) # Closes application when you hit "X"

if __name__ == "__main__":
    window()