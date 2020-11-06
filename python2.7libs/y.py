# script to do

#ajouter un bouton render et version linker dans le sop context 

#y.render set un node mantra set l'objet selectione dans force object du node mantra

#y.materialPreviz set up de shading avec shading ball et environment : y.shadingBall y.123

# script qui paste les node copier dans le press papier pour chaque node selectionne

# reset node to factory default (casse toutes les references)

# pre render snippet qui copie le hip file dans le dossiers du cache

# pre render snippet qui set La bonne resolution pour les simu (peut etre fait avec les take) 

# save selected style 3dsmax

# creer un node de proxy qui ce desactive au rendu 

# creer une ligne aligner au centre de la bbox

s="""
                                                                                                    
 .                                                                                                  
                                                                                                    
                                      ................  .....                                       
                                      ......  .. ...... .....                                       
                                      ....... .. ..  .. .....                                       
                                                                                                    
                                   .. .. ... ... ...  .. .. .. ..                                   
                                   .. .. ... ... .'.  ..... .. ..                                   
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                             ....... ...                                            
                                         .....................                                      
                                    .............................                                   
                                   .................................                                
                                 ....................................                               
                               ........................................                             
                              ..............'''..'''..''..'..............                           
                            .............''''''......'''.'''''............                          
                           .........''..''''''..  . ..,,'''''''............                         
                           ........''''''''...........;c,,,,,,,'............                        
                         .........'''''''.............,oo;,,,;,''..'.........                       
                        .........''',,';;..............cko;,;;;;,''''.........                      
 .                     .........,,',,,,:;..............;ddc;;:;;;'',''........                      
 .                     .......',,,,,;;;c:'''''''.....',:lodc::;;;,,,'''........                     
 .                     .......';,',;;;:cc;,,''''';cldxO0kodoc::;;;;;''''''.....                     
 .                   .........''',,;;:ccc;,,,',,;xKKKKKK0xodoc::;;;;,,,','......                    
 .                  ........''',,,;;::clc;,,,,;;cxKKKKKKKOoodoc:;;;;;,,,,'........                  
 .                 ........''',,,;;;:cccc:,,,;::ckKKKKKKK0xoddl:::::;;;,,,'..........               
 .                 ........,,',,;;:::cccc:;;;:::ckKKKKKKKKOoodlc::::::;;;,,''.........            . 
 .                 ........',,;;;;::cc::;;;:ccc:cxKKKKKKKK0dcllc:ccc:::;;;,'''........            . 
 .                ......'''',;;;;:::c:;;;;;clllccxKKKKKXKKk:',;::ccc:::;:;,'''........            . 
 .              ........,;'';,,;;::::;;:::;cllllldkOKKKKK0c'',:ccccc:::::;;,''........            . 
 .              ........''.,;,;::::cc:;;:::collllllxKKKKKo''';ccccllcc:;:;;,''........            . 
 .              ........'..,;,;:::ccc:;;::;colllolloOKKKx,'',cccllcccc:;:;,'''........            . 
 .              ...........,;;;:::ccc::;::;lolloooold0KO:'',:cllllllcc:::;;,,'........            . 
 .              .....'..''';;;:::ccccc::::;ldoooooddok0l,;;:clllllolccc:::;,,,........            . 
 .              ........''';;:cccccllc:::::ldoooooddoddc:::clloooooollc:c::,,,'.......            . 
 .             .........''';:;:cccclllc:::;lxdoddddddxo::::loooooooollcccc:;:l:'.......           . 
 .             .....'...''';:::ccclllllc:;:;cdddddddddl:::cloddddoooollccc::ll;'.......           . 
 .             .........''';:::cccclloolc:;'.,oddddxxdl:::codddddooooolccc:::;,''......           . 
 .             .........''';:::ccccllllll:;...':oxdxxoc:::lodddddoodoolclc:;;,'''......           . 
 .              ........''';:::ccclllllllc,.....,oxxxo:;:clodxddddddoollcc:;;,'''......           . 
 .              ........''';:;::cclllllcll;.',,''',cdo:::codxxddddddolllcc:;;,''......            . 
 .              ........''';::::cccllollcl:;;;;,,''';::;:lodxxxdddddolllcc:;;,''......            . 
 .              ........''';:::ccclloolllllc;;;,''''',:;coddxxkxxdddoollcc:;,,'.......            . 
 .                ......''';:::ccccllollllll::c:,,,',;:cloddxxkkkxddollcc::;,'........            . 
 .                ......'.';;;:cccclllllloolc::c:;;,;::loddxxxxxxkdoollcc:;,,'.......             . 
 .                ........',;;;::ccllllloooolc:cc:::ccloodxxxxxdddooollcc:;,''.......             . 
 .                 ........',;;:::cclllloooool::c::ccclddxxxxxxddooollc::;,''........             . 
 .                 ........',,;;;::clllllooooll:::::cloodxxxxddoooollc::;;,''.....                . 
 .                  .......',',;;::cccccloooollc;::ccloddddddddoolllcc:;;;,'......                . 
 .                   .......'',,;;::ccccclloollc:;:cllododdoooollllcc::;;,'......                   
 .                   .......''',,;;:cc::cclllllccccccoooooooolllcccc::;;,'......                    
 .                     ......'',,,;::::::ccllllllllllodoooollllcc:::;;,,'.....                      
                        ......''',;;:::::ccllllllooooooolllllccc::;;,,''.....                       
                         ......''',;;:;;:cclllllllllllllllcccc:::;;,,''.....                        
                          .......'',;;;;::cccclccccccllccccc:::;;,,''......                         
                          ........'',;,;;;:::cccccccccc:::::::;;,,''.......                         
                           ........'',',,;;;::cc:::::cc::;;;;,,'''........                          
                            ........''''',;;;;:::::::::;;;;,,'''.........                           
                             ........'..'',,,;;;;;;;;;;,,,,''''.........                            
                             ............''',,,,,,,,,,,,''''...........                             
                               .............'''','''''''.............                               
                                  .'c,....','';;',::,...............                                
                               ....ol.....;;'lOc,oxc'.............                                  
                             .,,.'loc:lolc;'cddoddlclllc:,;l;;:::c:,.                               
                             ;l..c::::c;;cl:l;;xdokl:ollxolldoloo;.::.                              
                             .lc;.........,c;.,;'.'.....';'.',........                              
                              ..  ........'..,,......................                               
                                    .. ................    ..                                       
                                                                                                    
 .                                    ............   ..                                             
                                        .......                                                     

"""
print (s)

