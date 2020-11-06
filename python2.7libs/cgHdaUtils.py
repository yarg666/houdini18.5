#
# houdini hda tools
# Author: fx boussard
# Version v 0.00.0, upgrade hda to theire last version
# date: 2019/05/20

import hou
def updateA7(node):
	typenamecomponents = node.type().nameComponents()
	studio = typenamecomponents[1]
	typename = typenamecomponents[2]
	choice = hou.ui.displayMessage("what ?", buttons=["selected A7 only","all A7s in this node","all A7s in the file","Cancel"],default_choice=3)
	if choice == 3:
		return
	elif choice == 0:
		getlastVersion(node,typename,studio)
	elif choice == 1:
		node = node.parent()
		recursiveFindNode(node,typename,studio)
	elif choice == 2:
		node = hou.node("/")
		recursiveFindNode(node,typename,studio)
	
def recursiveFindNode(node,reftypename,refstudio="CG"):
	childrens = node.children()
	for n in childrens:
		recursiveFindNode(n,reftypename,refstudio)
		getlastVersion(n,reftypename,refstudio)

def getlastVersion(node, reftypename,refstudio="CG"):
	typenamecomponents = node.type().nameComponents()
	studio = typenamecomponents[1]
	typename = typenamecomponents[2]
	if typename == reftypename and studio == refstudio:
		if not node.isLockedHDA():
			print node.name() + " is unlocked, no upgrade is allowed"
			return	
		a7name = node.name()
		parenta7name = node.parent().name()
		libraryPath = node.type().definition().libraryFilePath()
		definitions = hou.hda.definitionsInFile(libraryPath)
		higherdefinition = ""
		higherversion = 0.0
		versionslist=""
		for d in definitions:
			dtypenamecomponents = d.nodeTypeName().split("::")
			dstudio = dtypenamecomponents[0]
			dtypename = dtypenamecomponents[1]
			dversion = float(dtypenamecomponents[2])
			# print "version: " + str(dversion)
			versionslist += "v" + str(dversion) + " "
			if dversion >= higherversion:
				higherversion=dversion
				higherdefinition = d
		print "versions = " + versionslist
		print "higher version = v" + str(higherversion)
		lasttype = higherdefinition.nodeType()
		a7 = node.changeNodeType(lasttype.name(), keep_name=True, keep_parms=True, keep_network_contents=True, force_change_on_node_type_match=False)
		a7.matchCurrentDefinition()
		print "Upgrade: " + parenta7name + "/" + a7name
	