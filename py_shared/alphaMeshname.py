# adds alpha attributes to the first node of the selection or to 'ROOT' node if it exists and no selection given

import maya.cmds as mc

def plpy_alphaMeshname():
    attributeHolder = plpy_alphaMeshnameGetAttributeHolder()
    attrs = mc.listAttr(attributeHolder, string = 'alpha_*')
    if attrs != None:
	    for attr in attrs:
	    	mc.deleteAttr(attributeHolder + "." + attr)
    #print(attributeHolder)
    plpy_alphaMeshnameAttrs(attributeHolder)
    plpy_alphaMeshnameConnect(attributeHolder)
	

def plpy_alphaMeshnameAttrs(attributeHolder):
    
    #attributeHolder = plpy_alphaMeshnameAttributeHolder()
    
    selection = mc.ls(sl=True)
    
    if attributeHolder:
        #print "do!"
        #"""

        if not selection:
        	meshes = mc.ls(type = 'mesh')
        else:
        	meshes=plpy_getShapes()

        geo = sorted(set(mc.listRelatives(meshes, parent = True)))
        print geo
        for g in geo:
            pass
            print g
            mc.addAttr(attributeHolder, longName = 'alpha_' + g, keyable = True, minValue = 0, maxValue = 1, defaultValue = 1)
			

def plpy_alphaMeshnameConnect(attributeHolder):
    
    #attributeHolder = plpy_alphaMeshnameAttibuteHolder()
    attrs = set()
    meshes = set(  mc.listRelatives( plpy_getShapes(), parent = True )  )
    
    for i in meshes:
        #print(i)
        if mc.ls(i + ".alpha"):
            #print(i + ".alpha")
            attrs.update({str(i + ".alpha")})
        else:
            #print(i + ".visibility")
            attrs.update({str(i + ".visibility")})
    for a in list(attrs):
        mc.connectAttr(a, attributeHolder + ".alpha_" + a.split('.')[0], force = True)
        #print(attributeHolder + ".alpha_" + a.split('.')[0])
        #print(type(a))
        #pass
    return(list(attrs))
	

def plpy_alphaMeshnameGetAttributeHolder():

    attributeHolder = None
    
    if mc.ls('ROOT', type = 'joint') and not mc.ls(sl=True):
        print("'ROOT' joint found")
        attributeHolder = 'ROOT'
        print("using 'ROOT' node as attributeHolder")
    else:
        print("'ROOT' joint not found")
        if mc.ls(sl = True):
            attributeHolder = mc.ls(sl = True, long=True)[0]
            print("using selected node: '%s' as attributeHolder" %attributeHolder)
        else:
            print('nothing is selected to use as attributeHolder')
            
    return attributeHolder
	
	
def plpy_alphaMeshnameConnectReverse():

    alphaMeshnameAttrs = mc.listAttr('ROOT', string = 'alpha_*')
    for i in alphaMeshnameAttrs:
        print i
        mc.connectAttr('ROOT.' + i, i.replace('alpha_', '') + '.visibility', force = True)
		

plpy_alphaMeshname()