print ("***for help type: help(y) ***")

import hou
import random

def cgevResetTheDay():

	import nodesearch
	matchType = nodesearch.NodeType("CG::renderGeo*")
	matchName = nodesearch.Name("*")
	match = nodesearch.Group([matchType,matchName])
	                
	net = hou.node("/obj/")
	#self.listSort()
	for node in match.nodes(net,recursive =True):
	    node.parm("version").pressButton()
	    node.parm("version").set(1)

	list = hou.node("/obj").allSubChildren()
	for i in list:
	    if i.type().name()== "cam":
	        camPath= i.path()
	        break
	    else :
	        camPath="/obj/cam1"
	        
	    
	matchType = nodesearch.NodeType("CG::cgmantra*")
	matchName = nodesearch.Name("*")
	match = nodesearch.Group([matchType,matchName])
	                
	net = hou.node("/out/")
	#self.listSort()
	for node in match.nodes(net,recursive =True):

	    node.parm("version").pressButton()
	    node.parm("version").set(1)
	    node.parm("camera").set(camPath)
	    

def manual():
    
    """setup scene to manual mode
    """
    help(manual)

    import hou
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
    if mode == 'Manual':
        hou.setUpdateMode(hou.updateMode.AutoUpdate)


def unDeuxTrois():

	""" setup une start scene basique
	"""

	help(unDeuxTrois)   

	import hou 
	inc= 0
	black=hou.Color((0,0,0))
	obj = hou.node("/obj")
	netBox = ""
	netBoxSize= hou.Vector2(0.5,5.0)
	myListe = ("LIGHTING","MODELING","FX","RENDERING")

	for i in myListe:
		inc+=1
		
		netBox = hou.item("/obj").createNetworkBox()
		netBox.resize(netBoxSize)
		netBox.setComment(i)
		netBox.setColor(black)
		netBox.move(hou.Vector2(4.0*inc,0.0))

	


def quatreCinqSix():

    """ set the houdini desktop 
    """

    help(quatreCinqSix)

    import hou

    #decrire la configuration du desktop avec python
    # close treeView close python open spreadsheet,chage parameter to python 
    desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
    desktops_dict['Technical2'].setAsCurrent()
	
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
		
def previz():
	import hou
	import os 

	out = hou.node("/out")
	outChildren = out.children()
	range = (int(hou.expandString("$FSTART")),int(hou.expandString("$FEND")),1)
	#children list 
	outChildListe=[]
	for i in outChildren:
		outChildListe.append(i.name())
	previzName = "previzY"

	#check si le node previz exist
	if previzName not in outChildListe :
		openGl = out.createNode("previz",previzName)    
		openGl.setParms({"trange":"normal"})
		hou.parmTuple('/out/previzY/f').set(range)
		openGl.setParms({"tres":1})
		hou.parmTuple('/out/previzY/res').set((1280,720))
		
	# versionning automatique
	path = hou.parm('/out/previzY/vm_picture').eval()
	currentVersion=hou.parm('/out/previzY/version').eval()
	if os.path.exists(path):
		hou.parm('/out/previzY/version').set(currentVersion+1)
		hou.parm('/out/previzY/version').pressButton()
		
	hou.parm('/out/previzY/play').pressButton()
	hou.parm('/out/previzY/execute2').pressButton()
	
def play ():
	hou.parm('/out/previzY/play').pressButton()
	
	
