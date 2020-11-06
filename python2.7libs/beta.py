import os 
import hou
def test():
    cachePath = "//storf/diskf/SuperHeros/044-045/houdini/fx/jmargelin/044-045_fx_flameMain_jmargelin/vdb/flameMilieu1/v0021"
            # check if agree with dependency
            
    
    try: 
        os.path.exists(cachePath)
        checkCache = hou.ui.displayMessage("le cache existe deja",buttons=('annule','ecrase',), default_choice=1)
        if checkCache == 0:
            print "rendu annule"
            return 0
        else:
            print "rendu ecrase"
            pass
    except:
        pass
test()




