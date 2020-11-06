#librairies
import os
import hou
import ftrack

#variables


node = hou.pwd()

def range(node):

	shotId = os.getenv('FTRACK_SHOTID')

	shot = ftrack.Shot(id=shotId)

	#range
	startFrame = os.getenv('FS')
	endFrame = os.getenv('FE')
	print startFrame
	print endFrame
	pim = shot.get("pim")
	dim = shot.get("dim")
	print pim
	print dim

	node.parm("range1").set(startFrame)
	node.parm("range2").set(endFrame)
	node.parm("pimDim1").set(pim)	
	node.parm("pimDim2").set(dim)




"""from ftrackplugin import ftrackDialogs

def publishA7(A7):
    A7 = hou.pwd()
    my_asset_name = A7.parm("name").eval()
    asset_type = A7.parm("datatype").eval()
    if asset_type=="abc":
        publish_type="fx"
    else:
        publish_type="hcache"
    window = ftrackDialogs.ftrackPublishAssetQt(assetNode=A7)
    window.setAssetType(publish_type)
    window.setAssetName(my_asset_name)
    window.emit_published.connect(partial(getPublishResult,A7))
    window.show()
    
    
def getPublishResult(A7,publishedComponents):
    #A7=hou.pwd()
    if publishedComponents :
        A7.parm("publishlock").set(1)
        houCgevRender.cacheXml(A7)
        houCgevRender.cacheXmlCheck(A7)
        houCgevRender.setColor(A7)
        print "Publish Canceled success"
    else:
        print "Publish Canceled"
    print "publishedComponents finished"
    """


