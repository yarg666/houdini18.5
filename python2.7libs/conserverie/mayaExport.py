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

			#tranform
			transform=groupDel.createOutputNode("xform")
			transform.setParmExpressions({"scale":"ch('../MAYA_SCALE')"})
			#export type
			try:
				if transform.geometry().prims()[0].type().name() == 'VDB' or transform.geometry().prims()[0].type().name() == 'Volume':
					extension = "vdb"
					vdbConvert = transform.createOutputNode("convertvdb")
					null = vdbConvert.createOutputNode("null","vdb")
					null.setColor(blue)
					vdbConvert.setParms({"conversion":"vdb"})
				else :
					extension = "abc"
					null = transform.createOutputNode("null","abc")
					print "ok"	
			except :
				extension = "abc"
				null = transform.createOutputNode("null","abc")
				print "okcoral"	
	

				
			#renderGeo
			geoRender= null.createOutputNode("renderGeo",getName+"_maya")
			geoRender.setParms({"datatype":extension})