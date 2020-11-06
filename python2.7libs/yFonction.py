
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from lxml import etree

import shutil
import os,getpass,sys,hou
import platform
import subprocess
import datetime
import nodesearch



#mes variables
yUser =os.getenv('USER')
yUserList = ["USER","jmargelin","pmathon","jpinto","avienne"]
yProject=os.getenv("project")
#CGEV 
rootsCGEV = "//stord/diskd/BDD/"
projetCGEV="//storf/diskf/"
#HOME
rootsHOME = "/media/"+yUser+"/HIPHIPHIP/"
projetHOME = "/media/vfx/"
#----------------------------------------
#xml
xml="xmlFile/hip.xml"
#hBank
hBank="houdini_bank"
yType=["FLIP","RBD","POP","VOLUME","SOP_VEX","VELLUM","TERRAIN","CROWD","MATERIAUX","RND","VELOCITE"]
#vBank
vBank="vex_bank"

#PIPE
yDictPipe = {
"CGEV":[rootsCGEV+vBank,rootsCGEV+hBank,projetCGEV,rootsCGEV+xml],
"HOME":[rootsHOME+vBank,rootsHOME+hBank,projetHOME,rootsHOME+xml]
}
#ma liste de pipe 
yListePipe = yDictPipe.keys()

#print yListePipe

def quelPipe():
	if platform.system() == "Windows":
		pipe = "CGEV"
	else:
		pipe = "HOME"
	return pipe

#fonction globales
def yOpen(path):
	if platform.system() == "Windows":
		path = os.path.realpath(path)
		os.startfile(path)
	elif platform.system() == "Darwin":
		subprocess.Popen(["open", path])
	else:
		subprocess.Popen(["xdg-open", path])	




def yXml(pipe):

	#structure xml
	#recuperrer les varua
	cheminHip = hou.expandString("$HIP")
	nomFichier = hou.expandString("$HIPNAME")
	# faire le split du chemin
	split = cheminHip.split("/")
	#recuperrer touttes les variables
	version = split[-1]
	effet = split[-2]
	user = split[-3]
	shot = split[-6]
	projet = split[-7]
	path = cheminHip + "/" + nomFichier + ".hip"
	time = str(datetime.datetime.now())[:-10]
	# ouvrir xml et get roots
	temp = yDictPipe[pipe]
	xmlPath = temp[3]
	tree = etree.parse(xmlPath)
	tronc = tree.getroot()
	#recuperer xprojet
	xprojet  = tree.xpath("/projetTree/projet[@name='%s']" %projet)
	# si xprojet exist pas
	# creer xprojet et l'ajouter 
	if len(xprojet)==0:
		xprojet = etree.Element("projet",{"name":projet})
		tronc.append(xprojet)
	tree.write(xmlPath)
	# recuperrer xinfo
	tree = etree.parse(xmlPath)
	tronc = tree.getroot()
	xprojet  = tree.xpath("/projetTree/projet[@name='%s']" %projet)
	xInfo  = tree.xpath("/projetTree/projet[@name='%s']/shot[@effet='%s']" %(projet,effet))
	print (len(xInfo))

	# si xinfo exist pas  l'ajouter
	if len(xInfo)==0:
		xInfo = etree.Element("shot",{"shot":shot,"user":user,"effet":effet,"version":version,"fullpath":path,"path":cheminHip,"time":time})
		xprojet[0].append(xInfo)
	# else le mettre a jour
	elif version < xInfo[0].attrib["version"] :
		print "ne fais rien"
	else :	
		xInfo[0].attrib["version"] = version
		xInfo[0].attrib["path"] = cheminHip
		xInfo[0].attrib["fullpath"] = path
		xInfo[0].attrib["time"] = time
	#ecrire xml
	tree.write(xmlPath)



