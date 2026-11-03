import maya.cmds as cmds


def off(count):    #null作成
    slobj=cmds.ls(sl=True)
    num=0
    for selectobj in slobj:
        offset=cmds.group(empty=True)
        cmds.rename(f"{offset}", f"{selectobj}_Off")
        cmds.matchTransform(f"{selectobj}_Off", f"{selectobj}", pos=True, rot=True)

        for nums in range(count):
            num+=1
            offsets=cmds.group(empty=True)
            cmds.rename(f"{offsets}", f"{selectobj}_{num}")
            cmds.matchTransform(f"{selectobj}_{num}", f"{selectobj}", pos=True, rot=True)
            if num==1:
                cmds.parent(f"{selectobj}_{num}",f"{selectobj}_Off")
            if num>1:
                numm=num-1
                cmds.parent(f"{selectobj}_{num}", f"{selectobj}_{numm}")



            
def dup(rename,): #オブジェクトコピー
    slobj=cmds.ls(sl=True)    
    motoobj=slobj[-1]   
    for selectobj in slobj:
        #最後に選択したものは複製しない
        if selectobj==motoobj: continue
        #複製
        dupobj=cmds.duplicate(f"{motoobj}")[0]
        cmds.rename(f"{dupobj}", f"{selectobj}_{rename}")

        #位置の一致
        cmds.matchTransform(f"{selectobj}_{rename}", f"{selectobj}", pos=True, rot=True)


def off_dup(rename, count):    #null+複製
    slobj=cmds.ls(sl=True)
    motoobj=slobj[-1]
    num=0
    for selectobj in slobj:
        num=0
        #最後に選択したものは複製しない
        if selectobj==motoobj: continue
        #null
        offset=cmds.group(empty=True)
        cmds.rename(f"{offset}", f"{selectobj}_Off")
        cmds.matchTransform(f"{selectobj}_Off", f"{selectobj}", pos=True, rot=True)
        #Off以外のグループ作成
        for nums in range(count):
            num+=1
            offsets=cmds.group(empty=True)
            cmds.rename(f"{offsets}", f"{selectobj}_{num}")
            cmds.matchTransform(f"{selectobj}_{num}", f"{selectobj}", pos=True, rot=True)
            if num==1:
                cmds.parent(f"{selectobj}_{num}",f"{selectobj}_Off")
            if num>1:
                numm=num-1
                cmds.parent(f"{selectobj}_{num}", f"{selectobj}_{numm}")


        #複製
        dupobj=cmds.duplicate(f"{motoobj}")[0]
        cmds.rename(f"{dupobj}", f"{selectobj}_{rename}")

        #位置の一致
        cmds.matchTransform(f"{selectobj}_{rename}", f"{selectobj}_Off", pos=True, rot=True)

        if num==0:
            cmds.parent(f"{selectobj}_{rename}", f"{selectobj}_Off")

        if num!=0:
            cmds.parent(f"{selectobj}_{rename}", f"{selectobj}_{num}")

        cmds.makeIdentity(f"{selectobj}_{rename}", apply=True, rotate=True, translate=True)
        



        

def main(mode, ren ,cou): #モード複製名の変更、Off下のグループ数
    if mode=="off": off(ren, cou)
    if mode=="dup": dup(ren, cou)
    if mode=="off_dup": off_dup(ren, cou)




if __name__=="__main__":
    main()