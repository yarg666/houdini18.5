#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#return yProjectManager.yProjectManagerClass()
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os
import hou
import nodesearch
import platform
import subprocess
from lxml import etree

print "Hello from yCacheManager Beta"

class yCacheManagerClass(QWidget): 

	def __init__(self):
		super (yCacheManagerClass,self).__init__()
		
		#variables interface
		self.pipe=["CGEV"]
		self.user=["USER","jmargelin","fxboussard","tmekbel","abachiri","pmathon","dkessler","cguerton","rhajj"]
		
		
		#layout
		#init Table cache manager part I
		self.quickPublish = QCheckBox("quickPublishOnly",self)
		self.quickPublish.setStyleSheet('color: rgb(153,204,255)')
		self.cacheManagerLabel=QLabel()
		self.cacheManagerLabel.setText("fileCacheLister:")
		self.filterKeyCurrent=QLineEdit()
		self.filterKeyCurrent.setPlaceholderText('filter')
		self.refreshBoutonCurrent=QPushButton("refresh/checkVersion")
		self.rrender=QPushButton("rrender")
		self.update=QPushButton("updateVersion")
		# table part I
		self.tableCurrent = QTableWidget()
		self.tableCurrent.setColumnCount(6)
		self.tableCurrent.horizontalHeader().setStretchLastSection(1)
		self.tableCurrent.setColumnWidth(0,50)
		self.tableCurrent.setColumnWidth(1,100)
		self.tableCurrent.setColumnWidth(2,80)
		self.tableCurrent.setColumnWidth(3,50)
		self.tableCurrent.setColumnWidth(4,100)
		self.tableCurrent.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tableCurrent.setHorizontalHeaderLabels(["type","nom","current","last","explorer","chemin"]) 


		#init Table cache manager part II
		self.cacheBrowser=QLabel()
		self.cacheBrowser.setText("cacheBrowser:")
		self.quickPublishPartTwo = QCheckBox("quickPublishOnly",self)	
		self.quickPublishPartTwo.setStyleSheet('color: rgb(153,204,255)')
		#initialiser
		self.initToShot=QPushButton("initialiser")
		#pipe
		self.choisirPipe=QComboBox()
		for i in self.pipe:
			self.choisirPipe.addItem(i)
		#projet
		self.projectName=QComboBox()
		#shot
		self.shotName=QComboBox()
		self.shotName.addItem("SHOT")	
		#effet
		self.effetName=QComboBox()
		self.effetName.addItem("EFFET")	
		#username
		self.userName=QComboBox()
		for i in self.user:
			self.userName.addItem(i)
		#filter
		self.filterKey=QLineEdit()
		self.filterKey.setPlaceholderText('search')
		#load in scene
		self.loadButton=QPushButton("load")
		#refresh
		self.refreshBouton=QPushButton("refresh")
		#init Table cache manager part II
 		self.table = QTableWidget()
		self.table.setColumnCount(6)
		self.table.horizontalHeader().setStretchLastSection(1)
		self.table.setColumnWidth(0,50)
		self.table.setColumnWidth(1,100)
		self.table.setColumnWidth(2,80)
		self.table.setColumnWidth(3,50)
		self.table.setColumnWidth(4,100)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setHorizontalHeaderLabels(["type","nom","current","last","statue","chemin"])
		self.table.setDragEnabled(True)
		#layout
		mainLayout=QGridLayout()
		#add wdget part I:
		mainLayout.addWidget(self.cacheManagerLabel,0,0,1,3)
		mainLayout.addWidget(self.quickPublish,0,3,1,1)
		mainLayout.addWidget(self.update,1,1,1,1)
		mainLayout.addWidget(self.filterKeyCurrent,1,0,1,1)
		mainLayout.addWidget(self.refreshBoutonCurrent,1,3,1,1)
		mainLayout.addWidget(self.rrender,1,2,1,1)
		mainLayout.addWidget(self.tableCurrent,2,0,1,4)
		#add widget part II
		mainLayout.addWidget(self.cacheBrowser,3,0,1,3)
		mainLayout.addWidget(self.quickPublishPartTwo,3,3,1,1)
		mainLayout.addWidget(self.projectName,4,0,1,1)
		mainLayout.addWidget(self.shotName,4,1,1,1)
		mainLayout.addWidget(self.userName,4,2,1,1)
		mainLayout.addWidget(self.effetName,4,3,1,1)
		#mainLayout.addWidget(self.filterKey,5,0,1,2)
		mainLayout.addWidget(self.loadButton,5,0,1,2)
		mainLayout.addWidget(self.refreshBouton,5,3,1,1)
		mainLayout.addWidget(self.initToShot,5,2,1,1)
		mainLayout.addWidget(self.table,6,0,1,4)
		#launch layout
		self.setLayout(mainLayout)
		#launch fonction
		
		self.variables()
		self.projectNameMenu()
		self.fileCacheLister()
		self.button()
		self.setdefault()
		
	def variables(self):
		self.dollarHip=hou.expandString("$HIP")
		self.rootsBgeo =  ["/".join(self.dollarHip.split("/")[:-1])+"/bgeo/", "/".join(self.dollarHip.split("/")[:-1])+"/vdb/","/".join(self.dollarHip.split("/")[:-1])+"/abc/"]
		self.proj = "//storf/diskf/"

	def chooseInterface(self):
		self.fileCacheLister()
			
	def projectNameMenu(self):
		try:
			self.menuProjet()
		except:
			pass

