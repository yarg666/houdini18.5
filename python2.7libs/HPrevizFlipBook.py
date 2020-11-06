# coding: utf8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import os, sys, shutil, platform
from subprocess import Popen

import hou


class GUIprevizBrowse(QMainWindow):
# class GUI(QWidget):
	def __init__(self,parent):
		# super(GUI, self).__init__()
		super(GUIprevizBrowse, self).__init__(parent)
		self.cleanUI=self.initUI()
		self.errorDialog = QErrorMessage(self)
	def initUI(self):
		self.setStyleSheet(hou.qt.styleSheet())
		self.setProperty("houdiniStyle", True)
		self.setWindowTitle("flipBook Manager")
		self.resize(500,600)
		wrapper = QWidget()
		self.setCentralWidget(wrapper)
		mainLayout = QVBoxLayout()
		wrapper.setLayout(mainLayout)
		
		# previz path
		hou.hipFile.basename()
		self.projectpath = os.path.dirname(hou.hipFile.path())
		# is cegv file
		cgevdigit = self.projectpath.split('/')[-1]
		if cgevdigit.isdigit():
			self.projectpath = self.projectpath.replace(cgevdigit,"previz")
		else :
			self.projectpath +="/previz"
			
		if not os.path.isdir(self.projectpath):
			os.makedirs(self.projectpath)
			
		# houdini file range
		fstart=hou.playbar.frameRange()[0]
		fend=hou.playbar.frameRange()[1]
		
		# --- Make Previz layout ---
		previzHLayout = QHBoxLayout()
		previzHLayout.setSpacing(10)
		mainLayout.addLayout(previzHLayout)
		
		# --- Make Previz layout2 ---
		previzHLayout2 = QGridLayout()
		previzHLayout2.setSpacing(10)
		mainLayout.addLayout(previzHLayout2)
		
		# --- line ---
		labelline = QLabel()
		labelline.setFrameStyle(QFrame.HLine | QFrame.Raised)
		labelline.setLineWidth(2)
		mainLayout.addWidget(labelline)
		
		# --- Browser generic layout ---
		browserGHLayout = QGridLayout()
		browserGHLayout.setSpacing(20)
		browserGHLayout.setAlignment(Qt.AlignLeft)
		mainLayout.addLayout(browserGHLayout)
		
		# --- Browser Layout ---
		self.browserHLayout = QHBoxLayout()
		self.browserHLayout.setSpacing(10)
		mainLayout.addLayout(self.browserHLayout)
		
		# --- fill previzHLayout ---
		self.startFrame = QLineEdit(str(int(fstart)))
		self.startFrame.setValidator(QIntValidator(0, 100000))
		self.startFrame.setFixedWidth(40)
		self.startFrame.setMaxLength(4)
		self.startFrame.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout.addWidget(QLabel("Frames:"))
		previzHLayout.addWidget(self.startFrame)
		
		self.endFrame = QLineEdit(str(int(fend)))
		self.endFrame.setValidator(QIntValidator(0, 100000))
		self.endFrame.setFixedWidth(40)
		self.endFrame.setMaxLength(4)
		self.endFrame.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout.addWidget(QLabel("to:"))
		previzHLayout.addWidget(self.endFrame)
		
		self.filename = QLineEdit("default")
		self.filename.setFixedWidth(140)
		self.filename.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout.addWidget(QLabel("File Name:"))
		previzHLayout.addWidget(self.filename)
		
		self.sessionlabel = QLineEdit("previz")
		self.sessionlabel.setFixedWidth(140)
		self.sessionlabel.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout.addWidget(QLabel("Mplay Label"))
		previzHLayout.addWidget(self.sessionlabel)
		
		# --- fill previzHLayout2 ---
		self.useRes = QCheckBox()
		previzHLayout2.addWidget(QLabel("Use Res"),0,0)
		previzHLayout2.addWidget(self.useRes,0,1)
		
		self.resx = QLineEdit("1920")
		self.resx.setValidator(QIntValidator(1, 100000))
		self.resx.setFixedWidth(60)
		self.resx.setMaxLength(5)
		self.resx.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout2.addWidget(QLabel("x: "),0,2)
		previzHLayout2.addWidget(self.resx,0,3)
		
		self.resy = QLineEdit("1080")
		self.resy.setValidator(QIntValidator(1, 100000))
		self.resy.setFixedWidth(60)
		self.resy.setMaxLength(5)
		self.resy.setStyleSheet("font-size: 12px; font-weight: bold; ")
		previzHLayout2.addWidget(QLabel("y: "),0,4)
		previzHLayout2.addWidget(self.resy,0,5)
		
		self.fileformat = QComboBox()
		self.fileformat.addItem("png")
		self.fileformat.addItem("jpg")
		self.fileformat.addItem("exr")
		previzHLayout2.addWidget(QLabel("format:"),0,6)
		previzHLayout2.addWidget(self.fileformat,0,7)
		
		msgBoxBtn = QPushButton("process")
		msgBoxBtn.setFixedSize(100, 25)
		previzHLayout2.addWidget(msgBoxBtn,0,8)
		msgBoxBtn.clicked.connect(self.flipbook)
		
		cleanShotBtn = QPushButton("Cancel")
		cleanShotBtn.setFixedSize(100, 25)
		previzHLayout2.addWidget(cleanShotBtn,0,9)
		cleanShotBtn.clicked.connect(self.close_application)
		
		# --- fill browser Generic ---		
		browserGHLayout.addWidget(QLabel("        BROWSER"),0,0)
		self.useMplay = QCheckBox("Use Mplay")
		browserGHLayout.addWidget(QLabel("play with:"),0,1)
		browserGHLayout.addWidget(self.useMplay,0,2)
		
		# --- fill browser ---
		self.previzTree = self.makeTreeWidget()
		self.browserHLayout.addWidget(self.previzTree)
		
	def makeTreeWidget(self):
		previzlist=os.listdir(self.projectpath)
		
		self.treeWidget = QTreeWidget()
		
		headerLabels = ["Cache", "Play", "Folder" ,"Remove"]
		self.treeWidget.setColumnCount(len(headerLabels))
		self.treeWidget.setHeaderLabels(headerLabels)
		header = self.treeWidget.header()
		header.resizeSection(0, 170)
		header.resizeSection(1, 140)
		header.resizeSection(2, 140)
		header.resizeSection(3, 140)
		
		# self.treeWidget.itemActivated.connect(self.getCurrentItems)
		self.treeWidget.itemClicked.connect(self.getCurrentItems)
		
		for previz in previzlist:
			previzpath = self.projectpath + "/" + previz
			if os.path.isdir(previzpath):
				previzitems=os.listdir(previzpath)
				if len(previzitems) != 0:
					previzname = StandardItem([previz])
					
					self.treeWidget.addTopLevelItem(previzname)
					
					previzitems=os.listdir(previzpath)
					previzitem = previzitems[ int(len(previzitems)/2) ]
					# frame range
					try:
						if previz in previzitems[0]:
							fstart = previzitems[0].split(".")[-2]
						if previz in previzitems[-1]:
							fend = previzitems[-1].split(".")[-2]
					except:
						pass
						
					picturepath= previzpath + "/" + previzitem
					# picture
					picture = QPixmap(picturepath)
					label = QLabel("",self.treeWidget)
					label.setPixmap(picture)
					label.setScaledContents(1)
					label.setFixedSize(128, 64)
					
					# label.mousePressEvent = self.clickImg
					
					# play
					btnplay = QPushButton('Play',self.treeWidget)
					btnplay.resize(50,20)
					btnplay.clicked.connect(lambda x=picturepath.replace(picturepath.split(".")[-2],"*"   ):self.playimg(x))
					# openFolder
					btnopenfolder = QPushButton('openFolder',self.treeWidget)
					btnopenfolder.resize(50,20)
					btnopenfolder.clicked.connect(lambda x=os.path.dirname(picturepath):openfolder(x))
					# delete
					btnrmv = QPushButton('Delete',self.treeWidget)
					btnrmv.resize(50,20)
					btnrmv.clicked.connect(lambda x=os.path.dirname(picturepath):self.rmimg(x))
					
					previzDdetails = StandardItem(previzname,["",previzitem])
					# set previz StandardItem details
					previzDdetails.setName(previz)
					if fstart.isdigit() and fend.isdigit():
						previzDdetails.setRange([fstart,fend])

					self.treeWidget.setItemWidget(previzDdetails, 0,label)
					self.treeWidget.setItemWidget(previzDdetails, 1,btnplay)
					self.treeWidget.setItemWidget(previzDdetails, 2,btnopenfolder)
					self.treeWidget.setItemWidget(previzDdetails, 3,btnrmv)
				
		self.treeWidget.expandAll()
		return self.treeWidget
	
	# def clickImg(self,event,a="b"):
		# print "Click"
		# print event.button()
		# print a

	def getCurrentItems(self,it,col):
		"""Returns Current top level item and child index.
		If no child is selected, returns -1. 
		"""
		#Check if top level item is selected or child selected
		if self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem())==-1:
			self.filename.setText(it.name)
			self.sessionlabel.setText(it.name)
			if it.fstart != -1:
				self.startFrame.setText(str(int(it.fstart)))
				self.endFrame.setText(str(int(it.fend)))
			# print(it, col, it.text(col))
			# print it.name
			# return self.treeWidget.currentItem().parent() # ,self.treeWidget.currentItem().parent().indexOfChild(self.treeWidget.currentItem())
		else:
			pass
			# print 1
			# return self.treeWidget.currentItem(),-1
		
		
	def rmimg(self,path):
		try:
			shutil.rmtree(path)
		except:
			pass
		self.refreshTree()
	
	def refreshTree(self):
		while 1:
			child = self.browserHLayout.takeAt(0)
			if not child:
				break
			child.widget().deleteLater()
		previzTree = self.makeTreeWidget()
		self.browserHLayout.addWidget(previzTree)
		
	def flipbook(self):
		filename = self.filename.text().replace(" ","_")
		imgpath = self.projectpath + "/" + filename
		imgpathfiles = imgpath + "/" + filename + ".$F4." + self.fileformat.currentText()
		sessionlabel = self.sessionlabel.text()
		if not os.path.isdir(imgpath):
			os.makedirs(imgpath)
		f1 = float(self.startFrame.text())
		f2 = float(self.endFrame.text())
		useres = self.useRes.isChecked()
		resx = int(float(self.resx.text()))
		resy = int(float(self.resy.text()))
		# print imgpathfiles
		# print "res: " + str(resx) +"x" + str(resy)
		viewer=hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
		currentviewer = viewer.isCurrentTab()
		if currentviewer is False:
			 self.messageUi("Current viewer is not the first active viewer\nFilpbook is canceled !")
			 return
		
		
		flipbook_options = viewer.flipbookSettings().stash()
		flipbook_options.frameRange((f1,f2))
		flipbook_options.output(imgpathfiles)
		flipbook_options.sessionLabel(sessionlabel)
		
		flipbook_options.useResolution(useres)
		flipbook_options.resolution((resx,resy))
		
		viewer.flipbook(viewer.curViewport(), flipbook_options)
		self.refreshTree()
		
		
	def messageUi(self,message="must say sorry !"):
		msgBox = QMessageBox(self)
		msgBox.setWindowTitle("Warning")
		msgBox.setText(message)
		buttons=msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		msgBox.show()
		ret = msgBox.exec_()
		if ret == 1024:
			# self.cleanShot()
			return 1
			# print "clean done"
		if ret == 4194304:
			return 0
			# print "clean aborted"
		
	def close_application(self):
		print("bye bye")
		# sys.exit()
		self.close()
		
	def playimg(self,path):
		import scramble
		path=os.path.normpath(path)
		# print path
		player = 1-self.useMplay.isChecked()
		if player == 0:
			houpaths=hou.houdiniPath()
			for p in houpaths:
				if p.find("HOUDI") > -1:
					if p.find("/bin") > -1:
						houpath = p
			cmd = houpath + "/mplay " + str(path)
			# Popen(cmd, shell=True)
		else:
			path=path.replace("*","####")
			cmd = "C:/PROGRA~1/Tweak/rv-win64-x86-64-6.0.4/bin/rv.exe " + str(path)
		# print cmd
		Popen(cmd, shell=True)

def openfolder(path):
	sysname = platform.system()
	if sysname=="Windows":
		cmd = "explorer " + os.path.normpath(path)
		#subprocess.Popen(cmd)
		Popen(cmd)
	else :
		hou.ui.displayMessage("to be done for this os system")
		
def flipBookBrowser():
	# ui = GUI()
	ui = GUIprevizBrowse(hou.ui.mainQtWindow())
	go = ui.show()

class StandardItem(QTreeWidgetItem):
	def __init__(self,*args):
		super(StandardItem, self).__init__(*args)
		self.name=None
		self.cache=None
		self.color="white"
		self.state=None
		self.fstart=-1
		self.fend=-1
		
	def setColor(self,color="white"):
		self.color=color
	def setState(self,state=None):
		self.state=state
	def setCache(self,cache=None):
		self.cache=cache
	def setName(self,name=None):
		self.name=name
		
	def setRange(self,range=[-1,-1]):
		try:
			self.fstart=range[0]
			self.fend=range[1]
		except:
			pass
		
	def getMenu(self):
		menu = QMenu()
		#menu.setProperty("houdiniStyle", True)
		menu.addAction("whatFX",self.test)
		return menu

	def test(self):
		print "yo"