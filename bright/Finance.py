from PySide6.QtCore import QStringListModel, QDate
from PySide6.QtWidgets import QFrame, QListView, QVBoxLayout

from g import g
from ui.Finance import Ui_Finance
import mysql.connector as mysql

class Finnance(QFrame,Ui_Finance):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.dtStart.setDisplayFormat("yyyy/MM/dd")
        self.dtEnd.setDisplayFormat("yyyy/MM/dd")
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd = f"select 暱稱,會員編號 from 微亮會員"
        cursor.execute(cmd)
        rs = cursor.fetchall()
        conn.commit()
        conn.close()
        r_1 = [i[0] for i in rs]
        r_1.append("總和")
        self.cmNickname.addItems(r_1)


        self.textYear.setText("")
        self.dtStart.setDate(QDate.currentDate())
        self.dtEnd.setDate(QDate.currentDate())

        self.btnQuery.clicked.connect(self.btnQueryClick)
        self.btnMenu.clicked.connect(self.btnMenuClick)
    def btnMenuClick(self):
        from Menu import Menu
        frame=Menu()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnQueryClick(self):
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        start=self.dtStart.text().replace("/","-")
        end=self.dtEnd.text().replace("/","-")

        cmd = f"select sum(總價) from 會員占卜資料 where 暱稱='{self.cmNickname.currentText()}' and 占卜日期 between '{start}' and '{end}'"
        cursor.execute(cmd)
        rs = cursor.fetchall()
        r=rs[0]

        data=f'''
        顧客名稱：{self.cmNickname.currentText()} 
        
        查詢時段：{start} 至 {end}
        
        消費金額 : {r[0]}
        '''

        # data=""
        # for r in rs:
        #     data+=f"""
        #         {}
        #
        #         """
        self.textYear.setText(data)



