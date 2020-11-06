# coding: utf8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import os, sys
from functools import partial
import time
import hou

from lxml import etree
import getpass
import codecs
import shutil
import math

class MyDialog(QDialog):
	def __init__(self, parent = None, f = 0):
		super(MyDialog, self).__init__(parent, f)
		mainLayout = QVBoxLayout()
		self.setLayout(mainLayout)
		description = QLabel("This is coustom dialog.")
		mainLayout.addWidget(description)
		self.inputWidget = QLineEdit()
		mainLayout.addWidget(self.inputWidget)
		buttonArea = QHBoxLayout()
		mainLayout.addLayout(buttonArea)
		buttonArea.addStretch()
		okBtn = QPushButton("OK")
		buttonArea.addWidget(okBtn)
		okBtn.clicked.connect(self.accept)
		cancelBtn = QPushButton("Cancel")
		buttonArea.addWidget(cancelBtn)
		cancelBtn.clicked.connect(self.reject)
	def getInputText(self):
		return self.inputWidget.text()
		
class StandardItem(QTreeWidgetItem):
	def __init__(self,*args):
		super(StandardItem, self).__init__(*args)
		self.cache=None
		self.color="white"
		self.state=None
		
	def setColor(self,color="white"):
		self.color=color
	def setState(self,state=None):
		self.state=state
	def setCache(self,cache=None):
		self.cache=cache
		
	def getMenu(self):
		menu = QMenu()
		#menu.setProperty("houdiniStyle", True)
		menu.addAction("whatFX",self.test)
		return menu

	def test(self):
		print "hola"
		
