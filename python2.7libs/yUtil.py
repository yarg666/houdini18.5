def getCam():
	import hou
	list = hou.node("/obj").allSubChildren()
	for i in list:
	    if i.type().name()== "cam":
	        camPath= i.path()
	        break
	    else :
	        camPath="/obj/cam1"
	return camPath        

def copy2clip(txt):
    from subprocess import check_call
    cmd='echo '+txt.strip()+'|clip'
    return check_call(cmd, shell=True)

def copy(txt):
    import PySide.QtGui as qtg
    app = qtg.QApplication.instance()
    clipboard = app.clipboard()
    string =txt
    clipboard.setText(string)

