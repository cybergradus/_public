global plpy_transformsRealign
def plpy_transformsRealign(bake=True,link=True,*arg):
    
    selected = mc.ls(sl=True)
    current_time = mc.currentTime(q=True)
    attributes=['translate','rotate']
    pc = []
    
    if not arg:
        arg = selected[:2]
    
    #print(arg)
    
    if not arg:
            return
    if len(arg)==1:
        #print('len(arg)==1; arg:',arg)
        arg = [arg[0],arg[0]]
        #print('arg:',arg)
            
    keys = mc.keyframe(arg[0],q=True,attribute=attributes)
    k_set = set(keys)
    keys = list(k_set)
    keys.sort()
    #print(k_set)
    #print(keys)
    
    #print('arg:',arg)
    #print('arg[0]==arg[1]:',arg[0]==arg[1])
    
    if bake:
        #print('bake')
        if len(arg)>=2 and arg[0]==arg[1]:
            mc.bakeResults(  arg[0],simulation=True,pok=True,at=attributes,time=( list(keys)[0],list(keys)[-1] )  )
            pc_targets = mc.parentConstraint(q=True,targetList=True)
            if pc_targets:
                arg[0]=pc_targets[0]
                pc = mc.parentConstraint(arg[1],q=True)
        if len(arg)>=2 and arg[0]!=arg[1]:
            #mc.currentTime(keys[0])
            pc = mc.parentConstraint(arg[0],arg[1],mo=True)[0]
            mc.setAttr(pc+'.interpType',2)
            mc.bakeResults(  arg[1],simulation=True,pok=True,at=attributes,time=( list(keys)[0],list(keys)[-1] )  )
            mc.delete(pc)
                        
        if link:
            pc = mc.parentConstraint(arg[1],arg[0],mo=True)[0]
            mc.setAttr(pc+'.interpType',2)

        return  
    
    #print('pfff',arg[0],arg[1])
    
    if arg[0] == arg[1]:
        #print('wha?')
        pc_targets = mc.parentConstraint(q=True,targetList=True)
        if pc_targets:
            arg[0]=pc_targets[0]
        pc = mc.parentConstraint(arg[1],q=True)
        #print(pc)
        if not pc:
            return

    else:
        pc = mc.parentConstraint(arg[0],arg[1],mo=True)[0]
        mc.setAttr(pc+'.interpType',2)    
    
    for k in keys:
        mc.currentTime(k)
        mc.setKeyframe(arg[1],attribute=attributes)
        mc.setAttr(arg[1]+'.blendParent1',1)  
    
    for k in keys:
        #print(k)
        for a in ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']:
            #print(arg[0],a)
            #print(type(arg[0]),type(a))
            itt = mc.keyTangent(arg[0]+'.'+a, q=True, time=(k,k), itt=True)
            ott = mc.keyTangent(arg[0]+'.'+a, q=True, time=(k,k), ott=True)
            #print(k,itt,ott)
            if itt and ott:
                mc.keyTangent(arg[1]+'.'+a,time=(k,k),itt=itt[0],ott=ott[0])
                        
    mc.currentTime(current_time)
    if pc:
        mc.delete(pc)
        
    if link:
        pc = mc.parentConstraint(arg[1],arg[0],mo=True)[0]
        mc.setAttr(pc+'.interpType',2)

        

    
    
            