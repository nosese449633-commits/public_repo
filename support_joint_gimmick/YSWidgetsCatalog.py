import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui


class YSPushButton(QtWidgets.QPushButton):
    """シンプルなプッシュボタンウィジェット。

    クリックした際の処理を簡単に登録できます。
    """

    def __init__(self, text="", parent=None, on_clicked=None, enabled=True):
        """
        Args:
            text (str): ボタンに表示するテキスト。
            parent (QWidget, optional): 親ウィジェット。
            on_clicked (callable, optional): ボタンがクリックされた際に実行されるコールバック関数。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(text, parent)
        self.setEnabled(enabled)
        if on_clicked:
            self.clicked.connect(on_clicked)


class YSCheckBox(QtWidgets.QCheckBox):
    """状態の切り替えが可能なチェックボックスウィジェット。

    ON/OFFの状態を切り替えたい場合に使用します。
    """

    def __init__(self, text="", checked=False, parent=None, on_toggled=None, enabled=True):
        """
        Args:
            text (str): チェックボックスの横に表示するテキスト。
            checked (bool): 初期状態でのチェックの有無。
            parent (QWidget, optional): 親ウィジェット。
            on_toggled (callable, optional): チェック状態が変更された際に実行されるコールバック関数（引数に bool を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(text, parent)
        self.setEnabled(enabled)
        self.setChecked(checked)
        if on_toggled:
            self.toggled.connect(on_toggled)


class YSComboBox(QtWidgets.QComboBox):
    """プルダウン形式でアイテムを選択できるコンボボックスウィジェット。

    複数の選択肢から1つを選ばさせたい場合に使用します。
    """

    def __init__(self, items=None, default_index=0, parent=None, on_index_changed=None, on_text_changed=None, enabled=True):
        """
        Args:
            items (list[str], optional): ドロップダウンリストに追加するアイテムの文字列リスト。
            default_index (int): 初期選択状態とするアイテムのインデックス番号。
            parent (QWidget, optional): 親ウィジェット。
            on_index_changed (callable, optional): 選択インデックス変更時のコールバック関数（引数に int を受け取る）。
            on_text_changed (callable, optional): 選択テキスト変更時のコールバック関数（引数に str を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        if items:
            self.addItems(items)
        if on_index_changed:
            self.currentIndexChanged.connect(on_index_changed)
        if on_text_changed:
            self.currentTextChanged.connect(on_text_changed)

        self.setCurrentIndex(default_index)


class YSLineEdit(QtWidgets.QLineEdit):
    """1行のテキストを入力するためのウィジェット。

    ユーザーに短いテキストや名前を入力させたい場合に使用します。
    """

    def __init__(self, text="", placeholder_text="", parent=None, on_text_changed=None, on_editing_finished=None, enabled=True):
        """
        Args:
            text (str): 初期状態のテキスト。
            placeholder_text (str): 未入力時に薄く表示されるプレースホルダーテキスト。
            parent (QWidget, optional): 親ウィジェット。
            on_text_changed (callable, optional): テキスト変更時にリアルタイムで呼ばれるコールバック関数（引数に str を受け取る）。
            on_editing_finished (callable, optional): 入力確定時（Enter押下またはフォーカス喪失）のコールバック関数。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(text, parent)
        self.setEnabled(enabled)
        if placeholder_text:
            self.setPlaceholderText(placeholder_text)
        if on_text_changed:
            self.textChanged.connect(on_text_changed)
        if on_editing_finished:
            self.editingFinished.connect(on_editing_finished)


class YSPlainTextEdit(QtWidgets.QPlainTextEdit):
    """複数行のテキストを入力するためのウィジェット。

    詳細な説明や長文を入力させたい場合に使用します。
    """

    def __init__(self, text="", placeholder_text="", parent=None, on_text_changed=None, enabled=True):
        """
        Args:
            text (str): 初期状態のテキスト。
            placeholder_text (str): 未入力時に表示されるプレースホルダーテキスト。
            parent (QWidget, optional): 親ウィジェット。
            on_text_changed (callable, optional): テキスト変更時にリアルタイムで呼ばれるコールバック関数（引数に str を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(text, parent)
        self.setEnabled(enabled)
        if placeholder_text:
            self.setPlaceholderText(placeholder_text)
        
        self._on_changed_cb = on_text_changed
        if self._on_changed_cb:
            self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        if self._on_changed_cb:
            self._on_changed_cb(self.toPlainText())


class YSSpinBox(QtWidgets.QSpinBox):
    """整数値を増減・入力するためのスピンボックスウィジェット。

    個数や回数など、整数のパラメータを入力させたい場合に使用します。
    """

    def __init__(self, value=0, min_val=0, max_val=100, on_changed=None, parent=None, enabled=True):
        """
        Args:
            value (int): 初期値。
            min_val (int): 入力可能な最小値。
            max_val (int): 入力可能な最大値。
            on_changed (callable, optional): 値が変更された際のコールバック関数（引数に int を受け取る）。
            parent (QWidget, optional): 親ウィジェット。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self.setRange(min_val, max_val)
        self.setValue(value)
        if on_changed:
            self.valueChanged.connect(on_changed)


class YSDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    """浮動小数点数を増減・入力するためのスピンボックスウィジェット。

    倍率やスケールなど、小数のパラメータを入力させたい場合に使用します。
    """

    def __init__(self, value=0.0, min_val=0.0, max_val=100.0, decimals=2, step=0.1, on_changed=None, parent=None, enabled=True):
        """
        Args:
            value (float): 初期値。
            min_val (float): 入力可能な最小値。
            max_val (float): 入力可能な最大値。
            decimals (int): 表示および入力可能な小数点以下の桁数。
            step (float): スピンボックスの矢印をクリックした際の増減量。
            on_changed (callable, optional): 値が変更された際のコールバック関数（引数に float を受け取る）。
            parent (QWidget, optional): 親ウィジェット。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self.setRange(min_val, max_val)
        self.setDecimals(decimals)
        self.setSingleStep(step) 
        self.setValue(value)
        if on_changed:
            self.valueChanged.connect(on_changed)


class YSRadioButton(QtWidgets.QRadioButton):
    """単体のラジオボタンウィジェット。

    通常はグループ内で使用されますが、単独で配置することも可能です。
    他のラジオボタンとの排他制御は行いません。
    複数のラジオボタンをまとめて扱いたい場合はYSRadioGroup を使用してください。
    """

    def __init__(self, text="", checked=False, parent=None, on_toggled=None, enabled=True):
        """
        Args:
            text (str): ラジオボタンの横に表示するテキスト。
            checked (bool): 初期状態での選択の有無。
            parent (QWidget, optional): 親ウィジェット。
            on_toggled (callable, optional): 選択状態変更時のコールバック関数（引数に bool を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(text, parent)
        self.setEnabled(enabled)
        self.setChecked(checked)
        if on_toggled:
            self.toggled.connect(on_toggled)