#PART II
	def setdefault(self):
		try:
			projet = os.getenv("project")
			user = os.getenv("user")
			shot = os.getenv("shot")
			seq = os.getenv("sequence")
			plan = seq + "-" + shot

			assetName = os.getenv("assetname")
			effetName = ("_").join(assetName.split("_")[:-1][2:])

			index = self.projectName.findText(projet)
			self.projectName.setCurrentIndex(index)
			self.menuShot()
			index = self.shotName.findText(plan)
			self.shotName.setCurrentIndex(index)

			index = self.userName.findText(user)
			self.userName.setCurrentIndex(index)
			self.menuEffet()
			index = self.effetName.findText(effetName)
			self.effetName.setCurrentIndex(index)
			try:
				self.cacheBrowserF()
			except:
				pass
		except:
			pass		



	def menuProjet(self):
		self.projectName.clear()
		self.projectList=[]
		del self.projectList[:]
		self.projectName.addItem("PROJET")
		try:
			#liste les dossier a la racine
			for dir in os.walk(self.proj).next()[1]:
				self.projectList.append(dir)
			#trie la lise des dossier a la racine	
			projectListSorted=sorted(self.projectList)
			#ajouter les dossiers dans le menu
			
			for i in projectListSorted:
				self.projectName.addItem(i)
				
		except:
			pass
		try:
			self.cacheBrowserF()
		except:
			pass	

	def menuShot(self):
		self.shotList=[]
		del self.shotList[:]
		self.shotName.clear()
		
		projetSelect=self.projectName.currentText()
		self.shotName.addItem("SHOT")
		try:
			for shot in os.walk(self.proj+projetSelect+"/").next()[1]:
				try:
					for dir in os.walk(self.proj+projetSelect+"/"+shot).next()[1]:
						if str(dir) =="houdini":
							self.shotList.append(shot)
				except:
					pass
			shotSorted= sorted(self.shotList)	
			for i in shotSorted:
				self.shotName.addItem(i)
		except:
			pass

		try:
			self.cacheBrowserF()
		except:
			pass		

	def menuEffet(self):
		self.effetName.clear()
		projetSelect=self.projectName.currentText()
		shotSelect=self.shotName.currentText()
		userSelect=self.userName.currentText()

		path = self.proj+"/"+projetSelect+"/"+shotSelect+"/"+"houdini/fx/"+userSelect+"/"

		print "effet"
		try:
			for i in os.walk(path).next()[1]:
				print i
				print ("_").join(i.split("_")[2:-2])
				self.effetName.addItem(("_").join(i.split("_")[2:-1]))
		except:
			print "choisir un effet"
			pass

		try:
			self.cacheBrowserF()
		except:
			pass			

	def cacheBrowserF(self):
		projetSelect=self.projectName.currentText()
		shotSelect=self.shotName.currentText()
		userSelect=self.userName.currentText()
		effetSelect=self.effetName.currentText()
		task= "fx"
		xml= "houdiniCache.xml"

		path = self.proj+"/"+projetSelect+"/"+shotSelect+"/"+"houdini/fx/"+userSelect+"/"+shotSelect+"_"+task+"_"+effetSelect+"_"+userSelect
		#xml
		tree = etree.parse(path+"/"+xml)
		root = tree.getroot()
		cacheListe=[]
		del cacheListe[:]

		for i in root:
		    for sub in i:
		        temp = (i.tag,sub.attrib)
		        myQuickPublish= temp[1].get("quickPublish",{})
		        if self.quickPublishPartTwo.isChecked():
		        	print "publish"
		        	print myQuickPublish
		        	if myQuickPublish == "1":

		        		cacheListe.append(temp)
		        else:
		        	cacheListe.append(temp) 

		#tableau build
		self.table.setRowCount(0)
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		inc=0
		rowNew = 0
		while inc < len(cacheListe):
			myType= cacheListe[inc][1].get("type",{})
			myName= cacheListe[inc][1].get("name",{})
			myVersion= cacheListe[inc][1].get("version",{})
			myPublish= cacheListe[inc][1].get("quickPublish",{})
			pathCache = path+"/"+myType+"/"+myName+"/"+"v"+myVersion
			pathLastVersion = path+"/"+myType+"/"+myName

			if os.path.exists(path+"/"+myType+"/"+myName+"/"):
				self.table.insertRow(self.table.rowCount())
				#type
				type = QTableWidgetItem(myType)
				self.table.setItem(rowNew,0,type)
				#name
				name = QTableWidgetItem(myName)
				self.table.setItem(rowNew,1,name)
				#name.rowsMoved.connect(self.ouvrir)
				#currentVersion
				currentVersion = QTableWidgetItem(myVersion)
				self.table.setItem(rowNew,2,currentVersion)
				#lastVersion
				versionList = os.walk(pathLastVersion).next()[1]
				lastVersion = QTableWidgetItem(versionList[-1][1:])
				self.table.setItem(rowNew,3,lastVersion)
				#explorer
				published = QTableWidgetItem("neant")
				self.table.setItem(rowNew,4,published)

				print myPublish
				if myPublish == "1":
					published.setText("quickPublish") 

				#chemin
				chemin = QTableWidgetItem(pathCache)
				self.table.setItem(rowNew,5,chemin)
				rowNew+=1
				print "ok"
			else :
				print "pas ok"	
			inc+=1

		self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

	def ouvrir(self):
		colonne=self.sender().property("row")

		path = self.table.item(colonne,5).text()
		path = os.path.normpath(path)
		if platform.system() == "Windows":
			os.startfile(path)
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path])
		else:
			subprocess.Popen(["xdg-open", path])

	def loadSelect(self):
		selectList = self.table.selectedItems()

		nodeSelect = hou.selectedNodes()
		if len(nodeSelect) == 0:
			hou.ui.displayMessage("select one node",buttons=('OK',))

		refNode= nodeSelect[0]
		obj="/obj/"
		loadCachePath = "obj/load/"



		for i in selectList:

			getName = refNode.name()
			newCache = refNode.parent().createNode("renderGeo",i.text())

			newCache.setPosition(refNode.position())
			newCache.move([0, -1])
			#path = ""
			version = self.table.item(i.row(),3).text()
			myType = self.table.item(i.row(),0).text()
			if myType == "bgeo":
				myType = "bgeo.sc"

			"""if os.walk(self.proj).next()[1]	"""
			path = self.shotName.currentText() +"_"+i.text()+"_"+"v"+version+"."+"$F4"+"."+myType  

			newCache.parm("lecture").set(1)

			newCache.parm("lock").set(1)
			newCache.setParms({"path2":self.table.item(i.row(),5).text()+"/"+path})

			newCache.parm("oldV").set(version)
			newCache.parm("version2").set(version)
			print self.table.item(i.row(),4).text()
			if self.table.item(i.row(),4).text() == "quickPublish":
				newCache.parm("quickPublish").set(1)
			newCache.parm("version2").pressButton()	

			if newCache.parm("path2").rawValue().find(".abc") != -1 :
				newCache.parm("alembic2").set("1")
				abcPath = newCache.parm("path2").rawValue().replace(".$F4","")		
				newCache.parm("path2").set(abcPath)			