def mayaExport():
	import hou 

	nodes = hou.selectedNodes()
	obj = hou.node("/obj")
	red = hou.Color(1,0,0)
	blue=hou.Color((0.3,0.6,1))


	#children 
	children = obj.children()
	nameListe=[]
	renderListe = []
	childRenderListe =[]
	renderNode = []
	mayaNameListe = []
	

	for i in children:
	#children Name
		nameListe.append(i.name())
	#render Liste
		if "RENDER" in i.name():
			renderListe.append(i)
			childRenderListe.append(i.children())
			
	#cgRender in render list
	for i in childRenderListe:
		for f in i:
			if f.isRenderFlagSet():
				renderNode.append(f)

	#check if maya export exist already
	if "MAYA_EXPORT" not in nameListe:
		mayaExport =obj.createNode("geo","MAYA_EXPORT")
		mayaExport.setColor(red)
		#maya scale
		parm_group = mayaExport.parmTemplateGroup()
		parm_folder = hou.FolderParmTemplate("folder","MAYA_SCALE")
		parm_folder.addParmTemplate(hou.FloatParmTemplate("MAYA_SCALE","SET_MAYA_SCALE",1))
		parm_group.append(parm_folder)
		mayaExport.setParmTemplateGroup(parm_group)
		mayaExport.setParms({"MAYA_SCALE":1})
			

	#maya node adresse and child
	maya= hou.node("/obj/MAYA_EXPORT/")
	inMayaChild = maya.children()

	for i in inMayaChild:
			mayaNameListe.append(i.name())



	#pass a traver a liste des noeud de rendu
	for node in renderNode:

		parent = node.parent()
		getName = node.name()
		shortName = getName.split("_")

		if "in"+getName.capitalize() not in mayaNameListe:
			#create merge
			mergePath = node.path()
			objMerge = maya.createNode("object_merge","in"+getName.capitalize())
			objMerge.setParms({"objpath1":mergePath})
			#createUnpack
			unpack = objMerge.createOutputNode("unpack")
			#attribute delete
			attDel = unpack.createOutputNode("attribdelete")
			attDel.setParms({"ptdel":"* ^pscale ^v ^N ^Cd ^uv"})
			attDel.setParms({"vtxdel":"* ^uv"})
			attDel.setParms({"primdel":"* ^name"})
			attDel.setParms({"dtldel":"*"})
			attDel.bypass(1)
			#group delete
			groupDel=attDel.createOutputNode("groupdelete")
			groupDel.setParms({"group1":"*"})
			groupDel.bypass(1)
			#tranform
			transform=groupDel.createOutputNode("xform")
			transform.setParmExpressions({"scale":"ch('../MAYA_SCALE')"})
			#export type

			if transform.geometry().prims()[0].type().name() == 'VDB' or transform.geometry().prims()[0].type().name() == 'Volume':
				extension = "vdb"
				vdbConvert = transform.createOutputNode("convertvdb")
				null = vdbConvert.createOutputNode("null","vdb")
				null.setColor(blue)
				vdbConvert.setParms({"conversion":"vdb"})
			else :
				extension = "abc"
				null = transform.createOutputNode("null","abc")
				
			#renderGeo
			geoRender= null.createOutputNode("renderGeo",shortName[1]+"_maya")
			geoRender.setParms({"datatype":extension})
			



		
def renderPass():
	""" set des node de rendu pour chaque cgnull dans les node selectionnes """
	help(renderPass)
		

	nodes = hou.selectedNodes()
	obj = hou.node("/obj")
	out = hou.node("/out")

	#liste des noms de nodes
	children = obj.children()
	nameliste = []
	children = obj.children()
	for i in children:
			nameliste.append(i.name())
	   
	#recuperre la cam
	list = hou.node("/obj").allSubChildren()
	for i in list:
			if i.type().name()== "cam":
					camPath= i.path()
					break
			else :
					camPath="/obj/cam1"
					
	# liste les cg output pour chaque node selectionne
	listCgRender = [] 
	for node in nodes :
			node.setDisplayFlag(False)
			nodeChildren = node.children()
			for i in nodeChildren:
				if i.type().name()=="CG::cgnull::0.0":
					listCgRender.append(i)
	print (listCgRender)                
	for node in listCgRender :
		parent = node.parent()
		print(parent)
		getName = node.name()
		
		if "RENDER_"+getName.capitalize() not in nameliste:
		
			parent = node.parent()
			mergePath = node.path()
			getName = node.name()
			#render node
			renderNode = obj.createNode("geo","RENDER_"+getName.capitalize())
			renderNode.setPosition(parent.position())
			renderNode.move([4.0,0.0])
			passName = renderNode.name()
			#object merge
			objMerge = renderNode.createNode("object_merge","in"+getName.capitalize())
			objMerge.setParms({"objpath1":mergePath})
			#attribute delete
			attDel = objMerge.createOutputNode("attribdelete")
			attDel.setParms({"ptdel":"* ^pscale ^v ^N ^Cd"})
			attDel.setParms({"vtxdel":"*"})
			attDel.setParms({"primdel":"* ^name"})
			attDel.setParms({"dtldel":"*"})
			attDel.bypass(1)
			#nullGC
			myNull = attDel.createOutputNode("cgnull","RENDER_"+getName.capitalize())
			myNull.setRenderFlag(True)
			#out
			mantra = out.createNode("cgmantra",getName)
			mantra.setParms({"vobject":""})
			mantra.setParms({"forceobject":passName})
			mantra.setParms({"vm_renderengine":"pbrraytrace"})
			mantra.setParms({"camera":camPath})
    


