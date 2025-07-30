"""
Module contains the functionality associated with the |MotionBuilder|
configuration overlay portion of the configuration GUI.
"""
__all__ = ["MotionBuilderConfigOverlay"]

import ast
import inspect
import math
import numpy as np
import matplotlib as mpl
import re
import typing
import xarray as xr

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QWidget,
    QSizePolicy,
    QListWidget,
    QVBoxLayout,
    QComboBox,
    QFrame,
)
from typing import Any, Dict, Optional, Union

# noqa
# import of qtawesome must happen after the PySide6 imports
import qtawesome as qta

from bapsf_motion.actors import MotionGroup
from bapsf_motion.gui.configure import motion_group_widget as mgw
from bapsf_motion.gui.configure.bases import _ConfigOverlay
from bapsf_motion.gui.configure.helpers import read_parameter_hints
from bapsf_motion.gui.configure.motion_space_display import MotionSpaceDisplay
from bapsf_motion.gui.widgets import (
    DiscardButton,
    DoneButton,
    HLinePlain,
    IconButton,
    QLineEditSpecialized,
    StyleButton,
    VLinePlain,
)
from bapsf_motion.motion_builder import MotionBuilder
from bapsf_motion.motion_builder.layers import layer_registry
from bapsf_motion.motion_builder.exclusions import exclusion_registry, GovernExclusion
from bapsf_motion.utils import _deepcopy_dict
from bapsf_motion.utils import units as u

# noqa
mpl.use("qtagg")  # matplotlib's backend for Qt bindings
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # noqa


