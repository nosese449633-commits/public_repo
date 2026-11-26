from maya import cmds

def keycope():
    num=0
    conectlist={}
    moto=cmds.ls(sl=True)

    for obj in moto:
        num+=1
        cmds.duplicate(f"{obj}", rr=True, ic=True, name=f"{obj}_D")
        
        conectlist[f"child_{num}"]=f"{obj}_D"
        conectlist[f"conect_{num}"]=cmds.listConnections(f"{obj}", scn=True, s=False, d=True, p=True)[0]

    num=0
    for cobj in moto:
        num+=1
        cmds.connectAttr(f"{conectlist.get(f'child_{num}')}.output", f"{conectlist.get(f'conect_{num}')}", f=True)



def main():
    keycope()

if __name__=="__main__":
    main()