class YSRadioGroup(QtWidgets.QWidget):
    """複数のラジオボタンを内包し、排他選択を管理するウィジェット。

    複数の選択肢から必ず1つを選ばせる場合に使用します。

    Attributes:
        button_group (QtWidgets.QButtonGroup): ラジオボタンの排他制御を行うグループ。
    """

    def __init__(self, items=None, default_index=0, parent=None, on_changed=None, enabled=True):
        """
        Args:
            items (list[str], optional): 生成するラジオボタンのテキストのリスト。
            default_index (int): 初期選択状態とするアイテムのインデックス番号。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): 選択項目が変更された際のコールバック関数（引数に選択された文字列を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self._on_changed_cb = on_changed
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.buttonToggled.connect(self._on_button_toggled)
        
        if items:
            for i, item_text in enumerate(items):
                btn = QtWidgets.QRadioButton(item_text, self)
                layout.addWidget(btn)
                self.button_group.addButton(btn, i)
                if i == default_index:
                    btn.setChecked(True)

    def _on_button_toggled(self, button, checked):
        if checked and self._on_changed_cb:
            self._on_changed_cb(button.text())

    def value(self):
        """現在選択されているラジオボタンのテキストを取得する。

        Returns:
            str: 選択されているテキスト。未選択の場合は空文字。
        """
        btn = self.button_group.checkedButton()
        return btn.text() if btn else ""

    def setValue(self, text):
        """指定したテキストを持つラジオボタンを選択状態にする。

        Args:
            text (str): 選択状態にしたいラジオボタンのテキスト。
        """
        for btn in self.button_group.buttons():
            if btn.text() == text:
                btn.setChecked(True)
                break

    def current_text(self):
        """現在選択されているラジオボタンのテキストを取得する（valueのエイリアス）。

        Returns:
            str: 選択されているテキスト。
        """
        return self.value()

    def current_index(self):
        """現在選択されているラジオボタンのインデックスを取得する。

        Returns:
            int: 選択されているインデックス。
        """
        return self.button_group.checkedId()

    def set_current_index(self, index):
        """指定したインデックスのラジオボタンを選択状態にする。

        Args:
            index (int): 選択状態にしたいラジオボタンのインデックス。
        """
        btn = self.button_group.button(index)
        if btn:
            btn.setChecked(True)

    def set_current_text(self, text):
        """指定したテキストを持つラジオボタンを選択状態にする（setValueのエイリアス）。

        Args:
            text (str): 選択状態にしたいラジオボタンのテキスト。
        """
        self.setValue(text)


class _YSSliderGroupBase(QtWidgets.QWidget):
    """スライダーとラインエディットを同期させるウィジェットの抽象基底クラス。

    内部状態の管理、クランプ処理、シグナルブロックなどの共通ロジックを提供します。
    """

    def __init__(self, value, min_val, max_val, parent=None, on_changed=None, on_released=None, enabled=True):
        """
        Args:
            value (int | float): 初期値。
            min_val (int | float): 最小値。
            max_val (int | float): 最大値。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): 値が変更された際に呼び出されるコールバック。
            on_released (callable, optional): 操作が確定・離された際に呼び出されるコールバック。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self.min_val = min_val
        self.max_val = max_val
        self._on_changed_cb = on_changed
        self._on_released_cb = on_released
        
        # 内部キャッシュをクランプされた正しい型で初期化
        self._current_value = max(self.min_val, min(self.max_val, self._cast_value(value)))

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit = QtWidgets.QLineEdit(self._format_value(self._current_value), self)
        self.line_edit.setMaximumWidth(60)
        self.line_edit.setValidator(self._create_validator())
        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(self._to_slider_val(self.min_val), self._to_slider_val(self.max_val))
        self.slider.setValue(self._to_slider_val(self._current_value))

        self.slider.wheelEvent = lambda event: event.ignore()

        layout.addWidget(self.line_edit)
        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self._on_slider_changed)
        self.slider.sliderReleased.connect(self._on_slider_released)
        self.line_edit.editingFinished.connect(self._on_line_edit_finished)

    def _create_validator(self):
        raise NotImplementedError

    def _format_value(self, val):
        raise NotImplementedError

    def _to_slider_val(self, val):
        raise NotImplementedError

    def _from_slider_val(self, val):
        raise NotImplementedError

    def _cast_value(self, text):
        raise NotImplementedError

    def _on_slider_changed(self, slider_val):
        val = self._from_slider_val(slider_val)
        self.setValue(val)

    def _on_slider_released(self):
        if self._on_released_cb:
            self._on_released_cb(self.value())

    def _on_line_edit_finished(self):
        self.setValue(self.line_edit.text())
        
        if self._on_released_cb:
            self._on_released_cb(self._current_value)

    def value(self):
        """現在の値を取得する。

        Returns:
            int | float: スライダーの現在の値。
        """
        return self._current_value

    def setValue(self, val):
        """指定した値を設定する。

        値が変更された場合のみ、UIを同期し変更通知コールバックを実行します。
        無効な値が渡された場合は、サイレントに現在の値へとUIが復旧されます。

        Args:
            val (int | float | str): 設定したい値、または変換可能な文字列。
        """
        try:
            casted_val = self._cast_value(val)
        except ValueError:
            clamped_val = self._current_value
        else:
            clamped_val = max(self.min_val, min(self.max_val, casted_val))
        
        is_changed = (self._current_value != clamped_val)
        self._current_value = clamped_val
        
        # LineEditの同期 (シグナルブロックをtry...finallyで確実に制御)
        old_le_state = self.line_edit.blockSignals(True)
        try:
            self.line_edit.setText(self._format_value(clamped_val))
        finally:
            self.line_edit.blockSignals(old_le_state)

        # Sliderの同期 (シグナルブロックをtry...finallyで確実に制御)
        old_sl_state = self.slider.blockSignals(True)
        try:
            self.slider.setValue(self._to_slider_val(clamped_val))
        finally:
            self.slider.blockSignals(old_sl_state)
            
        if is_changed and self._on_changed_cb:
            self._on_changed_cb(clamped_val)


class YSIntSliderGroup(_YSSliderGroupBase):
    """整数値の入力用テキストフィールドとスライダーが連動する複合ウィジェット。

    スライダーでの直感的な操作と、テキスト入力での正確な指定を両立させたい場合に使用します。
    """

    def __init__(self, value=0, min_val=0, max_val=100, parent=None, on_changed=None, on_released=None, enabled=True):
        """
        Args:
            value (int): 初期値。
            min_val (int): 最小値。
            max_val (int): 最大値。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): スライダー移動時などの値変更中コールバック関数（引数に int を受け取る）。
            on_released (callable, optional): スライダー離脱時やテキスト入力確定時のコールバック関数（引数に int を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(value, min_val, max_val, parent, on_changed, on_released, enabled)

    def _create_validator(self):
        return QtGui.QIntValidator(-2147483648, 2147483647, self)

    def _format_value(self, val):
        return str(int(val))

    def _to_slider_val(self, val):
        return int(val)

    def _from_slider_val(self, val):
        return int(val)

    def _cast_value(self, val):
        return int(val)


class YSFloatSliderGroup(_YSSliderGroupBase):
    """浮動小数点数の入力用テキストフィールドとスライダーが連動する複合ウィジェット。

    小数のパラメータをスライダーとテキスト入力で調整させたい場合に使用します。
    """

    def __init__(self, value=0.0, min_val=0.0, max_val=100.0, decimals=2, parent=None, on_changed=None, on_released=None, enabled=True):
        """
        Args:
            value (float): 初期値。
            min_val (float): 最小値。
            max_val (float): 最大値。
            decimals (int): 扱う小数点以下の桁数。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): スライダー移動時などの値変更中コールバック関数（引数に float を受け取る）。
            on_released (callable, optional): スライダー離脱時やテキスト入力確定時のコールバック関数（引数に float を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        self.decimals = decimals
        self.multiplier = 10 ** decimals
        super().__init__(value, min_val, max_val, parent, on_changed, on_released, enabled)

    def _create_validator(self):
        validator = QtGui.QDoubleValidator(-1000000000.0, 1000000000.0, self.decimals, self)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        return validator

    def _format_value(self, val):
        return f"{val:.{self.decimals}f}"

    def _to_slider_val(self, val):
        return int(round(float(val) * self.multiplier))

    def _from_slider_val(self, val):
        return float(val) / self.multiplier

    def _cast_value(self, val):
        return float(val)