class GUI(QMainWindow):
# class GUI(QWidget):
	def __init__(self,parent):
		# super(GUI, self).__init__()
		super(GUI, self).__init__(parent)
		self.cleanUI=self.initUI()
		self.errorDialog = QErrorMessage(self)
	def initUI(self):
		self.setStyleSheet(hou.qt.styleSheet())
		self.setProperty("houdiniStyle", True)
		self.setWindowTitle("Cleaner")
		self.resize(1150, 600)
		wrapper = QWidget()
		self.setCentralWidget(wrapper)
		mainLayout = QVBoxLayout()
		wrapper.setLayout(mainLayout)
		
		# --- task box ---
		setUpHorizontalArea = QHBoxLayout()
		setUpHorizontalArea.setSpacing(20)
		mainLayout.addLayout(setUpHorizontalArea)

		# get SHOTS
		project = hou.getenv("project")
		projectpath = hou.hipFile.path()
		try:
			projectpath = projectpath.split(project)[0] + "/" + project
			print "PROJECT PATH: " + str(projectpath) 
		except:
			hou.ui.displayMessage("No project found")
			print "No project found"
			return
		usershots = listUserShots(projectpath,departement = "fx")
		# usershots=["FOO","TOTO"]
		
		self.taskbox = QComboBox()
		self.taskbox.addItems(usershots)
		self.taskbox.setEditable(False)
		self.taskbox.setInsertPolicy(QComboBox.NoInsert)
		
		self.taskbox.currentIndexChanged.connect(self.taskChange)
		# comboBox.completer().setCompletionMode(QCompleter.PopupCompletion)
		setUpHorizontalArea.addWidget(self.taskbox)
		
		# --- tree row ---
		self.treeHorizontalArea = QHBoxLayout()
		self.treeHorizontalArea.setSpacing(20)
		mainLayout.addLayout(self.treeHorizontalArea)
		
		# get path to be done again
		startpath = hou.hipFile.path()
		assetname = hou.getenv("assetname")
		
		if assetname == None:
			assetname = hou.hipFile.basename().replace(".hip","")
		try:
			startpath=startpath.split(assetname)[0]
		except:
			return
		print "Start Path: " + str(startpath)
		
		self.cacheTree = self.makeTreeWidget(startpath)
		self.treeHorizontalArea.addWidget(self.cacheTree)

		# --- bottom row ---
		bottomHrzArea = QHBoxLayout()
		bottomHrzArea.setSpacing(20)
		mainLayout.addLayout(bottomHrzArea)
		
		cleanShotBtn = QPushButton("Cancel")
		cleanShotBtn.setFixedSize(150, 25)
		bottomHrzArea.addWidget(cleanShotBtn)
		cleanShotBtn.clicked.connect(self.close_application)
		
		msgBoxBtn = QPushButton("Delete Caches")
		msgBoxBtn.setFixedSize(150, 25)
		bottomHrzArea.addWidget(msgBoxBtn)
		msgBoxBtn.clicked.connect(self.valid)
		
	def valid(self):
		msgBox = QMessageBox(self)
		msgBox.setWindowTitle("Warning")
		msgBox.setText("Do you want to delete all the unchecked caches ?")
		buttons=msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		msgBox.show()
		ret = msgBox.exec_()
		if ret == 1024:
			self.cleanShot()
			print "clean done"
		if ret == 4194304:
			return
			print "clean aborted"

		
	def taskChange(self):
		if self.taskbox.currentText() == "getShot":
			return
		path = self.taskbox.currentText() + "/"
		print path
		self.refreshTree(path)
		
	def refreshTree(self,shotpath):
		while 1:
			child = self.treeHorizontalArea.takeAt(0)
			if not child:
				break
			child.widget().deleteLater()
		self.cacheTree = self.makeTreeWidget(shotpath)
		self.treeHorizontalArea.addWidget(self.cacheTree)

		
	def makeTreeWidget(self,path):
		
		data = sortRender(path)
		data = xmlCheckInUse(data,path)
		
		treeWidget = QTreeWidget()
		headerLabels = ["Layer", "Date","export","Size"]
		treeWidget.setColumnCount(len(headerLabels))
		treeWidget.setHeaderLabels(headerLabels)
		header = treeWidget.header()
		header.resizeSection(0, 850)
		header.resizeSection(1, 140)
		header.resizeSection(2, 40)
		
		treeWidget.setAlternatingRowColors(True)
		
		checkable = Qt.ItemIsUserCheckable
		enable = Qt.ItemIsEnabled
		
		treeWidget.customContextMenuRequested.connect(self.contextMenu)
		# treeWidget.customContextMenuRequested.connect(self.openMenu)
		treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		# try :

		# if data == None:
			# data = [["empty"],["empty"],["empty"]]

		for layer in data[0]:
			#topItem = QTreeWidgetItem([layer])
			topItem = StandardItem([layer])
			# topItem.setFlags(Qt.ItemIsEnabled)
			topItem.setFlags(topItem.flags() | checkable)
			topItem.setCheckState(0,Qt.Unchecked)
			topItem.setForeground(0,QBrush(QColor("yellow")))
			topItem.setColor("yellow")
			topItem.setState(Qt.Unchecked)
			
			treeWidget.addTopLevelItem(topItem)
			
			for type in data[1]:
				# typeItem = QTreeWidgetItem(topItem, [type,"",""])
				typeItem = StandardItem(topItem, [type,"",""])
				# typeItem.setFlags(typeItem.flags() |Qt.ItemIsEnabled)
				typeItem.setFlags(typeItem.flags() | checkable)
				typeItem.setCheckState(0,Qt.Unchecked)
				typeItem.setState(Qt.Unchecked)
				
				for cache in data[2]:
					try :
						if type in cache.type:
							if layer in cache.path:
								# print "CACHE: " + str(cache.path)
								#childItem = QTreeWidgetItem(typeItem, [cache.path,cache.date,cache.export])
								childItem = StandardItem(typeItem, [cache.path,cache.date,cache.export,cache.size])
								childItem.setFlags(childItem.flags() | checkable)
								childItem.setCache(cache.path)
								if cache.inuse == 1:
									childItem.setColor("orange")
									childItem.setCheckState(0,Qt.Checked)
									childItem.setForeground(0,QBrush(QColor("orange")))
									childItem.setForeground(1,QBrush(QColor("orange")))
									childItem.setForeground(2,QBrush(QColor("orange")))
									childItem.setForeground(3,QBrush(QColor("orange")))
									childItem.setState(Qt.Checked)
								else:
									childItem.setCheckState(0,Qt.Unchecked)
									childItem.setState(Qt.Unchecked)
								if cache.export == "Yes":
									childItem.setColor("violet")
									childItem.setForeground(0,QBrush(QColor("violet")))
									childItem.setForeground(1,QBrush(QColor("violet")))
									childItem.setForeground(2,QBrush(QColor("violet")))
									childItem.setForeground(3,QBrush(QColor("violet")))
					except:
						pass
		# except:
			# print "no render Layers"
			# pass
		treeWidget.expandAll()
		treeWidget.itemChanged.connect(self.onCheck)
		return treeWidget
		
	# get selected item and open contextual menu 
	def contextMenu(self, pos):
		iterator = QTreeWidgetItemIterator(self.cacheTree,QTreeWidgetItemIterator.Selected)
		item =  iterator.value()
		menu = item.getMenu()
		menu.exec_( QCursor.pos() )
	
	# todo remove from xml
	def cleanShot(self):
		tree = self.cacheTree
		iterator = QTreeWidgetItemIterator(self.cacheTree,QTreeWidgetItemIterator.NotChecked)
		caches=[]
		user = getpass.getuser()
		
		while iterator.value():
			item = iterator.value()
			if item.cache != None:
				caches.append(item.cache)
				# print item.cache
			iterator+=1
						
		# for count in range(max + 1):
		ncache = len(caches)
		if ncache == 0:
			print "Nothing Selected"
			return
		
		# get current shot
		currentpath = caches[0].split(user)[0]+"/"+user
		
		max = 100
		progressDialog = QProgressDialog("Progress...", "Cancel", 0, max, self)
		progressDialog.setWindowTitle("Progress Dialog")
		
		for count in range(ncache):
			if ncache == 1:
				inc = 100.0/(ncache)
				progress = inc
			else:
				inc = 100.0/(ncache-1)
				progress = count*inc
			# qApp.processEvents()
			if progressDialog.wasCanceled():
				break
			progressDialog.setValue(progress)
			progressDialog.setLabelText("Progress... %d %%" % int(progress))
			# time.sleep(1)
			try:
				shutil.rmtree(caches[count])
			except:
				print "failed remove: " + str(caches[count])
				pass
			try:
				cleanXml(caches[count])
			except:
				print "failed xml remove"
				pass
				
		# update
		print "REMOVE DONE"
		try:
			self.refreshTree(currentpath)
		except:
			path
			
	def onCheck(self,item):
		state = item.checkState(0)
		if state == Qt.Unchecked:
			colorname = item.color
			color = QBrush(QColor(colorname))
			#color = QBrush(QColor("white"))
			newstate = Qt.Unchecked
		if state == Qt.Checked:
			color = QBrush(QColor("red"))
			newstate = Qt.Checked
			
		#item.setForeground(0,QBrush(QColor("red")))
		item.setForeground(0,color)
		child_count = item.childCount()
		for i in range(child_count):
			childitem = item.child(i)
			childitem.setCheckState(0,newstate)
			#childitem.setForeground(0,QBrush(QColor("red")))
			childitem.setForeground(0,color)
		
	def close_application(self):
		print("bye bye")
		# sys.exit()
		self.close()
		
