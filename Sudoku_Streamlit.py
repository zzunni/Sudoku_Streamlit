import streamlit as at

import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QTimer
import time

form_class = loadUiType("Sudoku.ui")[0]

class SudokuUI(QMainWindow, form_class):

    def __init__(self, parent=None):
        super(SudokuUI, self).__init__(parent)
        self.setupUi(self)

        global AVal, ButtonList

        # 버튼 리스트 초기화
        ButtonList = [[self.A00, self.A01, self.A02, self.A03, self.A04, self.A05, self.A06, self.A07, self.A08],
                      [self.A10, self.A11, self.A12, self.A13, self.A14, self.A15, self.A16, self.A17, self.A18],
                      [self.A20, self.A21, self.A22, self.A23, self.A24, self.A25, self.A26, self.A27, self.A28],
                      [self.A30, self.A31, self.A32, self.A33, self.A34, self.A35, self.A36, self.A37, self.A38],
                      [self.A40, self.A41, self.A42, self.A43, self.A44, self.A45, self.A46, self.A47, self.A48],
                      [self.A50, self.A51, self.A52, self.A53, self.A54, self.A55, self.A56, self.A57, self.A58],
                      [self.A60, self.A61, self.A62, self.A63, self.A64, self.A65, self.A66, self.A67, self.A68],
                      [self.A70, self.A71, self.A72, self.A73, self.A74, self.A75, self.A76, self.A77, self.A78],
                      [self.A80, self.A81, self.A82, self.A83, self.A84, self.A85, self.A86, self.A87, self.A88]]

        for i in range(9):
            for number in ButtonList[i]:
                number.clicked.connect(self.NumClick)

        AVal = []

        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(str(ButtonList[i][j].text()))
            AVal.append(temp)

        self.ShuffleClick()
        self.ShuffleButton.clicked.connect(self.ShuffleClick)
        self.pStart.clicked.connect(self.StartClick)
        self.FinishButton.clicked.connect(self.CompleteTestClick)

        # 타이머와 시간 변수 초기화
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateElapsedTime)
        self.startTime = 0
        self.elapsedTime = 0

        # 닉네임과 시간 저장을 위한 리스트
        self.pastRecords = []

    def ShuffleClick(self):
        random19 = list(range(1, 10))
        random.shuffle(random19)

        for i in range(9):
            for j in range(9):
                ButtonList[i][j].setText(str(random19[int(AVal[i][j]) - 1]))

        for i in range(9):
            for j in range(9):
                if random.random() > float(self.pEdit.text()):
                    ButtonList[i][j].setText("")

    def StartClick(self):
        # 타이머 시작
        self.startTime = time.time()
        self.elapsedTime = 0
        self.timer.start(1000)  # 1초마다 업데이트

    def updateElapsedTime(self):
        # 경과 시간 업데이트
        self.elapsedTime = int(time.time() - self.startTime)
        self.resEdit.setText(f"경과 시간: {self.elapsedTime} 초")

    def NumClick(self):
        global XLoc, YLoc
        for i in range(9):
            for j in range(9):
                if self.sender() == ButtonList[i][j]:
                    XLoc = i
                    YLoc = j

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            if event.key() == Qt.Key_1:
                ButtonList[XLoc][YLoc].setText("1")
            elif event.key() == Qt.Key_2:
                ButtonList[XLoc][YLoc].setText("2")
            elif event.key() == Qt.Key_3:
                ButtonList[XLoc][YLoc].setText("3")
            elif event.key() == Qt.Key_4:
                ButtonList[XLoc][YLoc].setText("4")
            elif event.key() == Qt.Key_5:
                ButtonList[XLoc][YLoc].setText("5")
            elif event.key() == Qt.Key_6:
                ButtonList[XLoc][YLoc].setText("6")
            elif event.key() == Qt.Key_7:
                ButtonList[XLoc][YLoc].setText("7")
            elif event.key() == Qt.Key_8:
                ButtonList[XLoc][YLoc].setText("8")
            elif event.key() == Qt.Key_9:
                ButtonList[XLoc][YLoc].setText("9")
            else:
                print("Error")
        ButtonList[XLoc][YLoc].setStyleSheet('QPushButton {color: red;}')

    def CompleteTestClick(self):
        # 타이머 중지 및 경과 시간 출력
        self.timer.stop()
        totalElapsedTime = self.elapsedTime

        # 닉네임 입력 받기
        nickname = self.nicknameEdit.text()
        if not nickname:
            self.resEdit.setText("등수를 확인하려면 닉네임을 입력한 후 다시 Finish를 눌러주세요  -->> ")
            return

        # 닉네임과 시간을 리스트에 추가
        self.pastRecords.append((nickname, totalElapsedTime))
        # 시간을 기준으로 정렬
        self.pastRecords.sort(key=lambda x: x[1])

        # 현재 참가자의 등수 찾기
        rank = self.pastRecords.index((nickname, totalElapsedTime)) + 1

        err = 0
        self.resEdit.setText("")
        for i in range(9):
            for j in range(9):
                AVal[i][j] = ButtonList[i][j].text()

        # 행 검사
        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(AVal[i][j])
            if len(set(temp)) != 9:
                self.resEdit.setText(f"{i + 1}번째 행 오류")
                err = 1
                break

        # 열 검사
        for j in range(9):
            temp = []
            for i in range(9):
                temp.append(AVal[i][j])
            if len(set(temp)) != 9:
                self.resEdit.setText(f"{j + 1}번째 열 오류")
                err = 1
                break

        # 9칸 영역 검사
        index = [0, 3, 6]
        for i in index:
            for j in index:
                temp = []
                for k in range(3):
                    temp.append(AVal[i][j + k])
                    temp.append(AVal[i + 1][j + k])
                    temp.append(AVal[i + 2][j + k])
                if len(set(temp)) != 9:
                    self.resEdit.setText(f"{i}, {j}의 3*3 매트릭스 오류")
                    err = 1
                    break

        if err == 0:
            self.resEdit.setText(f"!!! ~~~축하합니다~~~ !!!\n닉네임: {nickname}\n총 경과 시간: {totalElapsedTime} 초\n현재 참가자 중 {rank}등입니다.")

            # 팝업창에 전체 참가자 랭킹 보여주기
            self.showRankingPopup()

    def showRankingPopup(self):
        # 참가자들의 랭킹을 출력하는 팝업창
        ranking_text = "참가자 랭킹:\n\n"
        for i, (name, time) in enumerate(self.pastRecords):
            ranking_text += f"{i + 1}등: {name} - {time} 초\n"

        # QMessageBox 사용하여 팝업창 띄우기
        QMessageBox.information(self, "참가자 랭킹", ranking_text)

app = QApplication(sys.argv)
myWindow = SudokuUI(None)
myWindow.show()
app.exec_()
