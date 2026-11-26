import maya.cmds as cmds

def create_joint():
    cmds.joynt()



def match_select():
    selobj=cmds.ls(sl=True)

def main(selobj, mode):
    if mode=="Create_Joint": create_joint()
    else: match_select(selobj)