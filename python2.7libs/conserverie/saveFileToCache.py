
def secuHip()
	import os
	import shutil
	import hou
	#recuperre le chemein du cache et son nom
	currentNodePath ="`opfullpath(".")`"
	cachePath = hou.parm(currentNodePath + "/path").eval()
	cacheName = hou.parm(currentNodePath +"/filename").eval() 
	#recuperre le chemin du hip
	filePath = os.path.normpath(hou.hipFile.path())
	print "file"
	#secuDir = la ou doit etre copie le fichier qui a generer le cache
	secuDir = cachePath + "/secuFile/"
	secuPath =os.path.normpath(secuDir + cacheName + "_secuFile.hip")
	print "secu"

	#si le fichier n'existe pas il cree le dossier et copie le fichier courant dedans
	#si il existe il creer un fichier backup dans le fichier secu 


	if os.path.exists(secuDir):
		shutil.copy(filePath,secuPath)
		print "true"
		
	else :

		os.makedirs(secuDir)
		shutil.copy(filePath,secuPath)
		print "false"


	

