from PySide6.QtCore import QDate, QEvent
from PySide6.QtWidgets import QFrame, QMessageBox
import  mysql.connector as mysql
from g import g
from ui.Member import Ui_Member


class Member(QFrame,Ui_Member):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnMenu.clicked.connect(self.btMenuClick)
        self.btnReset.clicked.connect(self.btnResetClick)
        self.btnSave.clicked.connect(self.btnSaveClick)
        self.cmProfession.addItems(g.Profession)
        self.cmSex.addItems((g.Sex))
        self.dtBirthday.setDisplayFormat("yyyy/MM/dd")
        self.dtOnboard.setDate(QDate().currentDate())
        self.txts = {self.txtName: "姓名",
                     self.txtNumber:"會員編號",
                     self.txtNickname: "暱稱",
                     self.txtLine: "line帳號",
                     self.txtPhone: "電話",
                     self.txtRemark: "備註"}
        self.txtNumber.installEventFilter(self)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.FocusOut and watched is self.txtNumber and self.txtNumber.text() != "" \
                or event.type() == QEvent.Type.KeyPress and watched is self.txtNumber and event.text() == "\r":
            number = self.txtNumber.text().strip()  # 去除 enter
            if number != "":
                conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
                cursor = conn.cursor()
                cmd = f"select * from 微亮會員 where 會員編號='{number}'"
                cursor.execute(cmd)
                rs = cursor.fetchall()

                if len(rs)>0:
                    self.txtNumber.setEnabled(False)
                    r=rs[0]
                    self.txtName.setText(r[2])
                    self.txtNickname.setText(r[3])
                    self.txtLine.setText(r[4])
                    self.txtPhone.setText(r[5])
                    self.cmProfession.setCurrentText(r[6])
                    self.cmSex.setCurrentText(r[7])
                    self.dtBirthday.setDate(r[8])
                    self.dtOnboard.setDate(r[9])
                    self.txtRemark.setText(r[10])
                self.txtName.setFocus()
                return super(Member, self).eventFilter(watched, event)

    def btnSaveClick(self):
        for txt in self.txts:
            if txt.text()=="":
                dialog=QMessageBox()
                dialog.warning(self,
                               "會員系統",
                               f"{self.txts[txt]} 不可空白")
                return
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        if self.txtNumber.isEnabled():
            cmd=f"select * from 微亮會員 where 會員編號={self.txtNumber.text()}"
            cursor.execute(cmd)
            rs=cursor.fetchall()
            if len(rs)>0:
                dialog=QMessageBox()
                dialog.critical(self,"會員系統",f"帳號已被申請，請更改其他帳號")
                return
            else:
                cmd=f"""
                insert into 微亮會員 (會員編號,姓名,暱稱,Line帳號,電話,職業狀態,性別,生日,申請日期,備註) values(
                '{self.txtNumber.text()}',
                '{self.txtName.text()}',
                '{self.txtNickname.text()}',
                '{self.txtLine.text()}',
                '{self.txtPhone.text()}',
                '{self.cmProfession.currentText()}',
                '{self.cmSex.currentText()}',
                '{self.dtBirthday.text()}',
                '{self.dtOnboard.text()}',
                '{self.txtRemark.text()}')
            """
        else:
            cmd=f"""
            update 微亮會員 set 
            姓名='{self.txtName.text()}',
            暱稱='{self.txtNickname.text()}',
            Line帳號='{self.txtLine.text()}',
            電話='{self.txtPhone.text()}',
            職業狀態='{self.cmProfession.currentText()}',
            性別='{self.cmSex.currentText()}',
            生日='{self.dtBirthday.text()}',
            申請日期='{self.dtOnboard.text()}',
            備註='{self.txtRemark.text()}' 
            where 會員編號={self.txtNumber.text()}
            """


        cursor.execute(cmd)
        conn.commit()
        conn.close()
        self.reset()


    def btMenuClick(self):
        from Menu import Menu
        frame = Menu()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnResetClick(self):
        self.reset()

    def reset(self):
        import datetime
        for txt in self.txts:
            txt.setText("")
            txt.setEnabled(True)
        self.dtBirthday.setDate(datetime.date(2001, 1, 1))
        self.dtOnboard.setDate(QDate.currentDate())
        self.cmProfession.setCurrentText("無")
        self.cmSex.setCurrentText("男")
        self.txtName.setFocus()