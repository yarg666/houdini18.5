#
# houdini cache geometry tools
# Author:  Royal Render, Cgev, fx boussard , 
# Version v 3.00.0, cleanup and add xml database
# date: 2019/05/17
# Version v 4.00.0, cleanup and add xml database, single frame, xml
# date: 2019/05/20
# Version v 5.00.0, image path for cgmantra, colors, jpeg, xml path tag, change xmlversion
# date: 2019/05/28
# Version v 6.00.0, clean xmlpath
# date: 2019/06/03
# Version v 10.00.0, add cop, renderA7 class got now outputpath and f1 f2
# date: 2019/08/07

import sys
import os
import hou
import math
import datetime,time,re,platform
import getpass
import shutil

from lxml import etree

from cgev.common import	toBatch
from cgev.common import	log
from cgev.houdini import tools
from cgev.pipeline.appconnector import connectorScript
from cgev.common import environment

reload(toBatch)
reload(tools)

from cgev.pipeline.appconnector import connectortools

from subprocess import Popen

from cgev.common import envvars
from cgev.common import files
from cgev.common import newconfig
from cgev.common import helpers
from cgev.common import log
from cgev.common import texts
from cgev.common import decoder
from cgev.common import sealer
from cgev.common import resourceslocation

rrRoot = os.environ[envvars.RR_ROOT].replace('\\', '/')
submitter = rrRoot + "/bin/win/rrSubmitterconsole.exe"
submitterUI = rrRoot + "/bin/win/rrSubmitter.exe"
try:
	houdiniversion = os.environ["_HIP_SAVEVERSION"].split(".")
except:
	houdiniversion = os.environ["HOUDINI_VERSION"].split(".")



def checkPath():

	currentNode = hou.pwd()
	cachePath = currentNode.parm("path").eval()
	# check if agree with dependency

	if os.path.exists(cachePath):
		files = next(os.walk(cachePath))[2]
		if len(files)!=0: 
			checkCache = hou.ui.displayMessage("le cache existe deja",buttons=('annule','ecrase',), default_choice=0)
			if checkCache == 0:
				print "rendu annule"
				return 0
			else:
				print "rendu ecrase"
				return 1


def	fxRenderGeo(nodeA7=None):
	'''
	nodeA7 = renderGeo or cgmantra. process node to feed fxBatchHoudiniGeo()
	'''

	testA = checkPath()

	if testA==0:
		return


	if	nodeA7 == None:
		print "node	not	found"
		return

	selectedNodes=[]
	PreID=None
	WaitForPreID = False
	rendera7=RenderA7()
	
	##################### itself
	try:
		nodetypename = nodeA7.type().nameComponents()
		if	nodetypename[1] == "CG" and nodetypename[2]	== "renderGeo":
			selectedNodes=setRenderA7node(nodeA7,selectedNodes)
			rrui=nodeA7.parm("rrui").eval()
		elif nodetypename[1] == "CG" and nodetypename[2] == "cgmantra":
			cam = validCamera()
			if cam == 0:
				return
			selectedNodes=setRenderA7node(nodeA7,selectedNodes)
			rrui=nodeA7.parm("rrui").eval()
			nodeA7.parm('soho_outputmode').set(1)
			
		elif nodetypename[1] == "CG" and nodetypename[2] == "rendermaps":
			selectedNodes=setRenderA7node(nodeA7,selectedNodes)
			rrui=nodeA7.parm("rrui").eval()
			nodeA7.parm('soho_outputmode').set(1)
		else:
			print "not a CG::renderGeo node"
			return
	except:
		print	"issue with node type"
		return
	
	#################  input 2 check for dependencies
	try :
		in2 = nodeA7.inputs()[1]
		# check if agree with dependency
		okdep = hou.ui.displayMessage("render will proceed with dependency",buttons=('Abort !','No','Ok',), default_choice=2)
		if okdep == 0:
			hou.ui.displayMessage("render canceled")
			return
		in2nodes=[]
		in2nodes=dependencies(nodeA7,in2nodes)
		# in2nodes.reverse()
		if len(in2nodes) > 0:
			if okdep == 2:
				WaitForPreID = True
			for n in in2nodes:
				selectedNodes.append(n)
	except:
		print "no dependencies"
		pass
	
	# print 'WaitForPreID = ' + str(WaitForPreID)
	
	
	#	log.debug3('---------------------	RR	SUBMIT	----------------------------')
	i=0;
	selectedNodes.reverse()
	for	rendera7 in	selectedNodes:
		node=rendera7.renderNode
		type = rendera7.type
		batch=int(rendera7.batch)
		waitForWholeID=rendera7.waitForWholeID
		if WaitForPreID == True:
			PreID = i
			# print "PreID = " + str(PreID)
			i+=1
		sceneFile =	hou.hipFile.path()
		layer = node.path()
		
		outFile	= rendera7.outPath
		
		log.debug("outFile :" + outFile)

		log.debug3(node)
		log.debug3(sceneFile)
		log.debug3(layer)
		log.debug3(outFile)

		try:
			firstFrame = rendera7.f1
			lastFrame = rendera7.f2
		except:
			log.info('not frame settings in	node, using	general	settings')
			firstFrame, lastFrame = hou.playbar.timelineRange()
			firstFrame = str(int(firstFrame))
			lastFrame = str(int(lastFrame))

		frMsg = 'first : {first}, last : {last}'
		log.debug(frMsg.format(first=firstFrame,
								last=lastFrame))

		sceneFileRR = toBatch.rrScenePathGenerator(sceneFile)
		connectorScript.saveScriptCopy(sceneFileRR)
		
		# singleOutPut = ('.#.'	not	in	outFile)
		singleOutPut = rendera7.singleOutPut
		if type == "abc":
			singleOutPut = True
		# print 'rrSubmit singleOutPut', singleOutPut
		
		hip = hou.getenv('HIP')
		renderer = 'geoCGEV'
		if type == "abc":
			renderer='SimCGEV'
			
		if type == "cgifd" or type == "baketexture":
			renderer='createIFD'
			rrRoot = environment.getRoyalRenderRoot()
			RenVer_Arnold = ""
			try:
				import arnold
				RenVer_Arnold = " -customRenVer_Arnold " + AiGetVersionString()
			except:
				pass
				
			# check if in /out
			if node.parent().parent().name() == "out":
				sceneandlayer = sceneFileRR
			else:
				sceneandlayer = sceneFileRR + " -Layer " + layer 
				
			if type == "baketexture":
				sceneandlayer += " DoNotCheckForFrames=0~1"
			
			os.system(rrRoot + "\\win__rrSubmitter.bat " + sceneandlayer + "  "+RenVer_Arnold)
			return
			

		######### BATCH #################
		f1=int(firstFrame)
		f2=int(lastFrame)
		if singleOutPut==True:
			f1=int(hou.frame())
			f2 = f1
		flength=f2-f1
		fend=0
		fstart=0
		inc = math.ceil(flength/batch)
		# print 'n batch: ' + str(batch)
		for n in range(0,batch):
			# if batch>1:
			#	PreID=n
			fstart = f1+inc*n
			fend=max(min(-1+fstart+inc, f2), f1)
			
			if fstart + inc == f2:
				fend=f2
			
			if fend+inc > f2:
				fend=f2

			# print 'batch: ' + str(n+1)
			# print "frameStart: " + str(fstart)
			# print "frameEnd: " + str(fend)
			# print 'inc: ' +str(inc)
			rrbatch = fxBatchHoudiniGeo(sceneFileRR, outFile, int(fstart),
									int(fend), layer, hip,
									preID=PreID, waitForPreID=WaitForPreID,
									sendMailMp4=None, renderer=renderer,
									ui=rrui,
									singleOutPut=singleOutPut,
									numbatch='1',
									waitForWholeID=waitForWholeID)
			time.sleep(10)
			# print "batch: " + str(n)
		

