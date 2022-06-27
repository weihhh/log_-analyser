# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
#导入designer工具生成的login模块
from log_handler_gui import Ui_MainWindow
import re
import time
from dateutil import parser

pattern = r'\[(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}.\d{6})\]\[(\d+)-(\d+)\].*'
logTimeStamp = []
logStrList = []
logTimeGap = []
lastTimeStamp = 0



#TODO:
#1.更新时差按钮  （DONE）
#2.筛选后结果再次筛选
#3.reset到初始表格
#4.输入后回车筛选

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.folder_path=None
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton.clicked.connect(self.searchKeyWord)
        self.pushButton_2.clicked.connect(self.openFile)
        # self.pushButton_3.clicked.connect(self.updateTimeGap)
        self.ShowTable()

    def searchKeyWord(self):
        #利用line Edit控件对象text()函数获取界面输入
        keyWord = self.lineEdit.text()
        logSize = len(logStrList)
        tableLogSize = self.tableWidget.rowCount()
        resultNum = 0
        lastTimeStampInTable = 0
        #利用text Browser控件对象setText()函数设置界面显示
        # self.textBrowser.setText("登录成功!\n" + "用户名是: "+ username)
        self.tableWidget.setRowCount(logSize)
        for index, log in enumerate(logStrList):
            if keyWord in log:
                print("Key in: " + log)
                self.tableWidget.setItem(resultNum, 0, QTableWidgetItem(log))  # 设置j行i列的内容为Value
                if resultNum == 0:
                    lastTimeStampInTable = logTimeStamp[index]
                timeGapLocal = "{:.6f}".format((logTimeStamp[index] - lastTimeStampInTable).total_seconds())
                self.tableWidget.setItem(resultNum, 1,
                                         QTableWidgetItem(timeGapLocal))  # 设置j行i列的内容为Value
                lastTimeStampInTable = logTimeStamp[index]
                resultNum = resultNum + 1
            else:
                print("Key not in: " + log)
        print("Search result number: " + str(resultNum))
        self.tableWidget.setRowCount(resultNum)
        # if tableLogSize > resultNum:
        #     for rP in range(resultNum, logSize)[::-1]:
        #         print("Delete {0} key : {1}".format(str(rP), self.tableWidget.item(rP, 0).text()))
        #         self.tableWidget.removeRow(rP)
        #     print("After delete key : " + str(self.tableWidget.rowCount()))

    def openFile(self):
        # 选择文件夹槽
        self.folder_path = QFileDialog.getOpenFileName(self, "选择日志文件")
        if not self.folder_path:
            print("Not select file.")
            return
        logStrList.clear()
        logTimeGap.clear()
        self.textBrowser.setText("{0}\n".format(self.folder_path[0]))
        print("Selected file: {0}".format(self.folder_path[0]))
        with open(self.folder_path[0]) as f:
            for index, log in enumerate(f):
                patternCompiled = re.compile(pattern)
                result = patternCompiled.match(log)
                if not result:
                    print("Not match: ", log)
                    continue
                logStrList.append(log)
                timeStr = result.group(1)
                print("time extracted: ", timeStr)
                print("pid extracted: ", result.group(2))
                print("tid extracted: ", result.group(3))
                timeStamp = parser.parse(timeStr)
                logTimeStamp.append(timeStamp)
                # datetime_obj = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S.%f')
                # timeStamp = time.mktime(datetime_obj.timetuple()) * 1000000 + datetime_obj.microsecond
                print("time extracted by stamp: ", timeStamp)
                if index == 0:
                    logTimeGap.append("{:.6f}".format(0))
                else:
                    logTimeGap.append("{:.6f}".format((timeStamp - lastTimeStamp).total_seconds()))
                lastTimeStamp = timeStamp
                print(log)
        self.update_list()

    def update_list(self):
        # self.lb.delete(0, END)
        # self.lb.insert(END, '  time gap      ---     Log context')
        # for number, timeGap in enumerate(logTimeGap):
        #     self.lb.insert(END, '{0:<15} --- {1}'.format(timeGap, logStrList[number]))
        # for item in self.execlList.get_children():
        #     self.execlList.delete(item)
        self.tableWidget.setRowCount(len(logTimeGap))
        for index, timeGap in enumerate(logTimeGap):
            # insertItem = self.execlList.insert('', index, values=(timeGap, logStrList[index]))
            self.tableWidget.setItem(index, 0, QTableWidgetItem(logStrList[index]))  # 设置j行i列的内容为Value
            self.tableWidget.setItem(index, 1, QTableWidgetItem(timeGap))  # 设置j行i列的内容为Value

        # time.sleep(3)
        # self.tableWidget.removeRow(0)

    def ShowTable(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        j = 0#第几行（从0开始）
        i = 0#第几列（从0开始）
        Value = "Empty"#内容
        self.tableWidget.setItem(j, i, QTableWidgetItem(Value))#设置j行i列的内容为Value
        self.tableWidget.setColumnWidth(0,800)#设置j列的宽度
        # self.tableWidget.setRowHeight(i,50)#设置i行的高度
        self.tableWidget.setHorizontalHeaderLabels(['内容', '时差'])
        # self.tableWidget.verticalHeader().setVisible(False)#隐藏垂直表头
        # self.tableWidget.horizontalHeader().setVisible(False)#隐藏水平表


if __name__ == "__main__":
 #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
 #初始化
    myWin = MyMainForm()
 #将窗口控件显示在屏幕上
    myWin.show()
 #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())