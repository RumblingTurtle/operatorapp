from PyQt5 import QtWidgets,QtCore,QtGui
from utils import *
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

# Operator map view
class OrderMapView(QtWidgets.QMainWindow):
    def reloadDrivers(self):
        client = ServerClient("127.0.0.1", 9090, False)
        try:
            response = client.oneShotMessage("getDrivers", "utf-8", 1024)
        except Exception:
            print("Can't fetch driver data")
            return

        if response == None:
            return
        drivers = json.loads(response)
        self.driverMap.page().runJavaScript("addDrivers(" + response + ");")

    def printPoints(self, points):
        print(points)

    # Calls javascript function that fetches all points on the map
    def getPoints(self):
        points = self.map.page().runJavaScript('function getPoints(){coordinates = [];\
            objectToArray(pointHopper).forEach(function(d, i) {coordinates.push(d.geometry.coordinates);});\
            return coordinates.join(";");}\
            getPoints()', self.printPoints)

    # Function to reaload page
    def reloadPage(self):
        self.orderMap.setUrl(QtCore.QUrl(getAbsPath("orderMap.html")))

    def __init__(self, UI_Path):
        super(OrderMapView, self).__init__()
        uic.loadUi(UI_Path, self)
        self.orderMap.setUrl(QtCore.QUrl(getAbsPath("orderMap.html")))
        self.orderRefreshButton.clicked.connect(self.reloadDrivers)
        # Ctrl+R shortcut for refreshing the page
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.reloadPage)
        #Move to the right in order to eliminate intersection of the views
        moveFromCenter(self,False)
        self.show()