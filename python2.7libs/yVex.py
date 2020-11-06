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
		self.boutDeCode= QComboBox()
		self.grosCode= QComboBox()
		#ligne deux
		self.boutDeCodeAdd= QPushButton("saveBoutdeCode")
		self.grosCodeAdd= QPushButton("saveGrosCode")
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


		#layout
		self.mainLayout=QGridLayout()
		#layout	ligne un	
		self.mainLayout.addWidget(self.boutDeCode,0,0,1,2)
		self.mainLayout.addWidget(self.grosCode,0,2,1,2)
		#layout ligne deux
		self.mainLayout.addWidget(self.boutDeCodeAdd,1,0,1,2)
		self.mainLayout.addWidget(self.grosCodeAdd,1,2,1,2)
		#layout ligne trois
		self.mainLayout.addWidget(self.codeEdit,2,0,1,4)	
		#layout ligne quatre 
		self.mainLayout.addWidget(self.refresh,3,0,1,1)
		self.mainLayout.addWidget(self.open,3,1,1,1)
		#layout ligne cinq 
		self.mainLayout.addWidget(self.racine,4,0,1,1)
		#init fonction
		self.setLayout(self.mainLayout)

		self.variable()

		self.buttonConnect()
		

	def variable(self):
		temp = yDictPipe[self.racine.currentText()]
		self.rootPath = temp[0]
		self.vexList = ["boutDeCode","grosCode"]

		if os.path.exists(self.rootPath):
			self.chargerLesScripts()

	def openExpl(self):
		yOpen(self.rootPath)

	def chargerLesScripts(self):

		self.boutDeCode.clear()
		self.grosCode.clear()	

		self.listeBoutDeCode=os.listdir(self.rootPath+"/"+self.vexList[0])
		for i in self.listeBoutDeCode:
			self.boutDeCode.addItem(i[:-4])

		self.listeGrosCode=os.listdir(self.rootPath+"/"+self.vexList[1])
		for i in self.listeGrosCode:
			self.grosCode.addItem(i[:-4])

	def saveCode(self,listIndex):
		vexCode=self.codeEdit.toPlainText()

		name = hou.ui.readInput("filename",buttons=("cancel","ok"),default_choice=1)
		if name[0] == 0:
			return

		fichier = open(self.rootPath+"/"+self.vexList[listIndex]+"/"+name[1]+".txt", "a")
		fichier.write(vexCode)
		fichier.close()

		self.chargerLesScripts()

	def loadCode(self,listIndex,name):

		fichier = open(self.rootPath+"/"+self.vexList[listIndex]+"/"+name+".txt", "r")
		snippet = fichier.read()
		fichier.close()
		nodes = hou.selectedNodes()
		
		for i in nodes:
			currentSnip = i.parm("snippet").eval()
			i.setParms({"snippet":currentSnip+"\n"+snippet})	

	def saveBoutDeCode(self):
		self.saveCode(0)

	def loadBoutDeCode(self):
		self.loadCode(0,self.boutDeCode.currentText())
				
	def saveGrosCode(self):
		self.saveCode(1)

	def loadGrosCode(self):
		self.loadCode(1,self.grosCode.currentText())

	def buttonConnect(self):
		#boutDeCode
		self.boutDeCodeAdd.clicked.connect(self.saveBoutDeCode)
		self.boutDeCode.activated.connect(self.loadBoutDeCode)
		#grosCode
		self.grosCodeAdd.clicked.connect(self.saveGrosCode)
		self.grosCode.activated.connect(self.loadGrosCode)
		self.refresh.clicked.connect(self.chargerLesScripts)
		self.open.clicked.connect(self.openExpl)
		self.racine.activated.connect(self.variable)
		self.racine.activated.connect(self.chargerLesScripts)

