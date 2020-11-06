import os,getpass,sys
import hou

def hkeepSave():
    # selection
    selection=hou.selectedItems()
    if len(selection)==0:
        hou.ui.displayMessage("empty selection")
        return

    # user filename
    userfilename = hou.ui.readInput("filename",buttons=("cancel","ok"),default_choice=1)
    #userfilename = hou.ui.readMultiInput("filename",("filename","send to (optional)"),buttons=("cancel","ok"),default_choice=1)
    if userfilename[0] == 0:
        return
    rootpath =  "//stord/diskd/BDD/houdini_bank"
    # rootpath = filePath()
    project=os.getenv("project")
    if project == None:
        project=""

    user=getpass.getuser()
    parent = selection[0].parent()
    nodetype = parent.type().name().upper()
	
    # filepath check
    # filepath = rootpath +"/" + user + "/" + project + "/Hkeep/" + nodetype
    filepath = rootpath +"/" + user + "/Hkeep/" + nodetype
    
    try:
        if os.path.isdir(filepath)==0:
            os.makedirs(filepath)
    except:
        try :
            hou.ui.displayMessage("failed to create dir")
        except:
            print "failed display message"
        print "failed to create dir"
        return

    # bdd filename
    filename = nodetype + "_"+''.join(userfilename[1].split())

    # save file
    parent.saveItemsToFile(selection,filepath + "/" + filename + ".cmd")
	
    copytext = hou.ui.readInput("copy text to clipbaord: ",buttons=("ok","Cancel"),default_choice=1,initial_contents=filepath + "/" + filename + ".cmd")
    if copytext[0]==0:
	    hou.ui.copyTextToClipboard(filepath + "/" + filename + ".cmd")
	
    print filepath + "/" + filename + ".cmd"
    
    # send message
#    if userfilename[1][1] != "":
#        to do SPARK
#        cmd = "Spark " + userfilename[1][1] + " -t \" hkeepload " + filepath + "/" + filename + ".cmd" + "\""
#        os.system(cmd)
#        print cmd

        # send by email
#        content = "hkeepload " + filepath + "/" + filename + ".cmd"
#        dest = userfilename[1][1]
#        hkSendMaill(dest,content)

def hkeepLoad():
    try :
        #htab = hou.ui.paneTabUnderCursor()
        htab = hou.ui.curDesktop().paneTabUnderCursor()
        parent = htab.pwd()
        nodetype = parent.type().name().upper()
    except:
        hou.ui.displayMessage("keep mouse cursor over the paneTab")
        return

    # filepath
    user=getpass.getuser()
    # rootfilepath=filePath()
    # filepath = rootfilepath + "/Hkeep/" + nodetype
	
    rootpath =  "//stord/diskd/BDD/houdini_bank"
    project=os.getenv("project")
    if project == None:
        project=""
	
    filepath = rootpath +"/" + user + "/" + project + "/Hkeep/" + nodetype

    Hkeepfile = hou.ui.selectFile(start_directory=filepath, title="select a file",file_type=hou.fileType.Cmd,pattern="*.cmd")
    if Hkeepfile == '':
        return

    fileType = os.path.basename(Hkeepfile).split("_")[0]
    if nodetype != fileType:
        hou.ui.displayMessage("the current netwotk view context didn't match the element you have selected")
        return

    parent.loadItemsFromFile(Hkeepfile)

def filePath():
	# split directory
    hipfilepath,hipfilename= os.path.split(hou.hipFile.path())

    normpath = os.path.normpath(hipfilepath)
    pathitems = normpath.split(os.sep)

    rootpath = hipfilepath
    if pathitems[-1].isdigit():
        pathitems.pop(-1)
        rootpath = "//"+reduce(os.path.join,pathitems).replace("\\","/")
    return rootpath


########################################
############## EMAIL ###################
########################################	
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def hkSendMaill(dest,content):
    user=os.environ['USER']
    server = smtplib.SMTP('smtp', 0)
    fromaddr = user + "@lacompagnievfx.com"
    toaddr = dest + "@lacompagnievfx.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "HKeep" 
    
    body = content
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    