def listUserShots(path,departement = "fx"):
	usershots = ["getShot"]
	user = getpass.getuser()
	for file in os.listdir(path):
		shotfile = path + "/" + file
		if os.path.isdir(shotfile):
			for subshotfile in os.listdir(shotfile):
				if subshotfile == "houdini":
					houdir =  shotfile + "/" + subshotfile
					for subhoudir in os.listdir(houdir):
						if subhoudir == departement:
							houdepartement =  houdir + "/" + subhoudir
							for usershot in os.listdir(houdepartement):
								if usershot == user:
									usershots.append(houdepartement + "/" + usershot)
									print "USERSHOTS: " + str(usershot)

	print "TASK: " + str(usershots)
	return usershots
	
def sortRender(path):
	date = ""
	user = getpass.getuser()
	rendertypes = ["bgeo","vdb","abc"]
	renderlayers = []
	result = []
	dossier=[]
	sous_dossiers=[]
	fichiers=[]
	size=0
	
	for rep in os.listdir(path):
		if user in rep:
			taskpath = path + "/" + rep
			# print "taskpath = " + taskpath
			for rendertypetask in os.listdir(taskpath):
				for rendertype in rendertypes:
					if rendertypetask == rendertype:
						rendertypepath = taskpath + "/" + rendertypetask
						# print "rendertypepath  = " + rendertypepath
						for layer in os.listdir(rendertypepath):
							layersversionpath = rendertypepath + "/" + layer
							# print "layersversionpath = " + layersversionpath
							for layerversion in os.listdir(layersversionpath):
								layerversionpath = layersversionpath+"/"+layerversion
								layerpass = layerversionpath.split("/")[-2]
								if rendertype == "bgeo":
									ext = "bgeo.sc"
								else:
									ext = rendertype
								date = ""
								try :
									print "layer: " + layerversionpath
									size=0
									for fichier in  os.listdir(layerversionpath):
										# print "ext: " + str(ext)
										# print "endWith: " + str(fichier.endswith(ext))
										if fichier.endswith(ext):# and layer in fichiers[0]:
											size+=os.path.getsize(layerversionpath+"/"+fichier)
											if date == "":
												t = os.path.getmtime(layerversionpath+"/"+fichier)
												date = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(t))
											else:
												pass
								except:
									pass
								hcache = Hcache()
								hcache.setStandard(str(rendertype),str(layer),str(layerversionpath),str(layerpass),str(date),convert_size(size))
								hcache.setVersion(str(layerversion))
								result.append(hcache)
								try:
									if rep != renderlayers[-1]:
										renderlayers.append(str(rep))
									if rep == renderlayers[-1]:
										pass
								except:
									pass
									renderlayers.append(str(rep))
	
	# print "DONE " + codecs.decode(str(renderlayers),'unicode_escape') +", " + str(rendertypes) + ", " + str(result)
	return renderlayers,rendertypes,result
	
