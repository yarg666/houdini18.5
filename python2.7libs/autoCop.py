
def autoCop():
    from yUtil import getCam
    import nodesearch
    import hou
    #color
    black=hou.Color((0,0,0))
    list = hou.node("/obj").allSubChildren() #recherche les nodes cgMantra
    matchType = nodesearch.NodeType("CG::cgmantra*")
    matchName = nodesearch.Name("*")
    match = nodesearch.Group([matchType,matchName])
    net = hou.node("/out/") #le chemin out et  un copNet si il n existe pas
    if hou.node('/out/autoCop') == None:
        copnet = net.createNode("cop2net","autoCop")
    else :
        copnet = hou.node('/out/autoCop/')
    camPath = getCam() # aller rechercher l info backPlate dans la cam
    cam = hou.node(camPath)
    backPlateParm = cam.parm("vm_background")

    if (hou.node('/out/autoCop/backPlate')) == None: # backplate if dont exist et set
        backPlate = copnet.createNode("file","backPlate")
        backPlate.parm("filename1").setFromParm(backPlateParm)
        backPlate.setColor(black)
        backPlate.setRenderFlag(True)    
    # remplir autocop
    list = [] #recuperre tout les cgmantra
    for node in match.nodes(net,recursive =True):
        list.append(node.name())
    preSelect=[] #verifie qui est deja dans autoCop et update image path
    for i in list:
        if hou.node("/out/autoCop/"+"/"+i+"/")==None:
            preSelect.append(list.index(i)) 
        else :
            outputPath = hou.node("/out/"+i).parm("vm_picture")
            fileCopNode = hou.node("/out/autoCop/"+"/"+i+"/")
            fileCopNode.parm("filename1").setFromParm(outputPath) # maj path

    selListe=[]

    if len(preSelect) > 0 : 
        selListe= hou.ui.selectFromList(list,preSelect,clear_on_cancel=True) #ui select list

    for i in selListe:
        name = list[i]
        outputPath = hou.node("/out/"+name).parm("vm_picture")
        fileCopNode = hou.node("/out/autoCop/"+"/"+name+"/")
        if fileCopNode == None : #si le node de rendu existe pas creer 
            child = hou.node('/out/autoCop').children()
            for i in child: #check for render flag in child
                if i.isGenericFlagSet(hou.nodeFlag.Render) is True:
                    lastNode = i
            fileCop= copnet.createNode("file",name) # creer file dans autoCop
            add = lastNode.createOutputNode("add","add")
            add.setInput(1,fileCop,0)
            add.setName("add_"+add.input(1).name())
            add.setRenderFlag(True)
            fileCopNode=fileCop    
        fileCopNode.parm("filename1").setFromParm(outputPath) # set path

    

def updateAutoCop():
    import nodesearch
    import hou

    matchType = nodesearch.NodeType("CG::cgmantra*")
    matchName = nodesearch.Name("*")
    match = nodesearch.Group([matchType,matchName])
    net = hou.node("/out/") #le chemin out et  un copNet si il n existe pas
    # remplir autocop
    list = [] #recuperre tout les cgmantra
    for node in match.nodes(net,recursive =True):
        list.append(node.name())
    for i in list:
        if hou.node("/out/autoCop/"+"/"+i+"/")!=None: 
            outputPath = hou.node("/out/"+i).parm("vm_picture")
            fileCopNode = hou.node("/out/autoCop/"+"/"+i+"/")
            fileCopNode.parm("filename1").setFromParm(outputPath) # maj path

def copyPasteNuke():
    import yUtil
    reload(yUtil)
    import nodesearch
    import hou
    #color
    list = hou.node("/obj").allSubChildren() #recherche les nodes cgMantra
    matchType = nodesearch.NodeType("CG::cgmantra*")
    matchName = nodesearch.Name("*")
    match = nodesearch.Group([matchType,matchName])
    net = hou.node("/out/") #le chemin out et  un copNet si il n existe pas

    list = [] #recuperre tout les cgmantra
    for node in match.nodes(net,recursive =True):
        list.append(node.name())
        
    selListe= hou.ui.selectFromList(list)

    prefix = """
    Read {
     file """
    suffix = """ 
     localizationPolicy off
    }"""

    clipboard = ""

    for i in selListe:
        name = list[i]
        outputPath = hou.node("/out/"+name).parm("vm_picture").eval()
        clipboard  += prefix + outputPath[:-8]+"%04d.exr" + suffix


    popup = hou.ui.readInput("faire ctrl+c puis ctrl+v dans nuke",initial_contents=clipboard)