def fxBatchHoudiniGeo(sceneFile, outFile, firstFrame, lastFrame, layer, hip,
                    preID=None, waitForPreID=False, sendMailMp4=False,
                    renderer="default", ui=False,
                    singleOutPut=False,numbatch=1,waitForWholeID=None):
	'''
	push to farm
	'''
	if ui:
		subbmiterToUse = submitterUI
	else:
		subbmiterToUse = submitter

	if not singleOutPut:
		imageExtension = outFile.split('#')[-1]
		ImageFileNameOnly = os.path.basename(outFile).split('#')[0]
		imageFileName = os.path.basename(outFile)
	else:
		imageExtension = '.'+outFile.split('.')[-1]
		if imageExtension == "sc":
			imageExtension="bgeo.sc"
		ImageFileNameOnly = os.path.basename(outFile).split(imageExtension)[0]
		imageFileName = ImageFileNameOnly

	imageDirComplete = os.path.dirname(outFile)

	version = houdiniversion[0] + "." + houdiniversion[1] + houdiniversion[2][0] + houdiniversion[2][1]

	commandLines = [subbmiterToUse,
					' ' + sceneFile,
					" -Software Houdini",
					" -Version " + version,
					" -RequiredLicenses Houdini",
					" -Renderer "+renderer,
					" -SeqStart " + str(firstFrame),
					" -SeqEnd " + str(lastFrame),
					# " -ImageFileName " + str(outFile),
					# " -ImageFileNameOnly "+ImageFileNameOnly,
					#" -ImageDirComplete "+imageDirComplete,
					" -ImageDir "+imageDirComplete,
					" -ImageFilename "+imageFileName,
					" -ImageExtension " + imageExtension,
					" -AutoDeleteEnabled",
					" -ImageSingleOutputFile " + str(singleOutPut),
					" -PreID " + str(preID),
					" -Layer " + layer,
					" -CustomA " + layer,
					" -CustomB " + hip,
					" SequenceDivide= 0~0",
					" DefaultClientGroup=1~128Go",
					# " MaxClientsAtATime=1~1",
					" MaxClientsAtATime=1~"+str(numbatch),
					" CropEXR= 0~0",
					" PPEXRCropchannels = 0~0",
					# " AutoApproveJob = 1~1",

					#" PPSendMailMp4=1~"+str(int(sendMailMp4)),
					]


	if waitForPreID is True:
		commandLines += [" -WaitForPreID "+str(preID -1)]
	if waitForWholeID is not None:
		commandLines += [" -WaitForWholeID "+str(waitForWholeID)]

	command = generateCommand(commandLines)
	log.debug(command)

	p = Popen(command, shell=True)

def generateCommand(listOfStrings):
	'''
	makes a string from a list of strings
	@param listOfStrings: list of strings
	'''
	command = ''

	for element in listOfStrings:
		command += element

	return command
	