def bound():

    """return bound box and centroid"""

    help(bound)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        getName = node.name()
        outNull = node.createOutputNode("null",getName+"_IN_BOUND")
        outNull.setPosition(node.position())
        outNull.move([0, -1])
        outNull.setColor(black)
        outBound= outNull.createOutputNode("null",getName+"_BOUND_CENTROID")
        outBound.setColor(pink)
        #add create param to outBound
        parm_group = outBound.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","Bound_Centroid")
        parm_folder.addParmTemplate(hou.FloatParmTemplate("bound","Bound",3))
        parm_folder.addParmTemplate(hou.FloatParmTemplate("centroid","Centroid",3))
        parm_group.append(parm_folder)
        outBound.setParmTemplateGroup(parm_group)

        outBound.parm('boundx').setExpression("bbox(opinputpath('.',0),D_XSIZE)")
        outBound.parm('boundy').setExpression("bbox(opinputpath('.',0),D_YSIZE)")
        outBound.parm('boundz').setExpression("bbox(opinputpath('.',0),D_ZSIZE)")

        outBound.parm('centroidx').setExpression("centroid(opinputpath('.',0),D_X)")
        outBound.parm('centroidy').setExpression("centroid(opinputpath('.',0),D_Y)")
        outBound.parm('centroidz').setExpression("centroid(opinputpath('.',0),D_Z)")


def rotTool():

    """
    help rotate scatter with orient attribute
    """
    help(rotTool)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","rotTool")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""float x = rand(@ptnum);
float y = rand(@ptnum+311);
float z = rand(@ptnum-801);
@orient = sample_orientation_uniform(set(x,y,z));

"""}) 
        print("--- Don't forget create channels parameter in the wrangle node ---")

def normalizeGeoYVex ():

    """
    normalize the size of the geo and move it to zero
    """
    help(normalizeGeoYVex)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","normalizeGeoVexByHeight")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
//center geo
vector min, max;
getbbox(0, min, max);
vector centroid = (min+max)/2;;
@P+= centroid*-1;

@P*= 1/(max.y-min.y); //normalize by max height 
@P.y+=0.5; //normalize by max height

@P*=ch('realScale'); //real scale"""}) 
        print("--- Don't forget to just clic for create channels param in the wrangle node ---")

def normalizeGeoMaxSize ():

    """
    normalize by max size and centroid
    """
    help(normalizeGeoMaxSize)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","normalizeGeoVexByHeight")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
//center geo
vector min, max;
getbbox(0, min, max);
vector centroid = (min+max)/2;;
@P+= centroid*-1;

@P*= 1/(max(max.x-min.x,max.y-min.y,max.z-min.z)); //normalize by max size
@P*=2;"""}) 
        

# ajouter une boite de dialoque qui demande le nom du cache 
# ajouter le versionning



def bgeo ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(bgeo)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:



        parent = node.parent()  #hou.node("..")
        parentString =parent.name()   
        # ui 
        getName = hou.ui.readInput("cache Name ? ")[1]
        extension = hou.ui.selectFromList(("bgeo","vdb","abc"),height=3)


        if extension[0] == 0:
            print("bitch")
        
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #create In node 
        myFile = outNull.createOutputNode("file",getName.upper()+"_CACHE")
        myFile.setColor(pink)

        #create out node
        myWriteGeo= out.createNode("geometry",getName.upper()+"_CACHE")

        myWriteGeoName = "/out/{0}".format(myWriteGeo.name())
        #set param
        myWriteGeo.setParms({"soppath":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"sopoutput":"$HIP/cache/rop_sfx/bgeo.sc/$OS/v`padzero(3, ch('version'))`/$OS.$F5.bgeo.sc"})
        myWriteGeo.setParms({"trange":"normal"})

        #add create param for versionning and export format
        parm_group = myWriteGeo.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","version")
        parm_folder.addParmTemplate(hou.IntParmTemplate("version","Version",1))
        parm_group.append(parm_folder)
        myWriteGeo.setParmTemplateGroup(parm_group)

        # myfile Parm
        myFile.setParms({'file': "`chs('{0}/sopoutput')`".format(myWriteGeoName),})
        myFile.parm("file").disable(True)
        myFile.parm("file").eval()

        parm_group = myFile.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","version")
        parm_folder.addParmTemplate(hou.StringParmTemplate("version","Version",1, disable_when="{ 1 != 0 }"))
        parm_group.append(parm_folder)
        myFile.setParmTemplateGroup(parm_group)

        version = "`chs('{0}/version')`".format(myWriteGeoName)

        myFile.parm('version').set(version)






def vdb ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(vdb)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:
        parent = node.parent()  #hou.node("..")
        parentString =parent.name()    
        getName = node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #set read node to read myWriteGeo
        myFile = outNull.createOutputNode("file",getName.upper()+"_CACHE")
        myFile.setColor(pink)
        myFile.setParms({'file': '$HIP/cache/rop_sfx/vdb/$OS/v`padzero(3,chs("/out/$OS/version"))`/$OS.$F5.vdb'})
        myWriteGeo= out.createNode("geometry",getName.upper()+"_CACHE")
        myWriteGeo.setParms({"soppath":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"sopoutput":"$HIP/cache/rop_sfx/vdb/$OS/v`padzero(3, ch('version'))`/$OS.$F5.vdb"})
        myWriteGeo.setParms({"trange":"normal"})

        #add create param for versionning
        parm_group = myWriteGeo.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","version")
        parm_folder.addParmTemplate(hou.IntParmTemplate("version","Version",1))
        parm_group.append(parm_folder)
        myWriteGeo.setParmTemplateGroup(parm_group)

def abc ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(abc)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:
        parent = node.parent()  #hou.node("..")
        parentString =parent.name()    
        getName = node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #set read node to read myWriteGeo
        myFile = outNull.createOutputNode("alembic",getName.upper()+"_CACHE")
        myFile.setColor(pink)
        myFile.setParms({'fileName': '$HIP/cache/rop_sfx/abc/$OS/v`padzero(3,chs("/out/$OS/version"))`/$OS.abc'})
        #set write geo in out context
        myWriteGeo=out.createNode("alembic",getName.upper()+"_CACHE")
        #set parm
        myWriteGeo.setParms({"use_sop_path":1})
        myWriteGeo.setParms({"sop_path":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"filename":"$HIP/cache/rop_sfx/abc/$OS/v`padzero(3, ch('version'))`/$OS.abc"})
        myWriteGeo.setParms({"trange":"normal"})
        #add create param for versionning
        parm_group = myWriteGeo.parmTemplateGroup()
        versionParm =hou.IntParmTemplate("version","Version",1)
        target_folder = ("Main")
        parm_group.appendToFolder(target_folder,versionParm)
        myWriteGeo.setParmTemplateGroup(parm_group)
        


def pywy ():

    """
    create a node to test code with python
    """

    help(pywy)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        #create node from selected node
        pyNull = node.createOutputNode("null","pythonRunCode")
        pyNull.setColor(pink)
        #prepa param
        parm_group = pyNull.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","pywy")
        #button run code
        button=hou.ButtonParmTemplate("runcode","Run_Code")
        button.setTags({"script_callback_language":"python","script_callback":"exec(kwargs['node'].parm('pythonCode').eval())"})
        parm_folder.addParmTemplate(button)
        #multistring
        multistring=hou.StringParmTemplate("pythonCode","PythonCode",1)         
        multistring.setTags({"editor":"1","editorlang":"python"})
        parm_folder.addParmTemplate(multistring)
        #append param
        parm_group.append(parm_folder)
        pyNull.setParmTemplateGroup(parm_group)



def camUvDelete ():

    """
    delete geo by camera range
    """
    help(camUvDelete)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","camUvDelete")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
vector ndc=toNDC(chs("camPath"),@P);
@Cd = ndc; // viz
float secu = 0.1;
if(ndc.x+secu<0||ndc.x-secu>1||ndc.y+secu<0||ndc.y-secu>1||ndc.z>1){
removepoint(geoself(),@ptnum);
}"""}) 
        print("--- Don't forget to check the campath in camUvdelete ---")

