import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from Login import Login
from g import g
from ui.mainWindow import Ui_MainWindow


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.setupUi(self)
        # self.frame=Login(parent=self)
        # self.mainLayout.addWidget(self.frame)


        frame=Login()
        g.mainLayout=self.mainLayout
        g.mainLayout.addWidget(frame)
        g.mainWindow=self



if __name__ == "__main__":
    app=QApplication(sys.argv)

    w=MainWindow()

    w.show()

    app.exec()