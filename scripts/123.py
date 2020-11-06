import hou 
inc= 0
black=hou.Color((0,0,0))
obj = hou.node("/obj")
netBox = ""
netBoxSize= hou.Vector2(0.5,5.0)
myListe = ("LIGHTING/CAMERA/MATERIAL","ASSET/MODELING","FX","RENDERING","MAYA_EXPORT")


matnet = obj.createNode("matnet","matnet1")
matnet.move(hou.Vector2(5.0,2.0))

env = obj.createNode("envlight","envlight")
env.move(hou.Vector2(5.0,3.0))
env.setParms({"env_map":"$HFS/houdini/pic/hdri/HDRIHaven_kiara_5_noon_2k.rat"})




for i in myListe:
	inc+=1
	
	netBox = hou.item("/obj").createNetworkBox()
	netBox.resize(netBoxSize)
	netBox.setComment(i)
	netBox.setColor(black)
	netBox.move(hou.Vector2(4.0*inc,0.0))


