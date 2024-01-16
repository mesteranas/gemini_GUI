import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
from settings import *
language.init_translation()
class listBook(qt.QListWidget):
    def __init__(self,layout,text):
        super().__init__()
        self.layout=layout
        self.setAccessibleName(text)
        layout.addWidget(self)
        self.w=qt.QStackedWidget()
        layout.addWidget(self.w)
        self.currentRowChanged.connect(self.changeI)
    def add(self,text,tabLayout):
        w=qt.QWidget()
        w.setLayout(tabLayout)
        self.w.addWidget(w)
        self.addItem(text)
    def changeI(self,index):
        self.w.setCurrentIndex(index)