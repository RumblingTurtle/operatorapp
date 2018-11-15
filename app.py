from PyQt5 import QtWidgets,QtCore,QtGui
from utils import *
from PyQt5 import uic
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from drivermap import DriverMapView
from ordermap import OrderMapView

# Checks username and password in the database
def checkUser(username, password):
	try:
		client = ServerClient("127.0.0.1", 9090, False)
	except Exception:
		show_message("Connection error","Can't reach server")
		return 

	response = client.oneShotMessage(
	"checkuser:" + username + "|" + password, "utf-8", 128)
	print(response)
	if response == "OK":
		return "OK"
	else:
		# If login failed
		show_message("Invalid credentials","Please provide correct username and password")

# Login page Interface


class LoginPage(QtWidgets.QMainWindow):
	def __init__(self, UI_Path):
		super(LoginPage, self).__init__()
		uic.loadUi(UI_Path, self)
		self.loginButton.clicked.connect(self.login)
		self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self)
		self.shortcut.activated.connect(self.login)
		self.show()

	# Checks validity of the entered username and password
	def login(self):
		# Get text values
		username = self.username.text()
		password = self.password.text()

		# If one of the fields is empty
		if not password or not username:
			show_message("Invalid format",
						 "Username and password fields should be filled")
		elif checkUser(username, password):
			# change view
			self.hide()
			self.driverWindow = DriverMapView("drivermap.ui")
			self.orderWindow = OrderMapView("ordermap.ui")
			self.driverWindow.show()
			self.orderWindow.show()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = LoginPage("login.ui")
	sys.exit(app.exec_())
