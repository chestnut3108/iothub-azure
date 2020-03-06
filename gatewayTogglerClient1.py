# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gatewayToggler.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import socket
import sys
import threading

from PyQt5 import QtCore, QtGui, QtWidgets

from config import DeviceConfig, GatewayConfig
from socketUtil import socketServerStart




class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Device Id :-"+CLIENT_ID)
		Dialog.resize(400, 300)
		self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")
		self.pushButton = QtWidgets.QPushButton(Dialog)
		self.pushButton.setGeometry(QtCore.QRect(120, 20, 131, 31))
		self.pushButton.setCheckable(False)
		self.pushButton.setObjectName("pushButton")
		self.pushButton.clicked.connect(lambda:self.changeGatewayOnClick(self.pushButton))
		self.pushButton_2 = QtWidgets.QPushButton(Dialog)
		self.pushButton_2.setGeometry(QtCore.QRect(120, 70, 131, 41))
		self.pushButton_2.setObjectName("pushButton_2")
		self.pushButton_2.clicked.connect(lambda:self.changeGatewayOnClick(self.pushButton_2))
		self.pushButton_3 = QtWidgets.QPushButton(Dialog)
		self.pushButton_3.setGeometry(QtCore.QRect(40, 140, 75, 41))
		self.pushButton_3.setObjectName("pushButton_3")
		self.pushButton_3.clicked.connect(lambda:self.changeGatewayOnClick(self.pushButton_3))
		self.pushButton_4 = QtWidgets.QPushButton(Dialog)
		self.pushButton_4.setGeometry(QtCore.QRect(244, 142, 91, 41))
		self.pushButton_4.setObjectName("pushButton_4")
		self.pushButton_4.clicked.connect(lambda:self.changeGatewayOnClick(self.pushButton_4))
		self.retranslateUi(Dialog)
		self.buttonBox.accepted.connect(Dialog.accept)
		self.buttonBox.rejected.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Device Id :- "+CLIENT_ID))
		self.pushButton.setText(_translate("Dialog", "Factory"))
		self.pushButton_2.setText(_translate("Dialog", "Warehouse"))
		self.pushButton_3.setText(_translate("Dialog", "Store_A"))
		self.pushButton_4.setText(_translate("Dialog", "Store_B"))

	def changeGatewayOnClick(self,gatewayName):
		print( "Changing gateway to "+gatewayName.text())
		gatewayPort =  GatewayConfig[gatewayName.text()]
		s = socket.socket()
		s.connect(('127.0.0.1',gatewayPort))
		s.send(CLIENT_ID.encode())
		s.close()
		
		


CLIENT_ID = 'client1'
#Asynchronously listen to socket from server
server_port = DeviceConfig[CLIENT_ID]
x = threading.Thread(target=socketServerStart, args=[server_port], daemon=True)
x.start()



socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())
