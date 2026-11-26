from maya import cmds

keyj=cmds.ls(sl=True)[0]

def one_keys(): #1軸アニメ
    cmds.currentTime(0)
    cmds.cutKey() #キー削除（初期化）
    cmds.setAttr(f"{keyj}.rz", 0)
    cmds.setKeyframe(f"{keyj}", breakdown=False)
    cmds.currentTime(20)
    cmds.setAttr(f"{keyj}.rz", 90)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 
    cmds.currentTime(30)
    cmds.setAttr(f"{keyj}.rz", 120)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 
    cmds.currentTime(40)
    cmds.setAttr(f"{keyj}.rz", 160)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 

def tree_anim():#3軸アニメ
    cmds.currentTime(0)
    cmds.cutKey() #キー削除（初期化）
    cmds.setAttr(f"{keyj}.rz", 0)
    cmds.setKeyframe(f"{keyj}", breakdown=False)    
    cmds.currentTime(10)
    cmds.setAttr(f"{keyj}.rz", 90)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 
    cmds.currentTime(20)
    cmds.setAttr(f"{keyj}.rz", -50)
    cmds.setKeyframe(f"{keyj}", breakdown=False)    
    cmds.currentTime(30) 
    cmds.setAttr(f"{keyj}.rz", 0)  
    cmds.setAttr(f"{keyj}.ry", 0)
    cmds.setKeyframe(f"{keyj}", breakdown=False)    
    cmds.currentTime(40)
    cmds.setAttr(f"{keyj}.ry", 90)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 
    cmds.currentTime(50)
    cmds.setAttr(f"{keyj}.ry", -30)
    cmds.setKeyframe(f"{keyj}", breakdown=False)
    cmds.currentTime(60)
    cmds.setAttr(f"{keyj}.ry", 0)
    cmds.setAttr(f"{keyj}.rx", 0)
    cmds.setKeyframe(f"{keyj}", breakdown=False)    
    cmds.currentTime(70)
    cmds.setAttr(f"{keyj}.rx", 90)
    cmds.setKeyframe(f"{keyj}", breakdown=False) 
    cmds.currentTime(80)
    cmds.setAttr(f"{keyj}.rx", -90)
    cmds.setKeyframe(f"{keyj}", breakdown=False)   



def main():
    tree_anim()

if __name__=="__main__":
    main()