import os
import pickle

from PySide6.QtWidgets import QFrame, QMessageBox


from Menu import Menu
from g import g
from ui.Login import Ui_Login
import mysql.connector as mysql
class Login(QFrame,Ui_Login):
    def __init__(self,parent=None):
        from mainWindow import MainWindow
        super().__init__(parent)
        self.setupUi(self)
        self.btnLogin.clicked.connect(self.btnLoginClick)
        if os.path.exists("login.pickle"):
            with open("login.pickle","rb") as f:
                data=pickle.load(f)
                self.txtAccoubt.setText(data["userAccount"])
                self.txtPassword.setText(data["userPassword"])
                self.chkRemember.setChecked(True)


    def btnLoginClick(self):
        from mainWindow import MainWindow
        if self.txtAccoubt.text()=="" or self.txtPassword.text()=="":
            dialog=QMessageBox()
            dialog.warning(self,
                           "登入錯誤",
                           "<p style='font-size:12;'>帳號或密碼不可空白</p>")
            return
        try:
            conn=mysql.connect(host=g.dbHost,
                       user=g.dbAccount,
                       password=g.dbPassword,
                       database=g.db)

            account=self.txtAccoubt.text()
            password=self.txtPassword.text()
            account=account.replace("'","\\'")
            password=password.replace("'","\\'")
            cmd=f"select * from 員工資料 where 帳號='{account}' and 密碼='{password}'"
            cursor=conn.cursor()
            cursor.execute(cmd)
            rs=cursor.fetchall()
            if len(rs) >0:
                dailog=QMessageBox()
                dailog.warning(self,
                               "登入",
                               "<p style='font-size:12;'>登入成功</p>")
                if self.chkRemember.isChecked():
                    with open("login.pickle","wb") as f:
                        data={"userAccount":account,"userPassword":password}
                        pickle.dump(data,f)
                else:
                    if os.path.exists("login.pickle"):
                        os.remove("login.pickle")


                # self.parent.mainLayout.addWidget(Menu(parent=self))

                frame=Menu()
                g.mainLayout.addWidget(frame)
                self.close()
                frame.setFocus()
            else:
                dialogin=QMessageBox()
                dialogin.warning(self,
                                "登入",
                                 "<p style='font-size:20;color:#ff0000;'>登入或密碼錯誤</p>")
                self.txtAccoubt.setText("")
                self.txtPassword.setText("")



        except Exception as e:
            print(e)
            dialogin=QMessageBox()
            dialogin.warning(self,
                             "錯誤",
                             "<p style='font-size:20;color:#ff0000;'>網路錯誤</p>")
