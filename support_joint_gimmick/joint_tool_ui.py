import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from support_joint_gimmick.mains import obj_copy, parent_joint, mirror_joint, vertex_center
from support_joint_gimmick.supports import add_pairblend, bend_twist, spo_joint_copy, twist_bend
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
WINDOW_TITLE = "Joint Tools"

OPTIONVAR_GEOMETRY = f"{TOOL_NAME}_Geometry"


def hoge():
    print("hogehoge")


class YSFrameLayout(QtWidgets.QFrame):
    """折りたたみ可能なフレームレイアウトウィジェット。

    Mayaの `cmds.frameLayout` に近い見た目と動作をPySideで提供します。
    関連するUI要素を視覚的にグループ化し、必要に応じて表示/非表示を切り替える際に使用します。

    Notes:
        内部的に QVBoxLayout を持っており、addWidget() や addLayout() を使用して
        子要素を簡単に追加できます。
        親レイアウトへの追加は addLayout() ではなく addWidget() を使用します。
    """

    # 開閉状態が変更された際に発行されるシグナル（展開された場合に False, 折りたたまれた場合に True を渡す）
    toggled = QtCore.Signal(bool)

    def __init__(self, title="", collapsable=True, collapsed=False, parent=None, on_toggled=None, enabled=True,
                 auto_resize_window=False):
        """
        Args:
            title (str): ヘッダーに表示するタイトルテキスト。
            collapsable (bool): タイトルクリックによる折りたたみを有効にするかどうか。
            collapsed (bool): 初期状態で折りたたまれた状態にするかどうか。
            parent (QWidget, optional): 親ウィジェット。
            on_toggled (callable, optional): 開閉時に呼ばれるコールバック関数。
                引数には展開状態を表す bool (True=折りたたみ, False=展開) が渡されます。
            enabled (bool): ウィジェットの有効・無効状態。
            auto_resize_window (bool): 開閉に合わせて所属ウィンドウの高さを追従させるかどうか。
                QScrollArea など縦方向に伸縮するウィジェットを含むウィンドウでは
                意図しない縮小が起きるため有効化しないでください。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        
        # 内部状態
        self._title = title
        self._collapsable = collapsable
        self._collapsed = collapsed
        self._auto_resize_window = auto_resize_window
        self._expanded_content_height = 0

        # シグナル接続
        if on_toggled:
            self.toggled.connect(on_toggled)

        self._setup_ui()
        self._update_header_ui()

    def _setup_ui(self):
        """内部ウィジェットとレイアウトの構築"""
        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # ヘッダー (QToolButtonを使用し、ネイティブな矢印アイコンを描画)
        self._header_btn = QtWidgets.QPushButton()
        self._header_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._header_btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 4px;
                padding-left: 8px;
                background-color: #666666;
                border-radius: 2px;
                color: #eeeeee;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        self._header_btn.clicked.connect(self.toggle)

        # コンテンツエリア
        self._content_widget = QtWidgets.QWidget()
        self._content_widget.setObjectName("contentArea")
        
        # 子ウィジェットへ影響が伝播しないよう、オブジェクト名(#contentArea)で限定して指定
        self._content_widget.setStyleSheet("#contentArea { background-color: #4a4a4a; }")
        # -----------------------------------------------------------------------
        
        self._content_layout = QtWidgets.QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(12, 8, 8, 8)
        self._content_layout.setSpacing(6)

        self._main_layout.addWidget(self._header_btn)
        self._main_layout.addWidget(self._content_widget)

    def _update_header_ui(self):
        """現在のプロパティ状態に基づいてUIを更新する"""
        self._header_btn.setText(f" {self._title}")

        if not self._collapsable:
            prefix = "  "  # 折りたたみ不可のときは、矢印の代わりに半角スペース2つでインデントを合わせる
            self._header_btn.setCursor(QtCore.Qt.ArrowCursor)
        else:
            prefix = "▶ " if self._collapsed else "▼ "
            self._header_btn.setCursor(QtCore.Qt.PointingHandCursor)
            
        self._header_btn.setText(f"{prefix}{self._title}")
            
        self._content_widget.setVisible(not self._collapsed)

    def title(self):
        """ヘッダーに表示されているタイトルを取得する。

        Returns:
            str: 現在のタイトル文字列。
        """
        return self._title

    def setTitle(self, title):
        """ヘッダーに表示するタイトルを設定する。

        Args:
            title (str): 新しいタイトル文字列。
        """
        if self._title == title:
            return
            
        self._title = title
        self._update_header_ui()

    def isCollapsed(self):
        """現在折りたたまれているかどうかを取得する。

        Returns:
            bool: 折りたたまれている場合は True。
        """
        return self._collapsed

    def setCollapsed(self, collapsed):
        """折りたたみ状態を設定する。

        Args:
            collapsed (bool): 折りたたむ場合は True、展開する場合は False。
        """
        # 折りたたみ不可の状態で閉じようとした場合は無視
        if not self._collapsable and collapsed:
            return

        # 状態が変わらない場合は処理をスキップ
        if self._collapsed == collapsed:
            return

        # 非表示にすると実測値が取れなくなるため、折りたたむ前に高さを控える
        if collapsed:
            self._expanded_content_height = self._content_widget.height()

        self._collapsed = collapsed
        self._update_header_ui()
        
        # 状態変更を通知
        self.toggled.emit(self._collapsed)

        self._schedule_window_resize()

    def _schedule_window_resize(self):
        # レイアウトの再計算とコールバックによる内容変更が完了した後にリサイズする
        if self._auto_resize_window:
            QtCore.QTimer.singleShot(0, self._adjust_window_size)

    def _adjust_window_size(self):
        """所属するトップレベルウィンドウの高さをコンテンツの増減分だけ変更する。

        Qtはトップレベルウィンドウのサイズを子ウィジェットの縮小に追従させないため、
        折りたたみ時の余白を解消するには明示的なリサイズが必要になる。
        ウィンドウのsizeHintではなく増減分を使うのは、
        QLayout.totalSizeHint() が heightForWidth() をレイアウトのsizeHint幅で
        評価する仕様により、折り返しラベルを含むウィンドウで高さが過大に
        見積もられ、その余剰が他ウィジェットへ再配分されて表示位置がずれるため。
        """
        window = self.window()
        if window is None or window.isMaximized() or window.isFullScreen():
            return

        # レイアウトの最小サイズ制約を現在の内容で再計算させ、リサイズがクランプされるのを防ぐ
        window_layout = window.layout()
        if window_layout is not None:
            window_layout.activate()

        if self._collapsed:
            height_delta = -self._expanded_content_height
        else:
            height_delta = self._content_widget.sizeHint().height() - self._content_widget.height()

        if height_delta:
            window.resize(window.width(), window.height() + height_delta)

    def isCollapsable(self):
        """折りたたみ可能かどうかを取得する。

        Returns:
            bool: 折りたたみ可能な場合は True。
        """
        return self._collapsable

    def setCollapsable(self, collapsable):
        """折りたたみ可能かどうかを設定する。

        Args:
            collapsable (bool): 折りたたみ可能にする場合は True。
        """
        if self._collapsable == collapsable:
            return
            
        self._collapsable = collapsable
        
        # 折りたたみ不可になった際、現在閉じている場合は強制的に展開する
        if not self._collapsable and self._collapsed:
            # setCollapsedを経由させることでシグナル発行とUI更新を一元化
            self.setCollapsed(False)
        else:
            self._update_header_ui()

    def toggle(self):
        """折りたたみ状態を反転させる。

        折りたたみ可能 (collapsable=True) な場合のみ動作します。
        """
        if not self._collapsable:
            return

        self.setCollapsed(not self._collapsed)

    def contentWidget(self):
        """コンテンツを保持している内部のQWidgetを取得する。

        QScrollAreaに格納する場合などに使用します。

        Returns:
            QtWidgets.QWidget: コンテンツエリアのウィジェット。
        """
        return self._content_widget

    def contentLayout(self):
        """子ウィジェットを配置するためのレイアウトを取得する。

        通常は addWidget() や addLayout() の使用を推奨します。

        Returns:
            QtWidgets.QVBoxLayout: コンテンツ用のレイアウト。
        """
        return self._content_layout

    def addWidget(self, widget):
        """フレーム内にウィジェットを追加する。

        Args:
            widget (QtWidgets.QWidget): 追加するウィジェット。
        """
        self._content_layout.addWidget(widget)
        
    def addLayout(self, layout):
        """フレーム内にレイアウトを追加する。

        Args:
            layout (QtWidgets.QLayout): 追加するレイアウト。
        """
        self._content_layout.addLayout(layout)

    def clear(self):
        """フレーム内に追加されたすべてのウィジェットとレイアウトを削除する。"""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                # サブレイアウトの場合
                self._clear_layout(item.layout())
                
    def _clear_layout(self, layout):
        """レイアウト内のアイテムを再帰的に削除する"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())
            layout.deleteLater()




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
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        main_layout.addWidget(scroll_area)

        # スクロールの中に入る全体のコンテナ（入れ物）
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        scroll_area.setWidget(container)

        #タブウィジェットを作成して、container_layout に追加する
        self.tab_widget = QtWidgets.QTabWidget()
        container_layout.addWidget(self.tab_widget)  # main_layout ではなく container_layout に変更
        container_layout.addStretch()  # 下部に余白を詰める




        # ------------------------------------------------------------------
        # タブ1
        # ------------------------------------------------------------------
        self.tab_main = QtWidgets.QWidget()
        tab_main_layout = QtWidgets.QVBoxLayout(self.tab_main)
        tab_main_layout.setContentsMargins(8, 8, 8, 8)
        tab_main_layout.setSpacing(6)


        # ------------------------------------------------------------------
        # TODO: ここに実際のウィジェットを追加する
        # ------------------------------------------------------------------


        offcopyframe = YSFrameLayout(title="Offset/Copy", collapsable=True)
        #ここの変数.addWidgetにすること (tab_main_layout.addWidget(offcopyframe))を最後に入れること

        GPT_Lab=QtWidgets.QLabel("オフセット・コピー・両方行うツール")
        offcopyframe.addWidget(GPT_Lab)

        #複製数
        GP_Lab=QtWidgets.QLabel("〇オフセット下のグループ数")
        offcopyframe.addWidget(GP_Lab)

        self.BT_spn=QtWidgets.QSpinBox(self, value=1,minimum=0,maximum=10)
        offcopyframe.addWidget(self.BT_spn)

        #モード
        MD_Lab=QtWidgets.QLabel("〇モードを選択")
        offcopyframe.addWidget(MD_Lab)

        self.MD_cbx=QtWidgets.QComboBox(self)
        self.MD_cbx.addItem("off")
        self.MD_cbx.addItem("dup")
        self.MD_cbx.addItem("off_dup")
        offcopyframe.addWidget(self.MD_cbx)

        #変更名
        self.RN_tex=QtWidgets.QLineEdit()
        self.RN_tex.setPlaceholderText("複製したオブジェクトの接尾語を入力")
        offcopyframe.addWidget(self.RN_tex)

        #実行ボタン
        MN_Lab=QtWidgets.QLabel("★ボタンを押して実行")
        offcopyframe.addWidget(MN_Lab)


        MN_btn=QtWidgets.QPushButton("実行")
        offcopyframe.addWidget(MN_btn)
        MN_btn.clicked.connect(self.object_copy)
        #ボタンの色などの変更
        MN_btn.setStyleSheet("QPushButton{background-color: darkslateblue; }""QPushButton:hover{background-color: royalblue; }""QPushButton:pressed{background-color: indigo; }")

        mirrorframe = YSFrameLayout(title="JointMirror", collapsable=True)


        #ジョイントミラー＆子供と前軸の方向一致
        JM_Lab=QtWidgets.QLabel("ミラーと子供・前の方向一致")
        mirrorframe.addWidget(JM_Lab)

        JMA_Lab=QtWidgets.QLabel("〇前後に指定している軸を選択")
        mirrorframe.addWidget(JMA_Lab)

        self.JMA_cbx=QtWidgets.QComboBox(self)
        self.JMA_cbx.addItem("Y")
        self.JMA_cbx.addItem("Z")
        self.JMA_cbx.addItem("X")
        mirrorframe.addWidget(self.JMA_cbx)

        JM_btn=QtWidgets.QPushButton("実行")
        mirrorframe.addWidget(JM_btn)
        JM_btn.clicked.connect(self.mirror_joint)
        #ボタンの色などの変更
        JM_btn.setStyleSheet("QPushButton{background-color: darkslateblue; }""QPushButton:hover{background-color: royalblue; }""QPushButton:pressed{background-color: indigo; }")


        centerframe = YSFrameLayout(title="Vertex_CenterTools", collapsable=True)
        #頂点中心機能
        CT_Lab=QtWidgets.QLabel("■選択した頂点の中心かピボット位置を取得して配置")
        centerframe.addWidget(CT_Lab)

        CT_Lab=QtWidgets.QLabel("①どちらを取得したいか選択")
        centerframe.addWidget(CT_Lab)

        self.CT_cbx=QtWidgets.QComboBox(self)
        self.CT_cbx.addItem("Center")
        self.CT_cbx.addItem("Pivot_Center")
        centerframe.addWidget(self.CT_cbx)


        CTM1_Lab=QtWidgets.QLabel("②ジョイント作成か、位置の一致か選択")
        centerframe.addWidget(CTM1_Lab)

        self.CTA_cbx=QtWidgets.QComboBox(self)
        self.CTA_cbx.addItem("Create_Joint")
        self.CTA_cbx.addItem("Match_Select")
        centerframe.addWidget(self.CTA_cbx)

        CTM2_Lab=QtWidgets.QLabel("!!注意!!一致の場合はオブジェクトも選択してください")
        centerframe.addWidget(CTM2_Lab)

        CTB2_btn=QtWidgets.QPushButton("実行")
        centerframe.addWidget(CTB2_btn)
        CTB2_btn.clicked.connect(self.acquisition_center)
        #ボタンの色などの変更
        CTB2_btn.setStyleSheet("QPushButton{background-color: darkslateblue; }""QPushButton:hover{background-color: royalblue; }""QPushButton:pressed{background-color: indigo; }")



        singleframe = YSFrameLayout(title="SingleTools", collapsable=True)
        #ジョイント親子付けツール
        JP_Lab=QtWidgets.QLabel("■選択順に子供になる")
        singleframe.addWidget(JP_Lab)

        JP_btn=QtWidgets.QPushButton("実行")
        singleframe.addWidget(JP_btn)
        JP_btn.clicked.connect(self.joint_parent)
        #ボタンの色などの変更
        JP_btn.setStyleSheet("QPushButton{background-color: darkslateblue; }""QPushButton:hover{background-color: royalblue; }""QPushButton:pressed{background-color: indigo; }")



        # ------------------------------------------------------------------
        tab_main_layout.addWidget(offcopyframe)
        tab_main_layout.addWidget(mirrorframe)
        tab_main_layout.addWidget(centerframe)
        tab_main_layout.addWidget(singleframe)


        #一番最初に作ったタブに入れる作業
        # ------------------------------------------------------------------
        tab_main_layout.addStretch()

        #タブ1の名前と追加処理
        self.tab_widget.addTab(self.tab_main, "main")


        # ------------------------------------------------------------------
        # タブ2
        # ------------------------------------------------------------------
        self.tab_support = QtWidgets.QWidget()
        tab_support_layout = QtWidgets.QVBoxLayout(self.tab_support)
        tab_support_layout.setContentsMargins(8, 8, 8, 8)
        tab_support_layout.setSpacing(6)

        # ------------------------------------------------------------------
        # TODO: ここに実際のウィジェットを追加する
        # ------------------------------------------------------------------
        sub_label=QtWidgets.QLabel("補助骨のコンテンツエリアです")
        tab_support_layout.addWidget(sub_label)

        twistframe = YSFrameLayout(title="Twist_Bone", collapsable=True)

        #作成数
        BTB_Lab=QtWidgets.QLabel("〇ツイストジョイント作成数")
        twistframe.addWidget(BTB_Lab)

        self.BTB_spn=QtWidgets.QSpinBox(self, value=2,minimum=0,maximum=10)
        twistframe.addWidget(self.BTB_spn)


        #ツイストベンド
        TB_Lab=QtWidgets.QLabel("■ツイストベンド-ツイストに完全追従させる-")
        twistframe.addWidget(TB_Lab)


        TB_btn=QtWidgets.QPushButton("1つ選んで実行")
        twistframe.addWidget(TB_btn)
        TB_btn.clicked.connect(self.twist_bend)
        #ボタンの色などの変更
        TB_btn.setStyleSheet("QPushButton{background-color: dimgray; }""QPushButton:hover{background-color: steelblue; }""QPushButton:pressed{background-color: indigo; }")


        #ベンドツイスト
        BT_Lab=QtWidgets.QLabel("■ベンドツイスト-ベンドに完全追従させる-")
        twistframe.addWidget(BT_Lab)


        BT_btn=QtWidgets.QPushButton("2つ選んで実行")
        twistframe.addWidget(BT_btn)
        BT_btn.clicked.connect(self.bend_twist)
        #ボタンの色などの変更
        BT_btn.setStyleSheet("QPushButton{background-color: dimgray; }""QPushButton:hover{background-color: steelblue; }""QPushButton:pressed{background-color: indigo; }")

        weightframe = YSFrameLayout(title="Weight_Bone", collapsable=True)


        #ペアブレンド
        PB_Lab=QtWidgets.QLabel("■ペアブレンド　ウエイトは0.5")
        weightframe.addWidget(PB_Lab)

        PB_btn=QtWidgets.QPushButton("1つ選んで実行")
        weightframe.addWidget(PB_btn)
        PB_btn.clicked.connect(self.pairblend)
        #ボタンの色などの変更
        PB_btn.setStyleSheet("QPushButton{background-color: dimgray; }""QPushButton:hover{background-color: steelblue; }""QPushButton:pressed{background-color: indigo; }")

        #ペアブレンド・1~4方向複製
        PBD_Lab=QtWidgets.QLabel("■ペアブレンドと複製")
        weightframe.addWidget(PBD_Lab)

        #作成数
        PBDC_Lab=QtWidgets.QLabel("〇ウエイト補助骨作成数")
        weightframe.addWidget(PBDC_Lab)

        self.PBD_spn=QtWidgets.QSpinBox(self, value=2,minimum=1,maximum=4)
        weightframe.addWidget(self.PBD_spn)

        PBD_btn=QtWidgets.QPushButton("1つ選んで実行")
        weightframe.addWidget(PBD_btn)
        PBD_btn.clicked.connect(self.dup_pairblend)
        #ボタンの色などの変更
        PBD_btn.setStyleSheet("QPushButton{background-color: dimgray; }""QPushButton:hover{background-color: steelblue; }""QPushButton:pressed{background-color: indigo; }")


        # ------------------------------------------------------------------
        tab_support_layout.addWidget(twistframe)
        tab_support_layout.addWidget(weightframe)
        #一番最初に作ったタブに入れる作業
        # ------------------------------------------------------------------
        tab_support_layout.addStretch()

        # support タブを追加
        self.tab_widget.addTab(self.tab_support, "support")


    # ------------------------------------------------------------------
    #実行変数(ここに実行処理を記入)
    # ------------------------------------------------------------------

    def object_copy(self):

        mode=self.MD_cbx.currentText()
        name=self.RN_tex.text()
        count=self.BT_spn.value()
        obj_copy.main(mode, name, count)

    def setColor(self):
        dialog = QtWidgets.QColorDialog(QtCore.Qt.green, self)

        if dialog.exec():
            col = dialog.currentColor()
            self.re_col=print(col.red(), col.green(), col.blue())




    def over_color(self):
        obj=cmds.ls(sl=True)
        for objs in obj:
            cmds.setAttr(f"{objs}.overrideEnabled", 1)
            cmds.setAttr(f"{objs}.overrideRGBColors", 1)
            cmds.setAttr(f"{objs}.overrideColor", self.re_col)

    def mirror_joint(self):
        mode=self.JMA_cbx.currentText()
        mirror_joint.main(mode)


    def acquisition_center(self):
        cmode=self.CT_cbx.currentText()
        mode=self.CTA_cbx.currentText()
        selv=cmds.ls(sl=True, flatten=True)
        #頂点のみ選択
        vertics=cmds.filterExpand(selv, selectionMask=31) if selv else []
        obj=cmds.ls(sl=True, transforms=True)

        if not vertics:
            cmds.warning("頂点を選択してください")
            return

        vertex_center.main(vertics, obj, cmode, mode)



    def joint_parent(self):
        parent_joint.main()

    def twist_bend(self):
        count=self.BTB_spn.value()
        twist_bend.main(count)

    def bend_twist(self):
        count=self.BTB_spn.value()
        sel=cmds.ls(sl=True, type="joint")
        if not len(sel)==2:
            cmds.error("ジョイント個数が違います")
        else:
            bend_twist.main(sel, count)

    def pairblend(self):
        add_pairblend.main()

    def dup_pairblend(self):
        count=self.PBD_spn.value()
        spo_joint_copy.main(count)


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