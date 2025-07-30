"""
This module defines the configuration GUI for construction data runs.
Module contains both the `~PySide6.QtWidgets.QMainWindow` in
`ConfigureGUI` and the `~PySide6.QtWidgets.QApplication` in
`ConfigureApp`.
"""
__all__ = ["ConfigureGUI", "ConfigureApp"]

import logging
import logging.config
import re

from functools import partial
from pathlib import Path
from PySide6.QtCore import (
    Qt,
    QDir,
    Signal,
    Slot,
)
from PySide6.QtGui import QCloseEvent, QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QWidget,
    QSizePolicy,
    QPlainTextEdit,
    QListWidget,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
    QStackedWidget,
    QListWidgetItem,
)
from typing import Any, Dict, Union

# noqa
# import of qtawesome must happen after the PySide6 imports
import qtawesome as qta

from bapsf_motion.actors import RunManager, RunManagerConfig, MotionGroup
from bapsf_motion.gui.configure.helpers import gui_logger, gui_logger_config_dict
from bapsf_motion.gui.configure.motion_group_widget import MGWidget
from bapsf_motion.gui.lapd_xy_transform_calculator import LaPDXYTransformCalculator
from bapsf_motion.gui.widgets import (
    DiscardButton,
    DoneButton,
    QLogger,
    StyleButton,
    VLinePlain,
)
from bapsf_motion.utils import toml, _deepcopy_dict


_HERE = Path(__file__).parent


class RunWidget(QWidget):
    def __init__(self, parent: "ConfigureGUI", *, enable_run_name: bool = True):
        super().__init__(parent=parent)

        self._logger = gui_logger
        self._enable_run_name = (
            enable_run_name if isinstance(enable_run_name, bool) else True
        )

        # Define BUTTONS

        self.done_btn = DoneButton(parent=self)
        self.quit_btn = DiscardButton("Discard && Quit", parent=self)

        _btn = StyleButton("IMPORT", parent=self)
        _btn.setFixedHeight(48)
        _btn.setPointSize(16)
        _btn.setEnabled(False)
        self.import_btn = _btn

        _btn = StyleButton("EXPORT", parent=self)
        _btn.setFixedHeight(48)
        _btn.setPointSize(16)
        _btn.setEnabled(False)
        self.export_btn = _btn

        _btn = StyleButton("ADD", parent=self)
        _btn.setFixedHeight(38)
        _btn.setPointSize(16)
        self.add_mg_btn = _btn

        _btn = StyleButton("REMOVE", parent=self)
        _btn.setFixedHeight(38)
        _btn.setPointSize(16)
        _btn.setEnabled(False)
        self.remove_mg_btn = _btn

        _btn = StyleButton("Edit / Control", parent=self)
        _btn.setFixedHeight(38)
        _btn.setPointSize(16)
        _btn.setEnabled(False)
        self.modify_mg_btn = _btn

        # Define TEXT WIDGETS

        self.config_widget = QPlainTextEdit(parent=self)
        self.mg_list_widget = QListWidget(parent=self)
        _font = self.mg_list_widget.font()
        _font.setPointSize(14)
        self.mg_list_widget.setFont(_font)

        _txt_widget = QLineEdit(parent=self)
        font = _txt_widget.font()
        font.setPointSize(16)
        _txt_widget.setFont(font)
        self.run_name_widget = _txt_widget
        self.run_name_widget.setVisible(self._enable_run_name)

        _txt = QLabel("Run Name:  ", parent=self)
        _txt.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        _txt.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        font = _txt.font()
        font.setPointSize(16)
        _txt.setFont(font)
        self.run_name_label = _txt
        self.run_name_label.setVisible(self._enable_run_name)

        self.setLayout(self._define_layout())

        self._connect_signals()

    def _define_layout(self):

        # Create layout for banner (top header)
        banner_layout = self._define_banner_layout()

        # Create layout for toml window
        toml_widget = QWidget(parent=self)
        toml_widget.setLayout(self._define_toml_layout())
        toml_widget.setMinimumWidth(400)
        toml_widget.setMinimumWidth(500)
        toml_widget.sizeHint().setWidth(450)

        # Create layout for controls
        control_widget = QWidget(parent=self)
        control_widget.setLayout(self._define_control_layout())

        # Construct layout below top banner
        layout = QHBoxLayout()
        layout.addWidget(toml_widget)
        layout.addWidget(VLinePlain(parent=self))
        layout.addWidget(control_widget)

        # Populate the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(banner_layout)
        main_layout.addLayout(layout)

        return main_layout

    def _define_toml_layout(self):
        layout = QGridLayout()
        label = QLabel("Run Configuration", parent=self)
        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom
        )
        font = label.font()
        font.setPointSize(16)
        label.setFont(font)

        self.config_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        self.config_widget.setReadOnly(True)
        self.config_widget.font().setPointSize(14)
        self.config_widget.font().setFamily("Courier New")

        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.config_widget, 1, 0, 1, 2)
        layout.addWidget(self.import_btn, 2, 0)
        layout.addWidget(self.export_btn, 2, 1)

        return layout

    def _define_banner_layout(self):
        layout = QHBoxLayout()

        layout.addWidget(self.quit_btn)
        layout.addStretch()
        layout.addWidget(self.done_btn)

        return layout

    def _define_control_layout(self):
        layout = QVBoxLayout()

        mg_label = QLabel("Defined Motion Groups", parent=self)
        mg_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        )
        font = mg_label.font()
        font.setPointSize(16)
        mg_label.setFont(font)

        if self._enable_run_name:
            sub_layout = QHBoxLayout()
            sub_layout.addWidget(self.run_name_label)
            sub_layout.addWidget(self.run_name_widget)
            layout.addSpacing(18)
            layout.addLayout(sub_layout)
            layout.addSpacing(18)

        layout.addWidget(mg_label)
        layout.addWidget(self.mg_list_widget)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.add_mg_btn)
        sub_layout.addWidget(self.remove_mg_btn)
        layout.addLayout(sub_layout)

        layout.addWidget(self.modify_mg_btn)

        return layout

    def _connect_signals(self):
        self.mg_list_widget.itemClicked.connect(self.enable_mg_buttons)

    @Slot()
    def enable_mg_buttons(self):
        self.add_mg_btn.setEnabled(True)
        self.remove_mg_btn.setEnabled(True)
        self.modify_mg_btn.setEnabled(True)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def rm(self) -> Union[RunManager, None]:
        parent = self.parentWidget()  # type: "ConfigureGUI"
        try:
            return parent.rm
        except AttributeError:
            return None

    def closeEvent(self, event):
        self.logger.info("Closing RunWidget")
        event.accept()


