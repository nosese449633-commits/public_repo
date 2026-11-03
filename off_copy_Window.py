import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from support_joint_gimmick import obj_copy
import sys

try:
    from PySide6 import QtWidgets, QtCore
    #from PySide6 import QtGui
    #QAction = QtGui.QAction
except ImportError:
    from PySide2 import QtWidgets, QtCore
    #from PySide2 import QtGui
    #QAction = QtWidgets.QAction


TOOL_NAME = "GuiTemplate"
WINDOW_OBJECT_NAME = f"{TOOL_NAME}MainWindow"
WINDOW_TITLE = "Copy_Offset Tools"

OPTIONVAR_GEOMETRY = f"{TOOL_NAME}_Geometry"


def hoge():
    print("hogehoge")


class Gui(MayaQWidgetBaseMixin, QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(WINDOW_OBJECT_NAME)
        self.setWindowTitle(WINDOW_TITLE)

        self._build_ui()

        self._restore_geometry()

    # ------------------------------------------------------------------
    # UI構築
    # ------------------------------------------------------------------

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # TODO: ここに実際のウィジェットを追加する


        #複製数
        GP_Lab=QtWidgets.QLabel("〇オフセット下のグループ数")
        layout.addWidget(GP_Lab)

        self.BT_spn=QtWidgets.QSpinBox(self, value=1,minimum=0,maximum=10)
        layout.addWidget(self.BT_spn)

        #モード
        MD_Lab=QtWidgets.QLabel("〇モードを選択")
        layout.addWidget(MD_Lab)

        self.MD_cbx=QtWidgets.QComboBox(self)
        self.MD_cbx.addItem("off")
        self.MD_cbx.addItem("dup")
        self.MD_cbx.addItem("off_dup")
        layout.addWidget(self.MD_cbx)

        #変更名
        self.RN_tex=QtWidgets.QLineEdit()
        self.RN_tex.setPlaceholderText("複製したオブジェクトの接尾語を入力")
        layout.addWidget(self.RN_tex)

        #実行ボタン
        MN_Lab=QtWidgets.QLabel("★ボタンを押して実行")
        layout.addWidget(MN_Lab)


        MN_btn=QtWidgets.QPushButton("実行")
        layout.addWidget(MN_btn)
        MN_btn.clicked.connect(self.object_copy)

        MN_btn.setStyleSheet("QPushButton{background-color: navy; }""QPushButton:hover{background-color: royalblue; }""QPushButton:pressed{background-color: indigo; }")

        

    #実行変数
    def object_copy(self):

        mode=self.MD_cbx.currentText()
        name=self.RN_tex.text()
        count=self.BT_spn.value()
        obj_copy.main(mode, name, count)





    # ------------------------------------------------------------------
    # Window Geometry
    # ------------------------------------------------------------------

    def _restore_geometry(self):
        """
        optionVarからwindowのgeometry情報を取得して反映する
        """
        if not cmds.optionVar(exists=OPTIONVAR_GEOMETRY):
            return

        geometry_data = cmds.optionVar(query=OPTIONVAR_GEOMETRY)
        self.restoreGeometry(QtCore.QByteArray.fromBase64(geometry_data.encode("utf-8")))

    def _save_geometry(self):
        """
        optionVarへwindowのgeometry情報を保存する
        """
        geometry_data = (self.saveGeometry().toBase64().data().decode("utf-8"))
        cmds.optionVar(stringValue=(OPTIONVAR_GEOMETRY, geometry_data))

    # ------------------------------------------------------------------
    # Qt Events
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        self._save_geometry()
        super().closeEvent(event)

_window_instance = None

def main():
    global _window_instance

    if cmds.window(WINDOW_OBJECT_NAME, exists=True):
        cmds.deleteUI(WINDOW_OBJECT_NAME, window=True)

    _window_instance = Gui()
    _window_instance.show()

    return _window_instance


if __name__ == "__main__":
    main()