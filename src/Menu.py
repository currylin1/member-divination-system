from PySide6.QtWidgets import QFrame

from g import g
from ui.Menu import Ui_Menu


class Menu(QFrame,Ui_Menu):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btnOut.clicked.connect(self.btnOutClick)
        self.btnExit.clicked.connect(self.btnExitClick)
        self.btnMember.clicked.connect(self.btnMemberClick)
        self.btnDivination.clicked.connect(self.btnDivinationClick)
        self.btnQuery.clicked.connect(self.btnQueryClick)
        self.btnFinance.clicked.connect(self.btnFinanceClick)

    def btnFinanceClick(self):
        from Finance import Finnance
        frame=Finnance()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnQueryClick(self):
        from Query import  Quert
        frame=Quert()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnDivinationClick(self):
        from Divination import Divination
        frame=Divination()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnMemberClick(self):
        from Member import Member
        frame=Member()
        g.mainLayout.addWidget(frame)
        self.close()
        frame.setFocus()

    def btnOutClick(self):
        from Login import Login
        frame=Login()
        g.mainLayout.addWidget(frame)
        self.close()
        self.setFocus()

    def btnExitClick(self):
        g.mainWindow.close()