class MotionBuilderConfigOverlay(_ConfigOverlay):
    layer_registry = layer_registry
    exclusion_registry = exclusion_registry

    def __init__(self, mg: MotionGroup, parent: "mgw.MGWidget" = None):
        super().__init__(mg, parent)

        self._mb = None

        self._space_input_widgets = {}  # type: Dict[str, Dict[str, QLineEditSpecialized]]
        self._mpl_canvas_full_draw = True

        _parameter_hints = read_parameter_hints()
        self._parameter_hints_layer = _parameter_hints.pop("layer", None)
        self._parameter_hints_exclusion = _parameter_hints.pop("exclusion", None)

        # _param_inputs:
        #     dictionary of input parameters for instantiating an exclusion or
        #     points layer
        # _params_widget:
        #     top enclosing widget for setting and configuring parameter inputs
        #     for an exclusion or point layer (i.e. widget that contains all
        #     configuring widgets)
        # _params_field_widget:
        #     child widget of _params_widget that contains the actual input fields
        #     for configuring _param_inputs (i.e. widget container for all the
        #     input widgets that map to the layer/exclusion input args/kwargs)
        # _params_input_widgets:
        #     dictionary of the actual widgets that control the _param_inputs
        #     values (i.e. the input widgets that map to the layer/exclusion
        #     input args/kwargs)
        self._param_inputs = {}  # type: Dict[str, Any]
        self._params_widget = QWidget(parent=self)
        self._params_field_widget = QWidget(parent=self._params_widget)
        self._params_input_widgets = {}  # type: Dict[str, Dict[str, QLineEditSpecialized]]
        self.params_label = None
        self.params_add_btn = None
        self.params_discard_btn = None
        self.select_type_label = None
        self.params_combo_box = None
        self._initialize_params_layout_widgets()

        # SET UP LEFT WIDGETS (i.e. list boxes)

        self.exclusion_list_box = None  # type: Union[QListWidget, None]
        self.add_ex_btn = None
        self.remove_ex_btn = None
        self.edit_ex_btn = None
        self._initialize_exclusion_list_layout_widgets()

        self.layer_list_box = None  # type: Union[QListWidget, None]
        self.add_ly_btn = None
        self.remove_ly_btn = None
        self.edit_ly_btn = None
        self.layer_move_up_btn = None
        self.layer_move_down_btn = None
        self.layer_ml_combine_toggle = None
        self._initialize_layer_list_layout_widgets()

        # SET UP PLOT WIDGET
        self.mpl_canvas = MotionSpaceDisplay(parent=self)
        self.mpl_canvas.display_position = False
        self.mpl_canvas.display_target_position = False
        if isinstance(self.mg, MotionGroup) and isinstance(self.mg.mb, MotionBuilder):
            self.mpl_canvas.link_motion_builder(self.mg.mb)

        self.animate_ml_widget = QFrame(parent=self)
        self.animate_ml_widget.setObjectName("animate_ml_controls")
        self.animate_ml_widget.setStyleSheet(
            """
            QFrame#animate_ml_controls {
                border: 2px solid rgb(125, 125, 125);
                border-radius: 5px; 
                padding: 0px;
                margin: 0px;
            }
            """
        )
        self.animate_ml_widget.setFixedWidth(72)
        self.animate_ml_widget.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        _btn = StyleButton("\n".join(list("ANIMATE")), parent=self.animate_ml_widget)
        _btn.setFixedWidth(44)
        _btn.setFixedHeight(130)
        _font = _btn.font()
        _font.setBold(True)
        _btn.setFont(_font)
        self.animate_ml_btn = _btn

        _btn = StyleButton("\n".join(list("CLEAR")), parent=self.animate_ml_widget)
        _btn.setFixedWidth(44)
        _btn.setFixedHeight(100)
        _font = _btn.font()
        _font.setBold(True)
        _btn.setFont(_font)
        self.animate_ml_clear_btn = _btn

        # non-widget initialization

        self._initialize_motion_builder()
        self._initialize_exclusion_list_box()
        self._initialize_layer_list_box()
        self.setLayout(self._define_layout())

        self.update_exclusion_list_box()
        self.update_layer_list_box()
        self.update_layer_ml_combine_toggle()
        self.update_canvas()

        self._connect_signals()

    def _connect_signals(self):
        super()._connect_signals()

        self.configChanged.connect(self._config_changed_handler)

        self.add_ex_btn.clicked.connect(self._exclusion_configure_new)
        self.remove_ex_btn.clicked.connect(self._exclusion_remove_from_mb)
        self.edit_ex_btn.clicked.connect(self._exclusion_modify_existing)

        self.add_ly_btn.clicked.connect(self._layer_configure_new)
        self.remove_ly_btn.clicked.connect(self._layer_remove_from_mb)
        self.edit_ly_btn.clicked.connect(self._layer_modify_existing)

        self.params_discard_btn.clicked.connect(self._hide_and_clear_params_widget)
        self.params_add_btn.clicked.connect(self._add_to_mb)

        self.params_combo_box.currentTextChanged.connect(
            self._refresh_params_widget_from_combo_box_change
        )

        self.layer_list_box.itemSelectionChanged.connect(
            self.layer_list_box_set_btn_enable
        )
        self.exclusion_list_box.itemSelectionChanged.connect(
            self.exclusion_list_box_set_btn_enable
        )

        self.layer_ml_combine_toggle.clicked.connect(
            self._toggle_layer_to_motionlist_scheme
        )

        self.layer_move_up_btn.clicked.connect(self._layer_list_item_move_up)
        self.layer_move_down_btn.clicked.connect(self._layer_list_item_move_down)

        self.mpl_canvas.animateMotionListFinished.connect(
            self._animate_motion_list_finished
        )
        self.mpl_canvas.animateMotionListCleared.connect(
            self._animate_motion_list_finished
        )
        self.mpl_canvas.animateMotionListStarted.connect(
            self._animate_motion_list_btn_txt_to_pause
        )
        self.mpl_canvas.animateMotionListPaused.connect(
            self._animate_motion_list_btn_txt_to_animate
        )
        self.animate_ml_btn.clicked.connect(self._animate_motion_list)
        self.animate_ml_clear_btn.clicked.connect(
            self.mpl_canvas.animate_motion_list_clear
        )

    def _define_layout(self):
        #
        #  +-------------------------------------------------------+
        #  | banner_layout                                         |
        #  +-------------------+-----------------------------------+
        #  |     sidebar       | right_area                        |
        #  |                   |                                   |
        #  | +--------------+  |  +-----------------------------+  |
        #  | | motion_space |  |  | Plot                        |  |
        #  | |              |  |  |                             |  |
        #  | +--------------+  |  |                             |  |
        #  |                   |  |                             |  |
        #  | +--------------+  |  +-----------------------------+  |
        #  | |  exclusion   |  |                                   |
        #  | |  list        |  |  +--params_widget--------------+  |
        #  | +--------------+  |  |                             |  |
        #  |                   |  | banner                      |  |
        #  | +--------------+  |  |                             |  |
        #  | |  layer       |  |  | +--params_field_widget----+ |  |
        #  | |  list        |  |  | |                         | |  |
        #  | +--------------+  |  | +-------------------------+ |  |
        #  |                   |  +-----------------------------+  |
        #  +-------------------+-----------------------------------+
        #
        sub_layout = QHBoxLayout()
        sub_layout.setSpacing(0)
        sub_layout.setContentsMargins(0, 0, 0, 0)
        sub_layout.addWidget(self._define_sidebar_widget())
        sub_layout.addSpacing(8)
        sub_layout.addWidget(VLinePlain(parent=self))
        sub_layout.addSpacing(8)
        sub_layout.addWidget(self._define_right_area_widget())

        layout = QVBoxLayout()
        layout.setSpacing(12)

        layout.addLayout(self._define_banner_layout())
        layout.addWidget(HLinePlain(parent=self))
        layout.addSpacing(6)
        layout.addLayout(sub_layout)

        return layout

    @property
    def dimensionality(self):
        return self.mg.drive.naxes

    @property
    def axis_names(self):
        return self.mg.drive.anames

    @property
    def mb(self) -> Union[MotionBuilder, None]:
        if (
            self._mb is None
            and isinstance(self.mg, MotionGroup)
            and isinstance(self.mg.mb, MotionBuilder)
        ):
            return self.mg.mb

        return self._mb

    @property
    def parameter_hints_layer(self):
        if self._parameter_hints_layer is None:
            self._parameter_hints_layer = dict()
        return self._parameter_hints_layer

    @property
    def parameter_hints_exclusion(self):
        if self._parameter_hints_exclusion is None:
            self._parameter_hints_exclusion = dict()
        return self._parameter_hints_exclusion

    # -- LAYOUT AND WIDGET DEFINITIONS --

    def _define_banner_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(
            self.discard_btn,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        layout.addStretch()
        layout.addWidget(
            self.done_btn,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )
        return layout

    def _define_sidebar_widget(self):
        _widget = QWidget(parent=self)
        _widget.setFixedWidth(400)
        _widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(_widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)
        layout.addLayout(self._define_motion_space_layout())
        layout.addSpacing(20)
        layout.addLayout(self._define_exclusion_list_layout())
        layout.addSpacing(24)
        layout.addLayout(self._define_layer_list_layout())
        layout.addStretch()

        return _widget

    def _define_right_area_widget(self):
        _txt = QLabel("Motion\nList\nAnimate", parent=self.animate_ml_widget)
        _txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        _animate_title = _txt

        animate_layout = QVBoxLayout()
        animate_layout.setContentsMargins(8, 4, 8, 8)
        animate_layout.addWidget(_animate_title)
        animate_layout.addSpacing(4)
        animate_layout.addWidget(
            self.animate_ml_btn,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        animate_layout.addWidget(
            self.animate_ml_clear_btn,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        animate_layout.addStretch()
        self.animate_ml_widget.setLayout(animate_layout)

        side_control_layout = QVBoxLayout()
        side_control_layout.setContentsMargins(0, 0, 0, 0)
        side_control_layout.addWidget(self.animate_ml_widget)
        side_control_layout.addStretch()

        plot_layout = QHBoxLayout()
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_layout.addLayout(side_control_layout)
        plot_layout.addWidget(self.mpl_canvas)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(plot_layout)
        layout.addWidget(self._define_params_widget())
        layout.addStretch(1)

        _widget = QWidget(parent=self)
        _widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        _widget.setLayout(layout)
        return _widget

    def _define_motion_space_layout(self):

        _txt = QLabel("Motion Space", parent=self)
        font = _txt.font()
        font.setPointSize(16)
        font.setBold(True)
        _txt.setFont(font)

        layout = QGridLayout()
        layout.setContentsMargins(8, 4, 12, 4)
        layout.setSpacing(4)
        layout.setColumnMinimumWidth(4, 18)
        layout.setRowMinimumHeight(1, 12)
        layout.addWidget(
            _txt, 0, 0, 1, 8,
            alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )

        for ii, args in self.mb.config["space"].items():
            axis = self.mg.drive.axes[ii]
            name = args["label"]

            _txt = QLabel(name, parent=self)
            font = _txt.font()
            font.setPointSize(12)
            _txt.setFont(font)
            axis_label = _txt

            _txt = QLabel("range", parent=self)
            _txt.setFont(font)
            range_label = _txt

            _txt = QLineEditSpecialized(f"{args['range'][0]:.2f}", parent=self)
            _txt.setFont(font)
            _txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            _txt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            _txt.setObjectName(f"{name}_min")
            _txt.setValidator(QDoubleValidator(decimals=1))  # noqa
            _txt.editingFinishedPayload.connect(self._validate_space_inputs)
            min_range = _txt

            _txt = QLineEditSpecialized(f"{args['range'][1]:.2f}", parent=self)
            _txt.setFont(font)
            _txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            _txt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            _txt.setObjectName(f"{name}_max")
            _txt.setValidator(QDoubleValidator(decimals=1))  # noqa
            _txt.editingFinishedPayload.connect(self._validate_space_inputs)
            max_range = _txt

            _txt = QLabel("Δ", parent=self)
            _txt.setFont(font)
            delta_label = _txt

            _txt = QLineEditSpecialized(
                f"{(args['range'][1] - args['range'][0]) / args['num']:.2f}",
                parent=self
            )
            _txt.setFont(font)
            _txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            _txt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            _txt.setObjectName(f"{name}_delta")
            _txt.setValidator(QDoubleValidator(decimals=2))  # noqa
            _txt.editingFinishedPayload.connect(self._validate_space_inputs)
            delta = _txt

            _txt = QLabel(f"{axis.units}", parent=self)
            _txt.setFont(font)
            unit_label = _txt

            layout.addWidget(
                axis_label, ii + 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignRight
            )
            layout.addWidget(
                range_label, ii + 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
            layout.addWidget(
                min_range, ii + 2, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
            layout.addWidget(
                max_range, ii + 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
            layout.addWidget(
                delta_label, ii + 2, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignRight
            )
            layout.addWidget(
                delta, ii + 2, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
            layout.addWidget(
                unit_label, ii + 2, 7, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft
            )

            self._space_input_widgets[name] = {
                "min": min_range,
                "max": max_range,
                "delta": delta,
            }

        return layout

    def _define_exclusion_list_layout(self):

        _txt = QLabel("Exclusion Layers", parent=self)
        font = _txt.font()
        font.setPointSize(16)
        font.setBold(True)
        _txt.setFont(font)
        title = _txt

        sub_layout = QHBoxLayout()
        sub_layout.setContentsMargins(0, 0, 0, 0)
        sub_layout.setSpacing(8)
        sub_layout.addWidget(self.add_ex_btn)
        sub_layout.addWidget(self.remove_ex_btn)
        sub_layout.addWidget(self.edit_ex_btn)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(
            title,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )
        layout.addSpacing(2)
        layout.addWidget(self.exclusion_list_box)
        layout.addLayout(sub_layout)

        return layout

    def _define_layer_list_layout(self):

        _txt = QLabel('Point "Motion List" Layers', parent=self)
        font = _txt.font()
        font.setPointSize(16)
        font.setBold(True)
        _txt.setFont(font)
        title = _txt

        order_label = QLabel("\n".join(list("ORDER ITEM")), parent=self)
        order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        order_label.setFixedWidth(10)
        order_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        _font = order_label.font()
        _font.setBold(True)
        order_label.setFont(_font)

        _txt = QLabel("Merge", parent=self)
        _txt.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        _font = _txt.font()
        _font.setPointSize(12)
        _txt.setFont(_font)
        _merge_txt = _txt

        _txt = QLabel("Sequential", parent=self)
        _txt.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        _txt.setFont(_font)
        _sequential_txt = _txt

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        btn_layout.addWidget(self.add_ly_btn)
        btn_layout.addWidget(self.remove_ly_btn)
        btn_layout.addWidget(self.edit_ly_btn)

        order_layout = QVBoxLayout()
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.addStretch()
        order_layout.addWidget(self.layer_move_up_btn)
        order_layout.addSpacing(4)
        order_layout.addWidget(self.layer_move_down_btn)
        order_layout.addStretch()
        order_widget = QWidget(parent=self)
        order_widget.setLayout(order_layout)
        order_widget.setFixedWidth(24)

        list_layout = QHBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.addWidget(self.layer_list_box)
        list_layout.addWidget(order_label)
        list_layout.addWidget(order_widget)

        ml_combine_layout = QHBoxLayout()
        ml_combine_layout.setContentsMargins(0, 0, 0, 0)
        ml_combine_layout.addStretch()
        ml_combine_layout.addWidget(_sequential_txt)
        ml_combine_layout.addWidget(self.layer_ml_combine_toggle)
        ml_combine_layout.addWidget(_merge_txt)
        ml_combine_layout.addStretch()
        ml_combine_layout.addSpacing(24+10+12)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(
            title,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )
        layout.addSpacing(2)
        layout.addLayout(list_layout)
        layout.addLayout(ml_combine_layout)
        layout.addLayout(btn_layout)

        return layout

    def _define_params_layout(self):
        self.params_add_btn.setEnabled(False)

        banner_layout = QHBoxLayout()
        banner_layout.setContentsMargins(0, 0, 0, 0)
        banner_layout.addSpacing(12)
        banner_layout.addWidget(
            self.params_label,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        )
        banner_layout.addStretch(1)
        banner_layout.addWidget(
            self.select_type_label,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
        )
        banner_layout.addSpacing(4)
        banner_layout.addWidget(
            self.params_combo_box,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        )
        banner_layout.addStretch(1)
        banner_layout.addWidget(
            self.params_discard_btn,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
        )
        banner_layout.addWidget(
            self.params_add_btn,
            alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
        )
        banner_layout.addSpacing(12)
        banner_widget = QWidget(parent=self._params_widget)
        banner_widget.setLayout(banner_layout)
        banner_widget.setFixedHeight(38)

        hline = HLinePlain(parent=self._params_widget)
        hline.set_color(125, 125, 125)
        hline.setLineWidth(2)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(banner_widget)
        layout.addWidget(hline)
        layout.addWidget(self._params_field_widget)
        layout.addStretch()

        return layout

    def _define_params_widget(self):
        self._params_widget.setLayout(self._define_params_layout())
        self._params_widget.hide()
        return self._params_widget

    def _define_params_field_widget(self, ex_or_ly, _type):
        _registry = (
            self.exclusion_registry
            if ex_or_ly == "exclusion"
            else self.layer_registry
        )
        _hints = (
            self.parameter_hints_exclusion
            if ex_or_ly == "exclusion"
            else self.parameter_hints_layer
        )
        _hints = None if _type not in _hints else _hints[_type]

        self._param_inputs.update(
            {"_type": _type, "_registry": _registry, "_hints": _hints}
        )

        params = _registry.get_input_parameters(_type)

        _widget = QWidget(parent=self._params_widget)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(4)

        layout.setColumnMinimumWidth(0, 48)
        layout.setColumnMinimumWidth(2, 8)
        layout.setColumnMinimumWidth(4, 32)
        layout.setColumnMinimumWidth(5, 32)
        layout.setColumnMinimumWidth(6, 48)

        layout.setColumnStretch(0, 0)
        # layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)
        layout.setColumnStretch(3, 4)
        layout.setColumnStretch(4, 0)
        layout.setColumnStretch(5, 0)
        layout.setColumnStretch(6, 0)

        ii = 0
        _row_height = 24
        for key, val in params.items():
            # determine the seed/default value for the layer or exclusion input
            if key in self._param_inputs:
                default = self._param_inputs[key]
            elif val["param"].default is not val["param"].empty:
                default = val["param"].default
                self._param_inputs[key] = default
            else:
                default = None
                self._param_inputs[key] = default

            # determine parameter hint for layer or exclusion input
            _hint = None if (_hints is None or key not in _hints) else _hints[key]

            _txt = QLabel(key, parent=_widget)
            _txt.setFixedHeight(_row_height)
            _txt.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            font = _txt.font()
            font.setPointSize(14)
            _txt.setFont(font)
            _variable_name = _txt

            annotation = val['param'].annotation
            if inspect.isclass(annotation):
                annotation = annotation.__name__
            annotation = f"{annotation}".split(".")[-1]

            _txt = QLabel("", parent=_widget)
            _txt.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
            )
            _icon = qta.icon("msc.symbol-type-parameter")
            # size = math.floor(0.9 * _row_height)
            size = _row_height
            _txt.setPixmap(_icon.pixmap(QSize(size, size)))
            _txt.setToolTip(annotation)
            _txt.setToolTipDuration(30000)
            _type_icon = _txt

            text = "" if default is None else f"{default}"
            _txt = QLineEditSpecialized(text, parent=_widget)
            _txt.setObjectName(key)
            _txt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            _txt.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            font = _txt.font()
            font.setPointSize(14)
            _txt.setFont(font)
            _input = _txt
            if _hint is not None:
                _input.setPlaceholderText(_hint)
            _input.editingFinishedPayload.connect(self._update_param_inputs)

            _txt = QLabel("", parent=_widget)
            _txt.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
            )
            _icon = qta.icon("fa.question-circle-o")
            size = math.floor(0.95 * _row_height)
            _txt.setPixmap(_icon.pixmap(QSize(size, size)))
            _txt.setToolTip("\n".join(val["desc"]))
            _txt.setToolTipDuration(30000)
            _help_icon = _txt

            layout.setRowMinimumHeight(ii, _row_height)
            layout.setRowStretch(ii, 0)

            layout.addWidget(_variable_name, ii, 1)
            layout.addWidget(_input, ii, 3)
            layout.addWidget(_type_icon, ii, 4)
            layout.addWidget(_help_icon, ii, 5)

            ii += 1

        _widget.setLayout(layout)
        return _widget

    def _initialize_exclusion_list_layout_widgets(self):
        self.exclusion_list_box = QListWidget(parent=self)
        self.exclusion_list_box.setMinimumHeight(250)
        _font = self.exclusion_list_box.font()
        _font.setPointSize(11)
        self.exclusion_list_box.setFont(_font)

        self.add_ex_btn = self._generate_btn_widget("ADD")

        self.remove_ex_btn = self._generate_btn_widget("REMOVE")
        self.remove_ex_btn.setEnabled(False)

        self.edit_ex_btn = self._generate_btn_widget("EDIT")
        self.edit_ex_btn.setEnabled(False)

    def _initialize_layer_list_layout_widgets(self):
        self.layer_list_box = QListWidget(parent=self)
        self.layer_list_box.setMinimumHeight(250)
        _font = self.layer_list_box.font()
        _font.setPointSize(11)
        self.layer_list_box.setFont(_font)

        self.add_ly_btn = self._generate_btn_widget("ADD")

        self.remove_ly_btn = self._generate_btn_widget("REMOVE")
        self.remove_ly_btn.setEnabled(False)

        self.edit_ly_btn = self._generate_btn_widget("EDIT")
        self.edit_ly_btn.setEnabled(False)

        self.layer_move_up_btn = IconButton("fa.arrow-up", parent=self)
        self.layer_move_up_btn.setIconSize(20)
        self.layer_move_up_btn.setFixedWidth(24)
        self.layer_move_up_btn.setFixedHeight(48)
        self.layer_move_down_btn = IconButton("fa.arrow-down", parent=self)
        self.layer_move_down_btn.setIconSize(18)
        self.layer_move_down_btn.setFixedWidth(24)
        self.layer_move_down_btn.setFixedHeight(48)

        _btn = StyleButton("ML Combine", parent=self)
        _btn.setFixedHeight(24)
        font = _btn.font()
        font.setPointSize(10)
        _btn.setFont(font)
        _color_str = "rgb(52, 161, 219)"
        _btn.update_style_sheet(
            styles={
                "background-color": re.sub(
                    " +",
                    " ",
                    f"""qlineargradient(
                        x1:0,
                        y1:0, 
                        x2:1, 
                        y2:0,
                        stop: 0 {_color_str},
                        stop: 0.1 {_color_str},
                        stop: 0.12 rgb(163, 163, 163),
                        stop: 1 rgb(163, 163, 163)
                    )""".replace("\n", "")
                ),
            },
            action="base",
        )
        _btn.update_style_sheet(
            styles={
                "background-color": re.sub(
                    " +",
                    " ",
                    f"""qlineargradient(
                        x1:0,
                        y1:0, 
                        x2:1, 
                        y2:0,
                        stop: 0 rgb(163, 163, 163),
                        stop: 0.88 rgb(163, 163, 163),
                        stop: 0.9 {_color_str},
                        stop: 1 {_color_str}
                    )""".replace("\n", "")
                ),
            },
            action="checked",
        )
        _btn.setCheckable(True)
        _btn.setChecked(False)
        _btn.setFixedWidth(180)
        self.layer_ml_combine_toggle = _btn

    def _initialize_params_layout_widgets(self):
        self._params_widget.setMinimumHeight(300)
        size_policy = self._params_widget.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self._params_widget.setSizePolicy(size_policy)

        _txt = QLabel("", parent=self._params_widget)
        _font = _txt.font()
        _font.setPointSize(14)
        _font.setFamily("Courier New")
        _font.setBold(True)
        _txt.setFont(_font)
        self.params_label = _txt

        _btn = DoneButton("Add / Update", parent=self._params_widget)
        _btn.setFixedHeight(34)
        _font = _btn.font()
        _font.setPointSize(12)
        _btn.setFont(_font)
        _btn.shrink_width()
        self.params_add_btn = _btn

        _btn = DiscardButton(parent=self._params_widget)
        _btn.setFixedHeight(34)
        _font = _btn.font()
        _font.setPointSize(12)
        _btn.setFont(_font)
        _btn.shrink_width(scale=2)
        self.params_discard_btn = _btn

        _txt = QLabel("Type :", parent=self._params_widget)
        _font = _txt.font()
        _font.setPixelSize(16)
        _font.setBold(False)
        _txt.setFont(_font)
        self.select_type_label = _txt

        _txt = QComboBox(parent=self._params_widget)
        _txt.setFixedHeight(34)
        _txt.setFixedWidth(250)
        _txt.setEditable(False)
        font = _txt.font()
        font.setPointSize(12)
        _txt.setFont(font)
        self.params_combo_box = _txt

    def _initialize_exclusion_list_box(self):
        ex_types = set(ex.exclusion_type for ex in self.mb.exclusions)

        _available = self.exclusion_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        ex_names = []
        if not _available:
            self.logger.warning(
                "There are no coded exclusion layers that work with the "
                f"dimensionality of the existing probe drive, {self.dimensionality}."
            )
            self.add_ex_btn.setEnabled(False)
            self.remove_ex_btn.setEnabled(False)
            self.edit_ex_btn.setEnabled(False)

            exclusions = self.mb.exclusions.copy()
            for ex in exclusions:
                self.mb.remove_exclusion(ex.name)

        elif ex_types - _available:
            exclusions = self.mb.exclusions.copy()
            for ex in exclusions:
                if ex.exclusion_type in _available:
                    ex_names.append(
                        self._generate_list_name(ex.name, ex.exclusion_type)
                    )
                    continue

                self.mb.remove_exclusion(ex.name)

        self.exclusion_list_box.addItems(ex_names)

    def _initialize_layer_list_box(self):
        ly_types = set(ly.layer_type for ly in self.mb.layers)

        _available = self.layer_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        ly_names = []
        if not _available:
            self.logger.warning(
                "There are no coded point layers that work with the "
                f"dimensionality of the existing probe drive, {self.dimensionality}."
            )
            self.add_ly_btn.setEnabled(False)
            self.remove_ly_btn.setEnabled(False)
            self.edit_ly_btn.setEnabled(False)

            layers = self.mb.layers.copy()
            for ly in layers:
                self.mb.remove_layer(ly.name)

        elif ly_types - _available:
            layers = self.mb.layers.copy()
            for ly in layers:
                if ly.layer_type in _available:
                    ly_names.append(
                        self._generate_list_name(ly.name, ly.layer_type)
                    )
                    continue

                self.mb.remove_layer(ly.name)

        self.layer_list_box.addItems(ly_names)

    # -- WIDGET INTERACTION FUNCTIONALITY --

    @Slot()
    def _config_changed_handler(self):
        # Note: none of the methods executed here should cause a
        #       configChanged event
        self._validate_mb()

        # now update displays
        self.update_exclusion_list_box()
        self.update_layer_list_box()
        self.update_layer_ml_combine_toggle()
        self.update_canvas()

    @Slot()
    def _animate_motion_list(self):
        _btn_text = self.animate_ml_btn.text().replace("\n", "")
        if _btn_text == "PAUSE":
            self.mpl_canvas.animate_motion_list_pause()
        else:
            self.mpl_canvas.animate_motion_list()

    @Slot()
    def _animate_motion_list_btn_txt_to_animate(self):
        self.animate_ml_btn.setText("\n".join(list("ANIMATE")))

    @Slot()
    def _animate_motion_list_btn_txt_to_pause(self):
        self.animate_ml_btn.setText("\n".join(list("PAUSE")))

    @Slot()
    def _animate_motion_list_finished(self):
        self.animate_ml_btn.setText("\n".join(list("ANIMATE")))

    @Slot()
    def _exclusion_configure_new(self):
        if not self._params_widget.isHidden():
            self._hide_and_clear_params_widget()

        self.params_label.setText("New Exclusion")

        _available = self.exclusion_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        _icons = [None] * len(_available)
        _exclude_governors = (
            bool(self.mb.exclusions)
            and isinstance(self.mb.exclusions[0], GovernExclusion)
        )
        _govern_icon = qta.icon("mdi.crown")
        for ii, name in enumerate(tuple(_available)):
            ex = self.exclusion_registry.get_exclusion(name)
            if _exclude_governors and issubclass(ex, GovernExclusion):
                _available.remove(name)
                _icons = None
                continue

            if issubclass(ex, GovernExclusion):
                _icons[ii] = _govern_icon

        self._refresh_params_combo_box(_available, icons=_icons, _type="exclusion")
        self.params_combo_box.setObjectName("exclusion")

        self._refresh_params_widget()
        self._show_params_widget()

    @Slot()
    def _exclusion_modify_existing(self):
        item = self.exclusion_list_box.currentItem()
        name = self._get_layer_name_from_list_name(item.text())
        if name is None:
            return

        current_ex = None
        for _ex in self.mb.exclusions:
            if _ex.name == name:
                current_ex = _ex
                break
        if current_ex is None:
            return

        if not self._params_widget.isHidden():
            self._hide_and_clear_params_widget()

        self.params_label.setText(current_ex.name)
        _available = self.exclusion_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        _icons = [None] * len(_available)
        _exclude_governors = (
            bool(self.mb.exclusions)
            and isinstance(self.mb.exclusions[0], GovernExclusion)
            and not isinstance(current_ex, GovernExclusion)
        )
        _govern_icon = qta.icon("mdi.crown")
        for ii, name in enumerate(tuple(_available)):
            ex = self.exclusion_registry.get_exclusion(name)
            if _exclude_governors and issubclass(ex, GovernExclusion):
                _available.remove(name)
                _icons = None
                continue

            if issubclass(ex, GovernExclusion):
                _icons[ii] = _govern_icon

        self._refresh_params_combo_box(
            _available,
            icons=_icons,
            current=current_ex.exclusion_type,
            _type="exclusion",
        )
        self.params_combo_box.setObjectName("exclusion")

        self._param_inputs = current_ex.config.copy()
        self._param_inputs.pop("type")

        self._refresh_params_widget()
        self._show_params_widget()

    @Slot()
    def _exclusion_remove_from_mb(self):
        ex_row = self.exclusion_list_box.currentRow()
        ex = self.exclusion_list_box.takeItem(ex_row)

        name = self._get_layer_name_from_list_name(ex.text())
        if name is None:
            return

        self.mb.remove_exclusion(name)
        # ex.deleteLater()

        # TODO: remove params_widget if the removed exclusion is currently
        #       populating the params_widget

        self._mpl_canvas_full_draw = True
        self.configChanged.emit()

    @Slot()
    def _hide_and_clear_params_widget(self):
        self._params_field_widget.setEnabled(False)
        self._params_widget.hide()
        self._param_inputs = {}

    @Slot()
    def _layer_configure_new(self):
        if not self._params_widget.isHidden():
            self._hide_and_clear_params_widget()

        self.params_label.setText("New Layer")

        _available = self.layer_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        self._refresh_params_combo_box(_available)
        self.params_combo_box.setObjectName("layer")

        self._refresh_params_widget()
        self._show_params_widget()

    @Slot()
    def _layer_list_item_move_up(self):
        item = self.layer_list_box.currentItem()
        if item is None:
            # no item is selected
            return

        item_name = item.text()
        layer_name = self._get_layer_name_from_list_name(item_name)
        move_to_index = None
        for ii, layer in enumerate(self.mb.layers):
            if layer_name == layer.name:
                current_index = ii
                move_to_index = current_index - 1
                break

        if move_to_index is None:
            # item was not found, do nothing
            return
        elif move_to_index == -1:
            # item is already at the top of the list
            return

        layer = self.mb.layers.pop(current_index)  # noqa
        self.mb.layers.insert(move_to_index, layer)
        self.mb.generate()
        self._mpl_canvas_full_draw = False
        self.configChanged.emit()
        self.layer_list_box.setCurrentRow(move_to_index)

    @Slot()
    def _layer_list_item_move_down(self):
        item = self.layer_list_box.currentItem()
        if item is None:
            # no item is selected
            return

        item_name = item.text()
        layer_name = self._get_layer_name_from_list_name(item_name)
        move_to_index = None
        for ii, layer in enumerate(self.mb.layers):
            if layer_name == layer.name:
                current_index = ii
                move_to_index = current_index + 1
                break

        if move_to_index is None:
            # item was not found, do nothing
            return
        elif move_to_index == len(self.mb.layers):
            # item is already at the end of the list
            return

        layer = self.mb.layers.pop(current_index)  # noqa
        self.mb.layers.insert(move_to_index, layer)
        self.mb.generate()
        self._mpl_canvas_full_draw = False
        self.configChanged.emit()
        self.layer_list_box.setCurrentRow(move_to_index)

    @Slot()
    def _layer_modify_existing(self):
        item = self.layer_list_box.currentItem()
        name = self._get_layer_name_from_list_name(item.text())
        if name is None:
            return

        ly = None
        for _ly in self.mb.layers:
            if _ly.name == name:
                ly = _ly
                break
        if ly is None:
            return

        if not self._params_widget.isHidden():
            self._hide_and_clear_params_widget()

        self.params_label.setText(ly.name)
        _available = self.layer_registry.get_names_by_dimensionality(
            self.dimensionality
        )
        self._refresh_params_combo_box(_available, current=ly.layer_type)
        self.params_combo_box.setObjectName("layer")

        self._param_inputs = ly.config.copy()
        self._param_inputs.pop("type")

        self._refresh_params_widget()
        self._show_params_widget()

    @Slot()
    def _layer_remove_from_mb(self):
        ly_row = self.layer_list_box.currentRow()
        item = self.layer_list_box.takeItem(ly_row)

        name = self._get_layer_name_from_list_name(item.text())
        if name is None:
            return

        self.logger.info(f"Removing layer {name}.")
        self.mb.remove_layer(name)
        # ex.deleteLater()

        # TODO: remove params_widget if the removed exclusion is currently
        #       populating the params_widget

        self._mpl_canvas_full_draw = False
        self.configChanged.emit()

    def _refresh_params_combo_box(
        self,
        items,
        icons=None,
        current: Optional[str] = None,
        _type: Optional[str] = None,
    ):
        # disable combo box signals during depopulation
        self.params_combo_box.blockSignals(True)

        # update items
        self.params_combo_box.setObjectName("")
        self.params_combo_box.clear()
        self.params_combo_box.addItems(items)
        if current is None:
            self.params_combo_box.setCurrentIndex(0)
        else:
            self.params_combo_box.setCurrentText(current)

        # add item icons
        if icons is None:
            icons = []
        for ii, icon in enumerate(icons):
            if icon is None or icon == "":
                continue

            self.params_combo_box.setItemIcon(ii, icon)

        # set combo box tool tip
        if _type == "exclusion":
            self.params_combo_box.setToolTip(
                "Items with a crown are Govern exclusions.  You can only "
                "select one Govern exclusion."
            )
            self.params_combo_box.setToolTipDuration(30000)
        else:
            self.params_combo_box.setToolTip("")
            self.params_combo_box.setToolTipDuration(0)        # set combo box tool tip
        if _type == "exclusion":
            self.params_combo_box.setToolTip(
                "Items with a crown are Govern exclusions.  You can only "
                "select one Govern exclusion."
            )
            self.params_combo_box.setToolTipDuration(30000)
        else:
            self.params_combo_box.setToolTip("")
            self.params_combo_box.setToolTipDuration(0)

        # re-enable signals
        self.params_combo_box.blockSignals(False)

    def _refresh_params_widget(self):
        self.params_add_btn.setEnabled(False)

        _type = self.params_combo_box.currentText()
        ex_or_ly = self.params_combo_box.objectName()

        _widget = self._define_params_field_widget(ex_or_ly, _type)

        old_widget = self._params_field_widget
        self._params_widget.layout().replaceWidget(old_widget, _widget)
        self._params_field_widget = _widget

        old_widget.close()
        old_widget.deleteLater()

        self._validate_inputs()

    @Slot()
    def _refresh_params_widget_from_combo_box_change(self):
        self._param_inputs = {}
        self._refresh_params_widget()

    def _show_params_widget(self):
        self._params_field_widget.setEnabled(True)
        self._params_widget.show()

    @Slot()
    def _toggle_layer_to_motionlist_scheme(self):
        if not isinstance(self.mb, MotionBuilder):
            return

        _scheme = "merge" if self.layer_ml_combine_toggle.isChecked() else "sequential"
        self.logger.info(f"Toggling motion list scheme to {_scheme}.")
        self.mb.layer_to_motionlist_scheme = _scheme
        self._mpl_canvas_full_draw = False
        self.configChanged.emit()

    @Slot(object)
    def _update_param_inputs(self, input_widget: "QLineEditSpecialized"):
        param = input_widget.objectName()
        _input_string = input_widget.text()

        _type = self._param_inputs["_type"]
        _registry = self._param_inputs["_registry"]

        # Handle strings representing np.inf and np.nan
        for np_repr in ("inf", "nan"):
            single_quote_string = f"'{np_repr}'"
            double_quote_string = f'"{np_repr}"'
            if (
                np_repr in _input_string
                and not (
                    single_quote_string in _input_string
                    or double_quote_string in _input_string
                )
            ):
                _input_string = _input_string.replace(np_repr, single_quote_string)
                input_widget.setText(_input_string)

        try:
            _input = ast.literal_eval(_input_string)
        except (ValueError, SyntaxError) as err:
            params = _registry.get_input_parameters(_type)
            anno = params[param]["param"].annotation

            if inspect.isclass(anno) and issubclass(anno, str):
                _input = _input_string
            elif (
                typing.get_origin(anno) is Union
                and str in typing.get_args(anno)
            ):
                _input = _input_string
            elif _input_string == "":
                _input = None
            else:
                self.logger.exception(
                    f"Input '{input_widget.text()}' is not a valid type for '{param}'.",
                    exc_info=err,
                )
                _input = None
                input_widget.setText("")

        self._param_inputs[param] = _input

        self.logger.info(
            f"Updating input parameter {param} to {_input} for layer/exclusion "
            f"type {_type}."
        )

        self._validate_inputs()

    @Slot(object)
    def _validate_space_inputs(self, input_widget: QLineEditSpecialized):
        self.logger.info("Validating space inputs")
        w_name = input_widget.objectName()
        match = re.compile(r"(?P<label>.+)_(?P<what>(min|max|delta))").fullmatch(w_name)
        if match is None:
            # input_widget does not have a name corresponding to the space inputs
            return

        axis_index = None
        axis_config = None
        axis_label = match.group("label")
        axis_input_type = match.group("what")

        space_config = self.mb.config["space"].copy()
        for key, value in space_config.items():
            if value["label"] == axis_label:
                axis_index = key
                axis_config = value
                break

        if axis_config is None:
            # This should never happen
            return None

        if axis_input_type == "delta":
            old_val = (
                    (axis_config["range"][1] - axis_config["range"][0])
                    / axis_config["num"]
            )
        else:
            old_val = (
                axis_config["range"][0]
                if axis_input_type == "min"
                else axis_config["range"][0]
            )

        try:
            new_val = float(input_widget.text())
            new_val_good = True
        except ValueError:
            new_val = None
            new_val_good = False

        range_window = axis_config["range"][1] - axis_config["range"][0]
        old_delta = range_window / axis_config["num"]

        if not new_val_good:
            pass
        elif axis_input_type == "min" and new_val >= axis_config["range"][1]:
            new_val_good = False
        elif axis_input_type == "min" and (
                old_delta / (axis_config["range"][1] - new_val) >= 0.1
        ):
            new_val_good = False
        elif axis_input_type == "min":
            axis_config["range"][0] = new_val
            axis_config["num"] = int(
                np.ceil(
                    (axis_config["range"][1] - new_val) / old_delta
                )
            )
        elif axis_input_type == "max" and new_val <= axis_config["range"][0]:
            new_val_good = False
        elif axis_input_type == "max" and (
                old_delta / (new_val - axis_config["range"][0]) >= 0.1
        ):
            new_val_good = False
        elif axis_input_type == "max":
            axis_config["range"][1] = new_val
            axis_config["num"] = int(
                np.ceil(
                    (new_val - axis_config["range"][0]) / old_delta
                )
            )
        elif axis_input_type == "delta" and (
                new_val / (axis_config["range"][1] - axis_config["range"][0]) >= 0.1
        ):
            new_val_good = False
        elif axis_input_type == "delta":
            num = int(
                np.ceil(
                    (axis_config["range"][1] - axis_config["range"][0]) / new_val
                )
            )
            axis_config["num"] = num

        if not new_val_good:
            input_widget.setText(f"{old_val:.3f}")
            return

        space_config[axis_index] = axis_config
        config = {**self.mb.config, "space": space_config}
        self._spawn_motion_builder(config)

    def _validate_inputs(self):
        self.logger.info("Validating motion layer parameter inputs")
        _inputs = self._param_inputs.copy()
        _type = _inputs.pop("_type")
        _registry = _inputs.pop("_registry")
        _hints = _inputs.pop("_hints")
        params = _registry.get_input_parameters(_type)

        for key, val in _inputs.items():
            annotation = params[key]["param"]

            if val is not None:
                continue
            elif (
                annotation is None
                or (
                    hasattr(annotation, "__args__")
                    and type(None) in annotation.__args__
                )
            ):
                # val is None and is allowed to be None
                continue
            else:
                # not all inputs have been defined yet
                self.change_validation_state(False)
                return

        try:
            # let's spawn with a lower res space to reduce validation
            # time
            size = 11
            new_coords = {}
            for coord in self.mb.mask.coords.values():
                new_coords[coord.name] = np.linspace(
                    np.min(coord), np.max(coord), num=size
                )
            _ds = xr.Dataset(
                {
                    "mask": (
                        tuple(new_coords.keys()),
                        np.ones([size] * self.mb.mask.ndim, dtype=bool),
                    )
                },
                coords=new_coords,
            )

            _layer = _registry.factory(
                _ds,
                _type=_type,
                skip_ds_add=True,
                **_inputs,
            )
            self.change_validation_state(True)
        except (ValueError, TypeError) as err:
            self.logger.exception(
                "Supplied input arguments are not valid.",
                exc_info=err,
            )
            self.change_validation_state(False)

    def change_validation_state(self, valid: bool = False):
        self.params_add_btn.setEnabled(valid)

    @Slot()
    def exclusion_list_box_set_btn_enable(self, enable=True):
        self.edit_ex_btn.setEnabled(enable)
        self.remove_ex_btn.setEnabled(enable)

    @Slot()
    def layer_list_box_set_btn_enable(self, enable=True):
        self.edit_ly_btn.setEnabled(enable)
        self.remove_ly_btn.setEnabled(enable)

    def update_canvas(self):
        if self._mpl_canvas_full_draw:
            self.mpl_canvas.update_canvas()
        else:
            self.mpl_canvas.update_motion_list()

        self._mpl_canvas_full_draw = False

    def update_exclusion_list_box(self):
        self.logger.info("Updating Exclusion List Box")
        self.remove_ex_btn.setEnabled(False)
        self.edit_ex_btn.setEnabled(False)

        ex_names = (
            self._generate_list_name(ii, ex.name, ex.exclusion_type)
            for ii, ex in enumerate(self.mb.exclusions)
        )
        self.exclusion_list_box.clear()

        if not ex_names:
            return

        self.exclusion_list_box.addItems(ex_names)

    def update_layer_list_box(self):
        self.logger.info("Updating Layer List Box")
        self.remove_ly_btn.setEnabled(False)
        self.edit_ly_btn.setEnabled(False)

        ly_names = (
            self._generate_list_name(ii, ly.name, ly.layer_type)
            for ii, ly in enumerate(self.mb.layers)
        )

        self.layer_list_box.clear()

        if not ly_names:
            return

        self.layer_list_box.addItems(ly_names)

    def update_layer_ml_combine_toggle(self):
        _scheme = self.mb.layer_to_motionlist_scheme
        self.logger.info(f"Updating Layer ML Combine Toggle - {_scheme}")
        _check_state = False if _scheme == "sequential" else True
        self.layer_ml_combine_toggle.setChecked(_check_state)

    # -- NORMAL METHODS --

    @Slot()
    def _add_to_mb(self):
        _inputs = self._param_inputs.copy()
        _type = _inputs.pop("_type")
        _registry = _inputs.pop("_registry")
        _hints = _inputs.pop("_hints")
        _name = self.params_label.text()

        if _registry is self.exclusion_registry and _name == "New Exclusion":
            self.mb.add_exclusion(_type, **_inputs)
            self._mpl_canvas_full_draw = True
        elif _registry is self.exclusion_registry:
            # modifying existing exclusion
            self.mb.remove_exclusion(_name)
            self.mb.add_exclusion(_type, **_inputs)
            self._mpl_canvas_full_draw = True
        elif _name == "New Layer":
            self.mb.add_layer(_type, **_inputs)
            self._mpl_canvas_full_draw = False
        else:
            self.mb.remove_layer(_name)
            self.mb.add_layer(_type, **_inputs)
            self._mpl_canvas_full_draw = False

        self._hide_and_clear_params_widget()
        self.configChanged.emit()

    def _generate_btn_widget(self, txt: str):
        btn = StyleButton(txt, parent=self)
        btn.setFixedHeight(32)
        font = btn.font()
        font.setPointSize(16)
        btn.setFont(font)
        btn.setEnabled(True)

        return btn

    @staticmethod
    def _generate_list_name(_index, name, _type):
        return f"[{_index:02d}]  {name:<17} <type = {_type}>"

    @staticmethod
    def _get_layer_name_from_list_name(list_name):
        match = re.compile(
            r"(\[)(?P<index>\d+)(])\s+(?P<name>\S+)\s+(<type = )(?P<type>\S+)(>)"
        ).fullmatch(list_name)
        return None if match is None else match.group("name")

    def _initialize_motion_builder(self):
        if (
            not isinstance(self.mg, MotionGroup)
            or not isinstance(self.mb, MotionBuilder)
            or not isinstance(self.mg.mb, MotionBuilder)
        ):
            pass
        elif self.mb is self.mg.mb:
            config = _deepcopy_dict(self.mb.config)
            self._spawn_motion_builder(config)
            return

        config = {"space": {}}
        for ii, aname in enumerate(self.axis_names):
            axis = self.mg.drive.axes[ii]

            if axis.units.physical_type == u.get_physical_type("length"):
                _range = [-55.0, 55.0]
                num = int(np.ceil((_range[1] - _range[0]) / .25))

                _convert = (1 * u.cm).to(axis.units)  # type: u.Quantity
                _convert = _convert.value
                _range = [float(r * _convert) for r in _range]
            elif axis.units.physical_type == u.get_physical_type("angle"):
                _x = 3 * 360.0
                delta = 5.0
                if axis.units == u.rad:
                    _x = _x * (2.0 * np.pi / 360.0)
                    delta = delta * (np.pi / 180.0)

                _range = [float(-_x), float(_x)]
                num = int(np.ceil(2.0 * _x / delta))
            else:  # this should not happen
                _range = [-1.0, 1.0]
                num = 11

            config["space"][ii] = {
                "label": aname,
                "range": _range,
                "num": num,
            }

        self._spawn_motion_builder(config)

    def _spawn_motion_builder(self, config):
        self.logger.info("Rebuilding motion builder...")
        mb_config = _deepcopy_dict(config)
        mb_config["space"] = list(config["space"].values())

        exclusions = mb_config.pop("exclusion", None)
        if exclusions is not None:
            mb_config["exclusions"] = list(exclusions.values())

        layers = mb_config.pop("layer", None)
        if layers is not None:
            mb_config["layers"] = list(layers.values())

        self.logger.info(f"space looks like : {mb_config.get('space', None)}")
        self.logger.info(f"exclusion look like : {mb_config.get('exclusions', None)}")
        self.logger.info(f"layer looks like : {mb_config.get('layers', None)}")

        self._mb = MotionBuilder(**mb_config)
        self.mpl_canvas.link_motion_builder(self._mb)
        self._mpl_canvas_full_draw = True
        self.configChanged.emit()
        return self._mb

    def _validate_mb(self):
        if not isinstance(self.mb, MotionBuilder):
            self.done_btn.setEnabled(False)
            return
        elif len(self.mb.layers) == 0:
            self.done_btn.setEnabled(False)
            return

        self.done_btn.setEnabled(True)

    def return_and_close(self):
        config = self.mb.config

        self.logger.info(
            f"New MotionBuilder configuration is being returned, {config}."
        )
        self.returnConfig.emit(config)
        self.close()
