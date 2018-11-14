import os
import sys
from PyQt5 import QtWidgets,QtCore

#Server client import
sys.path.insert(0, '../saserver')

from client import ServerClient

#Abs path mapper
def getAbsPath(path):
	return (os.path.split(os.path.abspath(__file__))[0] + '/' + path).replace("\\", "/")

#Creates new messagebox with given title and description
def show_message(title, desc):
	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Information)
	msg.setText(desc)
	msg.setWindowTitle(title)
	msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
	msg.exec_()

def moveFromCenter(window, left):
	center = QtWidgets.QDesktopWidget().availableGeometry().center()
	fg = window.frameGeometry()
	widget = window.geometry()

	print(center)
	if left:
		x = center.x()-int(widget.width()*0.55)
	else:
		x = center.x()+int(widget.width()*0.55)

	y = center.y()
	fg.moveCenter(QtCore.QPoint(x, y))
	window.move(fg.topLeft())