def xmlCheckInUse(sortRender,path):
	""" get the result of sort render """
	# path = hou.hipFile.path()
	user = getpass.getuser()
	
	for layer in sortRender[0]:
		# print layer
		xmlfile = path.split(user)[0] + "/" + user + "/" + layer + "/houdiniCache.xml"
		print "xml file: " + str(xmlfile)
		
		if not os.path.isfile(xmlfile):
			print "No xml file"
			return sortRender
		try:
			parser = etree.XMLParser(remove_blank_text=True)
			tree = etree.parse(xmlfile, parser)
			print "xml loaded "
		except:
			print "xml loaded failed"
			return sortRender
		for cache in sortRender[2]:
			cachetype = cache.type
			cacheversion = cache.version
			layerpass = cache.layerpass
			# print "Layerpass: " +layerpass
			try:
				listtype = tree.find(cachetype)
				searchstring =  "cache[@name=\'" + layerpass + "\']"
				itemByname = listtype.find(searchstring)
				# print searchstring
				date = itemByname.get("date")
				version = itemByname.get("version")
				if str(cacheversion) == "v"+str(version):
					cache.setInUse(1)
			except:
				pass
				
			# export
			try:
				elementExport = tree.find("exports")
				listexport = list(elementExport)
				for exp in listexport:
					xmlname = exp.get('name')
					xmltype = exp.get('type')
					xmlversion = int(exp.get('version'))
					if xmlname == layerpass and xmltype == cachetype and xmlversion == int(cacheversion.replace("v","0")):
						cache.setExport("Yes")
			except:
				pass
	return sortRender
	