#PART I
	def chooseInterfaceTwo(self):

		self.projectNameMenu()
		self.variables()
		self.fileCacheLister()
	
	def listSort(self):
		#sortList by alphabetical order
		self.sortList= sorted(self.cacheNameListe)
		# systeme de filtres par mot
		selectionFilter=self.filterKeyCurrent.text()
		# test if there is a key word to filter the list with
		if len(selectionFilter) == 0:
			self.filterCacheNameListe=self.sortList
		else :
		#list sorted
			for listElement in self.sortList:
				if selectionFilter in listElement:
					self.filterCacheNameListe.append(listElement)			
					
	def clearListes(self):
		#create and clear all List
		self.cacheNameListe=[]
		del self.cacheNameListe[:]
		self.sortList= []
		del self.sortList[:]
		self.filterCacheNameListe=[]
		del self.filterCacheNameListe[:]
		self.geoType=[]
		del self.geoType[:]
		self.currentVerions=[]
		del self.currentVerions[:]
		self.cachePath=[]
		del self.cachePath[:]
		self.nodeListe=[]
		del self.nodeListe[:]
		self.nodePath=[]
		del self.nodePath[:]


	def fileCacheLister(self):
		#clearListes
		self.tableCurrent.clearSelection()
		self.clearListes()
		#get cache info
		myfiltre = self.filterKeyCurrent.text()
		matchType = nodesearch.NodeType("CG::renderGeo*")
		if len(myfiltre)!= 0:
			matchName = nodesearch.Name(myfiltre)
		else :
			matchName = nodesearch.Name("*")
		self.match = nodesearch.Group([matchType,matchName])
				
		net = hou.node("/obj/")
		#self.listSort()
		for node in self.match.nodes(net,recursive =True):
			
			self.nodePath.append(node)

			#quickPublish
			if self.quickPublish.isChecked():
				if node.parm("quickPublish").eval() == 1:
					self.cacheNameListe.append(str(node))
					self.cachePath.append(node.parm("path").eval()) 
					self.geoType.append(node.parm("datatype").eval())
					self.currentVerions.append(node.parm("version").eval())	
					#lecture
					if 	node.parm("lecture").eval() == 1:
						self.cachePath[-1] =("/").join(node.parm("path2").eval().split("/")[:-1])
						self.currentVerions[-1] =node.parm("version2").eval()	

			else:	
				self.cacheNameListe.append(str(node))
				self.cachePath.append(node.parm("path").eval()) 
				self.geoType.append(node.parm("datatype").eval())
				self.currentVerions.append(node.parm("version").eval())
				#lecture
				if 	node.parm("lecture").eval() == 1:
					self.cachePath[-1] =("/").join(node.parm("path2").eval().split("/")[:-1])
					self.currentVerions[-1] =node.parm("version2").eval()

		
		#get versions

		versionListe=[]	
		self.versionMetaListe=[]
		inc=0

		try:
			for cache in self.cachePath:
				for version in os.walk("/".join(cache.split("/")[:-1])).next()[1]:
					versionListe.append(version[1:])
				self.versionMetaListe.append(versionListe)
				versionListe=[]
				inc+=1		
		except:
			pass

		# build table
		inc=0
		self.tableCurrent.setSelectionMode(QAbstractItemView.MultiSelection)
		self.tableCurrent.setRowCount(len(self.cacheNameListe))
		self.tableCurrent.setSelectionMode(QAbstractItemView.MultiSelection)



		try:
			while inc < len(self.cacheNameListe):

				#type	
				type = QTableWidgetItem(self.geoType[inc])
				self.tableCurrent.setItem(inc,0,type)
				#name
				name = QTableWidgetItem(self.cacheNameListe[inc])
				self.tableCurrent.setItem(inc,1,name)
				#current version
				self.inUseVersion=QComboBox()
				try:
					for ver in self.versionMetaListe[inc]:
						self.inUseVersion.addItem(str(ver))
				except:
					self.inUseVersion.addItem(str(self.currentVerions[inc]).zfill(4))
					pass		
				index = self.inUseVersion.findText(str(self.currentVerions[inc]).zfill(4))
				self.inUseVersion.setCurrentIndex(index)
				self.tableCurrent.setCellWidget(inc,2,self.inUseVersion)
				self.inUseVersion.setProperty("row",inc)
				self.inUseVersion.activated.connect(self.changeVersion)
				#Last version
				try:
					self.last=QTableWidgetItem(self.versionMetaListe[inc][-1])
				except:
					self.last=QTableWidgetItem(str(self.currentVerions[inc]).zfill(4))
				self.tableCurrent.setItem(inc,3,self.last)

				self.openFolder = QPushButton("explorer")
				chemin = QTableWidgetItem("explorer")

				#en lecture
				if self.nodePath[inc].parm("quickPublish").eval() == 1:	
					self.openFolder.setText("quickPublish")
					chemin.setText(("/").join(self.nodePath[inc].parm("path2").eval().split("/")[:-1]))
				#en cache	
				if self.nodePath[inc].parm("quickPublish").eval() == 0:	
					chemin.setText(self.cachePath[inc])
					self.openFolder.setText("cache")
				#en panic
				if os.path.exists(self.cachePath[inc])==False:
					chemin.setText("pas de cache pas de chocolat")
					self.openFolder.setText("en panic")

				self.tableCurrent.setItem(inc,5,chemin)		
				self.openFolder.setProperty("row",inc)
				self.tableCurrent.setCellWidget(inc,4,self.openFolder)
				self.openFolder.clicked.connect(self.explorer)

				try:
					if str(self.currentVerions[inc]).zfill(4) != self.versionMetaListe[inc][-1]:
						self.tableCurrent.selectRow(inc)
				except:
					pass

				#chemin
				#increment
				inc+=1
		except:
			pass	
		self.tableCurrent.setSelectionMode(QAbstractItemView.ExtendedSelection)	

	def changeVersion(self,row):
		#colonne=self.sender().currentRow()

		print "prout"
		rowSend = self.sender().property("row")
		if rowSend == None :
			ligne=row
		else :
			ligne=rowSend	  
		cacheNode=self.tableCurrent.item(ligne,1).text()
		
		version=self.tableCurrent.cellWidget(ligne,2).currentText()#get newVersion
		match = nodesearch.Name(cacheNode,exact=True)
		net = hou.node("/obj/")

		for node in match.nodes(net,recursive =True):

			if node.parm("lecture").eval() == 1:
				print "lecture"
				try:
					node.parm("version2").set(version)
					node.parm("version2").pressButton()
				except:
					pass
			else: 
				try:
					node.parm("version").set(version)
					node.parm("version").pressButton()
				except:
					pass

	def updateFoncBeta(self):

		rowCount = self.tableCurrent.model().rowCount()
		
		for row in range(rowCount):
			
			combo = self.tableCurrent.cellWidget(row,2)
			lastIndex= combo.count() -1
			combo.setCurrentIndex(lastIndex)
			print "row"
			print row
			self.changeVersion(row)

			

	def rrenderSelect(self):
		selectList = self.tableCurrent.selectedItems()
		net = hou.node("/obj/")

		for i in selectList:
			i=i.text()
			matchType = nodesearch.NodeType("CG::renderGeo*")
			matchName = nodesearch.Name(i,exact= True)
			matchSelect = nodesearch.Group([matchType,matchName])
			for node in matchSelect.nodes(net,recursive =True):
				print ("rrender pour : " +i)
				node.parm("pushtorrender").pressButton()


	def explorer(self):
		colonne=self.sender().property("row")
		hipFile=self.tableCurrent.item(colonne,5)
		path = hipFile.text()
		if platform.system() == "Windows":
			os.startfile(os.path.normpath(path))
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path])
		else:
			subprocess.Popen(["xdg-open", path])

#BUTTON CONNECT
	def button(self):
		#part I
		self.filterKeyCurrent.returnPressed.connect(self.fileCacheLister)
		self.refreshBoutonCurrent.clicked.connect(self.fileCacheLister)
		self.update.clicked.connect(self.updateFoncBeta)
		self.rrender.clicked.connect(self.rrenderSelect)
		self.quickPublish.stateChanged.connect(self.fileCacheLister)
		#part II
		self.initToShot.clicked	.connect(self.setdefault)
		self.projectName.activated.connect(self.menuShot)
		self.projectName.activated.connect(self.menuEffet)
		self.shotName.activated.connect(self.menuEffet)
		self.userName.activated.connect(self.menuEffet)
		#part II browser
		self.effetName.activated.connect(self.cacheBrowserF)
		self.refreshBouton.clicked.connect(self.cacheBrowserF)
		self.quickPublishPartTwo.stateChanged.connect(self.cacheBrowserF)
		self.loadButton.clicked.connect(self.loadSelect)
		