class YSPathPickerGroup(QtWidgets.QWidget):
    """ファイルまたはフォルダのパスを選択・入力するための複合ウィジェット。

    パスの直接入力と、ダイアログからの選択を両立させたい場合に使用します。

    Attributes:
        line_edit (QtWidgets.QLineEdit): パスの表示・入力を行うテキストフィールド。
        browse_btn (QtWidgets.QPushButton): ブラウザを開くボタン。
    """

    def __init__(self, default_path="", dialog_title="Select Path", file_filter="All Files (*)", is_directory=False, parent=None, on_changed=None, enabled=True):
        """
        Args:
            default_path (str): 初期パス。
            dialog_title (str): ダイアログ表示時のタイトル。
            file_filter (str): ファイル選択時のフィルタ文字列（例: "All Files (*)"）。
            is_directory (bool): フォルダ選択モードとして扱う場合は True。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): パスが変更・確定された際のコールバック関数（引数に str を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self.dialog_title = dialog_title
        self.file_filter = file_filter
        self.is_directory = is_directory
        self._on_changed_cb = on_changed

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QtWidgets.QLineEdit(default_path, self)
        self.browse_btn = QtWidgets.QPushButton("...", self)
        self.browse_btn.setFixedWidth(30)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.browse_btn)

        self.browse_btn.clicked.connect(self._on_browse_clicked)
        self.line_edit.editingFinished.connect(self._on_line_edit_finished)

    def _on_browse_clicked(self):
        f_mode = 3 if self.is_directory else 1
        result = cmds.fileDialog2(
            fileMode=f_mode,
            caption=self.dialog_title,
            startingDirectory=self.line_edit.text(),
            okCaption="Select",
            fileFilter=self.file_filter if not self.is_directory else None
        )

        if result:
            self.setValue(result[0])
            if self._on_changed_cb:
                self._on_changed_cb(result[0])

    def _on_line_edit_finished(self):
        if self._on_changed_cb:
            self._on_changed_cb(self.line_edit.text())

    def value(self):
        """現在のパス文字列を取得する。

        Returns:
            str: 現在入力されているパス。
        """
        return self.line_edit.text()

    def setValue(self, val):
        """指定したパス文字列を設定する。

        Args:
            val (str): 設定したいパス。
        """
        with QtCore.QSignalBlocker(self.line_edit):
            self.line_edit.setText(val)

    def path(self):
        """現在のパス文字列を取得する（valueのエイリアス）。

        Returns:
            str: 現在入力されているパス。
        """
        return self.value()

    def setPath(self, path):
        """指定したパス文字列を設定する（setValueのエイリアス）。

        Args:
            path (str): 設定したいパス。
        """
        self.setValue(path)


class YSColorPicker(QtWidgets.QPushButton):
    """カラー選択用ウィジェット。

    クリックでカラーダイアログを開き、RGBまたはHexカラーを取得・設定できます。
    """

    def __init__(self, default_color=(255, 255, 255), return_type="rgb", parent=None, on_changed=None, enabled=True):
        """
        Args:
            default_color (tuple | str): 初期カラー。RGBタプル (255, 255, 255) または Hex文字列 "#FFFFFF"。
            return_type (str): 返却値の形式。"rgb" または "hex"。
            parent (QWidget, optional): 親ウィジェット。
            on_changed (callable, optional): 色変更時に呼ばれるコールバック関数（引数に設定された形式の色を受け取る）。
            enabled (bool): ウィジェットの有効・無効状態。
        """
        super().__init__(parent)
        self.setEnabled(enabled)
        self.return_type = return_type.lower()
        self._on_changed_cb = on_changed
        
        self.setMinimumSize(40, 20)
        self.setText("")
        
        self._color = QtGui.QColor()
        self.setValue(default_color)
        
        self.clicked.connect(self._on_clicked)

    def _update_stylesheet(self):
        self.setStyleSheet(
            f"QPushButton {{"
            f"    background-color: {self._color.name()}; "
            f"    border: 1px solid #555555; "
            f"    border-radius: 2px;"
            f"}}"
        )

    def _on_clicked(self):
        dialog = QtWidgets.QColorDialog(self._color, self)
        dialog.setWindowTitle("Select Color")
        dialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog, True)
        dialog.setStyleSheet("""
            QColorDialog {
                background-color: #535353;
            }
            QLabel, QCheckBox {
                color: #ffffff;
            }
        """)

        if dialog.exec():
            color = dialog.currentColor()
            if color.isValid():
                self.setValue(color)
                if self._on_changed_cb:
                    self._on_changed_cb(self.value())

    def value(self):
        """現在の色を取得する。

        Returns:
            tuple[int, int, int] | str: return_typeに応じた色（RGBタプルまたはHex文字列）を返す。
        """
        if self.return_type == "hex":
            return self._color.name()
        return (self._color.red(), self._color.green(), self._color.blue())

    def setValue(self, color_val):
        """指定した色をウィジェットに設定する。

        Args:
            color_val (tuple | str | QtGui.QColor): 設定したい色。RGBタプル、Hex文字列、または QColor オブジェクト。
        """
        if isinstance(color_val, QtGui.QColor):
            self._color = color_val
        elif isinstance(color_val, str) and color_val.startswith("#"):
            self._color.setNamedColor(color_val)
        elif isinstance(color_val, (tuple, list)) and len(color_val) >= 3:
            self._color.setRgb(color_val[0], color_val[1], color_val[2])
        else:
            self._color.setRgb(255, 255, 255)
            
        self._update_stylesheet()

    def get_value(self):
        """現在の色を取得する（valueのエイリアス）。

        Returns:
            tuple[int, int, int] | str: return_typeに応じた色（RGBタプル頑丈なHex文字列）を返す。
        """
        return self.value()

    def set_value(self, color_val):
        """指定した色をウィジェットに設定する（setValueのエイリアス）。

        Args:
            color_val (tuple | str | QtGui.QColor): 設定したい色。RGBタプル、Hex文字列、または QColor オブジェクト。
        """
        self.setValue(color_val)


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


TOOL_NAME = "YSWidgetsCatalogStandalone"
WINDOW_OBJECT_NAME = f"{TOOL_NAME}MainWindow"
WINDOW_TITLE = "YSWidgets Catalog"

OPTIONVAR_GEOMETRY = f"{TOOL_NAME}_Geometry"


class Gui(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """YSWidgetsライブラリのカタログ・デモ用ウィンドウ。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(WINDOW_OBJECT_NAME)
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(800, 900)

        self._build_ui()
        self._restore_geometry()

    # ------------------------------------------------------------------
    # UI構築
    # ------------------------------------------------------------------

    def _build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(12, 12, 12, 12)
        self.scroll_layout.setSpacing(12)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        self._build_buttons_category()
        self._build_input_category()
        self._build_value_category()
        self._build_selection_category()
        self._build_pickers_category()
        self._build_layout_category()

        self.scroll_layout.addStretch()

    # ------------------------------------------------------------------
    # カタログレイアウト用ヘルパー
    # ------------------------------------------------------------------

    def _add_catalog_row(self, parent_layout, name, description, widgets, horizontal_widgets=False):
        """カタログの1行を構成するレイアウトを追加する。"""
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setContentsMargins(8, 8, 8, 8)

        info_layout = QtWidgets.QVBoxLayout()
        title_lbl = QtWidgets.QLabel(f'<span style="font-size:14pt; font-weight:bold; color:#e0e0e0;">{name}</span>')
        desc_lbl = QtWidgets.QLabel(f'<span style="color:#aaaaaa;">{description}</span>')
        desc_lbl.setWordWrap(True)
        
        info_layout.addWidget(title_lbl)
        info_layout.addWidget(desc_lbl)
        info_layout.addStretch()

        row_layout.addLayout(info_layout, stretch=2)

        if horizontal_widgets:
            widget_layout = QtWidgets.QHBoxLayout()
        else:
            widget_layout = QtWidgets.QVBoxLayout()
            
        widget_layout.setSpacing(8)

        for w in widgets:
            widget_layout.addWidget(w)
            
        widget_layout.addStretch()
        row_layout.addLayout(widget_layout, stretch=3)

        parent_layout.addLayout(row_layout)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setStyleSheet("background-color: #333333;")
        parent_layout.addWidget(line)

    def _create_logger(self, widget_name, arg_name="value"):
        """シグナル発生時にコンソールへ値を出力するコールバックを生成する。"""
        def callback(*args):
            val = args[0] if args else "Triggered"
            print("-" * 30)
            print(f"{widget_name} -> {arg_name}: {val}")
            print("-" * 30)
        return callback

    # ------------------------------------------------------------------
    # カテゴリ構築
    # ------------------------------------------------------------------

    def _build_buttons_category(self):
        frame = YSFrameLayout(title="Buttons", collapsable=True)
        fl_layout = frame.contentLayout()

        btn_normal = YSPushButton("Normal Button", on_clicked=self._create_logger("YSPushButton", "on_clicked"))
        btn_normal.setToolTip("クリックすると登録された処理を実行する標準的なボタンです。")

        btn_disabled = YSPushButton("Disabled Button", enabled=False)
        btn_disabled.setToolTip("無効化(enabled=False)されているため、クリックできない状態のボタンです。")

        self._add_catalog_row(
            fl_layout,
            "YSPushButton",
            "シンプルなプッシュボタンです。\n処理を実行するトリガーとして使用します。",
            [btn_normal, btn_disabled],
            horizontal_widgets=True
        )
        self.scroll_layout.addWidget(frame)

    def _build_input_category(self):
        frame = YSFrameLayout(title="Input Widgets", collapsable=True)
        fl_layout = frame.contentLayout()

        # LineEdit
        le_empty = YSLineEdit(
            on_text_changed=self._create_logger("YSLineEdit", "on_text_changed"),
            on_editing_finished=self._create_logger("YSLineEdit", "on_editing_finished")
        )
        le_empty.setToolTip("テキストを入力すると on_text_changed が、Enterで確定すると on_editing_finished が発火します。")

        le_text = YSLineEdit(text="Default Text")
        le_text.setToolTip("初期値が設定された LineEdit です。")

        le_ph = YSLineEdit(placeholder_text="Enter some text...")
        le_ph.setToolTip("未入力時にガイドとなるプレースホルダーテキストを表示しています。")

        le_disabled = YSLineEdit(text="Disabled", enabled=False)
        le_disabled.setToolTip("入力不可(enabled=False)に設定された LineEdit です。")

        self._add_catalog_row(
            fl_layout,
            "YSLineEdit",
            "1行のテキスト入力フィールドです。\n名前や短い文字列を入力させる場合に使用します。",
            [le_empty, le_text, le_ph, le_disabled]
        )

        # PlainTextEdit
        pe_normal = YSPlainTextEdit(
            placeholder_text="Enter description...",
            on_text_changed=self._create_logger("YSPlainTextEdit", "on_text_changed")
        )
        pe_normal.setMaximumHeight(60)
        pe_normal.setToolTip("複数行のテキストを入力可能なウィジェットです。文字入力ごとに on_text_changed が発火します。")

        pe_disabled = YSPlainTextEdit(text="Disabled\nText\nArea", enabled=False)
        pe_disabled.setMaximumHeight(60)
        pe_disabled.setToolTip("入力不可(enabled=False)に設定された PlainTextEdit です。")

        self._add_catalog_row(
            fl_layout,
            "YSPlainTextEdit",
            "複数行のテキスト入力エリアです。\n長文や詳細な説明を入力させる場合に使用します。",
            [pe_normal, pe_disabled]
        )
        self.scroll_layout.addWidget(frame)

    def _build_value_category(self):
        frame = YSFrameLayout(title="Value Widgets", collapsable=True)
        fl_layout = frame.contentLayout()

        # SpinBox
        sp_int = YSSpinBox(value=10, min_val=0, max_val=100, on_changed=self._create_logger("YSSpinBox", "on_changed"))
        sp_int.setToolTip("0〜100の範囲で整数を入力・増減できるスピンボックスです。")

        sp_disabled = YSSpinBox(value=50, enabled=False)
        sp_disabled.setToolTip("無効化(enabled=False)されており、値の変更ができません。")

        self._add_catalog_row(
            fl_layout,
            "YSSpinBox",
            "整数値を入力・増減させるスピンボックスです。\n個数や回数などの指定に使用します。",
            [sp_int, sp_disabled],
            horizontal_widgets=True
        )

        # DoubleSpinBox
        sp_float = YSDoubleSpinBox(value=1.25, min_val=0.0, max_val=10.0, step=0.05, on_changed=self._create_logger("YSDoubleSpinBox", "on_changed"))
        sp_float.setToolTip("0.0〜10.0の範囲で小数を入力・増減できるスピンボックスです。0.05刻みで増減します。")

        sp_f_disabled = YSDoubleSpinBox(value=3.14, enabled=False)
        sp_f_disabled.setToolTip("無効化(enabled=False)されており、値の変更ができません。")

        self._add_catalog_row(
            fl_layout,
            "YSDoubleSpinBox",
            "小数を入力・増減させるスピンボックスです。\nスケールやウェイトなどの指定に使用します。",
            [sp_float, sp_f_disabled],
            horizontal_widgets=True
        )

        # IntSliderGroup
        sl_int = YSIntSliderGroup(
            value=50, min_val=0, max_val=100,
            on_changed=self._create_logger("YSIntSliderGroup", "on_changed"),
            on_released=self._create_logger("YSIntSliderGroup", "on_released")
        )
        sl_int.setToolTip("スライダー移動中(on_changed)と、マウスを離した時・入力確定時(on_released)の両方でイベントが取得できます。")

        sl_int_disabled = YSIntSliderGroup(value=25, min_val=0, max_val=100, enabled=False)
        sl_int_disabled.setToolTip("操作不可(enabled=False)に設定された整数用スライダーグループです。")

        self._add_catalog_row(
            fl_layout,
            "YSIntSliderGroup",
            "整数値の入力フィールドと連動するスライダーです。\n直感的に数値を調整させたい場合に使用します。",
            [sl_int, sl_int_disabled]
        )

        # FloatSliderGroup
        sl_float = YSFloatSliderGroup(
            value=0.35, min_val=0.0, max_val=1.0, decimals=2,
            on_changed=self._create_logger("YSFloatSliderGroup", "on_changed"),
            on_released=self._create_logger("YSFloatSliderGroup", "on_released")
        )
        sl_float.setToolTip("小数点第2位まで扱えるスライダーです。テキストとスライダーが同期します。")

        sl_float_disabled = YSFloatSliderGroup(value=0.75, min_val=0.0, max_val=1.0, enabled=False)
        sl_float_disabled.setToolTip("操作不可(enabled=False)に設定された小数用スライダーグループです。")

        self._add_catalog_row(
            fl_layout,
            "YSFloatSliderGroup",
            "小数値の入力フィールドと連動するスライダーです。\n0〜1の割合などを視覚的に調整させる場合に使用します。",
            [sl_float, sl_float_disabled]
        )
        self.scroll_layout.addWidget(frame)

    def _build_selection_category(self):
        frame = YSFrameLayout(title="Selection Widgets", collapsable=True)
        fl_layout = frame.contentLayout()

        # CheckBox
        chk_off = YSCheckBox("Option OFF", checked=False, on_toggled=self._create_logger("YSCheckBox", "on_toggled"))
        chk_off.setToolTip("初期状態がOFFのチェックボックスです。状態変更時に on_toggled が呼ばれます。")

        chk_on = YSCheckBox("Option ON", checked=True)
        chk_on.setToolTip("初期状態がONのチェックボックスです。")

        chk_disabled = YSCheckBox("Disabled", enabled=False)
        chk_disabled.setToolTip("操作不可(enabled=False)に設定されたチェックボックスです。")

        self._add_catalog_row(
            fl_layout,
            "YSCheckBox",
            "ON/OFFを切り替えるためのチェックボックスです。\n独立したオプションの有効/無効化に使用します。",
            [chk_off, chk_on, chk_disabled],
            horizontal_widgets=True
        )

        # RadioButton
        rb_off = YSRadioButton("Radio OFF", checked=False, on_toggled=self._create_logger("YSRadioButton", "on_toggled"))
        rb_off.setToolTip("単独で使用されているラジオボタンです。グループ化されていないため排他処理は行われません。")

        rb_on = YSRadioButton("Radio ON", checked=True)
        rb_on.setToolTip("初期状態がONの単一ラジオボタンです。")

        rb_disabled = YSRadioButton("Disabled", enabled=False)
        rb_disabled.setToolTip("操作不可(enabled=False)に設定されたラジオボタンです。")

        self._add_catalog_row(
            fl_layout,
            "YSRadioButton",
            "単体のラジオボタンです。\n通常はグループ化して排他選択に使用します。",
            [rb_off, rb_on, rb_disabled],
            horizontal_widgets=True
        )

        # RadioGroup
        rg_normal = YSRadioGroup(
            items=["Option A", "Option B", "Option C"], default_index=0,
            on_changed=self._create_logger("YSRadioGroup", "on_changed")
        )
        rg_normal.setToolTip("複数のラジオボタンをグループ化し、必ず1つだけが選択されるように制御します。")

        rg_init = YSRadioGroup(
            items=["Low", "Medium", "High"], default_index=1,
            on_changed=self._create_logger("YSRadioGroup", "on_changed")
        )
        rg_init.setToolTip("初期インデックスとして1 (Medium) が選択されているグループです。")

        rg_disabled = YSRadioGroup(items=["X", "Y", "Z"], enabled=False)
        rg_disabled.setToolTip("操作不可(enabled=False)に設定されたラジオボタングループです。")

        self._add_catalog_row(
            fl_layout,
            "YSRadioGroup",
            "排他選択を管理するラジオボタンのグループです。\n複数の選択肢から必ず1つを選ばせる場合に使用します。",
            [rg_normal, rg_init, rg_disabled]
        )

        # ComboBox
        cb_normal = YSComboBox(
            items=["Apple", "Banana", "Cherry"],
            on_index_changed=self._create_logger("YSComboBox", "on_index_changed")
        )
        cb_normal.setToolTip("アイテムを選択できるプルダウンです。インデックスの変更を取得できます。")

        cb_init = YSComboBox(items=["Red", "Green", "Blue"], default_index=2, 
            on_text_changed=self._create_logger("YSComboBox", "on_text_changed")
        )
        cb_init.setToolTip("初期インデックスとして 2 (Blue) が選択されたコンボボックスです。テキストの変更を取得できます。")

        cb_disabled = YSComboBox(items=["Disabled"], enabled=False)
        cb_disabled.setToolTip("操作不可(enabled=False)に設定されたコンボボックスです。")

        self._add_catalog_row(
            fl_layout,
            "YSComboBox",
            "プルダウン形式のコンボボックスです。\n省スペースで多数の選択肢を提示する場合に使用します。",
            [cb_normal, cb_init, cb_disabled]
        )
        self.scroll_layout.addWidget(frame)

    def _build_pickers_category(self):
        frame = YSFrameLayout(title="Pickers", collapsable=True)
        fl_layout = frame.contentLayout()

        # ColorPicker
        cp_rgb = YSColorPicker(default_color=(255, 128, 64), return_type="rgb", on_changed=self._create_logger("YSColorPicker (RGB)", "on_changed"))
        cp_rgb.setToolTip("クリックするとカラーダイアログが開き、RGBタプル形式 (r, g, b) で色を取得・設定できます。")

        cp_hex = YSColorPicker(default_color="#00FFaa", return_type="hex", on_changed=self._create_logger("YSColorPicker (Hex)", "on_changed"))
        cp_hex.setToolTip("クリックするとカラーダイアログが開き、16進数文字列 (#RRGGBB) 形式で色を取得・設定できます。")

        self._add_catalog_row(
            fl_layout,
            "YSColorPicker",
            "カラー選択用のボタンです。\nクリックでダイアログが開き、色を取得できます。",
            [cp_rgb, cp_hex],
            horizontal_widgets=True
        )

        # PathPickerGroup
        pp_file = YSPathPickerGroup(default_path="C:/temp/export.fbx", is_directory=False, on_changed=self._create_logger("YSPathPickerGroup (File)", "on_changed"))
        pp_file.setToolTip("ファイルを選択するためのパスウィジェットです。右側のボタンからダイアログを開けます。")

        pp_dir = YSPathPickerGroup(default_path="C:/project/assets", is_directory=True, on_changed=self._create_logger("YSPathPickerGroup (Dir)", "on_changed"))
        pp_dir.setToolTip("フォルダを選択するためのパスウィジェットです。ダイアログの挙動がフォルダ選択モードになります。")

        self._add_catalog_row(
            fl_layout,
            "YSPathPickerGroup",
            "ファイルやフォルダのパス選択UIです。\nテキスト入力とダイアログ選択の両方に対応します。",
            [pp_file, pp_dir]
        )
        self.scroll_layout.addWidget(frame)

    def _build_layout_category(self):
        frame = YSFrameLayout(title="Layout Widgets", collapsable=True)
        fl_layout = frame.contentLayout()

        # FrameLayout
        fl_expanded = YSFrameLayout(
            title="Expanded Frame", collapsable=True, collapsed=False,
            on_toggled=self._create_logger("YSFrameLayout", "on_toggled")
        )
        fl_expanded.setToolTip("折りたたみ可能で、初期状態が展開されているフレームレイアウトです。")
        fl_expanded.addWidget(QtWidgets.QLabel("展開状態のフレームです。"))

        fl_collapsed = YSFrameLayout(title="Collapsed Frame", collapsable=True, collapsed=True)
        fl_collapsed.setToolTip("折りたたみ可能で、初期状態が折りたたまれているフレームレイアウトです。")
        fl_collapsed.addWidget(QtWidgets.QLabel("折りたたまれたフレームです。"))

        fl_locked = YSFrameLayout(title="Non-Collapsable Frame", collapsable=False)
        fl_locked.setToolTip("折りたたみ不可(collapsable=False)に設定され、常に中身が表示されるフレームです。")
        fl_locked.addWidget(QtWidgets.QLabel("折りたたみ不可（固定）のフレームです。"))

        self._add_catalog_row(
            fl_layout,
            "YSFrameLayout",
            "折りたたみ可能なフレームレイアウトです。\n関連するUIをグループ化し、見やすく整理します。",
            [fl_expanded, fl_collapsed, fl_locked]
        )
        self.scroll_layout.addWidget(frame)

    # ------------------------------------------------------------------
    # Window Geometry
    # ------------------------------------------------------------------

    def _restore_geometry(self):
        if not cmds.optionVar(exists=OPTIONVAR_GEOMETRY):
            return
        geometry_data = cmds.optionVar(query=OPTIONVAR_GEOMETRY)
        self.restoreGeometry(QtCore.QByteArray.fromBase64(geometry_data.encode("utf-8")))

    def _save_geometry(self):
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