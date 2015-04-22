#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import threading
import csv
from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import datetime
from itertools import islice
from random import randint

class ClickRecorder(QtWidgets.QWidget):
    
    def __init__(self):
        super(ClickRecorder, self).__init__()
        self.counter = -1
        self.draw = False
        self.start = datetime.now()
        self.initUI()
        self.readDescription()
        self.calculateOrder()
        self.organizeTest()
        self.createCSV()
        
    def initUI(self):      
        self.setGeometry(150, 100, 750, 500)
        self.setWindowTitle('ReactionTime')
        self.show()

    def readDescription(self):
        userInput = sys.argv
        self.description = []
        with open(userInput[1]) as myFile:
            content = list(islice(myFile, 4))
        for i in content:
            varWithoutLineBreak = i.split("\n")[0]
            value = i.split(":")[1][1:]
            self.description.append(value)

    def calculateOrder(self):
        self.orderMatrix = [[1,2,3,4],[4,3,2,1],[2,4,1,3],[3,1,4,2]]
        self.order = self.orderMatrix[int(self.description[0])-1]
        self.currentTest = self.order[0]
        print (self.order)

    def organizeTest(self):
        if self.currentTest == 1:
            self.text = "Please press 'x' whenever the red" \
                        " rectangle \n is present on the screen!\n" \
                        "Use your RIGHT finger to perform the test!\n" \
                        "(Start by pressing 'Space')"
            self.usedHand = "R"
        elif self.currentTest == 2:
            self.text = "Please press 'x' whenever the red" \
                        " rectangle \n is present on the screen!\n" \
                        "Use your LEFT finger to perform the test!\n" \
                        "(Start by pressing 'Space')"
            self.usedHand = "L"
        elif self.currentTest == 3:
            self.text = "Please press 'x' or 'm' depending on which\n" \
                        " of both letters is presented on the screen\n" \
                        "Use your RIGHT fingers to perform the test!\n"\
                        "(Start by pressing 'Space')"
            self.usedHand = "R"
        elif self.currentTest == 4:
            self.text = "Please press 'x' or 'm' depending on which\n" \
                        " of both letters is presented on the screen\n" \
                        "Use your LEFT fingers to perform the test!\n"\
                        "(Start by pressing 'Space')"
            self.usedHand = "L"


    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.counter = 0
            self.startTimer()
        if ev.key() == QtCore.Qt.Key_X:
            diff = datetime.now() - self.start
            print (diff.microseconds / 1000)
            self.draw = False
            self.wr.writerow([str(datetime.now()), self.description[0], self.description[1], self.usedHand, str(self.order).strip('[]'), str(self.currentTest), self.counter, str(self.counter * self.currentTest), self.shownCharacter, "X", str(diff.microseconds / 1000)])
            self.update()
        if ev.key() == QtCore.Qt.Key_M:
            diff = datetime.now() - self.start
            print (diff.microseconds / 1000)
            self.draw = False
            self.wr.writerow([str(datetime.now()), self.description[0], self.description[1], self.usedHand, str(self.order).strip('[]'), str(self.currentTest), self.counter, str(self.counter * self.currentTest), self.shownCharacter, "M", str(diff.microseconds / 1000)])
            self.update()

    def startTimer(self):
        timeBetweenSignals = float(self.description[3]) / 1000
        t = threading.Timer(timeBetweenSignals, self.startTimer)
        t.start()
        if self.counter < int(self.description[2]) + 2 and self.counter > -1:
            self.start = datetime.now()
            self.update()
            if self.counter > 0:
                self.draw=True
            self.counter = self.counter + 1
        else:
            t.cancel()
            t.join()

    def createCSV(self):
        file = open("log_" + self.description[0] + ".csv", "w+")
        self.wr = csv.writer(file, delimiter=";", quoting = csv.QUOTE_ALL)
        self.wr.writerow(["timestamp", "user", "handedness", "used hand", "task-order", "condition" "repetition", "trial", "shown character", "pressed character", "reaction time(ms)"])

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()


    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 22))
        if self.counter > -1:
            if self.counter < int(self.description[2]) + 1 and self.currentTest < 3:
                self.text = ""
                self.drawRect(qp)
            elif self.counter < int(self.description[2]) + 1 and self.currentTest > 2:
                self.showRandomXOrM(qp)
            if self.counter == int(self.description[2]) + 1:
                if self.currentTest < 4:
                    self.draw = False
                    self.drawRect(qp)
                    self.currentTest = self.currentTest + 1
                    self.counter = -1
                    self.organizeTest()
                else:
                    self.text = "Thank you!"
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def showRandomXOrM(self,qp):
        if self.draw == True:
            random = randint(1,100)
            if random % 2 == 0:
                self.shownCharacter = "X"
                self.text = "X"
            else:
                self.shownCharacter = "M"
                self.text = "M"
        else:
            print ("FALSE")
            self.text = ""

    def drawRect(self,qp):
        if self.draw == True:
            self.shownCharacter = "Signal"
            rect = QtCore.QRect(350, 200, 80, 80)
            qp.setBrush(QtGui.QColor(168, 34, 3))
            qp.drawRoundedRect(rect, 10.0, 10.0)
        else:
            qp.CompositionMode_Clear


def main():
    app = QtWidgets.QApplication(sys.argv)
    click = ClickRecorder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
