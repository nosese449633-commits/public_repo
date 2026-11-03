import maya.cmds as cmds

def parent():
    joy=cmds.ls(sl=True)
    num=-1

    for count in joy:
        num+=1
        numm=num+1
        if count==joy[-1]:continue
        cmds.parent(f"{joy[num]}", f"{joy[numm]}")


def main():
    parent()#モードと複製名の変更



if __name__=="__main__":
    main()