def camUvDeleteAnim ():

    """
    delete geo by camera range also works with an animated camera
    """

    help(camUvDeleteAnim)

    import hou
    nodeSelect= hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))
    black=hou.Color ((0,0,0))

    for node in nodeSelect:
        parent = node.parent()
        parentString= parent.name()
        getName= node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null","inCamDeleteAnim")
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)
        #create left branch
        blackColor= outNull.createOutputNode("color","black")
        blackColor.move([-.75, -.75])
        blackColor.setParms({"colorr":0,"colorg":0,"colorb":0})
        #create right branch
        wrangleSnippet=outNull.createOutputNode("attribwrangle","camUvDelete")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
vector ndc=toNDC("/obj/root/transform/camera/cambaked/ppCam/ppCamShape",@P); // DONT FORGET TO FILL CAM PATH
@Cd = ndc; // viz
float secu = 0.1;
if(ndc.x+secu<0||ndc.x-secu>1||ndc.y+secu<0||ndc.y-secu>1||ndc.z>1){
removepoint(geoself(),@ptnum);
}"""}) 
        wrangleSnippet.move([0.75, -.75])
        redColor= wrangleSnippet.createOutputNode("color","red")
        redColor.move([0, -.35])
        redColor.setParms({"colorr":1,"colorg":0,"colorb":0}) 
        #create solver
        mysolver = blackColor.createOutputNode("solver","transferColor")
        solverName = mysolver.name()
        mysolver.move([0, -1.5]) 
        mysolver.setInput(1,redColor)
        mytransfert = hou.node('/obj/'+parentString+'/'+solverName+'/d/s').createNode('attribtransfer','transferUv')
        hou.node('/obj/'+parentString+'/'+solverName+'/d/s/transferUv').setInput(0,hou.node('/obj/'+parentString+'/'+solverName+'/d/s/Prev_Frame'))
        hou.node('/obj/'+parentString+'/'+solverName+'/d/s/transferUv').setInput(1,hou.node('/obj/'+parentString+'/'+solverName+'/d/s/Input_2'))
        mytransfert.setDisplayFlag(True) #set display flag true
        mytransfert.setParms({"thresholddist":0.1})
        time = mysolver.createOutputNode("timeshift","Fend")
        time.parm("frame").deleteAllKeyframes()
        time.setParms({"frame":240})
        
        removePointVex=time.createOutputNode("attribwrangle","deleteGeo")
        removePointVex.setColor(pink)
        removePointVex.setParms({"snippet":"""
