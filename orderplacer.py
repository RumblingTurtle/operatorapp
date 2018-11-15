from PyQt5 import QtWidgets,QtCore,QtGui
from utils import *
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

# Operator map view
class OrderPlacerView(QtWidgets.QMainWindow):

    def orderStringifier(self,order):
        oId = order["id"]
        rAddress = order["rAddress"]
        sAddress = order["sAddress"]
        receiverId = order["receiverId"]
        senderId = order["senderId"]
        status = order["status"]
        note = order["note"]
        sendDate = order["sendDate"]
        expectedDeliveryDate = order["expectedDeliveryDate"]
        path = order["path"]
        carrier = order["carrier"]

        return "Id: {} \nStatus: {} \nReceiver address: {} \nReceiver id: {} \nSender address: {} \nSender id: {} \nNote: {} \nDate sent: {} \nExpected arrival: {} \nCarrier id: {} \n"\
                    .format(oId,status,rAddress,receiverId,sAddress, senderId,note,sendDate,expectedDeliveryDate, carrier)

    def placeOrder(self,points):
        print(points)
        points = points.split(";")
        result = []
        for p in points:
            s = p.split(",")
            result.append([float(s[0]),float(s[1])])
        sendRequest("setRoute:"+str(self.order["id"])+"|"+json.dumps(result))
        self.close()

    def denyOrder(self):
         self.denyButton.clicked.connect(self.denyOrder)
    # Calls javascript function that fetches all points on the map
    def getPoints(self):
        points = self.orderPlacerMap.page().runJavaScript('function getPoints(){coordinates = [];\
            objectToArray(pointHopper).forEach(function(c) {coordinates.push(c);});\
            return coordinates.join(";");}\
            getPoints()', self.placeOrder)
                    

    def reloadWarehouses(self):
        warehouses, response = sendRequest("getWarehouses")
        #Result is unparsable
        if warehouses == None:
            return
        self.orderPlacerMap.page().runJavaScript("addWarehouses(" + response + ");")

    # Function to reaload page
    def reloadPage(self):
        self.orderPlacerMap.setUrl(QtCore.QUrl(getAbsPath("orderPlacer.html")))
        self.reloadWarehouses()

    def __init__(self, UI_Path, order):
        super(OrderPlacerView, self).__init__()
        uic.loadUi(UI_Path, self)
        self.orderPlacerMap.setUrl(QtCore.QUrl(getAbsPath("orderPlacer.html")))
        self.mapRefreshButton.clicked.connect(self.reloadPage)
        self.denyButton.clicked.connect(self.denyOrder)
        # Ctrl+R shortcut for refreshing the page
        self.placeOrderButton.clicked.connect(self.getPoints)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.reloadPage)
        self.order = order
        self.orderText.setText(self.orderStringifier(self.order))
        self.show()