def cleanFiles(path,imagename):
	files = os.listdir(path)
	for file in files:
		if imagename in file:
			try:
				os.remove(os.path.join(path, file))
			except OSError:
				print("Error while deleting file")


################################################################################################
#########################################	FX	UTILS	################################
################################################################################################

class RenderA7:
	def __init__(self):
		"""houdini cgev render A7"""
		self.passName=""
		self.renderNode=""
		self.preID=""
		self.waitForID=False
		self.waitForWholeID=None
		self.batch=1
		self.type=None
		self.singleOutPut=False
		# cop changes
		self.f1=None
		self.f2=None
		self.outPath=None
		# xml stuff
		self.version=None
		self.export=None
		self.exportDpt=None
		self.user=None
		self.date=None
		# for good
		self.ext=None

	def setPassName(self,passname):
		self.passName=passname
	def setRenderNode(self,renderNode):
		self.renderNode=renderNode
	def setPreID(self,preID):
		self.preID=preID
	def setWaitForID(self,waitForID):
		self.waitForID=waitForID
	def setWaitForWholeID(self,waitForWholeID):
		self.waitForWholeID=waitForWholeID
	def setBatch(self,batch):
		self.batch=batch
	def setType(self,type):
		self.type=type
	def setSingleOutPut(self,singleOutPut):
		self.singleOutPut=singleOutPut
		
		# cop change
	def setF1(self,f1):
		self.f1=f1
	def setF2(self,f2):
		self.f2=f2
	def setOutPath(self,outpath):
		self.outPath=outpath
		
		# xml stuff
	def setVersion(self,version):
		self.version=version
	def setExport(self,export):
		self.export=export
	def setExportDpt(self,exportDpt):
		self.exportDpt=exportDpt
	def setUser(self,user):
		self.user=user
	def setDate(self,date):
		self.date=date
	def setExt(self,ext):
		self.ext=ext
	
# check dor dependencies
def dependencies(node,listNodes):
	"""
	check node on input 2 to setRenderA7node()
	"""
	rendera7=RenderA7()
	try :
		in2 = node.inputs()[1]
		in2type=in2.type().nameComponents()
		if	in2type[1] == "CG" and in2type[2] == "renderGeo":
			# xml 
			cacheXml(in2)
			cacheXmlCheck(in2)
			# end xml
			listNodes=setRenderA7node(in2,listNodes)
			dependencies(in2,listNodes)
			rrui = 0
			# WaitForPreID = True
		if "merge" == in2type[2]:
			mergein=in2.inputs()
			for i in mergein :
				in2type = i.type().nameComponents()
				if	in2type[1] == "CG" and in2type[2] == "renderGeo":
					listNodes=setRenderA7node(i,listNodes)
					dependencies(i,listNodes)
					rrui = 0
					# WaitForPreID = True
		if "object_merge" == in2type[2]:
			nobj = int(float(in2.parm("numobj").eval()))
			for n in range(1,nobj+1):
				objnum = "objpath"+str((nobj+1)-n)
				mergednode = in2.parm(objnum).evalAsNode()
				mergednodetype = mergednode.type().nameComponents()
				if	mergednodetype[1] == "CG" and mergednodetype[2] == "renderGeo":
					listNodes=setRenderA7node(mergednode,listNodes)
					dependencies(mergednode,listNodes)
					rrui = 0
		
	except:
		# print "no dependencies"
		pass
	return listNodes

# set abc or bgeo node to render
def setRenderA7node(nodeA7,selectedNodes):
	"""
	return a list of a7object ready to render
	"""

	rendera7=RenderA7()
	rendera7.setRenderNode(hou.node( nodeA7.path() + "/render" ))
	rendera7.setType(nodeA7.parm("datatype").eval())
	rendera7.setBatch(nodeA7.parm("numbatch").eval())
	
	rendera7.setF1(nodeA7.parm('f1').evalAsString())
	rendera7.setF2(nodeA7.parm('f2').evalAsString())
	
	if rendera7.type != "cgifd" and rendera7.type != "baketexture":
		#rendera7.setExt(nodeA7.parm('abcbgeoextention').evalAsString())
		rendera7.setExt(nodeA7.parm('extention').evalAsString())
		
	if  rendera7.type == "abc":
		rendera7.setRenderNode(hou.node( nodeA7.path() + "/render_alembic" ))
	if  rendera7.type == "cgifd":
		rendera7.setExt(nodeA7.parm('extention').evalAsString())
		rendera7.setRenderNode(hou.node( nodeA7.path() + "/mantra" ))
	
	if  rendera7.type == "baketexture":
		rendera7.setExt(nodeA7.parm('extention').evalAsString())
		rendera7.setRenderNode(hou.node( nodeA7.path() + "/baketexture" ))
	
	rendera7.setOutPath(tools.getOutFile(rendera7.renderNode))
	
	# single Frame
	trange = nodeA7.parm("trange").eval()

	# cop
	if  rendera7.type == "cop":
		#copnode=hou.node( nodeA7.parm("coppath").eval() )
		#rendera7.setRenderNode(copnode)
		#rendera7.setOutPath(tools.getOutFile(  hou.node(nodeA7.path() + "/render")  ))
		rendera7.setRenderNode(hou.node( nodeA7.path() + "/ropnet/cop" ))
		
	singleOutPut = (trange	== 0)
	rendera7.setSingleOutPut(singleOutPut)
	
	# manual dependency
	try:
		if nodeA7.parm("depenable").eval() == 1:
			depid = nodeA7.parm("dependency").eval()
			if depid is not "":
				rendera7.setWaitForWholeID(depid)
	except:
		pass
	selectedNodes.append(rendera7)
	return selectedNodes