if(@Cd.x<0.5)removepoint(0,@ptnum);
"""}) 
        removePointVex.setDisplayFlag(True)

    print("--- Don't forget to check the campath in camUvdelete ---")


def fillHoles ():

    '''
    add point between point if the distance between them is to big
    '''

    help(fillHoles)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","simpleFillHoles")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
float searchrad=ch("searchrad");
float mindist=ch("mindist");
int maxpoints=chi("maxpoints");
int fillpoints=chi("fillpts");

vector clpos;
int handle=pcopen(0,"P",@P,searchrad,maxpoints+1);
int i=0;
while(pciterate(handle))
{
    if (i==0) // the first point found should be the closest, in this case, itself. We want to skip it.
    {
        i++;
        continue;
    }
    pcimport(handle,"P",clpos);
    if (length(@P-clpos)>mindist)
    {
        vector pointstep=(clpos-@P)/(fillpoints*2+1); // this ensures there are no duplicate point
                                                     // at the cost of doubling the fill points number
        for (int t=0;t<fillpoints;t++)
            addpoint(0,@P+(pointstep*float(t+1)));
    }
}
"""}) 
    print("--- Don't forget to create the channel ---")


def pointDeleteByProximity ():

    '''
    if a point is to far from is neighbour then delete it
    '''
    
    help(pointDeleteByProximity)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","pointDeleteByProximity")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
int numPoint = chi("numPoint");

int mypc = pcopen(0,"P",@P,chf("radius"),numPoint);

@Cd= chramp("ramp",fit(pcnumfound(mypc),0,numPoint,0,1));

if (@Cd.x<chf("seuilColor"))removepoint(0,@ptnum);
"""}) 
    
    print("--- Don't forget to create the channel ---")

def inputColor ():
    """
    set the color of inputs node to the color of the selected node
    """

    help(inputColor)

    import hou
    nodeSelect = hou.selectedNodes()
   
    for node in nodeSelect:
        inputNode = node.inputs()
        currentColor = node.color()
        for n in inputNode:
            n.setColor(currentColor)


def inputSelectNode ():

    """
    select all inputs node of the selected node
    usefull with a lot of merge node
    """

    help(inputSelectNode)

    import hou
    nodeSelect = hou.selectedNodes()
    
    for node in nodeSelect:
        inputNode = node.inputs()
        node.setSelected(False)
        for n in inputNode:
            n.setSelected(True)
    


def importAbcAsset ():
    
    """
    import all alembic file from $HIP/abc/ in a new sop call alembicImport
    """

    help(importAbcAsset)

    import hou
    import os
 
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/abc/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    alembicImport= obj.createNode ("geo","alembicImport")
    
    file1 = hou.node("/obj/alembicImport/file1")
    file1.destroy()
  
    for n in listPath:
        print (n)
        currentFile=alembicImport.createNode("alembic",n)
        #set fileName
        currentFile.setParms({"fileName":"$"+"HIP/abc/"+n})

    #reload geo callback
    #prepa param
    parm_group = alembicImport.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder","reload")
    #button run code
    button=hou.ButtonParmTemplate("reload","Reload")
    button.setTags({"script_callback_language":"python","script_callback":"import y \ny.reloadAlembic()"})
    parm_folder.addParmTemplate(button)
    #append param
    parm_group.append(parm_folder)
    alembicImport.setParmTemplateGroup(parm_group)

def reloadAlembic ():

    import hou
    import os
    alembicImport= hou.node("/obj/alembicImport")
    
    children = alembicImport.children()
    for n in children:
        n.destroy()
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/abc/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    alembicImport= hou.node("/obj/alembicImport")
  
    for n in listPath :
        print (n)
        currentFile=alembicImport.createNode("alembic",n)
        #set fileName
        currentFile.setParms({"fileName":"$"+"HIP/abc/"+n})


def importGeoAsset ():
    
    """
    import all geo file from $HIP/geo/ in a new sop call geoImport
    """

    help(importGeoAsset)

    import hou
    import os
 
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/geo/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    geoImport= obj.createNode ("geo","geoImport")

    file1 = hou.node("/obj/geoImport/file1")
    file1.destroy()
  
    for n in listPath :
        print (n)
        currentFile=geoImport.createNode("file",n)
        #set fileNames
        currentFile.setParms({"file":"$"+"HIP/geo/"+n})
    
    #reload geo callback
    #prepa param
    parm_group = geoImport.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder","reload")
    #button run code
    button=hou.ButtonParmTemplate("reload","Reload")
    button.setTags({"script_callback_language":"python","script_callback":"import y \ny.reloadGeo()"})
    parm_folder.addParmTemplate(button)
    #append param
    parm_group.append(parm_folder)
    geoImport.setParmTemplateGroup(parm_group)


def reloadGeo ():

    import hou
    import os
    geoImport= hou.node("/obj/geoImport")
    
    children = geoImport.children()
    for n in children:
        n.destroy()
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/geo/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    geoImport= hou.node("/obj/geoImport")
  
    for n in listPath :
        print (n)
        currentFile=geoImport.createNode("file",n)
        #set fileName
        currentFile.setParms({"file":"$"+"HIP/geo/"+n})

def exit():
    """
    change scene mode in manual, save, and exit 
    """
    help(exit)
    import hou
    
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
    hou.hipFile.save(file_name=None, save_to_recent_files=True)
    hou.exit(exit_code=0, suppress_save_prompt=False)

def open():
    """change scene mode in manual, save, and open open windows"""

    help (open)

    import hou
    
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
        
    hou.hipFile.save(file_name=None, save_to_recent_files=True)
    f=hou.ui.selectFile()
    hou.hipFile.load(f) 

def explorer():
    """open explorer at $HIP path"""
    help(explorer)
    
    import hou
    import os
    import platform
    import subprocess

    path = hou.expandString("$HIP")

    print(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def explorerPublish():
    """open explorer at $HIP path"""
    help(explorerPublish)
    
    import hou
    import os
    import platform
    import subprocess

    path = hou.expandString("$HIP")+'/../../publish/images/'+hou.expandString("$HIPNAME")

    print(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def fileMaker():
    """Create some basic folder at root $HIP"""
    import hou
    import os
    from os.path import exists

    path = hou.expandString("$HIP")
    structure = ["abc","geo","screenShot","cache","render","source","ref"]
    
    
    for n in structure:
        if exists(path + '/'+ n):
            continue
        else:
            dossiers = path + '/'+ n 
            os.makedirs(dossiers)
            print (dossiers)


def screenShot():

    """take a screen shot of the current viewport at the current frame"""

    help(screenShot)

    import hou

    import toolutils

    import os

    import nodegraphutils



    #selected node

    if hou.selectedNodes() and len(hou.selectedNodes()) == 1:

        nodeSelect = hou.selectedNodes()[0]

    else:

        return



    # Get the scene viewer

    scene= toolutils.sceneViewer()

    flipbook_options = scene.flipbookSettings().stash()

    # set frame range

    flipbook_options.frameRange((hou.frame(),hou.frame()))



    #set output path

    path = hou.expandString("$HIP")

    name = nodeSelect.name()

    root = os.path.join(path, "screenShot", name)

    if os.path.exists(root):

        listPath = os.listdir(root)

        inc = len(listPath)

        inc = int(inc)   

        outputPath = "{}{}.{:04d}.jpg".format(root, name, inc)

    else:

        os.makedirs(root)

        inc = 0

        outputPath = "{}{}.{:04d}.jpg".format(root, name, inc)



    #set flipbook current path     

    flipbook_options.output(outputPath)

    #run flipbook

    scene.flipbook(scene.curViewport(),flipbook_options, open_dialog=False)



    # reload image

    image = hou.NetworkImage() 

    image.setPath(outputPath)

    image.setRect(hou.BoundingRect(0, 0, 5, 5))

    image.setRelativeToPath(nodeSelect.path())



    images = nodegraphutils.loadBackgroundImages(nodeSelect.parent())



    if images:

        images.append(image)

    else:

        images = [image]

    nodegraphutils.saveBackgroundImages(nodeSelect.parent(), images)

	
"""
def materialPreviz()
	import hou
	obj=hou.node("/obj")

	cam = obj.createNode("cam","shaderBallCam")
   	cam.setParms({"resx":350,"resy":350})
   	cam.setParms({"tx":2,"ty":0.5,"tz":0})

   	shaderBall = obj.createNode ("geo","shaderBall")
    shaderBall.move([-2, 0])
    file1= hou.node("/obj/shaderBallCam/file1")
    file1.destroy()
    shaderBallGeo=geo1.createNode("testgeometry_shaderball","shaderball")

	shaderBallSol = obj.createNode ("geo","shaderBallSol")
    shaderBallSol.move([-2,-2])
    file2= hou.node("/obj/shaderBallSol/file1")
    file2.destroy()
    #objetSol

