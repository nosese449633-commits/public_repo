from maya import cmds

def create(nodes):
    #条件設定
    ziku="XYZ"
    joycou=2 #ここを変更
    num=0
    numm=3 #joycouの個数+1
    renum=numm
    

    #親ジョイントの取得
    par=cmds.listRelatives(f"{nodes[0]}", p=True)[0]

    #位置計算(子供X軸数値÷ジョイント個数+1)
    xiti=cmds.getAttr(f"{nodes[1]}.tx")
    deviti=xiti/numm

    #基礎ジョイントの作成
    for jnt in range(joycou):
        num+=1
        dup=cmds.duplicate(f"{nodes[0]}", po=True)[0]
                
        if num==1: cmds.rename(dup, f"{nodes[0]}_bend")
        if num==2: cmds.rename(dup, f"{nodes[0]}_twist")

    #親子付け・位置調整
    cmds.parent(f"{nodes[0]}_twist",f"{nodes[0]}_bend")
    cmds.setAttr(f"{nodes[0]}_twist.tx", float(deviti))

    #ベンド抽出
    cmds.createNode("aimConstraint", name=f"AC_{nodes[0]}_bend")
    for axis in "XYZ":
        cmds.connectAttr(f"{nodes[0]}.rotate{axis}", f"AC_{nodes[0]}_bend.rotate{axis}")

    
    cmds.connectAttr(f"{nodes[1]}.translate", f"AC_{nodes[0]}_bend.target[0].targetTranslate")
    cmds.connectAttr(f"AC_{nodes[0]}_bend.matrix", f"AC_{nodes[0]}_bend.target[0].targetParentMatrix")
    for axis in "XYZ":
        cmds.connectAttr(f"AC_{nodes[0]}_bend.constraintRotate{axis}", f"{nodes[0]}_bend.rotate{axis}")
    
    #ツイスト抽出
    cmds.createNode("multMatrix", name=f"Mm_{nodes[1]}")
    cmds.createNode("decomposeMatrix", name=f"Dm_{nodes[1]}")
    cmds.connectAttr(f"{nodes[0]}.matrix", f"Mm_{nodes[1]}.matrixIn[0]")
    cmds.connectAttr(f"{nodes[0]}_bend.inverseMatrix", f"Mm_{nodes[1]}.matrixIn[1]")
    cmds.connectAttr(f"Mm_{nodes[1]}.matrixSum", f"Dm_{nodes[1]}.inputMatrix")
    for axis in "XYZ":
        cmds.connectAttr(f"Dm_{nodes[1]}.outputRotate{axis}", f"{nodes[0]}_twist.rotate{axis}")

    num=0
    
    #複数ジョイント作成
    for djn in range(joycou):
        num+=1
        renum-=1
        dupjoy=cmds.duplicate(f"{nodes[0]}", po=True)[0]
        cmds.rename(dupjoy, f"{nodes[0]}_twist_{num}")
        cmds.parent(f"{nodes[0]}_twist_{num}", f"{nodes[0]}_bend")
        cmds.setAttr(f"{nodes[0]}_twist_{num}.tx", deviti*num)

        #接続
        cmds.createNode("pairBlend", name=f"Pb_{nodes[0]}_{num}")
        cmds.setAttr(f"Pb_{nodes[0]}_{num}.rotInterpolation", 1)

        cmds.connectAttr(f"Dm_{nodes[1]}.outputRotate", f"Pb_{nodes[0]}_{num}.inRotate2")
        for axis in ziku:
            cmds.connectAttr(f"Pb_{nodes[0]}_{num}.outRotate{axis}", f"{nodes[0]}_twist_{num}.rotate{axis}")
            
        #Weightアトリビュート追加
        cmds.addAttr(f"{nodes[0]}_twist_{num}", longName="Weights", attributeType="float", maxValue=1, minValue=0, keyable=True)
        cmds.connectAttr(f"{nodes[0]}_twist_{num}.Weights", f"Pb_{nodes[0]}_{num}.weight")
        cmds.setAttr(f"{nodes[0]}_twist_{num}.Weights", (1/numm)*num)

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
        

"""" #確認用キューブ
    
    cmds.polyCube(name="bend")
    cmds.polyCube(name="twist")
    cmds.parent("bend",f"{nodes[0]}_bend")
    cmds.parent("twist",f"{nodes[0]}_twist")
    cmds.setAttr("twist.tx", 0)
"""

#エラー用
def main():
    sel=cmds.ls(sl=True, type="joint")
    if not len(sel)==2:
        cmds.error("ジョイント個数が違います")

    cmds.undoInfo(ock=True)
    try:
        create(sel)
        cmds.undoInfo(cck=True)
    except:
        cmds.undoInfo(cck=True)
        cmds.undo()

"""

def main():
    sel=cmds.ls(sl=True, type="joint")
    create(sel)
"""
if __name__ == "__main__":
    main()