# set the path and filename to	save geometry to disk
def	setoutputpath(A7):
	'''
	A7 : hda cgev render node. Set the A7 with all path and necessary parm to render
	'''
	name = A7.parm("name").eval()
	version = A7.parm("version").eval()
	type = A7.parm("datatype").eval()
	try:
		task = os.environ["task"]
	except:
		task = "task"
	user = getpass.getuser()
	
	
	trange = A7.parm("trange").eval()
	versionstr = "%04d"%version
	mantraversionstr = "%03d"%version
	hipfilepath,hipfilename= os.path.split(hou.hipFile.path())
	
	try:
		assetname = os.environ["assetname"].replace("_"+user,"")
	except:
		assetname = hipfilename.replace(".hip","")
	
	try:
		shot = os.getenv("shot")
		seq = os.getenv("sequence")
		if shot == None :
			shot = "shot"
		if seq == None:
			seq="seq"
		effect = seq + "-" + shot
	except:
		effect = hipfilename.split(".")[0]

	# split directory
	normpath = os.path.normpath(hipfilepath)
	pathitems = normpath.split(os.sep)
	
	rootpath = hipfilepath
	if pathitems[-1].isdigit():
		pathitems.pop(-1)
		rootpath = "//"+reduce(os.path.join,pathitems).replace("\\","/")
		
	#	create path and	filename
	path = rootpath + "/" + type + "/" + str(name) + "/v" + versionstr
	filename = effect + "_" + str(name) + "_v" + versionstr
	mantrafilename = assetname + "_" + str(name) + "_v" + mantraversionstr
	
	A7.parm("path").set(path)
	# set type path, bgeo or alembic
	if	type=="bgeo" or	type=="bgeowrangle" or type=="bgeofloat":
		A7.parm("bgeopath").set(path)
		A7.parm("extention").set("bgeo.sc")
		# A7.parm("abcbgeoextention").set("bgeo.sc")
		A7.parm("cachealembic").set(0)
	if	type=="cop":
		A7.parm("bgeopath").set(path)
		A7.parm("extention").set("exr")
		# A7.parm("abcbgeoextention").set("exr")
		A7.parm("cachealembic").set(0)
		
		try:
			origincopparms = hou.node(A7.parm("coppath").eval()).parms()
		except:
			hou.ui.displayMessage("cop not defined")
			return
			
		for p in origincopparms:
			name = p.name()
			if name != "f1" and name != "f2" and name != "f3" and name != "copoutput":
				if name == "coppath":
					coppath=p.unexpandedString()
					if coppath.split("/")[0] != "":
						coppath = p.path().replace("coppath","")+coppath
					hou.node("./ropnet/cop").parm(name).set(coppath)
				else:
					try:
						hou.node("./ropnet/cop").parm(name).set( p.unexpandedString())
					except:
						hou.node("./ropnet/cop").parm(name).set( p.eval())
		
		
	if	type=="abc":
		A7.parm("abcpath").set(path)
		A7.parm("extention").set("abc")
		# A7.parm("abcbgeoextention").set("abc")
		A7.parm("cachealembic").set(1)
	if	type=="vdb" or type=="vdbwrangle" or type=="vdbfloat":
		A7.parm("bgeopath").set(path)
		A7.parm("extention").set("vdb")
		# A7.parm("abcbgeoextention").set("vdb")
		A7.parm("cachealembic").set(0)
	if	type=="cgifd" or type == "baketexture":
		#picpath = path.replace("cgifd",'render')
		try:
			ext = A7.parm("extention").eval()
		except:
			ext = "exr"
		
		picpath = path.split("houdini")[0] + "houdini/images/" + task + "/" + user + "/" + assetname + "/" + str(name) + "/v" + mantraversionstr
		ifdpath = path.replace("cgifd",'ifds')
		# fullpicpath = picpath + "/" + mantrafilename + ".$F4.exr"
		fullpicpath = picpath + "/" + mantrafilename + ".$F4." + ext
		if type == "baketexture":
			ifdpath = path.replace("baketexture",'ifds')
			fullpicpath = picpath + "/" + mantrafilename + ".%(UDIM)d.$F4." + ext
		fullifdpath = ifdpath + "/" + filename + ".$F4.ifd.sc"
		A7.parm("picturespath").set(picpath)
		A7.parm("ifdspath").set(ifdpath)
		A7.parm("soho_diskfile").set(fullifdpath)
		
		# set Shared temp storage
		A7.parm("vm_tmpsharedstorage").set(ifdpath+"/storage")
		
		
		if type == "cgifd":
			A7.parm("vm_picture").set(fullpicpath)
			
		if type == "baketexture":
			A7.parm("vm_uvoutputpicture1").set(fullpicpath)
			A7.parm("vm_picture").set(fullpicpath.replace(".%(UDIM)d.$F4.",".####."))
		
		
	if type=="maps":
		A7.parm("mappath").set(path)

	# set	filename hda	attrib
	A7.parm("filename").set(filename)
	
	# padding
	if trange == 0:
		A7.parm("padding").set("single")
	else:
		A7.parm("padding").set("$F4")
	
	# xml cache file
	# if type != "cop" and type != "baketexture":
	
	# Bg Camera
	cambackGround()
	
	cacheXmlCheck(A7)