"""

def wranglePreset():
    '''
    a simple wrangle preset for lazy man
    '''
    
    help(wranglePreset)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","wranglePreset")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""


//delete by attribute value		
//int match_point = findattribval(1, "point", "id", @id);
//if (match_point==-1) removepoint(0,@ptnum);
		
//delete
//if (@Cd.x<chf("seuilColor"))removepoint(0,@ptnum);
//if (rand(@ptnum+654)<chf("seuil"))removepoint(0,@ptnum);

//volumesample
//if (volumesample(1,"surface",@P)<0)removepoint(0,@ptnum);

//pscale
//@pscale*= fit01(rand(@ptnum+654),0.8,1.2);

//pcopen pcfilter
//int handle = pcopen(1,"P",@P,chf("radius"),chi("numPoint"));
//@Cd = pcfilter(handle,"Cd");

//chramp color
//@Cd= chramp("ramp",fit(@curvature,0,1000,0,1));

// normalize curve ramp
//@Cd= chramp("Cd",float(@ptnum)/float(@numpt));

//dot
//if (dot(@N,chv("vector"))>ch("select")){
//@Cd.x=1;}

//constraint
//s@constraint_name= "ConRelGlue" ;
//s@constraint_type= "all" ;

//group en fonction de la distance a la camera
//vector camDir = point(1,"P",0)-@P;
//f@pointDist = length(camDir);

//if (@pointDist>ch("distFromCam")){
//@group_foreground = 1 ; } 
//else {@group_background = 1;}

//forloop
//int i;
//for (i=0; i<chi("iteration"); i+=1) {
//}


//tangent
//@N= @P-point(0,"P",@ptnum-1);
//if (@ptnum==0)@N= point(0,"N",@ptnum-2);

//rotation
//@N=@N;
//@up=set(0,1,0);
//@orient = quaternion(maketransform(@N,@up));

//vector4 x = quaternion(radians(ch("x")),{1,0,0});
//vector4 y = quaternion(radians(ch("y")),{0,1,0});
//vector4 z = quaternion(radians(ch("z")),{0,0,1});

//@orient = qmultiply(@orient,x);
//@orient = qmultiply(@orient,y);
//@orient = qmultiply(@orient,z);

//move point by primUv
//vector uv;int prim;
//xyzdist(1,@P,prim,uv);
//@P= primuv(2,"P",prim,uv);
//@N= primuv(2,"N",prim,uv);

//point on curve with primUv
//vector uv;
//uv.x = ch("uvX");
//uv.y= ch("uvY");
//@P= primuv(1,"P",0,uv);

//noise
//vector freq = chv("frequence");vector offset = chv("offset");
//float amp = ch("amplitude");int turb = chi("turbulence");
//float rough = ch("rough");float atten = ch("attenuation");

//onoise(@P*freq - offset, turb, rough, atten) * amp
//snoise(@P*freq - offset, turb, rough, atten) * amp
//@Cd*=anoise(@P*freq - offset, turb, rough, atten) * amp;

//vop_correctperlinNoiseVF(@P*freq - offset, turb, rough, atten) * amp
//vop_correctperlinNoiseVV(@P*freq - offset, turb, rough, atten) * amp
//vop_simplexNoiseVF(@P*freq - offset, turb, rough, atten) * amp
//vop_simplexNoiseVV(@P*freq - offset, turb, rough, atten) * amp
//vop_perlinNoiseVF(@P*freq - offset, turb, rough, atten) * amp
//vop_perlinNoiseVV(@P*freq - offset, turb, rough, atten) * amp 


"""})


