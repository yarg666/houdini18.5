#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#    return yProjectManager.yProjectManagerClass()


import yFonction
reload(yFonction)
from yFonction import *

print "hello from yVex"

class yVex(QWidget): 

	def __init__(self):

		super (yVex,self).__init__()
		#ligne un	
		self.saveCodeIn= QPushButton("saveCodeIn->")
		self.choisirB=QComboBox()
		for i in yChoisirVex:
			self.choisirB.addItem(i)
		#ligne deux
		#ligne trois 
		self.codeEdit= QTextEdit()
		#ligneQuatre
		self.refresh= QPushButton("refresh")
		self.open= QPushButton("open")
		#ligneCinq
		self.racine=QComboBox()
		self.choisirRoots=yListePipe
		for i in self.choisirRoots:
			self.racine.addItem(i)
		self.racine.setCurrentText(quelPipe())		
		#tree view
		self.tree = QTreeView()
		#listView
		self.list = QListView()
		#layout
		self.mainLayout=QGridLayout()
		#layout	ligne un	
		self.mainLayout.addWidget(self.saveCodeIn,0,0,1,2)
		self.mainLayout.addWidget(self.choisirB,0,2,1,2)
		#layout ligne deux
		#layout ligne trois
		self.mainLayout.addWidget(self.tree,2,0,1,2)
		self.mainLayout.addWidget(self.codeEdit,2,2,1,2)	
		#layout ligne quatre 
		self.mainLayout.addWidget(self.refresh,3,0,1,1)
		self.mainLayout.addWidget(self.open,3,1,1,1)
		#layout ligne cinq 
		self.mainLayout.addWidget(self.racine,4,0,1,1)
		#init fonction
		self.setLayout(self.mainLayout)
		self.variable()
		self.buttonConnect()
		self.initRacine()
	
	def initRacine(self):
		temp = yDictPipe[self.racine.currentText()]
		self.rootPath = temp[0]
		self.createModel()		

	def createModel(self):
		print("create Model")
		self.model = QFileSystemModel()
		self.model.setRootPath(self.rootPath)
		self.tree.setModel(self.model)
		self.tree.setColumnHidden(1, 1)
		self.tree.setColumnHidden(2, 1)
		self.tree.setColumnHidden(3, 1)
		self.list.setModel(self.model)
		self.list.setRootIndex(self.model.index(self.rootPath))
		self.tree.setRootIndex(self.model.index(self.rootPath))	

	def variable(self):
		temp = yDictPipe[self.racine.currentText()]
		self.rootPath = temp[0]

	def openExpl(self):
		yOpen(self.rootPath)

	def saveCodeInF(self):
		print "savecodeIn"
		vexCode=self.codeEdit.toPlainText()
		#menu name
		filepath = self.rootPath + "/" +self.choisirB.currentText()
		listName = os.listdir(filepath)
		self.newList=[]
		for i in listName:
			self.newList.append(i.split(".")[0])
		self.cancel = 0
		self.userfilename = QDialog()
		self.grid = QGridLayout()
		self.userfilename.setLayout(self.grid)
		self.nom = QLabel("choisir nom:",self.userfilename)
		self.grid.addWidget(self.nom,1,0)
		self.nomArchive = QLineEdit(self.userfilename)
		self.grid.addWidget(self.nomArchive,1,1)
		self.listNom = QComboBox()
		self.listNom.addItem("ecrase un setup")
		for i in self.newList:
			self.listNom.addItem(i)
		self.grid.addWidget(self.listNom,2,0,1,2)
		self.okButton = QPushButton("ok")
		self.grid.addWidget(self.okButton,3,0,1,1)
		self.cancelB = QPushButton("cancel")
		self.grid.addWidget(self.cancelB,3,1,1,1)
		self.connectPopUp()
		x = self.userfilename.exec_()
		fileName = self.nomArchive.text()
		if self.cancel == 1:
			return
		if len(fileName) == 0:
			return	
		#choisir cat
		cat = self.choisirB.currentText()
		fichier = open(self.rootPath+"/"+cat+"/"+fileName+".txt", "a")
		fichier.truncate(0)
		fichier.write(vexCode)
		fichier.close()
		self.createModel()


	def nomFile(self):
		self.nomArchive.setText(self.listNom.currentText())

	def close(self):
		self.userfilename.close()

	def cancelF(self):
		self.cancel = 1
		self.userfilename.close()	

	def connectPopUp(self):
		self.listNom.activated.connect(self.nomFile)
		self.okButton.clicked.connect(self.close)
		self.cancelB.clicked.connect(self.cancelF)


	def loadF(self,index):
		filePath = self.model.filePath(index)
		fichier = open(filePath, "r")
		snippet = fichier.read()
		fichier.close()
		nodes = hou.selectedNodes()
		if len(nodes) == 0:
			hou.ui.displayMessage("selectionne un wrangle !")

		for i in nodes:
			currentSnip = i.parm("snippet").eval()
			i.setParms({"snippet":currentSnip+"\n"+snippet})

	def afficheTxt(self,index):
		filePath = self.model.filePath(index)
		fichier = open(filePath, "r")
		snippet = fichier.read()
		fichier.close()
		print snippet
		self.codeEdit.setText(snippet)


	def buttonConnect(self):
		#save
		self.saveCodeIn.clicked.connect(self.saveCodeInF)
		#load
		self.tree.doubleClicked.connect(self.loadF)
		self.list.doubleClicked.connect(self.loadF)
		#txt
		self.tree.clicked.connect(self.afficheTxt)
		self.list.clicked.connect(self.afficheTxt)
		#autre
		self.refresh.clicked.connect(self.createModel)
		self.open.clicked.connect(self.openExpl)
		self.racine.activated.connect(self.variable)


