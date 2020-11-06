#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#    return yProjectManager.yProjectManagerClass()
#from PySide2 import  QtGui, QtCore 
import yFonction
reload(yFonction)
from yFonction import *

print "hello from yProjet"

class yProjectManagerClass(QWidget): 

	def __init__(self):
		super (yProjectManagerClass,self).__init__()
		#variables de projet
		self.proj=projetHOME
		self.pipe=yDictPipe.keys()
		self.user=yUserList
		#les widgets
		self.racine=QComboBox()
		for i in self.pipe:
			self.racine.addItem(i)

		self.racine.setCurrentText(quelPipe())	




		self.roots=QLineEdit(self.proj)
		self.projectName=QComboBox()

		self.shotName=QComboBox()
		self.shotName.addItem("SHOT")
		self.shotName.hide()
		self.userName=QComboBox()
		self.userName.hide()
		for i in self.user:
			self.userName.addItem(i)
		self.filterKey=QLineEdit()
		self.filterKey.setPlaceholderText('search')
		self.refreshBouton=QPushButton("refresh")

		self.saveInc=QPushButton("SAVE")
		self.saveInc.hide()
		self.new=QPushButton("NEW")
		self.new.hide()
	    #le layout
		self.mainLayout=QGridLayout()
		#table
		self.table = QTableWidget()
		self.table.setColumnCount(5)
		self.table.horizontalHeader().setStretchLastSection(1)
		self.table.setColumnWidth(0,100)
		self.table.setColumnWidth(1,60)
		self.table.setColumnWidth(2,145)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setHorizontalHeaderLabels(["effet","version","date","explorer","chemin"]) 
		#add widget to layout
		self.mainLayout.addWidget(self.racine,0,0,1,1)
		#self.mainLayout.addWidget(self.roots,1,0,1,4)
		#self.mainLayout.addWidget(self.filterKey,2,0,1,3)
		self.mainLayout.addWidget(self.projectName,0,1,1,1)

		self.mainLayout.addWidget(self.refreshBouton,2,3,1,1)
		self.mainLayout.addWidget(self.table,3,0,1,4)
		
		self.mainLayout.addWidget(self.shotName,0,2,1,1)
		self.mainLayout.addWidget(self.userName,0,3,1,1)

		self.mainLayout.addWidget(self.new,0,2,1,1)
		self.mainLayout.addWidget(self.saveInc,0,3,1,1)

		self.setLayout(self.mainLayout)
		#fonction lancee au demarage
		self.initRacine()
		self.parseXml()
		self.chooseInterface()
		self.buttonConnect()
		self.projectNameMenu()
 



	def chooseInterface(self):
		if self.racine.currentText() == "HOME":
			self.HOME()
		elif self.racine.currentText() == "CGEV":
			self.cgev()	

	def initRacine(self):
		temp = yDictPipe[self.racine.currentText()]
		self.rootPath = temp[2]
			
	def openScene(self,hipName):
		colonne=self.table.currentRow()
		hipFile=self.table.item(colonne,4)
		#open hipFile
		hou.hipFile.load(hipFile.text())
		
	def changeVersion(self):
		#colonne=self.sender().currentRow()
		colonne=self.sender().property("row")

		hipFile=self.table.item(colonne,4)
		
		version=self.table.cellWidget(colonne,1)#get newVersion

		chaine_liste = hipFile.text().split(".")
		oldVersion=chaine_liste[-2][-3:]
		newVersion = hipFile.text().replace(oldVersion,version.currentText().zfill(3))	

		itemVersion= QTableWidgetItem(newVersion)
		self.table.setItem(colonne,4,itemVersion)
		
	def hipNameFromList(self,hipName):
		self.hipFileFromList=hipName.data()  

	def openSceneAndApplyScript(self):
		myScriptToWrite=self.textScript.toPlainText()
		applyScriptPath=os.getcwd() + "/applyScript.py"
		writeMyScript = open(applyScriptPath, 'w')
		writeMyScript.write(myScriptToWrite)
		reload (applyScript)
		applyScript.temp()

		
		
	def clearListes(self):
		#create and clear all List
		self.projectList=[]
		del self.projectList[:]
		self.tempList = []
		del self.tempList[:]
		self.sortList= []
		del self.sortList[:]
		self.listeFlitre=[]
		del self.listeFlitre[:]

		#self.listWidget.clear()

	def clearMenuProjet(self):
		self.projectName.clear()
		self.shotName.clear()

	def projectNameMenu(self):
		try:
			self.menuProjet()
		except:
			pass	
		
	def parseXml(self):
		temp = yDictPipe[self.racine.currentText()]
		xmlPath = temp[3]
		self.tree = etree.parse(xmlPath)
		self.tronc = self.tree.getroot()
		
	def menuProjet(self):
		self.projectName.clear()
		self.projectList=[]
		del self.projectList[:]
		self.projectName.addItem("PROJET")
		#recupperrrer liste Projet
		for i in self.tronc:
			self.projectList.append(i.attrib["name"])
		#trie la lise des dossier a la racine	
		self.projectList=sorted(self.projectList)
		#ajouter les dossiers dans le menu
		for i in self.projectList:
			self.projectName.addItem(i)
		#projet courant
		projet = os.getenv("PROJECT")
		index = self.projectName.findText(projet)
		self.projectName.setCurrentIndex(index)
		#user courant
		user = os.getenv("user")
		index = self.userName.findText(user)
		self.userName.setCurrentIndex(index)
		#lancer menuShot
		self.menuShot()	

	def menuShot(self):
		self.shotList=[]
		del self.shotList[:]
		self.shotName.clear()
		#init shot
		projetSelect=self.projectName.currentText()
		self.shotName.addItem("SHOT")
		#recup emplacement de projet dans xml
		xprojet  = self.tree.xpath("/projetTree/projet[@name='%s']" %projetSelect)
		for i in xprojet:
			for sub in i:
				#print sub.attrib
				self.shotList.append(sub.attrib["shot"])
		shotSorted= sorted(self.shotList)
		cleanList = []
		for i in shotSorted:
			if i not in cleanList:
				cleanList.append(i)
		shotSorted = cleanList		
		#ajoute shot dans menu shot
		for i in shotSorted:
				self.shotName.addItem(i)
		print self.shotName.item()

	def listSort(self):
		#sortList by alphabetical order
		self.sortList= sorted(self.tempList)
		# systeme de filtres par mot
		selectionFilter=self.filterKey.text()
		# test if there is a key word to filter the list with
		if len(selectionFilter) == 0:
			self.listeFlitre=self.sortList
		else :
			for listElement in self.sortList:
				if selectionFilter in listElement:
					self.listeFlitre.append(listElement)
		#list sorted

	def saveIncFonc(self):
		hou.hipFile.saveAndIncrementFileName() 	

	def newFileFonc(self):
		if self.projectName.currentText()=="PROJET":
			newProjet= hou.ui.readInput("nom du projet? ") [1]
			if not os.path.exists(self.roots.text()+newProjet):
				os.makedirs(self.roots.text()+newProjet)
			newFile= hou.ui.readInput("nom de la scene? ") [1]
			hou.hipFile.clear()
			hou.hipFile.save(self.roots.text()+newProjet+"/"+newFile+"_v000.hiplc", True)
			hou.hipFile.load(self.roots.text()+newProjet+"/"+newFile+"_v000.hiplc")
			self.projectNameMenu()				
			index= self.projectName.findText(newProjet)
			self.projectName.setCurrentIndex(index)
		else :
			newFile= hou.ui.readInput("nom de la scene? ") [1]
			hou.hipFile.clear()
			currentProjet=self.projectName.currentText()
			if not os.path.exists(self.roots.text()+currentProjet+"/"+newFile+"_v000.hiplc"):
				hou.hipFile.save(self.roots.text()+currentProjet+"/"+newFile+"_v000.hiplc", True)
				hou.hipFile.load(self.roots.text()+currentProjet+"/"+newFile+"_v000.hiplc")


		self.chooseInterface()

	def HOME(self):
		self.shotName.hide()
		self.userName.hide()
		self.saveInc.show()
		self.new.show()
		#reset roots
		self.roots.clear()
		self.roots.insert(self.rootPath)
		self.proj=self.roots.text()
		#clearListes
		self.clearListes()
		#recuper le dossier selectionne
		projetSelect=self.projectName.currentText()
		#filter par projet
		if projetSelect=="PROJET":
			pass
		else:
			for file in os.listdir(self.proj+projetSelect):
				if file.endswith('.hip') or file.endswith('.hiplc') or file.endswith('.hipnc') :
					hipPath = self.proj+projetSelect+"/"+file
					self.tempList.append(hipPath)
		
		#build liste effet sans doublons
		myEffet=[]
		for i in self.tempList:
			myEffet.append(i.split("_")[-2].split("/")[-1])
		myEffet=list(set(myEffet))
		#creer une meta liste , contient un liste par effet
		newTempList	=[]	
		i=0	
		try:
			while i < len(myEffet):
				tempEffet=[]
				for l in self.tempList:
					if str(myEffet[i]) in l:
						tempEffet.append(l)
				newTempList.append(sorted(tempEffet))
				i+=1
		except:
			pass
		del self.tempList[:]	
		#garde la derniere verion 
		i=0	
		try:	
			while i<len(newTempList):
				self.tempList.append(newTempList[i][-1])
				i+=1
		except:
			pass
		#trie la liste			
		self.listSort()
		#cree le tableau
		inc=0
		self.table.setRowCount(len(self.listeFlitre))
		
		for hipPathSorted in self.listeFlitre:
			#nam
			name=QTableWidgetItem(hipPathSorted.split("_")[-2].split("/")[-1])
			self.namefichier= QTableWidgetItem(hipPathSorted)
			self.table.setItem(inc,0,name)
			#version qcombo
			self.version=QComboBox()
			versionInt=hipPathSorted.split("_")[-1].split(".")[-2][1:]

			for ver in range(0,int(versionInt)+1):
				self.version.addItem(str(ver))
			self.version.setCurrentIndex(int(versionInt))

			self.table.setCellWidget(inc,1,self.version)
			self.projectName.activated.connect(self.chooseInterface)
			self.version.setProperty("row",inc)
			self.version.activated.connect(self.changeVersion)
			#modified time
			myTime=time.ctime(os.path.getmtime(hipPathSorted))
			timeItem=QTableWidgetItem(myTime)
			self.table.setItem(inc,2,timeItem)
			#open folder
			self.openFolder=QPushButton("explorer")
			self.openFolder.setProperty("row",inc)
			self.table.setCellWidget(inc,3,self.openFolder)
			self.openFolder.clicked.connect(self.explorer)

			#chemin
			self.table.setItem(inc,4,self.namefichier)
			inc+=1

	def explorer(self):
		colonne=self.sender().property("row")
		hipFile=self.table.item(colonne,4)
		#open hipFile
		path = hipFile.text()
 		path = path.split("/")[:-1]
 		path = "/".join(path)
		print "path "
		print path
		if platform.system() == "Windows":
			os.startfile(os.path.normpath(path))
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path])
		else:
			subprocess.Popen(["xdg-open", path])

	def cgev(self):
		self.shotName.show()
		self.userName.show()
		self.saveInc.hide()
		self.new.hide()
		#clearListes
		self.clearListes()
		#recuper le projet selectionne
		projetSelect=self.projectName.currentText()
		#recupere le shot selectionne
		shotSelect=self.shotName.currentText()
		#user
		if self.userName.currentText()== "USER":
			xInfo  = self.tree.xpath("/projetTree/projet[@name='%s']/shot[@shot='%s']" %(projetSelect,shotSelect))
		else :
			userSelect=self.userName.currentText()
			xInfo  = self.tree.xpath("/projetTree/projet[@name='%s']/shot[@shot='%s'][@user='%s']" %(projetSelect,shotSelect,userSelect))
		# fabrication du tableau
		inc=0
		self.table.setRowCount(len(xInfo))
		#boucle dans les hip trouve
		for i in xInfo:
			#nom
			name=QTableWidgetItem(i.attrib["effet"].split("_")[-2])
			self.table.setItem(inc,0,name)
						#version qcombo
			self.version=QComboBox()
			versionInt=i.attrib["version"]
			for ver in range(1,int(versionInt)+1):
				self.version.addItem(str(ver))
			self.version.setCurrentIndex(self.version.count()-1)	
			self.version.setCurrentIndex(self.version.count()-1)	
			self.table.setCellWidget(inc,1,self.version)
			self.projectName.activated.connect(self.chooseInterface)
			self.version.setProperty("row",inc)
			self.version.activated.connect(self.changeVersion)
			#modified time
			timeItem=QTableWidgetItem(i.attrib["time"])
			self.table.setItem(inc,2,timeItem)
			#open folder
			self.openFolder=QPushButton("explorer")
			self.openFolder.setProperty("row",inc)
			self.table.setCellWidget(inc,3,self.openFolder)
			self.openFolder.clicked.connect(self.explorer)	
			self.namefichier= QTableWidgetItem(i.attrib["fullpath"])
			self.table.setItem(inc,4,self.namefichier)
			#incrementation des lignes
			inc+=1

	def buttonConnect(self):
		self.racine.activated.connect(self.initRacine)
		self.refreshBouton.clicked.connect(self.chooseInterface)
		#self.filterKey.returnPressed.connect(self.chooseInterface)
		self.table.doubleClicked.connect(self.openScene)
		self.projectName.activated.connect(self.menuShot)
		self.projectName.activated.connect(self.chooseInterface)
		self.shotName.activated.connect(self.chooseInterface)
		self.userName.activated.connect(self.chooseInterface)
		self.racine.activated.connect(self.clearMenuProjet)
		self.racine.activated.connect(self.chooseInterface)
		self.racine.activated.connect(self.menuProjet)
		self.saveInc.clicked.connect(self.saveIncFonc)
		self.saveInc.clicked.connect(self.chooseInterface)
		self.new.clicked.connect(self.newFileFonc)