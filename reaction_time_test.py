#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import threading
import csv
import time
from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import datetime
from itertools import islice
from random import randint


class ClickRecorder(QtWidgets.QWidget):

    def __init__(self):
        super(ClickRecorder, self).__init__()
        self.counter = -1
        self.trial = 0
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
        self.orderMatrix = [[1, 2, 3, 4], [4, 3, 2, 1],
                            [2, 4, 1, 3], [3, 1, 4, 2]]
        self.order = self.orderMatrix[(int(self.description[0]) % 4) - 1]
        self.pos = 0
        self.currentTest = self.order[self.pos]

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
            self.diff = 0
            self.shownCharacter = ""
            self.pressedCharacter = ""
            self.draw = True
            self.startTimer()
        else:
            diff = datetime.now() - self.start
            self.diff = diff.microseconds / 1000
        self.pressedCharacter = str(ev.text())

    def startTimer(self):
        self.draw = not self.draw
        timeBetweenSignals = float(self.description[3]) / 1000
        t = threading.Timer(timeBetweenSignals, self.startTimer)
        t.start()
        if self.counter < int(self.description[2])\
           + 2 and self.counter > -1:
            if(self.draw is True):
                self.start = datetime.now()
                self.update()
                self.trial += 1
                self.counter += 1
                self.pressedCharacter = ""
                self.diff = 1000
            else:
                if self.counter != 0:
                    self.wr.writerow([str(datetime.now()), self.description[0],
                                      self.description[1], self.usedHand,
                                      str(self.order).strip('[]'),
                                      str(self.currentTest),
                                      str(self.counter), str(self.trial),
                                      self.shownCharacter,
                                      self.pressedCharacter, str(self.diff)])
                self.update()
        else:
            t.cancel()
            t.join()

    def createCSV(self):
        file = open("log_" + self.description[0] + ".csv", "w+")
        self.wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_ALL)
        self.wr.writerow(["timestamp", "user", "handedness",
                          "used hand", "task-order", "condition",
                          "repetition", "trial", "shown character",
                          "pressed character", "reaction time(ms)"])

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 22))
        if self.counter > -1:
            if self.counter < int(self.description[2])\
               + 1 and self.currentTest < 3:
                self.text = ""
                self.drawRect(qp)
            if self.counter < int(self.description[2])\
               + 1 and self.currentTest > 2:
                self.showRandomXOrM(qp)
            if self.counter == int(self.description[2]) + 1:
                if self.pos < 3:
                    self.draw = False
                    self.drawRect(qp)
                    self.pos += 1
                    self.currentTest = self.order[self.pos]
                    self.counter = -1
                    self.organizeTest()
                else:
                    self.text = "Thank you!"
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def showRandomXOrM(self, qp):
        if self.draw is True:
            random = randint(1, 100)
            if random % 2 == 0:
                self.shownCharacter = "x"
                self.text = "X"
            else:
                self.shownCharacter = "m"
                self.text = "M"
        else:
            self.text = ""

    def drawRect(self, qp):
        if self.draw is True:
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
