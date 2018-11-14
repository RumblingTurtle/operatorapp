from PyQt5 import QtWidgets,QtCore,QtGui
from utils import *
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

# Operator map view
class DriverMapView(QtWidgets.QMainWindow):
	def reloadDrivers(self):
		client = ServerClient("127.0.0.1", 9090, False)
		try:
			response = client.oneShotMessage("getDrivers", "utf-8", 1024)
		except Exception:
			show_message("Connection error","Can't reach server")
			return

		if response == None:
			return
		drivers = json.loads(response)
		
		self.driverMap.page().runJavaScript("addDrivers(" + response + ");")
		driverElements = []
		for driver in drivers:
			driverElements.append(str(driver["id"])+":"+driver["name"]+" "+ driver["surname"])

		self.driverList.clear()
		for dinfo in driverElements:
			self.driverList.addItem(QtGui.QIcon(), dinfo)

	# Function to reaload page
	def reloadPage(self):
		self.driverMap.setUrl(QtCore.QUrl(getAbsPath("driverMap.html")))

	def __init__(self, UI_Path):
		super(DriverMapView, self).__init__()
		uic.loadUi(UI_Path, self)
		self.driverMap.setUrl(QtCore.QUrl(getAbsPath("driverMap.html")))
		self.driverRefreshButton.clicked.connect(self.reloadDrivers)

		# Ctrl+R shortcut for refreshing the page
		self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
		self.shortcut.activated.connect(self.reloadPage)
		#Move to the left in order to eliminate intersection of the views 
		moveFromCenter(self,True)
		self.show()