class ConfigureGUI(QMainWindow):
    _OPENED_FILE = None  # type: Union[Path, None]
    configChanged = Signal()

    def __init__(
        self,
        *,
        config: Union[Path, str, Dict[str, Any], RunManagerConfig] = None,
        defaults: Union[Path, str, Dict[str, Any], None] = None,
    ):
        super().__init__()

        self._rm = None  # type: Union[RunManager, None]
        self._mg_being_modified = None  # type: Union[MotionGroup, None]

        # setup logger
        self._logging_config_dict = _deepcopy_dict(gui_logger_config_dict)
        logging.config.dictConfig(self._logging_config_dict)
        self._logger = gui_logger
        self._rm_logger = logging.getLogger("RM")

        # setup defaults
        self._defaults = None  # original defaults
        self._defaults_updated = None  # updated with configs from configured MGs
        self._set_defaults(defaults=defaults)

        self._define_main_window()

        enable_run_name = False if (
            self.defaults is not None
            and "run_name" in self.defaults
            and self.defaults["run_name"] != ""
        ) else True

        # define "important" qt widgets
        self._log_widget = QLogger(self._logger, parent=self)
        self._run_widget = RunWidget(parent=self, enable_run_name=enable_run_name)
        self._mg_widget = None  # type: Union[MGWidget, None]

        self._stacked_widget = QStackedWidget(parent=self)
        self._stacked_widget.addWidget(self._run_widget)

        # set up menu bar
        self._launched_windows = dict()  # type: Dict[str, Union[QMainWindow, QWidget]]
        self._define_menu_bar()

        layout = self._define_layout()

        widget = QWidget(parent=self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self._rm_logger.addHandler(self._log_widget.handler)

        self._connect_signals()

        if isinstance(config, Path) and not config.exists():
            config = None

        if config is None:
            run_name = (
                "A New Run" if self.defaults is None
                else self.defaults.get("run_name", "A New Run")
            )
            config = {"name": run_name}

        self.replace_rm(config=config)

    def _connect_signals(self):
        # Note: _mg_widget signals are connected in _spawn_mg_widget()
        #
        self._run_widget.import_btn.clicked.connect(self.toml_import)
        # self._run_widget.export_btn.clicked.connect(self.toml_export)
        self._run_widget.done_btn.clicked.connect(self.save_and_close)
        self._run_widget.quit_btn.clicked.connect(self.close)

        self._run_widget.add_mg_btn.clicked.connect(self._motion_group_configure_new)
        self._run_widget.remove_mg_btn.clicked.connect(self._motion_group_remove_from_rm)
        self._run_widget.modify_mg_btn.clicked.connect(
            self._motion_group_modify_existing
        )

        self._run_widget.run_name_widget.editingFinished.connect(self.change_run_name)

        self.configChanged.connect(self._config_changed_handler)

    def _define_main_window(self):
        self.setWindowTitle("Run Configuration")
        self.resize(1760, 990)
        self.setMinimumHeight(990)
        self.setMinimumWidth(1760)

    def _define_menu_bar(self):
        menu = self.menuBar()

        # calculator drop-down menu
        lapd_xy_calc_action = QAction("lapd_xy parameters", parent=self)
        lapd_xy_calc_action.triggered.connect(self._launch_lapd_xy_calculator)

        calc_menu = menu.addMenu("Calculators")
        calc_menu.addAction(lapd_xy_calc_action)

    def _define_layout(self):

        self._log_widget.setMinimumWidth(400)
        self._log_widget.setMaximumWidth(500)
        self._log_widget.sizeHint().setWidth(450)
        self._log_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Ignored)

        layout = QHBoxLayout()
        layout.addWidget(self._stacked_widget)
        layout.addWidget(VLinePlain(parent=self))
        layout.addWidget(self._log_widget)

        return layout

    @property
    def defaults(self) -> Dict[str, Any]:
        if self._defaults_updated is not None:
            return self._defaults_updated
        return self._defaults

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def rm(self) -> Union[RunManager, None]:
        return self._rm

    @rm.setter
    def rm(self, new_rm):
        if not isinstance(new_rm, RunManager):
            return
        elif isinstance(self._rm, RunManager):
            self._rm.terminate()

        self._rm = new_rm

    @property
    def logging_config_dict(self):
        return self._logging_config_dict

    @Slot()
    def _config_changed_handler(self):
        self.update_display_config_text()
        self.update_display_rm_name()
        self.update_display_mg_list()
        self.update_motion_builder_defaults()

    def replace_rm(self, config):
        if isinstance(self.rm, RunManager):
            self.rm.terminate()

        self.logger.info(f"Replacing the run manager with new config: {config}.")
        _rm = RunManager(config=config, auto_run=True, build_mode=True)

        _remove = []
        for key, mg in _rm.mgs.items():
            if mg.drive.naxes != 2:
                self.logger.warning(
                    f"The Configuration GUI currently only supports motion"
                    f" groups with a dimensionality of 2, got {mg.drive.naxes}"
                    f" for motion group '{mg.name}'.  Removing motion group."
                )
                _remove.append(key)

        for key in _remove:
            _rm.remove_motion_group(key)

        self.rm = _rm
        self.configChanged.emit()

    @Slot()
    def save_and_close(self):
        # save the toml configuration
        # TODO: write code to save current toml configuration to a tmp file

        self.close()

    @Slot()
    def toml_export(self):
        ...

    @Slot()
    def toml_import(self):
        path = QDir.currentPath() if self._OPENED_FILE is None \
            else f"{self._OPENED_FILE.parent}"

        file_name, _filter = QFileDialog.getOpenFileName(
            self,
            "Open file",
            path,
            "TOML file (*.toml)",
        )
        file_name = Path(file_name)

        if not file_name.is_file():
            # dialog was canceled
            return

        self.logger.info(f"Opening and reading file: {file_name} ...")

        with open(file_name, "rb") as f:
            run_config = toml.load(f)

        self.replace_rm(run_config)
        self._OPENED_FILE = file_name
        self.logger.info(f"... Success!")

    def update_display_config_text(self):
        self.logger.info(f"Updating the run config toml: {self.rm.config.as_toml_string}")
        self._run_widget.config_widget.setPlainText(self.rm.config.as_toml_string)

    def update_display_rm_name(self):
        rm_name = self.rm.config["name"]
        self._run_widget.run_name_widget.setText(rm_name)

    def update_display_mg_list(self):
        self._run_widget.mg_list_widget.clear()
        self._run_widget.remove_mg_btn.setEnabled(False)
        self._run_widget.modify_mg_btn.setEnabled(False)

        if self.rm.mgs is None or not self.rm.mgs:
            return

        for key, mg in self.rm.mgs.items():
            label = self._generate_mg_list_name(key, mg.config["name"])
            self.logger.info(f"Adding to MG List - {label}")
            _icon = (
                qta.icon("fa5.window-close", color="red") if mg.terminated
                else qta.icon("fa5.check-circle", color="green")
            )  # type: QIcon
            _item = QListWidgetItem(
                _icon,
                label,
                listview=self._run_widget.mg_list_widget,
            )

    @Slot()
    def change_run_name(self):
        name = self._run_widget.run_name_widget.text()

        if self.rm is None:
            self.replace_rm({"name": name})
        else:
            self.rm.config.update_run_name(name)
            self.configChanged.emit()

    @Slot()
    def _motion_group_configure_new(self):
        self._spawn_mg_widget()
        self._switch_stack()

    @Slot()
    def _motion_group_modify_existing(self):
        item = self._run_widget.mg_list_widget.currentItem()
        key, mg_name = self._get_mg_name_from_list_name(item.text())
        mg = self.rm.mgs[key]

        if not mg.terminated:
            mg.terminate(delay_loop_stop=True)

        self._mg_being_modified = mg
        self._spawn_mg_widget(mg)
        self._mg_widget.mg_index = key
        self._switch_stack()

    @Slot()
    def _motion_group_remove_from_rm(self):
        item = self._run_widget.mg_list_widget.currentItem()
        identifier, mg_name = self._get_mg_name_from_list_name(item.text())
        self.rm.remove_motion_group(identifier=identifier)
        self.configChanged.emit()

    @Slot()
    def _restart_run_manager(self):
        if isinstance(self.rm, RunManager) and not self.rm.terminated:
            # RunManager is still running, no need to restart
            return

        if not isinstance(self.rm, RunManager):
            # No RunManager to restart
            return

        self.replace_rm(self.rm.config)

        self._mg_being_modified = None

    def _set_defaults(self, defaults: Union[Path, str, Dict[str, Any], None]):
        if defaults is None:
            self._defaults = None
            return
        elif isinstance(defaults, str):
            # could be path to TOML file or a TOML like string
            if Path(defaults).exists():
                with open(defaults, "rb") as f:
                    defaults = toml.load(f)
            else:
                defaults = toml.loads(defaults)
        elif isinstance(defaults, Path):
            # path to TOML file
            with open(defaults, "rb") as f:
                defaults = toml.load(f)
        elif not isinstance(defaults, dict):
            raise TypeError(
                f"Expected 'defaults' to be of type dict, got type {type(defaults)}."
            )

        if (
            "bapsf_motion" not in defaults.keys()
            or not isinstance(defaults["bapsf_motion"], dict)
        ):
            # dictionary does not contain a setup for bapsf_motion
            defaults = None
        elif (
            "defaults" not in defaults["bapsf_motion"].keys()
            or not isinstance(defaults["bapsf_motion"]["defaults"], dict)
        ):
            # dictionary does not contain a defaults setup for bapsf_motion
            defaults = None
        else:
            defaults = defaults["bapsf_motion"]["defaults"]

        self._defaults = defaults

    def update_motion_builder_defaults(self):
        if not isinstance(self.rm, RunManager):
            self._defaults_updated = None
            return

        if len(self.rm.mgs) == 0:
            self._defaults_updated = None
            return

        if self._defaults is not None:
            self._defaults_updated = _deepcopy_dict(self._defaults)

        if self._defaults is None:
            self._defaults_updated = {"motion_builder": {}}
        elif "motion_builder" not in self._defaults:
            self._defaults_updated["motion_builder"] = {}
        else:
            self._defaults_updated["motion_builder"] = _deepcopy_dict(
                self._defaults["motion_builder"]
            )

        mb_defaults = self._defaults_updated["motion_builder"]
        n_mb_configs = len(mb_defaults) - 1
        for mg in self.rm.mgs.values():
            drive_name, ml_name = MGWidget.split_motion_group_name(mg.config["name"])

            _id = None
            for _default_id in mb_defaults.keys():
                if _default_id == "default":
                    continue

                if ml_name == mb_defaults[_default_id]["name"]:
                    _id = _default_id
                    break

            if _id is None:
                _id = f"{n_mb_configs}"
                n_mb_configs += 1

            mb_defaults[_id] = {
                "name": ml_name,
                **_deepcopy_dict(mg.config["motion_builder"]),
            }

    def _spawn_mg_widget(self, mg: MotionGroup = None):
        config = None if not isinstance(mg, MotionGroup) else mg.config

        # terminate RunManager so we can avoid communication issue during
        # MotionGroup configuration
        if isinstance(self.rm, RunManager) and not self.rm.terminated:
            self.rm.terminate()

        self._mg_widget = MGWidget(
            mg_config=config,
            defaults=self.defaults,
            parent=self,
        )
        self._mg_widget.closing.connect(self._switch_stack)
        self._mg_widget.returnConfig.connect(self.add_mg_to_rm)
        self._mg_widget.discard_btn.clicked.connect(self._restart_run_manager)

        return self._mg_widget

    @Slot()
    def _switch_stack(self):
        _w = self._stacked_widget.currentWidget()
        if isinstance(_w, RunWidget):
            self._stacked_widget.addWidget(self._mg_widget)
            self._stacked_widget.setCurrentWidget(self._mg_widget)
        else:
            # the stack widget is the MGWidget instance
            self._stacked_widget.removeWidget(_w)
            self._stacked_widget.setCurrentIndex(0)
            _w.close()
            _w.deleteLater()
            self._mg_widget = None

    @Slot(int, object)
    def add_mg_to_rm(self, index: int, mg_config: Dict[str, Any]):
        index = None if index == -1 else index

        self.logger.info(
            f"Adding MotionGroup to the run: index = '{index}', config = {mg_config}."
        )

        self.rm.add_motion_group(config=mg_config, identifier=index)
        self._restart_run_manager()
        self._mg_being_modified = None

    @staticmethod
    def _generate_mg_list_name(index, mg_name):
        return f"[{index:2d}]   {mg_name}"

    @staticmethod
    def _get_mg_name_from_list_name(list_name):
        match = re.compile(
            r"\[\s*(?P<index>[0-9]+)\]\s+(?P<name>.+)"
        ).fullmatch(list_name)
        return (
            None
            if match is None
            else (int(match.group("index")), match.group("name"))
        )

    def _launch_lapd_xy_calculator(self):
        if "lapd_xy_calculator" in self._launched_windows:
            _window = self._launched_windows["lapd_xy_calculator"]
            _window.show()
            _window.activateWindow()
            _window.closing.connect(  # noqa
                partial(self._launched_windows_closed, "lapd_xy_calculator")
            )
            return

        _window = LaPDXYTransformCalculator()
        _window.setObjectName("lapd_xy_calculator")
        _window.show()
        _window.activateWindow()

        self._launched_windows["lapd_xy_calculator"] = _window

    @Slot(str)
    def _launched_windows_closed(self, name: str):
        if name not in self._launched_windows:
            return

        _window = self._launched_windows.pop(name)
        _window.deleteLater()

    def closeEvent(self, event: "QCloseEvent") -> None:
        self.logger.info("Closing ConfigureGUI")

        self.configChanged.disconnect()

        if isinstance(self.rm, RunManager) and not self.rm.terminated:
            self.rm.terminate()
            self.rm = None

        if isinstance(self._mg_widget, MGWidget):
            self._mg_widget.close()

        self._run_widget.close()

        for _window in self._launched_windows.values():
            _window.close()
            _window.deleteLater()
        self._launched_windows = dict()

        event.accept()


class ConfigureApp(QApplication):
    qss_file_path = (_HERE / "configure.qss").resolve()

    def __init__(
        self,
        *args,
        config: Union[Path, str, Dict[str, Any], RunManagerConfig] = None,
        defaults: Union[Path, str, Dict[str, Any], None] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setStyle("Fusion")
        self.styleHints().setColorScheme(Qt.ColorScheme.Light)
        self.reload_style_sheet()

        self._window = ConfigureGUI(config=config, defaults=defaults)
        self._window.show()
        self._window.activateWindow()

    def reload_style_sheet(self):
        with open(self.qss_file_path, "r") as f:
            qss_style = f.read()

        self.setStyleSheet(qss_style)
