
import sqlite3
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMainWindow
from PyQt5.uic import loadUi
import sys 
import re

import time
import datetime
from PyQt5.QtCore import QTime, QTimer, QDate, Qt


import csv







class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI,self).__init__()
        #loadUi("./UI/login.ui",self)
        loadUi("UI//login.ui",self)
        self.signUpButton.clicked.connect(self.sign_up_button)
        self.emailInputLogin.returnPressed.connect(self.loginButton.click)
        self.loginButton.clicked.connect(self.login_button)
        self.errorTextLogin.setText("")
        self.errorTextSignUp.setText("")
        self.db = None

        # This is example of changing screen
        #self.loginButton.clicked.connect(self.go_main_menu)

    def go_main_menu(self):
        main_menu = MainMenuUI()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_button(self):
        self.name = self.nameInputSignUp.text()
        self.user_email = self.emailInputSignUp.text()
        
        def is_valid_email(email):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                return True
            else:
                return False        
        if self.name == "" or self.user_email == "":
            self.errorTextSignUp.setText("'name' or 'email' fields cannot be left blank!")
        elif not is_valid_email(self.user_email):
            self.errorTextSignUp.setText("Sorry, your mail address is not valid.")
        else:
            with sqlite3.connect("pomodoro.db") as db:
                im = db.cursor()
                im.execute("SELECT * FROM users")
                e_mail = [i[2] for i in im.fetchall()]
                if self.user_email in e_mail:
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' already exists.")
                else:
                    im.execute("INSERT INTO users(name, user_email) VALUES(?, ?)", (self.name, self.user_email))
                    db.commit()
                    self.errorTextSignUp.setText(f"The user '{self.user_email}' has been successfully registered.")
                    self.nameInputSignUp.clear()
                    self.emailInputSignUp.clear()     


    def login_button(self):
    
        with sqlite3.connect("pomodoro.db") as db:            
            im = db.cursor()    
            im.execute("SELECT * FROM users")
            self.login = self.emailInputLogin.text()
            
            for i in im.fetchall():
                im.execute("SELECT * FROM users")
                if self.login == "" or "@" not in self.login:
                    self.errorTextLogin.setText("For login please enter a valid email address!")                   
                
                elif self.login in i:
                    self.go_main_menu()
                    break                               

                else:
                    self.errorTextLogin.setText("Sorry, your email address is not registered!")
                 

class MainMenuUI(QDialog):
    def __init__(self):
        super(MainMenuUI,self).__init__()
        loadUi("./UI/mainMenu.ui",self)

class PomodoroUI(QDialog):
    def __init__(self):
        super(PomodoroUI,self).__init__()
        loadUi("./UI/pomodoro.ui",self)


class ShortBreakUI(QDialog):
    def __init__(self):
        super(ShortBreakUI,self).__init__()
        loadUi("./UI/shortBreak.ui",self)

class LongBreakUI(QDialog):
    def __init__(self):
        super(LongBreakUI,self).__init__()
        loadUi("./UI/longBreak.ui",self)


app = QApplication(sys.argv)
UI = LoginUI() # This line determines which screen you will load at first

# You can also try one of other screens to see them.
    #UI = MainMenuUI()
    # UI = PomodoroUI()
    # UI = ShortBreakUI()
    # UI = LongBreakUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.setWindowTitle("Time Tracking App")
widget.show()
sys.exit(app.exec_())
