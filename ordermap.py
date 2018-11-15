from PyQt5 import QtWidgets,QtCore,QtGui
from utils import *
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from orderplacer import OrderPlacerView
import json

# Operator map view
class OrderMapView(QtWidgets.QMainWindow):

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

    def reloadOrders(self):
        self.orderList.clear()
        self.orderText.clear()
        orders, response = sendRequest("getOrders")
        #Result is unparsable
        if orders == None:
            return

        self.orders = orders
        keys = ["Order "+str(order["id"]) for order in self.orders]
        self.orderList.clear() 
        self.orderList.setCurrentIndex(0)
        self.orderList.addItems(keys)

    def onOrderSelect(self):
        self.orderMap.page().runJavaScript("removeRoutes();")
        if len(self.orderList.currentText().split(" "))==1:
            return
        selectedID = int(self.orderList.currentText().split(" ")[1])

        for order in self.orders:
            if order["id"]==selectedID:
                self.orderMap.page().runJavaScript("removeDrivers();")
                self.orderMap.page().runJavaScript("addWarehouses([" + self.warehouses + "]);")
                self.orderText.setText(self.orderStringifier(order))
                pointsToFit = []
                for driver in self.drivers:
                    if order["carrier"] == None:
                        return
                    elif driver["id"] == int(order["carrier"]):
                        self.orderMap.page().runJavaScript("renderDrivers([" + json.dumps(driver) + "]);")
                        if order["path"] == None:
                            #You can start specifying the route
                            return
                        else:
                            self.orderMap.page().runJavaScript("renderPath(" + json.dumps(order["path"]) + "); fitAll();")

    def placeOrder(self):
        if len(self.orderList.currentText().split(" "))==1:
            return
        selectedID = int(self.orderList.currentText().split(" ")[1])

        for order in self.orders:
            if order["id"]==selectedID:
                if order["status"].lower()!="created".lower():
                    show_message("Error","This order is already processed")
                    return
                else:
                    self.placer = OrderPlacerView("orderplacer.ui",order)

    def reloadDrivers(self):
        drivers, response = sendRequest("getDrivers")
        #Result is unparsable
        self.drivers = drivers
        if drivers ==None:
            return
        self.orderMap.page().runJavaScript("renderDrivers(" + response + ");")

    def reloadWarehouses(self):
        warehouses, response = sendRequest("getWarehouses")
        self.warehouses = response
        #Result is unparsable
        if warehouses ==None:
            return
        self.orderMap.page().runJavaScript("addWarehouses(" + response + ");")

    # Function to reaload page
    def reloadPage(self):
        self.orderMap.setUrl(QtCore.QUrl(getAbsPath("orderMap.html")))
        self.orderList.clear()
        self.orderText.clear()

    def reloadData(self):
        self.reloadWarehouses()
        self.reloadDrivers()
        self.reloadOrders()

    def __init__(self, UI_Path):
        super(OrderMapView, self).__init__()
        uic.loadUi(UI_Path, self)
        self.orderMap.setUrl(QtCore.QUrl(getAbsPath("orderMap.html")))
        self.orderRefreshButton.clicked.connect(self.reloadData)
        # Ctrl+R shortcut for refreshing the page
        self.createOrderButton.clicked.connect(self.placeOrder)

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.reloadPage)
        self.orderList.currentIndexChanged.connect(self.onOrderSelect)
        #Move to the right in order to eliminate intersection of the views
        moveFromCenter(self,False)
        self.show()