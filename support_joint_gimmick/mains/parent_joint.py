import maya.cmds as cmds

def parent():
    joy=cmds.ls(sl=True)
    num=-1

    for count in range(len(joy)-1):
        num+=1
        numm=num+1
        cmds.parent(joy[count], joy[count+1])
        print(count)


def main():
    parent()#モードと複製名の変更



if __name__=="__main__":
    main()