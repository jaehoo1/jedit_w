#!/usr/bin/python3
import sys
from typing import Pattern
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore
from PyQt5.QtPrintSupport import *
import webbrowser
import os
from urllib.parse import quote
import datetime
import io
import re
import collections
# QTextEdit https://wikidocs.net/38024

form_class = uic.loadUiType(os.path.dirname(os.path.realpath(__file__)) + "/notepad.ui")[0]

class findWindow(QDialog):
    def __init__(self, parent):
        super(findWindow, self).__init__(parent)
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "/find.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancel.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
            #print("up")
        elif self.radioButton_down.isChecked():
            self.up_down = "down"
            #print("down")

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
            cs = QtCore.Qt.CaseSensitive # 민감
        else:
            cs = QtCore.Qt.CaseInsensitive # 민감하지 않다
        
        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos) # 검색
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1): # 검색된 결과가 있다면
            self.setCursor(index, len(pattern)+index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        #print(self.cursor.selectionStart(), self.cursor.selectionEnd())
        self.cursor.setPosition(start) # 앞에 커서를 찍고
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start) # 뒤로 커서를 움직인다
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('jedit')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        ret = msgBox.exec_()


class infoWindow(QDialog):
    def __init__(self, parent):
        super(infoWindow, self).__init__(parent)
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "/info.ui", self)
        self.show()

        self.pushButton_confirm.clicked.connect(self.close)


class goWindow(QDialog):
    def __init__(self, parent):
        super(goWindow, self).__init__(parent)
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "/go.ui", self)
        self.show()
        self.lineEdit.setText(str(parent.ln))
        self.parent = parent

        self.pushButton_go.clicked.connect(self.goFunction)
        self.pushButton_cancel.clicked.connect(self.close)

    def goFunction(self, parent):
        self.max = 1
        self.string = self.parent.plainTextEdit.toPlainText()
        for i in self.string:
            if i == '\n':
                self.max += 1
        print(self.max)
        if len(self.lineEdit.text()) == 0:
            dest = 1000000000
        else:
            dest = int(self.lineEdit.text())
        print(dest)
        if dest <= self.max and dest != 0:
            dest -= 1
            line = 0
            i = 0
            while line < dest:
                if self.string[i] == '\n':
                    line +=1
                i += 1
            cursor = self.parent.plainTextEdit.textCursor()
            cursor.setPosition(i)
            self.parent.plainTextEdit.setTextCursor(cursor)
            self.close()
        else:
            QMessageBox().about(self, 'jedit - 줄 이동', '줄 번호가 전체 줄 수를 넘습니다.')
#        self.lineEdit.setInputMask("999999999")
#        self.lineEdit.textChanged.connect(self.textchanged)

#        def textchanged(self, text):
#            print("change")
#        number = self.ui.number_lineEdit.text()
#        try:
#            number = int(number)
#        except Exception:
#        QMessageBox().about(self, 'Error', '여기에는 숫자만 입력할 수 있습니다.')


class findReplaceWindow(QDialog):
    def __init__(self, parent):
        super(findReplaceWindow, self).__init__(parent)
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "/findReplace.ui", self)
        self.show()

        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancel.clicked.connect(self.close)

        self.pushButton_replace.clicked.connect(self.replaceFunction)
        self.pushButton_replace_all.clicked.connect(self.replaceAllFunction)