def nullMerge():

    '''
    create a null and a merge node just after, for lazy lazy man.
    '''
    
    help(nullMerge)

    import hou

	
    obj = hou.node("/obj")    
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))
    black=hou.Color((0,0,0))

    for node in nodeSelect:
	

	
        nullName=hou.ui.readInput("what is your name ? ") [1]
        randColor= hou.Color( (random.random(),random.random(),random.random()) )
        myNull=node.createOutputNode("null","out" + nullName.capitalize() )
        myNull.setPosition(node.position())
        myNull.move([0, -.75])
        myNull.setColor(randColor)
        parent=myNull.parent()
        parentName=parent.name()
        myNullName= "out" + nullName.capitalize()
        pos = myNull.position()

        print parentName + myNullName

        myMerge=parent.createNode("object_merge",nullName+"Merge")
        myMerge.setColor(randColor)
        myMerge.setParms({'objpath1':"/obj/"+parentName+"/"+myNullName})
        myMerge.setPosition(pos)
        #myMerge=setParms({'objpath1':'mynullPath'})


def polygoneFlow ():

    '''
    select face by normal orientation with color, blur the color and prepare the normal
    for velocity source
    '''
    
    help(polygoneFlow)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","selectByOrientationRGB")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""

		
//red
if (dot(@N,{1,0,0})>ch("red")){
@Cd={1,0,0};
}
if (dot(@N,{-1,0,0})>ch("red")){
@Cd={1,0,0};
}
//green
if (dot(@N,{0,1,0})>ch("green")){
@Cd={0,1,0};
}
if (dot(@N,{0,-1,0})>ch("green")){
@Cd={0,1,0};
}
//blue
if (dot(@N,{0,0,1})>ch("blue")){
@Cd={0,0,1};
}
if (dot(@N,{0,0,-1})>ch("blue")){
@Cd={0,0,1};
}

"""}) 
        wrangleBlur= wrangleSnippet.createOutputNode("attribwrangle","blurCdNormal")
        wrangleBlur.setColor(pink)
        wrangleBlur.setParms({"snippet":"""

// blur Cd 
int handle = pcopen(0,"P",@P,chf("radius"),chi("numPoint"));
vector newColor = pcfilter(handle,"Cd");
@Cd= newColor;

//tweakNormal
if (@Cd.x>0.1){
@N= cross(@N,chv("red"));
}
else if (@Cd.y>0.1){
@N= cross(@N,chv("green"));
}
else @N =cross(@N,chv("blue"));

@N*=ch("normMult");

"""}) 

    print("--- Don't forget to create the channel ---")

	
def transformMatrix ():

    '''
    bouge un objet vers l'origine du monde en fonction d'un point donne
    
    '''
    
    help(transformMatrix)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","transformToOrigin")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
 

vector basePtPos = point (0,"P",chi("basepoint")); 

matrix m = ident();

v@Z_axis =normalize( basePtPos - point(0,"P",neighbour(0,chi("basepoint"),1)));
v@Y_axis =normalize( cross(@Z_axis,basePtPos-point(0,"P",neighbour(0,chi("basepoint"),0))))*-1;
v@X_axis =normalize ( cross (@Z_axis,@Y_axis))*-1 ;

m*= set (@X_axis,@Y_axis,@Z_axis);
translate (m,basePtPos);

4@myMatrix = m;
m=invert(m);


@P*= m;





"""}) 
        wrangleBlur= wrangleSnippet.createOutputNode("attribwrangle","revertTransform")
        wrangleBlur.setInput(1,wrangleSnippet)
        wrangleBlur.setColor(pink)
        wrangleBlur.setParms({"snippet":"""
4@Um = point (1,"myMatrix",0);
@P*= @Um ;
"""}) 

    print("--- Don't forget to create the channel ---")