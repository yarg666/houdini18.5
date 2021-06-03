import y
reload(y)

import mayaExport
reload(mayaExport)

def setCon():
    from cgev.pipeline.appconnector.connectorMenu import MenuHandler; MenuHandler.openShotWindow()
def saveWip():
    from cgev.pipeline.appconnector.connectorMenu import MenuHandler; MenuHandler.saveShotWindow(False)

import hou

from cgev.common import texts
from cgev.pipeline.data import session
from cgev.pipeline.process import server

def getValues(project, sequence, shot, task):

    projectObjAM = server.getProject(project)
    sequenceObjAm = server.getSequence(project, sequence)
    shotObjAM = server.getShot(project, sequence, shot)
    taskObjAM = server.getTask2(project, sequence, shot, task)

    projectName = projectObjAM.getName()
    projectId = projectObjAM.getId()
    sequenceName = sequenceObjAm.getName()
    sequenceId = sequenceObjAm.getId()
    shotName = shotObjAM.getName()
    shotId = shotObjAM.getId()

    if taskObjAM is not None:
        taskName = taskObjAM.getName().lower()
        taskId = taskObjAM.getId()
    else:
        taskName = task
        taskId = ""

    firstFrame = shotObjAM.getFrameStart()
    lastFrame = shotObjAM.getFrameEnd()

    return {texts.projectName: projectName,
            texts.projectId: projectId,
            texts.sequenceName: sequenceName,
            texts.sequenceId: sequenceId,
            texts.shotName: shotName,
            texts.shotId: shotId,
            texts.taskName: taskName,
            texts.taskId: taskId,
            texts.firstFrame: firstFrame,
            texts.lastFrame: lastFrame,
            }

def yBuild():

    import os
    import hou
    import ftrack
    from cgev.pipeline.data import session
    
    
    scene_path = hou.hipFile.path()
    project = scene_path.split('/')[4]
    sequence, shot = scene_path.split('/')[5].split('-')
    task = scene_path.split('/')[7]
    
    values = getValues(project, sequence, shot, task)
    context = session.getContext()
    context.setContext(values)
    session.setContext(context)
    #current node
    node = hou.pwd()
    #set context
    #...
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
    resx = shot.get("Render_Rez_X")
    resy = shot.get("Render_Rez_Y")
    pixelRatio = shot.get("pixelAspect")
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
    query += '(type.name is "Camera" or type.name is "Geometry" or type.name is "Animation")'
    query = query.format(projName, seqName, shotName)
    assets = sessionFT.query(query)
    obj = hou.node("/obj")
    children = obj.children()
    childName=[]
    
    for i in children :
        childName.append(i.name())
        
    if "HOUDINI_SCALE" not in childName:
        houdiniScale=obj.createNode("null","HOUDINI_SCALE")#houdini scale
        houdiniScale.parm("scale").set("0.01")
        houdiniScale.setPosition([3,10])
    if "CG_IMPORT" in childName:
        hou.node("/obj/CG_IMPORT").destroy()

    cgevImport = hou.node("/obj/HOUDINI_SCALE/").createOutputNode("geo","CG_IMPORT")
    cgevImport.setPosition([5,7])
    importMerge = cgevImport.createNode("merge","collect_abc")        
            
    # Asset loop
    for asset in assets:
        # Get last version
        version = asset['versions'][-1]
        # Last version's components loop
        for component_obj in version['components']:
            # Only care about the alembic component
            if component_obj['name'] == 'alembic':
                file_path = component_obj['component_locations'][0]
                file_path = file_path['resource_identifier'].replace('\\', '/')
                if "camera" in file_path:
                    #create camera
                    if asset.values()[0] in childName:
                        hou.node("/obj/"+asset.values()[0]).destroy()
                    camArch =hou.node("/obj/HOUDINI_SCALE/").createOutputNode("alembicarchive",asset.values()[0])
                    camArch.parm("fileName").set(file_path)
                    camArch.setPosition([0.8,7])
                    camArch.parm("buildHierarchy").pressButton()
                    #resolution
                    #imagePlane
                    print ("cam")
                else :
                    #create geometry
                    newAbc = cgevImport.createNode("alembic",asset.values()[0])
                    newAbc.moveToGoodPosition()
                    newAbc.parm("fileName").set(file_path)
                    group = newAbc.createOutputNode("group",asset.values()[0]+"_grp")
                    group.parm("crname").set(asset.values()[0])
                    importMerge.setNextInput(group)
                print file_path
                break
    #get image plane 
    for asset in assets:
        # Get last version
        version = asset['versions'][-1]
        # Last version's components loop
        for component_obj in version['components']:
            # Only care about the mayaComponent component
            if component_obj['name'] == 'imagePlanePath':
                file_path = component_obj['component_locations'][0]
                file_path = file_path['resource_identifier'].replace('\\', '/')
                print file_path
                break                
    #set camera background et resolution
    list = hou.node("/obj").allSubChildren()
    for i in list:
        if i.type().name()== "cam":
            i.parm("vm_background").set(file_path)
            i.parm("resx").set(resx)
            i.parm("resy").set(resy)
            i.parm("aspect").deleteAllKeyframes()
            i.parm("aspect").set(pixelRatio)
            break
                
    
    importMerge.moveToGoodPosition()
    nullImport = importMerge.createOutputNode("null","out_CG_IMPORT")
    
def fxTemp():
    import hou

    obj = hou.node("/obj")

    newFx = obj.createNode("geo","newFx")
    newFx.setPosition([0,10])
    cgInput=newFx.createNode("cgIn","inputAsset")
    cgRender = cgInput.createOutputNode("renderGeo")
    fxName = cgRender.name()[:-6]
    newFx.setName(fxName+"_fx")
    null = hou.node("/obj/"+newFx.name()+"/"+fxName)
    null.moveToGoodPosition()
    null.parm("newparameter").pressButton()
    