import maya.cmds as cmds


def create (joy, joycou):
    num=0
    numm=joycou+1 #joycの数+1
    renum=numm
    
    
    #親の取得
    par=cmds.listRelatives(joy, p=True)[0]

    #位置計算
    xiti=cmds.getAttr(f"{joy}.tx")
    deviti=xiti/(numm)

    #ジョイント作成
    for kaisu in range(joycou):
        num+=1
        renum-=1
        if num==1:
            #ベンドジョイント作成
            dupjoy=cmds.duplicate(par, po=True)[0]
            cmds.rename(dupjoy, f"{joy}_Bend")
            cmds.parent(f"{joy}_Bend", par)
            trax=cmds.getAttr(f"{joy}.tx")
            cmds.setAttr(f"{joy}_Bend.tx", trax)
           

            
            #ツイストジョイント作成
            dupjoys=cmds.duplicate(par, po=True)[0]
            cmds.rename(dupjoys, f"{joy}_Twist_Bace")
            cmds.parent( f"{joy}_Twist_Bace", par)
            cmds.setAttr(f"{joy}_Twist_Bace.tx", xiti-deviti*num)

            #クオータニオン・オイラー関連ノード作成
            cmds.createNode("eulerToQuat", name=f"Eq_{joy}_Twist_Bace")
            eq=f"Eq_{joy}_Twist_Bace"
            cmds.createNode("quatNormalize", name=f"Qn_{joy}_Twist_Bace")
            qn=f"Qn_{joy}_Twist_Bace"
            cmds.createNode("quatToEuler", name=f"Qe_{joy}_Twist_Bace")
            qe=f"Qe_{joy}_Twist_Bace"

            #接続
            cmds.connectAttr(f"{joy}.rotate", f"{eq}.inputRotate")
            for axis in "XW":
                cmds.connectAttr(f"{eq}.outputQuat{axis}", f"{qn}.inputQuat{axis}")
            cmds.connectAttr(f"{qn}.outputQuat", f"{qe}.inputQuat")
            for axis in "XYZ":
                cmds.connectAttr(f"{qe}.outputRotate{axis}", f"{joy}_Twist_Bace.rotate{axis}")

        
            #ベンド抽出
            mm=cmds.createNode("multMatrix", name=f"Mm_{joy}_Bace")
            dm=cmds.createNode("decomposeMatrix", name=f"Dm_{joy}_Bace")

            cmds.connectAttr(f"{joy}.matrix", f"{mm}.matrixIn[0]")
            cmds.connectAttr(f"{joy}_Twist_Bace.inverseMatrix", f"{mm}.matrixIn[1]")
            
            cmds.connectAttr(f"{mm}.matrixSum", f"{dm}.inputMatrix")
            for axis in "XYZ":
                cmds.connectAttr(f"{dm}.outputRotate{axis}", f"{joy}_Bend.rotate{axis}")

            cmds.parent(f"{joy}_Bend", f"{joy}_Twist_Bace")

            



        #制御可能ツイストジョイント
        dupjoys=cmds.duplicate(par, po=True)[0]
        cmds.rename(dupjoys, f"{joy}_Twist_{num}")
        cmds.parent(f"{joy}_Twist_{num}", par)
        cmds.setAttr(f"{joy}_Twist_{num}.tx", (xiti)-(deviti*num))
        cmds.addAttr(f"{joy}_Twist_{num}", longName="Weights", attributeType="float", maxValue=1, minValue=0, keyable=True)

        cmds.createNode("pairBlend", name=f"Pb_{joy}_{num}")
        cmds.setAttr(f"Pb_{joy}_{num}.rotInterpolation", 1)
        cmds.connectAttr(f"{qe}.outputRotate", f"Pb_{joy}_{num}.inRotate2")
        for axis in "XYZ":
            cmds.connectAttr(f"Pb_{joy}_{num}.outRotate{axis}", f"{joy}_Twist_{num}.rotate{axis}")
        cmds.connectAttr(f"{joy}_Twist_{num}.Weights", f"Pb_{joy}_{num}.weight")
        cmds.setAttr(f"{joy}_Twist_{num}.Weights", (1/numm)*renum)
        if 0.01>(1/numm)*renum: cmds.setAttr(f"{joy}_Twist_{num}.Weights", 0.01)


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
    sel=cmds.ls(sl=True, type="joint")
    create(sel[0], 2)

"""
#エラー用
def main():
    sel=cmds.ls(sl=True, type="joint")
    if not len(sel)==1:
        cmds.error("ジョイント個数が違います")

    cmds.undoInfo(ock=True)
    try:
        cmds.undoInfo(cck=True)
        create(sel[0], 2)
    except:
         cmds.undoInfo(cck=True)
         cmds.undo()
         print("b")
"""

if __name__ == "__main__":
    main()
