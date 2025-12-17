from PySide6.QtCore import QEvent, QDate
from PySide6.QtWidgets import QFrame

from g import g
from ui.Divination import Ui_Divination
import mysql.connector as mysql

class Divination(QFrame,Ui_Divination):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd = f"select 暱稱,會員編號 from 微亮會員"
        cursor.execute(cmd)
        rs = cursor.fetchall()
        conn.commit()
        # conn.close()

        r_1=[i[0] for i in rs]
        self.cmNickname.addItems(r_1)
        d_number={}
        for i,v in rs:
            d_number[i]=v
        nick=self.cmNickname.currentText()

        self.txtNumber.setText(f"{d_number[nick]}")
        self.cmNickname.currentIndexChanged.connect(self.updateMembernumber)
        self.cmType.addItems(g.Type)
        self.dtDate.setDate(QDate.currentDate())
        self.cmFirst.addItems(g.IChing)
        self.cmSecond.addItems(g.IChing)
        self.cmThird.addItems(g.IChing)
        self.cmLast.addItems(g.IChing)
        self.cmNumber.addItems(g.Promber)
        self.cmSale.addItems(g.Money)

        x=int(self.cmNumber.currentText())
        y=int(self.cmSale.currentText())
        self.txtTotal.setText(f"{x*y}")
        self.cmSale.currentIndexChanged.connect(self.updateMoney)
        self.cmNumber.currentIndexChanged.connect(self.updateNumber)


        cmd_1 = f"select 會員編號 from 會員占卜資料 where 暱稱='{nick}' and 占卜日期='{self.dtDate.text()}'"
        cursor.execute(cmd_1)
        datachange = self.dtDate.text().replace("/", "-").replace("'","\\'")
        dataNumber =f"{datachange}-{len(cursor.fetchall()) + 1}"
        conn.commit()
        conn.close()
        self.txtData.setText(str(dataNumber))

        self.dtDate.dateChanged.connect(self.dtDateChange)

        self.btnMenu.clicked.connect(self.btMenuClick)
        self.btnReset.clicked.connect(self.btnResetClick)
        self.btnSave.clicked.connect(self.btnSaveClick)

    #     self.cmNickname.installEventFilter(self)
    #
    # def eventFilter(self, watched, event):
    #     if event.type()==QEvent.Type.FocusOut and watched is self.cmNickname and self.cmNickname.currentText() !="" \
    #         or event.type()==QEvent.Type.KeyPress and watched is self.cmNickname and event.text()=="\r":
    #         nickname=self.cmNickname.currentText()
    #         if nickname !="":
    #             conn=mysql.connect(host=g.dbHost,user=g.dbAccount,password=g.dbPassword,database=g.db)
    #             cursor=conn.cursor()
    #             cmd=f"select * from 會員占卜資料 where 暱稱='{nickname}'"
    #             cursor.execute(cmd)
    #             rs=cursor.fetchone()
    #             if len(rs)>0:
    #                 self.cmNickname.setEnabled(False)  #設定成不可修改
    #                 self.cmType.setCurrentText()
    #
    #
    #
    #         self.cmNickname.setFocus()
    #     return super(Divination,self).eventFilter(watched,event)

    def dtDateChange(self):
        nickname=self.cmNickname.currentText()
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()

        cmd_1 = f"select 會員編號 from 會員占卜資料 where 暱稱='{nickname}' and 占卜日期='{self.dtDate.text()}'"
        cursor.execute(cmd_1)

        dataNumber=cursor.fetchall()
        conn.commit()
        datachange=self.dtDate.text().replace("/","-").replace("'","\\'")
        print(datachange)
        dataNumber =f"{datachange}-{len(dataNumber) + 1}"
        conn.commit()
        conn.close()
        self.txtData.setText(dataNumber)


    def btnSaveClick(self):
        conn = mysql.connect(host=g.dbHost,
                             user=g.dbAccount,
                             password=g.dbPassword,
                             database=g.db)
        cursor = conn.cursor()

        cmd=f"""
            insert into 會員占卜資料 (會員編號,暱稱,問題類型,資料編號,占卜日期,占卜問題,現況卦,建議卦,結果卦,底卦,題數,單價,總價,注意事項) values(
            '{self.txtNumber.text()}',
            '{self.cmNickname.currentText()}',
            '{self.cmType.currentText()}',
            '{self.txtData.text()}',
            
            '{self.dtDate.text()}',
            '{self.txtPromble.text()}',
            '{self.cmFirst.currentText()}',
            '{self.cmSecond.currentText()}',
            '{self.cmThird.currentText()}',
            '{self.cmLast.currentText()}',
            '{self.cmNumber.currentText()}',
            '{self.cmSale.currentText()}',
            '{self.txtTotal.text()}',
            '{self.txtDetail.toPlainText()}'
            )
        """
        cursor.execute(cmd)
        conn.commit()
        conn.close()
        self.reset()


    def updateMoney(self):
        x = int(self.cmNumber.currentText())
        y = int(self.cmSale.currentText())
        self.txtTotal.setText(f"{x*y}")
    def updateNumber(self):
        x = int(self.cmNumber.currentText())
        y = int(self.cmSale.currentText())
        self.txtTotal.setText(f"{x*y}")




    def updateMembernumber(self):
        nickname=self.cmNickname.currentText()
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd = f"select 會員編號 from 微亮會員 where 暱稱='{nickname}'"
        cursor.execute(cmd)
        rs = cursor.fetchall()
        r=rs[0]

        self.txtNumber.setText(f"{r[0]}")

        # cmd_1 = f"select 會員編號 from 會員占卜資料 where 暱稱='{nickname}' and 占卜日期={self.dtDate.text()}"
        # cursor.execute(cmd_1)
        #
        # dataNumber=cursor.fetchall()
        # conn.commit()
        # dataNumber =f"{self.dtDate.text()}-{len(dataNumber) + 1}"
        # conn.commit()
        # conn.close()
        # self.txtData.setText(str(dataNumber))





    def btMenuClick(self):
        from Menu import Menu
        frame=Menu()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnResetClick(self):
        self.reset()
    def reset(self):
        self.txtPromble.setText("")
        self.txtDetail.setText("")
        self.cmNickname.setCurrentText("大可")
        self.cmType.setCurrentText("其他")
        self.dtDate.setDate(QDate.currentDate())
        self.cmFirst.setCurrentText("無")
        self.cmSecond.setCurrentText("無")
        self.cmThird.setCurrentText("無")
        self.cmLast.setCurrentText("無")
        self.cmNumber.setCurrentText("0")
        self.cmSale.setCurrentText("750")

        self.cmNickname.setFocus()



