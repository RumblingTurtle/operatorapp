import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import csv
import os

#Returns absolute path relative to cwd
def getAbsPath(path):
    return (os.path.split(os.path.abspath(__file__))[0]+'/'+path).replace("\\","/")

#Checks username and password in the database(Server communication routine neede)
def checkUser(username, password):
        return True

#Creates new messagebox with given title and description
def show_message(title, desc):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(desc)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec_()

#Login page Interface
class LoginPage(QtWidgets.QMainWindow):
    def __init__(self, UI_Path):
        super(LoginPage, self).__init__()
        uic.loadUi(UI_Path, self)
        self.loginButton.clicked.connect(self.login)
        self.show()

    #Checks validity of the entered username and password
    def login(self):
        #Get text values
        username = self.username.text()
        password = self.password.text()

        #If one of the fields is empty
        if not password or not username:
            show_message("Invalid format","Username and password fields should be filled")
        elif checkUser(username,password):
            #change view
            self.hide()
            self.myOtherWindow = MapView("map.ui")
            self.myOtherWindow.show()
        else:
            #If login failed
            show_message("Invalid credentials","Please provide correct username and password")

#Operator map view
class MapView(QtWidgets.QMainWindow):
    def printPoints(self, points):
        print(points)

    #Calls javascript function that fetches all points on the map
    def getPoints(self):
        points = self.map.page().runJavaScript('function getPoints(){coordinates = [];\
            objectToArray(pointHopper).forEach(function(d, i) {coordinates.push(d.geometry.coordinates);});\
            return coordinates.join(";");}\
            getPoints()', self.printPoints)

    #Function to reaload page
    def reloadPage(self):
        self.map.setUrl(QtCore.QUrl(getAbsPath("map.html")))

    def __init__(self, UI_Path):
        super(MapView, self).__init__()
        uic.loadUi('map.ui', self)
        self.map.setUrl(QtCore.QUrl(getAbsPath("map.html")))
        self.pointsButton.clicked.connect(self.getPoints)
        #Ctrl+R shortcut for refreshing the page
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.reloadPage)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginPage("login.ui")
    sys.exit(app.exec_())    