#        self.radioButton_down.clicked.connect(self.updown_radio_button)
#        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    # def updown_radio_button(self):
    #     if self.radioButton_up.isChecked():
    #         self.up_down = "up"
    #         #print("up")
    #     elif self.radioButton_down.isChecked():
    #         self.up_down = "down"
    #         #print("down")

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
            self.pushButton_replace.setEnabled(True)
            self.pushButton_replace_all.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)
            self.pushButton_replace.setEnabled(False)
            self.pushButton_replace_all.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
            cs = QtCore.Qt.CaseSensitive # 민감
        else:
            cs = QtCore.Qt.CaseInsensitive # 민감하지 않다
        
        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()

        if self.up_down == "down":
            index = reg.indexIn(text, pos) # 검색
        else:
            pos -= len(pattern) + 1
            index = reg.lastIndexIn(text, pos)
        print(index, pos)

        if (index != -1) and (pos > -1): # 검색된 결과가 있다면
            self.setCursor(index, len(pattern)+index)
        else:
            self.notFoundMsg(pattern)

    def setCursor(self, start, end):
        #print(self.cursor.selectionStart(), self.cursor.selectionEnd())
        self.cursor.setPosition(start) # 앞에 커서를 찍고
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start) # 뒤로 커서를 움직인다
        self.pe.setTextCursor(self.cursor)

    def notFoundMsg(self, pattern):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('jedit')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('''"{}"을(를) 찾을 수 없습니다.'''.format(pattern))
        msgBox.addButton('확인', QMessageBox.YesRole)
        ret = msgBox.exec_()

    def replaceFunction(self):
        self.cursor = self.parent.plainTextEdit.textCursor()
        search = self.lineEdit.text()
        cursored = self.pe.toPlainText()[self.cursor.selectionStart():self.cursor.selectionEnd()]
        if not self.checkBox_CaseSensitive.isChecked():
            search = search.lower()
            cursored = cursored.lower()
        if search != cursored:
            self.findNext()
        else:
            print(self.lineEdit_2.text())
            self.cursor.insertText(self.lineEdit_2.text())
            self.findNext()

    def replaceAllFunction(self):
        search = self.lineEdit.text()
        length = len(search)
        if not self.checkBox_CaseSensitive.isChecked():
            search = search.lower()
        while True:
            if not self.checkBox_CaseSensitive.isChecked():
                index = self.parent.plainTextEdit.toPlainText().lower().find(search)
            else:
                index = self.parent.plainTextEdit.toPlainText().find(search)
            print(index)
            if index==-1:
                break
            print(self.parent.plainTextEdit.toPlainText()[:index])
            print(self.lineEdit_2.text())
            print(self.parent.plainTextEdit.toPlainText()[index+length:])
            self.parent.plainTextEdit.setPlainText(self.parent.plainTextEdit.toPlainText()[:index] + self.lineEdit_2.text() + self.parent.plainTextEdit.toPlainText()[index+length:])
            

