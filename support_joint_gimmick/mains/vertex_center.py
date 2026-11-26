import maya.cmds as cmds

def get_vertex_center(vertics):

    positions=[]
    for vertex in vertics:
        pos=cmds.pointPosition(vertex, world=True)
        positions.append(pos)

    #合計を計算
    total_X=0
    total_Y=0
    total_Z=0

    for pos in positions:#pos=(x,y,z)
        total_X +=pos[0]
        total_Y +=pos[1]
        total_Z +=pos[2]

    #選択数を取得
    vercou=len(positions)

    center_X=total_X/vercou
    center_Y=total_Y/vercou
    center_Z=total_Z/vercou

    center=(center_X, center_Y, center_Z)

    print("中心座標", center)

    return center

def get_pivot_center(vertics):
    positions=[]
    for vertex in vertics:
        pos=cmds.pointPosition(vertex, world=True)
        positions.append(pos)

    min_X=min(pos[0] for pos in positions)
    max_X=max(pos[0] for pos in positions)

    min_Y=min(pos[1] for pos in positions)
    max_Y=max(pos[1] for pos in positions)

    min_Z=min(pos[2] for pos in positions)
    max_Z=max(pos[2] for pos in positions)


    center_X=(min_X + max_X)/2
    center_Y=(min_Y + max_Y)/2
    center_Z=(min_Z + max_Z)/2

    center=(center_X, center_Y, center_Z)

    print("ピボット中心座標", center)

    return center



def create_joint(center):
    cmds.select(cl=True)
    jt=cmds.joint()
    cmds.setAttr(f"{jt}.translateX", center[0])
    cmds.setAttr(f"{jt}.translateY", center[1])
    cmds.setAttr(f"{jt}.translateZ", center[2])



def match_select(obj, center):
    for ob in obj:
        cmds.setAttr(f"{ob}.translateX", center[0])
        cmds.setAttr(f"{ob}.translateY", center[1])
        cmds.setAttr(f"{ob}.translateZ", center[2])




def main(vertics, obj, cmode, mode):
    if cmode=="Center":
        center=get_vertex_center(vertics)
    else:
        center=get_pivot_center(vertics)

    if mode=="Match_Select": match_select(obj, center)
    else: create_joint(center)


if __name__=="__main__":
    main()