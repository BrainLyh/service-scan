# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ver1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(439, 345)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 131, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ftp_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ftp_label.setObjectName("ftp_label")
        self.verticalLayout.addWidget(self.ftp_label)
        self.mysql_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.mysql_label.setObjectName("mysql_label")
        self.verticalLayout.addWidget(self.mysql_label)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 50, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ftp_scan = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.ftp_scan.setObjectName("ftp_scan")
        self.verticalLayout_2.addWidget(self.ftp_scan)
        self.mysql_scan = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.mysql_scan.setObjectName("mysql_scan")
        self.verticalLayout_2.addWidget(self.mysql_scan)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(40, 140, 256, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ftp_label.setText(_translate("Form", "FTP server"))
        self.mysql_label.setText(_translate("Form", "MySQL server"))
        self.ftp_scan.setText(_translate("Form", "开始扫描"))
        self.mysql_scan.setText(_translate("Form", "开始扫描"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">扫描结果如下：</span></p></body></html>"))