class wordCountWindow(QDialog):
    def __init__(self, parent):
        super(wordCountWindow, self).__init__(parent)
        uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + "/wordCount.ui", self)
        self.show()

        string = parent.plainTextEdit.toPlainText()
        list = re.split('\W+', string)
        tuple = collections.Counter(list)

        self.tableWidget.setRowCount(len(tuple))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['단어', '횟수'])
        iter = 0
        for i in tuple:
            self.tableWidget.setItem(iter, 0, QTableWidgetItem(i))
            self.tableWidget.setItem(iter, 1, QTableWidgetItem(str(tuple[i])))
            iter+=1


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveas.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close)

        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)
        self.action_delete.triggered.connect(self.deleteFunction)
        self.action_all_select.triggered.connect(self.selectAllFunction)
        self.action_datetime.triggered.connect(self.dateTimeFunction)

        self.action_find.triggered.connect(self.findFunction)
        self.action_find_replace.triggered.connect(self.findReplaceFunction)
        self.action_go.triggered.connect(self.goFunction)

        self.action_font.triggered.connect(self.fontFunction)

        self.action_zoom_in.triggered.connect(self.zoomInFunction)
        self.action_zoom_out.triggered.connect(self.zoomOutFunction)
        self.action_zoom_init.triggered.connect(self.zoomInitFunction)
        self.action_status_bar.triggered.connect(self.statusBarFunction)

        self.action_print.triggered.connect(self.printFunction)
        self.action_google.triggered.connect(self.googleFunction)
        self.action_help.triggered.connect(self.helpFunction)
        self.action_mail.triggered.connect(self.mailFunction)
        self.action_info.triggered.connect(self.infoFunction)
        self.action_new_window.triggered.connect(self.newWindowFunction)
        self.action_new_make.triggered.connect(self.newMakeFunction)

        self.action_word_count.triggered.connect(self.wordCountFunction)

        self.plainTextEdit.textChanged.connect(self.textChangedFunction)
        self.plainTextEdit.cursorPositionChanged.connect(self.cursorPositionChangedFunction)


        self.opened = False
        self.opened_file_path = '제목 없음'
        self.zoom = 0

        self.status_bar = True
        self.ln = 0
        self.col = 0
        self.statusbar.showMessage(self.statusMessage(), 0)
        
        self.mainWindow = []

        
    def ischanged(self):
        if not self.opened: # 열린적이 있고 변경 사항이 있으면
            if self.plainTextEdit.toPlainText().strip():    # 열린적은 없는데 에디터 내용이 있으면
                return True
            return False
        current_data = self.plainTextEdit.toPlainText() # 현재 데이터
        # 파일에 저장된 데이터
        with io.open(self.opened_file_path, "r") as f:
            file_data = f.read()
        if current_data == file_data:   # 열린적이 있고 변경사항이 없으면
            return False
        else:   # 열린적이 있고 변경사항이 있으면
            return True

    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}에 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole) #0
        msgBox.addButton('저장 안 함', QMessageBox.NoRole) #1
        msgBox.addButton('취소', QMessageBox.RejectRole) #2
        ret = msgBox.exec_()
        if ret == 0:
            self.saveFunction()
        else:
            return ret

    def closeEvent(self, event):
        if self.ischanged():  # 열린적이 있고 변경 사항이 있으면 # 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()
            if ret == 2:
                event.ignore()

    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()
        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)
        self.opened = True
        self.opened_file_path = fname
        print("save {}!!".format(fname))

    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()
        self.plainTextEdit.setPlainText(data)
        self.opened = True
        self.opened_file_path = fname
        print("open {}!!".format(fname))


    def openFunction(self):
        if self.ischanged():  # 열린적이 있고 변경 사항이 있으면 # 열린적은 없는데 에디터 내용이 있으면
            ret = self.save_changed_data()
        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plainTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def deleteFunction(self):
        string = self.plainTextEdit.toPlainText()
        cursor = self.plainTextEdit.textCursor()
        string = string[:cursor.selectionStart()] + string[cursor.selectionEnd():]
        after_positon = cursor.selectionStart()
        self.plainTextEdit.setPlainText(string)
        cursor.setPosition(after_positon)
        self.plainTextEdit.setTextCursor(cursor)

    def selectAllFunction(self):
        self.plainTextEdit.selectAll()

    def dateTimeFunction(self):
        now = str(datetime.datetime.now())
        hour = int(now[11:13])
        string = ''
        if hour < 12:
            string += '오전 '
        else:
            string += '오후 '
        if hour > 12:
            hour -= 12
        string += str(hour) + ':' + now[14:16] + ' '
        string += now[:10]
        self.plainTextEdit.insertPlainText(string)

    def zoomInFunction(self):
        if self.zoom < 40:
            self.plainTextEdit.zoomIn()
            self.zoom += 1
            self.statusbar.showMessage(self.statusMessage(), 0)

    def zoomOutFunction(self):
        if self.zoom > -9:
            self.plainTextEdit.zoomOut()
            self.zoom -= 1
            self.statusbar.showMessage(self.statusMessage(), 0)

    def zoomInitFunction(self):
        if self.zoom > 0:
            self.plainTextEdit.zoomOut(self.zoom)
        elif self.zoom < 0:
            self.plainTextEdit.zoomIn(abs(self.zoom))
        self.zoom = 0
        self.statusbar.showMessage(self.statusMessage(), 0)

    def statusBarFunction(self):
        if self.status_bar:
            self.status_bar = False
            self.statusBar().hide()
        else:
            self.status_bar = True
            self.statusBar().show()
        
    def findFunction(self):
        findWindow(self)

    def goFunction(self):
        goWindow(self)

    def findReplaceFunction(self):
        findReplaceWindow(self)

    def printFunction(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.plainTextEdit.print_(dlg.printer())

    def googleFunction(self):
        cursor = self.plainTextEdit.textCursor()
        url = self.plainTextEdit.toPlainText()[cursor.selectionStart():cursor.selectionEnd()]
        url = "google.com/search?q=" + url
        webbrowser.open(url)

    def helpFunction(self):
        webbrowser.open("https://jaehoo1.github.io/jedit/help.html")

    def mailFunction(self):
        webbrowser.open("https://jaehoo1.github.io/jedit/contact.html")

    def infoFunction(self):
        infoWindow(self)

    def newWindowFunction(self):
        window = WindowClass()
        self.mainWindow.append(window)
        window.show()

    def newMakeFunction(self):
        print("new")
        if self.ischanged():
            print("changed")
            ret = self.save_changed_data()
            if ret == 2:
                return
        self.plainTextEdit.clear()
        self.opened = False
        self.opened_file_path = '제목 없음'

    def statusMessage(self):
        result = ''
        string = self.plainTextEdit.toPlainText()
        pos = self.plainTextEdit.textCursor().position()
        self.ln = 1
        self.col = 1

        i=0
        while i < pos:
            if string[i] == '\n':
                self.ln += 1
                self.col = 0
            i += 1
            self.col += 1
        
        result += "Ln " + str(self.ln) + ", " + "Col " + str(self.col) + "          " + str((self.zoom+10)*10) + "%" + "          Windows (CRLF)"
        return result

    def textChangedFunction(self):
        self.statusbar.showMessage(self.statusMessage(), 0)

    def cursorPositionChangedFunction(self):
        self.statusbar.showMessage(self.statusMessage(), 0)
    
    def mouseMoveEvent(self, event):
        self.statusbar.showMessage(self.statusMessage(), 0)

    def fontFunction(self):
        font, fc = QFontDialog.getFont()
        if fc:
#            self.colorLabel.setFont(font)
#            app.setFont(font)
            self.plainTextEdit.setFont(font)

    def wordCountFunction(self):
        wordCountWindow(self)


app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()