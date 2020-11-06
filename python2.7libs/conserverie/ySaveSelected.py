#install in python interface
#import yProjectManager
#reload(yProjectManager)

#def createInterface():
#    return yProjectManager.yProjectManagerClass()
import yFonction
reload(yFonction)
from yFonction import *

print "hello from ySave"

class ySaveSelected(QWidget): 

	def __init__(self):

		super (ySaveSelected,self).__init__()

		#button		
		self.saveButton=QPushButton("save selected")
		self.refresh=QPushButton("refresh")
		self.delete=QPushButton("delete")
		#treeView
		self.tree = QTreeView()
		#listView
		self.list = QListView()
		#check box
		self.checkBox = QCheckBox("sauver ton beau setup dans hBase ?",self)
		self.checkBox.setStyleSheet('color: rgb(153,204,255)')
		#menu deroulant
		self.type=yType
		#les widgets
		self.choisirType=QComboBox()
		for i in self.type:
			self.choisirType.addItem(i)
		self.choisirType.hide()
		# roots path
		self.open= QPushButton("open")

		self.racine=QComboBox()
		self.choisirRoots=yListePipe
		for i in self.choisirRoots:
			self.racine.addItem(i)
		self.racine.setCurrentText(quelPipe())	

	    #le layout
		self.mainLayout=QGridLayout()
		self.mainLayout.addWidget(self.checkBox,0,0,1,1)
		self.mainLayout.addWidget(self.choisirType,0,2,1,2)
		self.mainLayout.addWidget(self.racine,1,0,1,1)		
		self.mainLayout.addWidget(self.saveButton,1,1,1,1)
		self.mainLayout.addWidget(self.refresh,1,2,1,1)
		self.mainLayout.addWidget(self.delete,1,3,1,1)
		self.mainLayout.addWidget(self.tree,2,0,1,4)
		self.mainLayout.addWidget(self.open,3,0,1,1)


		#self.mainLayout.addWidget(self.list,1,1,1,3)

		#init fonction
		self.setLayout(self.mainLayout)
		self.buttonConnect()
		self.initRacine()

	

	def initRacine(self):
		temp = yDictPipe[self.racine.currentText()]
		self.rootPath = temp[1]
		
		self.createModel()	

	def saveSelected(self):
	    # selection
	    selection=hou.selectedItems()

	    if len(selection)==0:
	        hou.ui.displayMessage("empty selection")
	        return
	    # user filename
	    userfilename = hou.ui.readInput("filename",buttons=("cancel","ok"),default_choice=1)
	    #userfilename = hou.ui.readMultiInput("filename",("filename","send to (optional)"," type"),buttons=("cancel","ok"),default_choice=1)
	    if userfilename[0] == 0:
	        return

	    user=os.getenv("user")
	    if user == None:
	    	user="jm"
	    else :
	    	user=user[:2]	

	    project=yProject
	    print project
	    if project == None:
	        project=""
	        self.checkBox.setChecked(True)


	    #print user
	    parent = selection[0].parent()
	    nodetype = parent.type().name().upper()
		
	    # filepath check
	    #filepath = self.rootpath +"/" + user + "/" + project + "/Hkeep/" + nodetype
	    if self.checkBox.isChecked():
	    	filepath = self.rootPath +"/" + "hBase" + "/" +self.choisirType.currentText()
	    else:
	    	filepath = self.rootPath +"/" + project
			
		print filepath	
	    
	    try:
	        if os.path.isdir(filepath)==0:
	            os.makedirs(filepath)
	    except:
	        try :
	            hou.ui.displayMessage("failed to create dir")
	        except:
	            print "failed display message"
	        print "failed to create dir"
	        return

	    # bdd filename
	    filename = nodetype + "_"+''.join(userfilename[1].split())

	    # save file
	    parent.saveItemsToFile(selection,filepath + "/" + filename + "_" + user +".cmd")

	    self.createModel()

	def openExpl(self):
		yOpen(self.rootPath)

	def buttonConnect(self):
		self.racine.activated.connect(self.initRacine)
		self.saveButton.clicked.connect(self.saveSelected)
		self.tree.clicked.connect(self.treeClicked)
		self.tree.doubleClicked.connect(self.treeDoubleClicked)
		self.list.doubleClicked.connect(self.treeDoubleClicked)
		self.refresh.clicked.connect(self.createModel)
		self.delete.clicked.connect(self.moveToTrash)
		self.checkBox.stateChanged.connect(self.hideMenu)
		self.open.clicked.connect(self.openExpl)

	def hideMenu(self):
		if self.checkBox.isChecked():
			self.choisirType.show()
		else:
			self.choisirType.hide()


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

	def treeClicked(self,index):
		if self.model.isDir(index):
			self.list.setRootIndex(index)
		else:
			self.list.setRootIndex(index.parent())

		self.filePathOne = self.model.filePath(index)
		self.tempIndex = index

	def treeDoubleClicked (self,index):
		if self.model.isDir(index):
			pass
		else:
			try :
				#htab = hou.ui.paneTabUnderCursor()
				htab = hou.ui.curDesktop().paneTabUnderCursor()
				parent = htab.pwd()
				nodetype = parent.type().name().upper()
			except:
				hou.ui.displayMessage("keep mouse cursor over the paneTab")
				return

			self.filePath = self.model.filePath(index)

			parent.loadItemsFromFile(self.filePath)

	def moveToTrash(self):
		if self.model.isDir(self.tempIndex):
			pass
		else:
			self.filePathOne = self.model.filePath(self.tempIndex)	
			oldPath = self.filePathOne

			splitPath = oldPath.split("/")[-2:]


			trashPath = self.rootPath + "/xxx_trash"
	 		newPath = trashPath+"/"+"/".join(splitPath)

	 		trashCreate = newPath.split("/")[:-1]
	 		trashCreate = "/".join(trashCreate)+"/"

	 		if os.path.exists(trashCreate)==False:
	 			os.makedirs(trashCreate)

			shutil.move(oldPath,trashCreate)

		self.createModel()

	def showDialog(self):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Message box pop up window")
		msgBox.setWindowTitle("QMessageBox Example")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)