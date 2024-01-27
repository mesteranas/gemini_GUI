import sys
from custome_errors import *
sys.excepthook = my_excepthook
import winsound
import pyperclip
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
import google.generativeai as genai
import PIL.Image
genai.configure(api_key="")
IMGModel = genai.GenerativeModel('gemini-pro-vision')
TextModel=genai.GenerativeModel('gemini-pro')
class M(qt2.QObject):
    finished=qt2.pyqtSignal(str)
class message (qt2.QRunnable):
    def __init__(self,choice,data,path=""):
        super().__init__()
        self.choice=choice
        self.data=data
        self.path=path
        self.t=M()
        self.finish=self.t.finished
    def sendI(self):
        try:
            img=PIL.Image.open(self.path)
            response = IMGModel.generate_content([self.data,img])
            self.finish.emit(response.text)
        except:
            self.finish.emit(_("error"))
    def sendText(self):
        try:
            response = TextModel.generate_content(self.data)
            self.finish.emit(response.text)
        except:
            self.finish.emit(_("error"))

    @qt2.pyqtSlot()
    def run(self):
        if self.choice==0:
            self.sendText()
        elif self.choice==1:
            self.sendI()

class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        service=guiTools.listBook(layout,_("select service"))
        layout1=qt.QVBoxLayout()
        layout2=qt.QVBoxLayout()
        self.message=qt.QLineEdit()
        self.message.setAccessibleName(_("message"))
        layout1.addWidget(self.message)
        self.path=qt.QLineEdit()
        self.path.setAccessibleName(_("path"))
        self.path.setReadOnly(True)
        layout2.addWidget(self.path)
        self.browse=qt.QPushButton(_("browse"))
        self.browse.setDefault(True)
        self.browse.clicked.connect(self.onbrowse)
        layout2.addWidget(self.browse)
        self.IMG_ask=qt.QLineEdit()
        self.IMG_ask.setAccessibleName("ask gemini about this this photo")
        layout2.addWidget(self.IMG_ask)
        self.convertText=qt.QPushButton(_("send"))
        self.convertText.setDefault(True)
        self.convertText.clicked.connect(lambda:self.runThread(0,self.message.text()))
        layout1.addWidget(self.convertText)
        self.sendIMG=qt.QPushButton(_("send"))
        self.sendIMG.setDefault(True)
        self.sendIMG.clicked.connect(lambda:self.runThread(1,self.IMG_ask.text(),path=self.path.text()))
        layout2.addWidget(self.sendIMG)
        self.result=qt.QTextEdit()
        self.result.setReadOnly(True)
        self.result.setAccessibleName(_("result"))
        layout.addWidget(self.result)
        service.add(_("text model"),layout1)
        service.add(_("image model"),layout2)
        self.Threadpool=qt2.QThreadPool()
        self.setting=qt.QPushButton(_("settings"))
        self.setting.setDefault(True)
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)


        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}_GUI".format(settings_handler.appName)))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def onbrowse(self):
        file=qt.QFileDialog()
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            self.path.setText(file.selectedFiles()[0])
            self.path.setFocus()
    def runThread(self,choise,data,path=""):
        thread=message(choise,data,path=path)
        thread.t.finished.connect(self.end)
        self.Threadpool.start(thread)
        winsound.PlaySound("data/sounds/1.wav",1)
        self.sendIMG.setDisabled(True)
        self.convertText.setDisabled(True)
    def end(self,text):
        self.result.setText(text)
        self.sendIMG.setDisabled(False)
        self.convertText.setDisabled(False)
        winsound.PlaySound("data/sounds/2.wav",1)
        self.result.setFocus()

App=qt.QApplication([])
w=main()
w.show()
App.exec()