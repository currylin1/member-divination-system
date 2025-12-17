import platform

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QFrame
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer

from g import g
from ui.Query import Ui_Query
import mysql.connector as mysql

class Quert(QFrame,Ui_Query):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd = f"select 暱稱,會員編號 from 微亮會員"
        cursor.execute(cmd)
        rs = cursor.fetchall()
        conn.commit()

        r_1=[i[0] for i in rs]
        # r_2= [i[1] for i in rs]
        self.cmNickname.addItems(r_1)
        d_number={}
        for i,v in rs:
            d_number[i]=v
        x=self.cmNickname.currentText()
        self.txtNumber.setText(f"{d_number[x]}")
        cmd = f"select 占卜日期 from 會員占卜資料 where 暱稱='{x}'"
        cursor.execute(cmd)
        rs2 = cursor.fetchall()
        conn.commit()
        date2 = set([str(i[0]) for i in rs2])
        self.cmDate.addItems(date2)

        cmd_1 = f"select 資料編號 from 會員占卜資料 where 暱稱='{x}' and 占卜日期='{self.cmDate.currentText()}'"
        cursor.execute(cmd_1)
        dataN=cursor.fetchall()
        conn.commit()
        dataNumber =[str(data[0]) for data in dataN]
        conn.close()

        self.cmDatanumber.addItems(dataNumber)
        self.cmDate.currentIndexChanged.connect(self.cmDateChange)

        self.btnMenu.clicked.connect(self.btnMenuClick)
        self.btnReset.clicked.connect(self.btnResetClick)
        self.btnQuery.clicked.connect(self.btnQueryClick)
        self.btnPrint.clicked.connect(self.btnPrintClick)
    def btnPrintClick(self):
        useros = platform.system()
        if useros == "Linux":
            pdfmetrics.registerFont(TTFont('hei', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
        else:
            pdfmetrics.registerFont(TTFont('hei', 'simsun.ttc'))

        doc = SimpleDocTemplate(
            'tmp2.pdf',
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        nickname = f"""
        {self.cmNickname.currentText()}
        """

        content = []
        content.append(Paragraph(
            nickname,
            ParagraphStyle(
                name="Centered",
                fontSize=28,
                fontName="hei",
                alignment=TA_CENTER)
            )
        )

        content.append(Spacer(1, 30))

        data = [["占卜資訊", "第二格"],
                ["問題", f"{self.txtPromble.text()}"],
                ["易經占卜卦象資訊", ""],
                ["現況掛", f"{self.txtFirst.text()}"],
                ["建議掛", f"{self.txtSecond.text()}"],
                ["結果掛", f"{self.txtThird.text()}"],
                ["底掛", f"{self.txtLast.text()}"],
                [f"注意事項：{self.txtDetail.toPlainText()}", "  "]]
        # (行,列)
        table = Table(
            data=data,
            colWidths=[50, 120],
            rowHeights=[30, 30, 30, 30, 30, 30, 30, 30],
            style=[
                ('FONTNAME', (0, 0), (-1, -1), 'hei'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('SPAN', (0, 0), (1, 0)), ('SPAN', (0, 2), (1, 2)), ('SPAN', (0, 7), (1, 7)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ],
        )
        content.append(table)


        doc.build(content)

    def btnQueryClick(self):
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd=f"select * from 會員占卜資料 where 暱稱='{self.cmNickname.currentText()}' and 占卜日期='{self.cmDate.currentText()}' and 資料編號='{self.cmDatanumber.currentText()}'"
        cursor.execute(cmd)
        r=cursor.fetchone()
        self.txtType.setText(r[4])
        self.txtPromble.setText(r[6])
        self.txtFirst.setText(r[7])
        self.txtSecond.setText(r[8])
        self.txtThird.setText(r[9])
        self.txtLast.setText(r[10])
        self.txtDetail.setText(r[14])




    def cmDateChange(self):
        x=self.cmNickname.currentText()
        conn = mysql.connect(host=g.dbHost, user=g.dbAccount, password=g.dbPassword, database=g.db)
        cursor = conn.cursor()
        cmd_1 = f"select 資料編號 from 會員占卜資料 where 暱稱='{x}' and 占卜日期='{self.cmDate.currentText()}'"
        cursor.execute(cmd_1)
        dataN = cursor.fetchall()
        conn.commit()
        dataNumber = [str(data[0]) for data in dataN]
        conn.close()
        self.cmDatanumber.clear()
        self.cmDatanumber.addItems(dataNumber)

    def btnMenuClick(self):
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
        self.txtType.setText("其他")
        self.txtPromble.setText("無")
        self.cmDate.setCurrentText("")
        self.txtFirst.setText("無")
        self.txtSecond.setText("無")
        self.txtThird.setText("無")
        self.txtLast.setText("無")
        self.cmDatanumber.setCurrentText("")
        self.cmDate.setCurrentText("")


        self.cmNickname.setFocus()