def cleanXml(cachepath):
	print "XML path start: " + cachepath
	user = getpass.getuser()
	print "user: " + user
	layer = cachepath.split("/")[-4]
	print "Layer: " + layer
	xmlfile = cachepath.split(layer)[0] + "/" + layer + "/houdiniCache.xml"
	print "xml file: " + str(xmlfile)

	name = cachepath.split("/")[-2]
	print "Name: " + name
	type = cachepath.split("/")[-3]
	print "Type: " + type
	version = cachepath.split("/")[-1].replace("v","")
	print "Version: " + version

	# get xml file
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse(xmlfile, parser)

	elementExport = tree.find(type)
	listexport = list(elementExport)
	for exp in listexport:
		xmlname = exp.get('name')
		xmltype = exp.get('type')
		xmlversion = exp.get('version')
		if xmlname == name and xmltype == type and xmlversion == version:
			elementExport.remove(exp)
			
	with open(xmlfile, 'w') as fid:	
		fid.write(etree.tostring(tree, pretty_print=True))
	
def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

	
def sortIFDs(path):
	date = ""
	user = getpass.getuser()
	rendertypes = ["ifds"]
	renderlayers = []
	result = []
	dossier=[]
	sous_dossiers=[]
	fichiers=[]
	size=0
	
	for rep in os.listdir(path):
		if user in rep:
			taskpath = path + "/" + rep
			for rendertypetask in os.listdir(taskpath):
				for rendertype in rendertypes:
					if rendertypetask == rendertype:
						# ifd directory found, create full path to ifds
						rendertypepath = taskpath + "/" + rendertypetask
						for layer in os.listdir(rendertypepath):
							layersversionpath = rendertypepath + "/" + layer
							# print "layersversionpath = " + layersversionpath
							for layerversion in os.listdir(layersversionpath):
								layerversionpath = layersversionpath+"/"+layerversion
								layerpass = layerversionpath.split("/")[-2]
								
								if rendertype == "ifds":
									ext = "ifd.sc"
								else:
									ext = "ifd"
								date = ""
								try :
									print "layer: " + layerversionpath
									for fichier in  os.listdir(layerversionpath):
										if fichier.endswith(ext):# and layer in fichiers[0]:
											size+=os.path.getsize(layerversionpath+"/"+fichier)
											if date == "":
												t = os.path.getmtime(layerversionpath+"/"+fichier)
												date = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(t))
											else:
												pass
								except:
									pass
								hcache = Hcache()
								hcache.setStandard(str(rendertype),str(layer),str(layerversionpath),str(layerpass),str(date),convert_size(size))
								hcache.setVersion(str(layerversion))
								result.append(hcache)
								try:
									if rep != renderlayers[-1]:
										renderlayers.append(str(rep))
									if rep == renderlayers[-1]:
										pass
								except:
									pass
									renderlayers.append(str(rep))
	
	# print "DONE " + codecs.decode(str(renderlayers),'unicode_escape') +", " + str(rendertypes) + ", " + str(result)
	return renderlayers,rendertypes,result
	
	
### CACHE CLASS
class Hcache:
	""" infos to modify hda """
	def __init__(self):
		""" project, user, film,seq, shot, otlstudio, otlscom """
		self.path = ""
		self.type = ""
		self.layer = ""
		self.date = ""
		self.inuse = -1
		self.layerpass = ""
		self.export = ""
		self.version = -1
		self.size = 0

	# standard infos
	def setStandard(self,cachetype,cachelayer,cachepath,cachelayerpass,cachedate,size):
		""" cachetype,cachelayer,cachepath """
		self.date = cachedate
		self.path = cachepath
		self.type = cachetype
		self.layer = cachelayer
		self.layerpass = cachelayerpass
		self.size = size
	def setInUse(self,value = -1):
		self.inuse = value
	def setExport(self,value = ""):
		self.export = value
	def setVersion(self,value = -1):
		self.version = value
		
		
def main():
	# ui = GUI()
	ui = GUI(hou.ui.mainQtWindow())
	go = ui.show()
	# sys.exit(ui.exec_())
# main()