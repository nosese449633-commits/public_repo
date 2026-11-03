import maya.cmds as cmds

def joymain(axis):
    renum=0
    num=0
    numm=0
    oyajoi={}
    #ジョイントミラー
    joy=cmds.ls(sl=True)
    mjoy=cmds.mirrorJoint(f"{joy[0]}", mb=True, mirrorYZ=True, sr=["L_", "R_"])[0]

    #ミラーしたジョイントの選択
    cmds.select(hi=True)
    mjoys=cmds.ls(sl=True)
    

    #ミラージョイントの親子関係を外す
    for name in mjoys:
        renum-=1
        num+=1
        mjois=mjoys[renum]

        oyajoi[f"child{num}"]=f"{mjois}"
        oyajoi[f"oya{num}"]=cmds.listRelatives(f"{mjois}",p=True)

        cmds.parent(f"{mjois}", world=True)

        #とある軸に180を入力
        if axis=="Y":
            cmds.setAttr(f"{mjois}.rotateZ", 180)
            cmds.makeIdentity(f"{mjois}", apply=True, rotate=True)


        if axis=="Z":
            cmds.setAttr(f"{mjois}.rotateY", 180)
            cmds.makeIdentity(f"{mjois}", apply=True, rotate=True)

        if axis=="X":
            cmds.setAttr(f"{mjois}.rotateZ", 180)
            cmds.makeIdentity(f"{mjois}", apply=True, rotate=True)

        


    #親子関係修復作業
    for reoya in range(num):
        numm+=1
        cmds.parent(oyajoi[f"child{numm}"],oyajoi[f"oya{numm}"])

    labe()

#ジョイントラベル
def labe():
    alljoy=cmds.ls(type="joint")

    for ajoy in alljoy:
        lside=ajoy.find("L_")
        rside=ajoy.find("R_")
        if lside !=-1:
            cmds.setAttr(f"{ajoy}.side", 1)
            cmds.setAttr(f"{ajoy}.type", 18)
            rejoyname=ajoy.replace("L_", "")
            cmds.setAttr(f"{ajoy}.otherType", rejoyname, type="string")
            continue
        if rside !=-1:
            cmds.setAttr(f"{ajoy}.side", 2)
            cmds.setAttr(f"{ajoy}.type", 18)
            rejoyname=ajoy.replace("R_", "")
            cmds.setAttr(f"{ajoy}.otherType", rejoyname, type="string")
            continue

        cmds.setAttr(f"{ajoy}.side", 0)
        cmds.setAttr(f"{ajoy}.type", 18)
        cmds.setAttr(f"{ajoy}.otherType", ajoy, type="string")


    

def main():
    joymain("Y")#前方向の軸を何にしたいか（-YなどもYでOK）

if __name__ == "__main__":
    main()