# BackGround Camera
def cambackGround():
	try:
		bg_enable=hou.pwd().parm("background_camera").eval()
		campath = hou.pwd().parm("camera").eval()
		camera=hou.node(campath)
		camera.parm("vm_bgenable").set(bg_enable)
	except:
		pass
		
def validCamera():
	try:
		campath = hou.pwd().parm("camera").eval()
		camera=hou.node(campath)
		type=camera.type().name()
		if type != "cam":
			hou.ui.displayMessage("check for a valid camera")
			return 0
		else:
			return 1
	except:
		hou.ui.displayMessage("check for a valid camera")
		return 0

	
# replace space with underscore
def replacespace(parmname):
	name = hou.pwd().parm(parmname).eval()
	name=name.replace(" ","_")
	hou.pwd().parm(parmname).set(name)


# render button
def pushrenderlocal():

	testA = checkPath()

	if testA==0:
		return

	rendertype=hou.pwd().parm("datatype").eval()
	if rendertype == "bgeo" or rendertype == "vdb":
		hou.node("./render").parm("execute").pressButton()
	if rendertype == "abc":
		hou.node("./render_alembic").parm("execute").pressButton()
	if rendertype == "cop":
		hou.node("./ropnet/cop").parm("execute").pressButton()

# reload button
def reloadgeo():
	rendertype=hou.pwd().parm("datatype").eval()
	if rendertype == "bgeo":
		hou.node("./bgeo").parm("reload").pressButton()
	if rendertype == "abc":
		hou.node("./alembic1").parm("reload").pressButton()
	if rendertype == "vdb":
		hou.node("./bgeo").parm("reload").pressButton()

# check if directory exist and create it if not
def mkdiroutput(path):
	if not os.path.isdir(os.path.expandvars(path)):
		os.makedirs(os.path.expandvars(path))

def openfolder():

	sysname = platform.system()
	try :
		path=hou.pwd().parm("picturespath").eval()
	except:
		rendertype=hou.pwd().parm("datatype").eval()
		if rendertype == "bgeo" or rendertype == "bgeowrangle" or rendertype == "bgeofloat" or rendertype == "cop":
			# path=hou.pwd().parm("bgeopath").eval()
			path=hou.pwd().parm("path").eval()
		if rendertype == "abc":
			# path=hou.pwd().parm("abcpath").eval()
			path=hou.pwd().parm("path").eval()
		if rendertype == "vdb" or rendertype == "vdbwrangle" or rendertype == "vdbfloat":
			# path=hou.pwd().parm("bgeopath").eval()
			path=hou.pwd().parm("path").eval()
		if rendertype == "maps":
			path=hou.pwd().parm("path").eval()

	if sysname=="Windows":
		cmd = "explorer " + os.path.normpath(path)
		#subprocess.Popen(cmd)
		Popen(cmd)
	else :
		hou.ui.displayMessage("to be done for this os system")

# def bgeotoalembic():
	# test=hou.pwd().parm("extention").eval()
	# if test=="abc":
		# test = "bgeo.sc"
	# return test

# reload button
def reloadgeo():
	rendertype=hou.pwd().parm("datatype").eval()
	if rendertype == "bgeo" or rendertype == "vdb":
		hou.node("./reload_cache").parm("reload").pressButton()
	if rendertype == "abc":
		hou.node("./alembic_cache").parm("reload").pressButton()

def padd():
	if hou.pwd().parm('float').eval()==1:
		hou.pwd().parm('padding').set('$FF')
	else:
		hou.pwd().parm('padding').set('$F4')

def setColor(A7):
	A7.setColor(hou.Color(0,0,0))
	if A7.parm('publishlock').eval()==1:
		A7.setColor(hou.Color(0,0,0))
		
	if A7.parm('datatype').eval()=="abc":
		A7.setColor(hou.Color(0,0,0))
		if A7.parm('publishlock').eval()==1:
			A7.setColor(hou.Color(0,0,0))
			
	if A7.parm('datatype').eval()=="vdb":
		A7.setColor(hou.Color(0,0,0))
		if A7.parm('publishlock').eval()==1:
			A7.setColor(hou.Color(0,0,0))
			
	if A7.parm('datatype').eval()=="cgifd":
		A7.setColor(hou.Color(0,0,0))
		if A7.parm('publishlock').eval()==1:
			A7.setColor(hou.Color(0,0,0))



		
def playimg(path,player=1):
	import scramble
	path=os.path.normpath(path)
	if player == 0:
		houpaths=hou.houdiniPath()
		for p in houpaths:
			if p.find("HOUDI") > -1:
				if p.find("/bin") > -1:
					houpath = p
		cmd = houpath + "/mplay " + str(path)
	else:
		path=path.replace("*","####")
		cmd = "C:/PROGRA~1/Tweak/rv-win64-x86-64-6.0.4/bin/rv.exe " + str(path)
	Popen(cmd, shell=True)
		
