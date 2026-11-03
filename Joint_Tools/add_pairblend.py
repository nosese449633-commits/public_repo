import maya.cmds as cmds
joy=1 #複製数

def pair(joycou):
    joyn=cmds.ls(sl=True, type="joint")[0]
    num=0
    

    for jnt in range(joycou):
        num+=1
        
        #ジョイント作成
        dup=cmds.duplicate(joyn, po=True)[0]
        cmds.rename(dup, f"{joyn}_Wt_{num}")
        motor=cmds.getAttr(f"{joyn}.radius")
        cmds.setAttr(f"{joyn}_Wt_{num}.radius", motor+1)
        

        #pairBlend
        cmds.createNode("pairBlend", name=f"Pb_Wt_{joyn}_{num}")
        cmds.connectAttr(f"{joyn}.rotate", f"Pb_Wt_{joyn}_{num}.inRotate2")
        for axis in "XYZ":
            cmds.connectAttr(f"Pb_Wt_{joyn}_{num}.outRotate{axis}", f"{joyn}_Wt_{num}.rotate{axis}")

        #Weightアトリビュート追加
        cmds.addAttr(f"{joyn}_Wt_{num}", longName="Weights", attributeType="float", maxValue=1, minValue=0, keyable=True)
        cmds.connectAttr(f"{joyn}_Wt_{num}.Weights", f"Pb_Wt_{joyn}_{num}.weight")
        cmds.setAttr(f"{joyn}_Wt_{num}.Weights", 0.5)

    labe()


      
#ジョイントラベル
def labe():
    alljoy=cmds.ls(type="joint")

    for ajoy in alljoy:
        lside=ajoy.find("L_")
        rside=ajoy.find("R_")
        if lside !=-1:
            print("左")
            cmds.setAttr(f"{ajoy}.side", 1)
            cmds.setAttr(f"{ajoy}.type", 18)
            rejoyname=ajoy.replace("L_", "")
            cmds.setAttr(f"{ajoy}.otherType", rejoyname, type="string")
            continue
        if rside !=-1: 
            print("右")
            cmds.setAttr(f"{ajoy}.side", 2)
            cmds.setAttr(f"{ajoy}.type", 18)
            rejoyname=ajoy.replace("R_", "")
            cmds.setAttr(f"{ajoy}.otherType", rejoyname, type="string")
            continue

        cmds.setAttr(f"{ajoy}.side", 0)
        cmds.setAttr(f"{ajoy}.type", 18)
        cmds.setAttr(f"{ajoy}.otherType", ajoy, type="string")        
        

"""
#エラー用
def main():
    sel=cmds.ls(sl=True, type="joint")
    if not len(sel)==1:
        cmds.error("ジョイント個数が違います")

    cmds.undoInfo(ock=True)
    try:
        pair(2) #ジョイント数を入力
        cmds.undoInfo(cck=True)
    except:
        cmds.undoInfo(cck=True)
        cmds.undo()
"""

def main():
    pair(1)


if __name__ == "__main__":
    main()