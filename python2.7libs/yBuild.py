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


def yBuild():

    import os
    import hou
    import ftrack
    from cgev.pipeline.data import session
    
    #current node
    node = hou.pwd()
    #shot id
    shotId = os.getenv('FTRACK_SHOTID')
    shot = ftrack.Shot(id=shotId)
    # names
    shotName = shot.getName()
    seqName = os.getenv('sequence')
    projName = os.getenv('PROJECT')
    #range var
    startFrame = os.getenv('FS')
    endFrame = os.getenv('FE')
    pim = shot.get("pim")
    dim = shot.get("dim")
    #shot description var
    description = shot.get("description")
    #set parm
    node.parm("range1").set(startFrame)
    node.parm("range2").set(endFrame)
    node.parm("pimDim1").set(pim)   
    node.parm("pimDim2").set(dim)
    node.parm("shot").set(description)
    #get asset path last version
    #delete and recreate import ftrack with all last asset
    #get cam path last version
    #delete cam and replace with last cam

    sessionFT = session.getSessionFT()
    
    query = 'Asset where parent.parent.parent.name is "{}" and '
    query += 'parent.parent.name is "{}" and parent.name is "{}" and '
    query += '(type.name is "Geometry")'
    query = query.format(projName, seqName, shotName)
    assets = sessionFT.query(query)
    obj = hou.node("/obj")
    #destroy cgev import 
    try :
        hou.node('/obj/CGEV_IMPORT').destroy()
    except : 
        pass
    #create cgevf import 
    cgevImport = obj.createNode("geo","CGEV_IMPORT")
    # Asset loop
    for asset in assets:
        # Get last version
        version = asset['versions'][-1]
        # Last version's components loop
        for component_obj in version['components']:
            # Only care about the mayaComponent component
            if component_obj['name'] == 'alembic':
                file_path = component_obj['component_locations'][0]
                file_path = file_path['resource_identifier'].replace('\\', '/')
                print file_path
                break