def cleanIfds(node):
	ifdspath = node.parm("ifdspath").eval()
	pathtodel =  ifdspath.replace("/"+ifdspath.split("/")[-1],"")
	choice = hou.ui.displayMessage("clean ifds files", buttons=["this Layer only","all layers for this Houdini file","Cancel"],default_choice=2)
	if choice == 2:
		return
	elif choice == 0:
		pathtodel = os.path.normpath(pathtodel)
	elif choice == 1:
		pathtodel =  pathtodel.replace("/"+pathtodel.split("/")[-1],"")
		pathtodel = os.path.normpath(pathtodel)
	
	if not os.path.isdir(pathtodel):
		print "ifd dir not found, nothing to do"
		return
		
	if "ifds" in pathtodel:
		finalcheck = choice-2
		if pathtodel.split("\\")[finalcheck]=="ifds":
			print "delete path " + pathtodel
			shutil.rmtree(pathtodel, ignore_errors=True)

			
def ifdLock(node):
	ifdunlock = node.parm("ifdunlock").eval()
	# soho_outputmode = node.parm("soho_outputmode").eval()
	if ifdunlock == 0:
		node.parm('soho_outputmode').set(0)

############################################################################
################################# XML ######################################
############################################################################

def versionXmlUpdate(node):
	""" check if version is on disk, update A7 with time and date and the xml file with the version choosed by the user"""
	hipfilename=hou.hipFile.basename()
	name = node.parm("name").eval()
	type = node.parm("datatype").eval()
	versionint = node.parm("version").eval()
	version = "%04d"%versionint
	found=1


	# try:
		# ext = node.parm("abcbgeoextention").eval()
	# except:
	ext = node.parm("extention").eval()
		
	if type == "abc":
		ext = "abc"
		
	user = getpass.getuser()
	date = "----"
	
	path = node.parm("path").eval()
	# versiondir = os.path.normpath(path + "/v" + "%04d"%versionint)
	versiondir = os.path.normpath(path)
	
	if type == "cgifd" or type == "baketexture":
		path = node.parm("picturespath").eval()
		versiondir = os.path.normpath(path)
	
	if not os.path.isdir(versiondir):
		print "version not found: "
		found=0
		# look for the higher existing version on disk
		for v in range(versionint-1,0,-1):
			versiondir =  versiondir.replace( versiondir.split("\\")[-1],"v"+"%04d"%v)
			if os.path.isdir(versiondir):
				version = "%04d"%v
				break

		# return
	
	# On DISK
	try:
		files= os.listdir(versiondir)
	except:
		print "No version found"
		return
	for file in files:
		if file.endswith(ext) and name in file:
			t = os.path.getmtime(versiondir+"/"+file)
			date = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(t))
			break
			
	# if date == "----":		
		# return
		
	# set node parms
	node.parm("lastversion").set(version)
	node.parm("date").set(date)
	
	if found==0:
		return
		
	# XML
	xpath = xmlpath()
	xmlfile = xpath + "/houdiniCache.xml"
	if not os.path.isfile(xmlfile):
		print "no xml file !"
		return
		
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse(xmlfile, parser)
	
	try:
		listtype = tree.find(type)
		searchstring =  "cache[@name=\'" + name + "\']"
		itemByname = listtype.find(searchstring)
		updateExpElemnts(itemByname,version,date,versiondir,hipfilename)

		with open(xmlfile, 'w') as fid:	
			fid.write(etree.tostring(tree, pretty_print=True))
	except:
		pass


def cacheXmlCheck(node):
	""" check if version is exported, if so, lock node """
	
	name = node.parm("name").eval()
	type = node.parm("datatype").eval()
	versionint = node.parm("version").eval()
	version = "%04d"%versionint
	# export = node.parm("publishlock").eval()
	try:
		exportDpt = os.environ["task"]
	except:
		exportDpt = node.parm("departement").eval()
	user = getpass.getuser()
			
	path = xmlpath()
	
	date = "----"
	node.parm("date").set(date)
	node.parm("publishdate").set(date)
	node.parm("lastversion").set(date)
	
	xmlfile = os.path.normpath(path + "/houdiniCache.xml")
	if not os.path.isfile(xmlfile):
		return
		
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse(xmlfile, parser)
	
	try:
		listtype = tree.find(type)
		searchstring =  "cache[@name=\'" + name + "\']"
		itemByname = listtype.find(searchstring)
		date = itemByname.get("date")
		xmlversion = itemByname.get("version")
		# if xmlversion == version:
			# datetime.datetime.strptime("2013-1-25", '%Y-%m-%d').strftime('%m/%d/%y')
		node.parm("lastversion").set(xmlversion)
		node.parm("date").set(date)
	except:
		pass
	
	elementExport = tree.find("exports")
	listexport = list(elementExport)
	for exp in listexport:
		xmlname = exp.get('name')
		xmltype = exp.get('type')
		xmlversion = exp.get('version')
		xmldate = exp.get('date')
		if xmlname == name and xmltype == type and xmlversion == version:
			node.parm("publishlock").set(1)
			node.parm("publishdate").set(xmldate)
			return
	node.parm("publishlock").set(0)
	

def cacheXml(node):
	""" node: cg_renderA7. Create a cacheXml file from A7 parameters. Xml file contain cache name type date and time ..."""
	hipfilename = str(hou.hipFile.basename())
	path = node.parm("path").eval()
	name = node.parm("name").eval()
	type = node.parm("datatype").eval()
	renderNode = str(node.path())
	versionint = node.parm("version").eval()
	version = "%04d"%versionint
	user = getpass.getuser()
	date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
	export = node.parm("publishlock").eval()
	exportDpt = node.parm("departement").eval()
	cachepath = node.parm("path").eval()
	quickPublish = str(node.parm("quickPublish").eval())	

	if type == "cgifd":
		cachepath = node.parm("picturespath").eval()

	if export is False:
		export = None
		exportDpt = None
	
	path = xmlpath()
	# if type != "cop" and type != "baketexture":
	cacheXmlUpdate(quickPublish,path,name,renderNode,type,version,user,date,cachepath,export,exportDpt,hipfilename)
	
