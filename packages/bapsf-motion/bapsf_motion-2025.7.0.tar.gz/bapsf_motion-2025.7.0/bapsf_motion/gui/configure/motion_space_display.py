"""
Module contains the `~PySide6.QtWidgets.QWidget` used for displaying /
plotting the :term:`motion space` associated with a |MotionBuilder|
instance.
"""
__all__ = ["MotionSpaceDisplay"]

import logging
import numpy as np
import warnings

from PySide6.QtCore import Signal, QTimer, Slot
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout
from typing import List, Union

from bapsf_motion.gui.configure.helpers import gui_logger
from bapsf_motion.motion_builder import MotionBuilder

# noqa
# the matplotlib backend imports must happen after import matplotlib and PySide6
import matplotlib as mpl
mpl.use("qtagg")  # matplotlib's backend for Qt bindings
from matplotlib import pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.backend_bases import Event, MouseEvent, PickEvent, DrawEvent
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # noqa
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar  # noqa


class MotionSpaceDisplay(QFrame):
    mbChanged = Signal()
    targetPositionSelected = Signal(list)
    animateMotionListStarted = Signal()
    animateMotionListFinished = Signal()
    animateMotionListPaused = Signal()
    animateMotionListCleared = Signal()

    _default_legend_names = [
        "motion_list", "probe", "position", "target", "insertion_point"
    ]

    def __init__(
        self, mb: MotionBuilder = None, parent=None
    ):
        super().__init__(parent=parent)

        self._logger = logging.getLogger(f"{gui_logger.name}.MSD")

        self._mb = None
        self.link_motion_builder(mb)
        self._display_position = True
        self._display_target_position = True
        self._display_probe = True
        self._animate_payload = None

        self._motionlist_plot_names = None  # type: Union[None, List[str]]

        self._motionlist_plot_names = None  # type: Union[None, List[str]]

        self.setStyleSheet(
            """
            MotionSpaceDisplay {
                border: 2px solid rgb(125, 125, 125);
                border-radius: 5px; 
                padding: 0px;
                margin: 0px;
            }
            """
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.mpl_canvas = FigureCanvas()
        self.mpl_canvas.setParent(self)

        self.mpl_toolbar = NavigationToolbar(self.mpl_canvas, parent=self)

        self.setLayout(self._define_layout())

        self._cid_on_draw = None
        self._draw_all = True

        self._mpl_pick_callback_id = None
        self._connect_signals()

    def _connect_signals(self):
        self.mbChanged.connect(self.update_canvas)
        self.targetPositionSelected.connect(self.update_target_position_plot)
        self.animateMotionListFinished.connect(self.animate_motion_list_pause)

        # matplotlib events
        self._mpl_pick_callback_id = self.mpl_canvas.mpl_connect(
            "pick_event", self.on_pick  # noqa
        )
        self._cid_on_draw = self.mpl_canvas.mpl_connect("draw_event", self.on_draw)  # noqa

    def _define_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.mpl_canvas)

        return layout

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def mb(self) -> Union[MotionBuilder, None]:
        return self._mb

    @property
    def display_position(self) -> bool:
        return self._display_position

    @display_position.setter
    def display_position(self, value: bool):
        if not isinstance(value, bool):
            return

        self._display_position = value
        if not value:
            self._display_probe = value

    @property
    def display_target_position(self) -> bool:
        return self._display_target_position

    @display_target_position.setter
    def display_target_position(self, value: bool):
        if not isinstance(value, bool):
            return

        self._display_target_position = value

    @property
    def display_probe(self) -> bool:
        return self._display_probe

    @display_probe.setter
    def display_probe(self, value: bool):
        if not isinstance(value, bool):
            return

        self._display_probe = value
        if value:
            self._display_position = value

    @property
    def is_animating_motion_list(self):
        if self._animate_payload is None:
            return False

        if self._animate_payload["finished"]:
            return False

        _timer = self._animate_payload["timer"]  # type: QTimer
        return _timer.isActive()

    def _get_plot_axis_by_name(self, name: str):
        fig_axes = self.mpl_canvas.figure.axes
        for ax in fig_axes:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                legend_handles, legend_labels = ax.get_legend_handles_labels()

            if name not in legend_labels:
                continue

            index = legend_labels.index(name)
            handler = legend_handles[index]

            return ax, handler

        return None

    def animate_motion_list(self):
        if self._animate_payload is not None and not self._animate_payload["finished"]:
            self._animate_payload["timer"].start()
            self.animateMotionListStarted.emit()
            return
        elif self._animate_payload is not None:
            self.animate_motion_list_clear()
            self._animate_payload = None
        elif self.mb.motion_list is None:
            self.animate_motion_list_clear()
            return

        self._animate_motion_list_init_payload()
        self._animate_payload["timer"].start()  # noqa

        self.animateMotionListStarted.emit()

    def _animate_motion_list_init_payload(self):
        delay = 200  # msec
        _timer = QTimer(parent=self)
        _timer.setInterval(delay)
        _timer.timeout.connect(self._update_motion_list_trace)

        motionlist_size = self.mb.motion_list.shape[0]
        index_step = np.floor(motionlist_size / (60000 / _timer.interval())).astype(int)
        index_step = 1 if index_step == 0 else index_step

        self._animate_payload = {
            "index": 0,  # type: int
            "index_step": index_step,  # type: int
            "delay": delay,  # type: int
            "timer": _timer,  # type: QTimer
            "finished": False,
        }

    @Slot()
    def animate_motion_list_pause(self):
        if self._animate_payload is None:
            return

        self._animate_payload["timer"].stop()

        if not self._animate_payload["finished"]:
            self.animateMotionListPaused.emit()

    @Slot()
    def animate_motion_list_clear(self):
        if self._animate_payload is None:
            return

        self._animate_payload["timer"].stop()
        self._animate_payload["timer"].deleteLater()
        self._animate_payload = None

        _animate_ml_labels = ["motionlist_start", "motionlist_stop", "motionlist_trace"]
        for _label in _animate_ml_labels:
            stuff = self._get_plot_axis_by_name(_label)
            if stuff is None:
                continue

            ax, handler = stuff
            handler.remove()

        self.mpl_canvas.draw()

        self.animateMotionListCleared.emit()

    @Slot()
    def _update_motion_list_trace(self, *, to_index: int = None):
        if to_index is None and self._animate_payload is None:
            return
        elif to_index is None:
            to_index = self._animate_payload["index"]
        elif self._animate_payload is None:
            return
        elif self._animate_payload["finished"]:
            return

        # update plot
        _animate_ml_labels = ["motionlist_start", "motionlist_stop", "motionlist_trace"]
        for _label in _animate_ml_labels:

            stuff = self._get_plot_axis_by_name(_label)

            if stuff is not None and _label in ("motionlist_start", "motionlist_stop"):
                ax, handler = stuff  # type: plt.Axes, PathCollection

                index = 0 if _label == "motionlist_start" else to_index
                point = self.mb.motion_list[index, ...].squeeze()

                handler.set_offsets(point)
            elif stuff is not None:
                # this is the trace
                ax, handler = stuff  # type: plt.Axes, plt.Line2D

                xdata = self.mb.motion_list[0:to_index + 1, 0]
                ydata = self.mb.motion_list[0:to_index + 1, 1]

                handler.set_xdata(xdata)
                handler.set_ydata(ydata)
            elif _label == "motionlist_trace":
                # trace has not been made yet
                ax = self.mpl_canvas.figure.gca()

                xdata = self.mb.motion_list[0:to_index + 1, 0]
                ydata = self.mb.motion_list[0:to_index + 1, 1]

                ax.plot(
                    xdata,
                    ydata,
                    color="black",
                    linewidth=1,
                    label=_label,
                    animated=True,
                )
            else:
                # this is the start and end points
                ax = self.mpl_canvas.figure.gca()

                points = self.mb.motion_list[0:to_index + 1, ...]

                ax.scatter(
                    x=points[..., 0],
                    y=points[..., 1],
                    s=6 ** 2,
                    linewidth=1,
                    facecolors="none",
                    edgecolors="black",
                    label=_label,
                    animated=True,
                )

        self.mpl_canvas.draw()
        if to_index == self.mb.motion_list.shape[0]-1:
            self._animate_payload["finished"] = True
            self.animateMotionListFinished.emit()
            return

        to_index += self._animate_payload["index_step"]
        if to_index >= self.mb.motion_list.shape[0]:
            to_index = self.mb.motion_list.shape[0] - 1

        self._animate_payload["index"] = to_index

    def on_draw(self, event: DrawEvent):
        if self._draw_all:
            self.mpl_canvas.mpl_disconnect(self._cid_on_draw)
            self.mpl_canvas.draw()
            self._cid_on_draw = self.mpl_canvas.mpl_connect("draw_event", self.on_draw)
            self._draw_all = False
        else:
            fig = self.mpl_canvas.figure
            fig_axes = fig.axes  # type: List[plt.Axes]
            for ax in fig_axes:
                artists = ax.get_children()
                for artist in artists:
                    if not artist.get_animated():
                        continue

                    fig.draw_artist(artist)

            self.mpl_canvas.blit(fig.bbox)

    def on_pick(self, event: PickEvent):
        if not self.display_target_position:
            return

        gui_event = event.guiEvent  # type: QMouseEvent

        artist = event.artist  # noqa
        if not isinstance(artist, PathCollection):
            self.logger.warning(
                f"Currently only know how to retrieve data from a "
                f"PathCollection artist (i.e. an artist created with "
                f"pyplot.scatter()), received artist type {type(artist)}."
            )
            return

        # A PickEvent associated with a PathCollection artist will have
        # the attribute ind.  ind is a list of ints corresponding to the
        # indices of the data used to create the scatter plot
        if len(event.ind) != 1:
            self.logger.info(
                f"Could not select data point, too many point close to "
                f"the mouse click."
            )
            return
        index = event.ind[0]  # noqa

        # get the date from the artist
        data = artist.get_offsets()
        target_position = data[index, :]

        self.logger.info(f"target position = {target_position}")
        self.targetPositionSelected.emit(target_position)

    def link_motion_builder(self, mb: Union[MotionBuilder, None]):
        self.logger.info(f"Linking Motion Builder {mb}")

        self.blockSignals(True)
        self.unlink_motion_builder()
        self.blockSignals(False)

        if not isinstance(mb, MotionBuilder):
            self.mbChanged.emit()
            return

        self._mb = mb
        self.setHidden(False)
        self.mbChanged.emit()

    def unlink_motion_builder(self):
        self._mb = None
        self.setHidden(True)
        self.mbChanged.emit()

    @Slot()
    def update_canvas(self):
        if not isinstance(self.mb, MotionBuilder):
            self.setHidden(True)
            return

        if self.isHidden():
            self.setHidden(False)

        self.logger.info("Redrawing Motion Space Display...")

        # stop motion list animation while re-plotting
        is_animating = self.is_animating_motion_list
        self.blockSignals(True)
        self.animate_motion_list_clear()
        self.blockSignals(False)

        # retrieve last position
        stuff = self._get_plot_axis_by_name("position")
        if stuff is not None:
            ax, handler = stuff  # type: plt.Axes, PathCollection
            position = handler.get_offsets()
        else:
            position = None

        # retrieve last target position
        stuff = self._get_plot_axis_by_name("target")
        if stuff is not None:
            ax, handler = stuff  # type: plt.Axes, PathCollection
            target_position = handler.get_offsets()
        else:
            target_position = None

        self._draw_all = True
        fig = self.mpl_canvas.figure
        fig.clear()
        ax = fig.gca()

        xdim, ydim = self.mb.mspace_dims
        self.mb.mask.plot(x=xdim, y=ydim, ax=ax, add_colorbar=False, label="mask")

        fig.tight_layout()

        # Draw motion list
        self.update_motion_list()

        # Draw insertion point
        insertion_point = self.mb.get_insertion_point()
        if insertion_point is not None:
            ax.scatter(
                x=insertion_point[0],
                y=insertion_point[1],
                s=3 ** 2,
                linewidth=2,
                facecolors="none",
                edgecolors="red",
                label="insertion_point",
            )

            # reset x range of plot
            xlim = ax.get_xlim()
            if insertion_point[0] > xlim[1]:
                xlim = [xlim[0], 1.05 * insertion_point[0]]
            elif insertion_point[0] < xlim[0]:
                xlim = [1.05 * insertion_point[0], xlim[1]]
            ax.set_xlim(xlim)

            # reset y range of plot
            ylim = ax.get_ylim()
            if insertion_point[1] > ylim[1]:
                ylim = [ylim[0], 1.05 * insertion_point[1]]
            elif insertion_point[1] < ylim[0]:
                ylim = [1.05 * insertion_point[1], ylim[1]]
            ax.set_ylim(ylim)

        # Draw target position
        if self.display_target_position:
            self.update_target_position_plot(position=target_position)

        # Draw current position
        if self.display_position:
            self.update_position_plot(position=position)

        # Draw legend
        self.update_legend()

        self.mpl_canvas.draw()

        # re-start the motion list animation
        if is_animating:
            self.blockSignals(True)
            self.animate_motion_list()
            self.blockSignals(False)

        self.logger.info("Re-draw DONE.")

    def update_legend(self):
        _plotted_layers = (
            [] if self._motionlist_plot_names is None else self._motionlist_plot_names
        )
        _names = set(self._default_legend_names + _plotted_layers)

        # gather handles for legend
        handles = []
        for name in _names:
            stuff = self._get_plot_axis_by_name(name)
            if stuff is None:
                continue

            ax, handle = stuff
            handles.append(handle)

        if len(handles) == 0:
            self.mpl_canvas.draw()
            return

        ax = self.mpl_canvas.figure.gca()
        ax.legend(handles=handles)

        self.mpl_canvas.draw()

    def update_motion_list(self):
        self.animate_motion_list_clear()

        # plot the individual point layers (if join scheme is sequential)
        _layer_names = [layer.name for layer in self.mb.layers]
        _plotted_layer_names = set(
            [] if self._motionlist_plot_names is None else self._motionlist_plot_names
        )
        _labels = _layer_names + list(_plotted_layer_names - set(_layer_names))
        _plotted_layer_names = []
        edgecolor = "none"
        facecolors = [
            "deepskyblue",
            "orangered",
            "slategrey",
            "teal",
            "darkorange",
            "darkviolet",
            "deeppink",
        ]
        color_index = 0
        for _label in _labels:
            stuff = self._get_plot_axis_by_name(_label)
            if stuff is not None:
                ax, handler = stuff  # type: plt.Axes, PathCollection

                if (
                    _label not in _layer_names
                    or self.mb.layer_to_motionlist_scheme == "merge"
                    or len(self.mb.layers) == 1
                ):
                    handler.remove()
                else:
                    data = self.mb._ds[_label].data
                    pts = self.mb.flatten_points(data)
                    mask = self.mb.generate_excluded_mask(pts)
                    pts = pts[mask, ...]

                    handler.set_offsets(pts)
                    handler.set_facecolor(facecolors[color_index])
                    handler.set_edgecolor(edgecolor)

                    color_index += 1
                    _plotted_layer_names.append(_label)
            elif (
                _label not in _layer_names
                or self.mb.layer_to_motionlist_scheme == "merge"
                or len(self.mb.layers) == 1
            ):
                pass
            else:
                ax = self.mpl_canvas.figure.gca()

                data = self.mb._ds[_label].data
                pts = self.mb.flatten_points(data)
                mask = self.mb.generate_excluded_mask(pts)
                pts = pts[mask, ...]

                ax.scatter(
                    x=pts[..., 0],
                    y=pts[..., 1],
                    s=4 ** 2,
                    facecolors=facecolors[color_index],
                    edgecolors=edgecolor,
                    label=_label,
                    animated=True,
                )

                color_index += 1
                _plotted_layer_names.append(_label)

            color_index = color_index % len(facecolors)
        self._motionlist_plot_names = _plotted_layer_names

        # add motion list "base" plot
        _label = "motion_list"
        motion_list = self.mb.motion_list
        facecolors = (
            "none" if (
                motion_list is None
                or (
                    len(self.mb.layers) > 1
                    and self.mb.layer_to_motionlist_scheme == "sequential"
                )
            ) else "deepskyblue"
        )
        stuff = self._get_plot_axis_by_name(_label)
        if stuff is not None:
            ax, handler = stuff  # type: plt.Axes, PathCollection

            if motion_list is None:
                handler.remove()
            else:
                handler.set_offsets(motion_list)
                handler.set_facecolor(facecolors)
        elif motion_list is None:
            pass
        else:
            ax = self.mpl_canvas.figure.gca()

            ax.scatter(
                x=motion_list[..., 0],
                y=motion_list[..., 1],
                s=4 ** 2,
                linewidth=1,
                facecolors=facecolors,
                edgecolors="black",
                picker=True,
                label=_label,
                animated=True,
            )

        self.update_legend()
        self.mpl_canvas.draw()

    @Slot(list)
    def update_target_position_plot(self, position):
        self.logger.info(f"Drawing target position {position}")

        if not self.display_target_position:
            position = None
        elif isinstance(position, np.ndarray):
            position = position.squeeze()
            position = position.tolist()

        if not bool(position):
            position = None

        # add target position dot
        _label = "target"
        stuff = self._get_plot_axis_by_name(_label)
        if stuff is not None:
            ax, handler = stuff  # type: plt.Axes, PathCollection

            if position is None:
                handler.remove()
            else:
                handler.set_offsets(position)
        elif position is None:
            pass
        else:
            ax = self.mpl_canvas.figure.gca()

            ax.scatter(
                x=position[0],
                y=position[1],
                s=7 ** 2,
                linewidth=2,
                facecolors="none",
                edgecolors="blue",
                label=_label,
                animated=True,
            )

        self.update_legend()
        self.mpl_canvas.draw()

    def update_position_plot(self, position):
        self.logger.info(f"Drawing position {position}")

        if not self.display_position:
            position = None
        elif isinstance(position, np.ndarray):
            position = position.squeeze()
            position = position.tolist()

        if not bool(position):
            position = None

        # add position dot
        _label = "position"
        stuff = self._get_plot_axis_by_name(_label)
        if stuff is not None:
            ax, handler = stuff  # type: plt.Axes, PathCollection

            if position is None:
                handler.remove()
            else:
                handler.set_offsets(position)
        elif position is None:
            return
        else:
            ax = self.mpl_canvas.figure.gca()

            ax.scatter(
                x=position[0],
                y=position[1],
                s=7 ** 2,
                linewidth=2,
                facecolors="none",
                edgecolors="black",
                label=_label,
                animated=True,
            )

        # add probe shaft (line from insertion to position
        _label = "probe"
        stuff = self._get_plot_axis_by_name(_label)
        insertion_point = (
            None if not isinstance(self.mb, MotionBuilder)
            else self.mb.get_insertion_point()
        )
        if (
            (insertion_point is None or position is None or not self.display_probe)
            and stuff is not None
        ):
            # not enough to update plot, so remove EXISTING plot
            ax, handler = stuff
            handler.remove()
        elif insertion_point is None or position is None or not self.display_probe:
            # nothing to plot and plot does NOT already exist
            pass
        elif stuff is not None:
            # update existing plot
            ax, handler = stuff  # type: plt.Axes, plt.Line2D

            xdata = [insertion_point[0], position[0]]
            ydata = [insertion_point[1], position[1]]

            handler.set_xdata(xdata)
            handler.set_ydata(ydata)
        else:
            # plot does NOT exist, make plot
            ax = self.mpl_canvas.figure.gca()

            xdata = [insertion_point[0], position[0]]
            ydata = [insertion_point[1], position[1]]

            ax.plot(
                xdata,
                ydata,
                color="black",
                linewidth=2,
                label=_label,
                animated=True,
            )

        self.update_legend()
        self.mpl_canvas.draw()

    def closeEvent(self, event):
        self.logger.info(f"Closing {self.__class__.__name__}")
        super().closeEvent(event)
