import hou 

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
		