def  xmlpath():
	""" create xml path from hip file path """
	houfilepath = hou.hipFile.path()
	assetname = hou.getenv("assetname")
	houfilename = hou.hipFile.basename()
	# xmlpath=""
	if assetname == None:
		xmlpath = houfilepath.split(houfilename)[0]
		# assetname = hou.hipFile.basename().replace(".hip","")
	else:
		xmlpath=houfilepath.split(assetname)[0] + assetname
	return xmlpath
	
def cacheXmlBase(path):
	"""Create houdiniCache.xml and check for types in the files. path: path to directory."""
	xmlfile = os.path.normpath(path + "/houdiniCache.xml")
	typelist=['bgeo','vdb','abc','cgifd','exports','cop','baketexture']
	
	if not os.path.isfile(xmlfile):
		try:
			# creer le fichier
			root = etree.Element('caches')
			tree = etree.ElementTree(root)
			for type in typelist:
				type = etree.SubElement(root, type)

			with open(xmlfile, 'w') as fid:
					fid.write(etree.tostring(tree, pretty_print=True))
		except:
			print "Can't create xml"

	else:
	# check for elements and add some if not present
		try:
			parser = etree.XMLParser(remove_blank_text=True)
			tree = etree.parse(xmlfile, parser)
			caches = tree.getroot()
			for cache in caches:
				if cache.tag in typelist:
					typelist.pop(typelist.index(cache.tag))
			
			if len(typelist) > 0:
				print "xml added types: " + str(typelist)
				for t in typelist:
					t = etree.SubElement(caches, t)
					
				with open(xmlfile, 'w') as fid:
					fid.write(etree.tostring(tree, pretty_print=True))
		except:
			print "Can't update xml file with new types"
			
	return xmlfile
	
def cacheXmlUpdate(quickPublish,path,name,renderNode,type,version,user,date,cachepath,export=None,exportDpt=None,hipfilename=None):
	"""
	path: path to directory.
	name: layer name.
	renderNode: A7 user name (most often same as name)
	type: bgeo, vdb,abc. cgifd todo.
	version: layer user version.
	user: user name.
	date: cache date and time (2999-12-31_00:00:00)
	export: 0 or 1 if exported
	exportDpt: departement destination (lighting, fx)
	"""
	elementExport=""
	# if type != "cop" and type != "baketexture" :
	xmlfile = cacheXmlBase(path)
	
	found=0

	
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse(xmlfile, parser)
	
	if export == 0:
		elementsType = tree.find(type)

		listElementsType=list(elementsType)
		# for elmnts in tree.iter():
		for elmnts in listElementsType:
			xmlname = elmnts.get('name')
			xmltype = elmnts.get('type')
			if xmlname == name and xmltype == type:
				# elmnts.set("version",str(version))
				updateExpElemnts(quickPublish,elmnts,version,date,cachepath,hipfilename)
				found+=1
				
		if found==0:
			a1 = etree.SubElement(elementsType,'cache',name=name,rendernode=renderNode,type=type,version=version,user=user,date=date,hipfile=hipfilename,quickPublish=quickPublish)
			b1 = etree.SubElement(a1,"path")
			b1.text = str(cachepath)
		
	found=0
	if export == 1:
		elementExport = tree.find("exports")
		listexport = list(elementExport)
		for exp in listexport:
			xmlname = exp.get('name')
			xmltype = exp.get('type')
			xmlversion = exp.get('version')
			if xmlname == name and xmltype == type and xmlversion == version:
				updateExpElemnts(exp,version,date,cachepath,hipfilename)
				found+=1
		if found==0:
			a1 = etree.SubElement(elementExport,'export',name=name,rendernode=renderNode,type=type,version=version,user=user,date=date,export=str(export),exportDpt=exportDpt)
			b1 = etree.SubElement(a1,"path")
			b1.text = str(cachepath)
		
	with open(xmlfile, 'w') as fid:	
		fid.write(etree.tostring(tree, pretty_print=True))
		
def updateExpElemnts(quickPublish,element,version,date,cachepath,hipfilename):
	# print element
	element.set("version",str(version))
	element.set("date",str(date))
	element.set("hipfile",str(hipfilename))
	element.set("quickPublish",quickPublish)
	pathexist = element.find("path")
	if pathexist == None:
		path = etree.SubElement(element, 'path')
	else:
		path = pathexist
	path.text = str(cachepath)
		
def removeExpElement(node):
	""" when unlock remove the export item """
	lock = node.parm("publishlock").eval()
	if lock == 1:
		return
	user = getpass.getuser()
	path = node.parm("path").eval()
	
	path = xmlpath()
	
	if node.parm("datatype").eval() != "cop":
		xmlfile = cacheXmlBase(path)
	
	name = node.parm("name").eval()
	type = node.parm("datatype").eval()
	versionint = node.parm("version").eval()
	version = "%04d"%versionint
	
	parser = etree.XMLParser(remove_blank_text=True)
	tree = etree.parse(xmlfile, parser)
	
	elementExport = tree.find("exports")
	listexport = list(elementExport)
	for exp in listexport:
		xmlname = exp.get('name')
		xmltype = exp.get('type')
		xmlversion = exp.get('version')
		if xmlname == name and xmltype == type and xmlversion == version:
			elementExport.remove(exp)
			
	with open(xmlfile, 'w') as fid:	
		fid.write(etree.tostring(tree, pretty_print=True))
		




def secuHip():
	import os
	import shutil
	import hou
	#recuperre le chemein du cache et son nom
	#currentNodePath =hou.expandString("`opfullpath(".")`")
	#cachePath = hou.parm(currentNodePath + "/path").eval()
	#cacheName = hou.parm(currentNodePath +"/filename").eval() 
	currentNode = hou.pwd()
	try: 
		cachePath = currentNode.parm("picturespath").eval()
		print cachePath
	except:
		cachePath = currentNode.parm("path").eval()
		print cachePath

	cacheName = hou.pwd().parm("filename").eval() 

	#recuperre le chemin du hip
	filePath = os.path.normpath(hou.hipFile.path())
	print "file"
	#secuDir = la ou doit etre copie le fichier qui a generer le cache
	secuDir = cachePath + "/secuFile/"
	secuPath =os.path.normpath(secuDir + cacheName + "_secuFile.hip")


	#si le fichier n'existe pas il cree le dossier et copie le fichier courant dedans
	#si il existe il creer un fichier backup dans le fichier secu 
	hou.hipFile.save()


	if os.path.exists(secuDir):
		shutil.copy(filePath,secuPath)

		
	else :

		os.makedirs(secuDir)
		shutil.copy(filePath,secuPath)


def colorCheckCache():
	# si une version du cache existe le node devient noire si il n'existe pas il devient vert
	currentNode = hou.pwd()
	pink=hou.Color((0.98,0.275,0.275))
	green=hou.Color((0,1,0))
	black=hou.Color((0,0,0))
	bleu=hou.Color((0.3,0.5,0.9))

	if currentNode.parm("lecture").eval() == 0:
		try: 
			cachePath = currentNode.parm("picturespath").eval()
			print cachePath
		except:
			cachePath = currentNode.parm("path").eval()
	else :
		cachePath = ("/").join(currentNode.parm("path2").eval().split("/")[:-1])

	if os.path.exists(cachePath):
		currentNode.setColor(black)
		currentNode.setUserData('nodeshape', "null")
	else :
		currentNode.setUserData('nodeshape', "circle")
		currentNode.setColor(black)

	if currentNode.parm("quickPublish").eval() == 1:
		currentNode.setColor(bleu)

	if currentNode.parm("lecture").eval() == 1:
		currentNode.setColor(green)
	if currentNode.parm("lecture").eval() == 0:
		currentNode.setColor(black)	



				


def lecture():
	currentNode = hou.pwd()
	green=hou.Color((0,1,0))
	black=hou.Color((0,0,0))
	#lecture a la volee	
	#set version
	versionLecture = currentNode.parm("version").eval()
	
	currentNode.parm("version2").set(versionLecture)

	#set path
	bgeopath= ("/").join(currentNode.parm("bgeopath").eval().split("/")[:-1])

	path=currentNode.parm("bgeopath").eval() + "/" + currentNode.parm("filename").eval() + ".$F4" + "." + currentNode.parm("extention").eval()
	currentNode.parm("path2").set(path)

	if currentNode.parm("path2").rawValue().find(".abc") != -1 :
		currentNode	.parm("alembic2").set("1")
		abcPath = currentNode.parm("path2").rawValue().replace(".$F4","")		
		currentNode.parm("path2").set(abcPath)



	currentNode.parm("oldV").set(versionLecture)

	if currentNode.parm("lecture").eval() == 1:
		currentNode.parm("lock").set(1)
	if currentNode.parm("lecture").eval() == 1:
		currentNode.setColor(green)
	if currentNode.parm("lecture").eval() == 0:
		currentNode.setColor(black)		


def versionLecture():

	currentNode = hou.pwd()
	#eval old version
	oldVersion = currentNode.parm("oldV").eval()
	#eval newVersion
	version = currentNode.parm("version2").eval()
	#eval path
	path = currentNode.parm("path2").rawValue()
	#trouve et remplace les version
	padOldVersion = "v"+str(oldVersion).zfill(4)
	padVersion = "v"+str(version).zfill(4)
	path = path.replace(padOldVersion,padVersion)
	#set le nouveau path
	currentNode.parm("path2").set(path)
	#set oldV
	currentNode.parm("oldV").set(version)

def commentaire():
	currentNode = hou.pwd()
	#emplacement fichier commentaire
	cachePath = currentNode.parm("path").eval()
	secuDir = cachePath + "/secuFile/"
	commentPath =os.path.normpath(secuDir + "comment.txt")

	if os.path.exists(secuDir):
		commentEval = currentNode.parm("commentaire").eval()
		with open(commentPath, "w") as comment:
			comment.write(commentEval)

def commentaireLoad():
	currentNode = hou.pwd()
	#emplacement fichier commentaire
	cachePath = currentNode.parm("path").eval()
	secuDir = cachePath + "/secuFile/"
	commentPath =os.path.normpath(secuDir + "comment.txt")

	if os.path.exists(commentPath):
		print "existe"
		with open(commentPath, "r") as comment:
			text = comment.read()
			currentNode.parm("commentaire").set(text)
	else :
		currentNode.parm("commentaire").set("ecrire commentaire")		
