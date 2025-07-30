"""Module that defines the LaPD related transform classes."""
__all__ = ["LaPDXYTransform", "LaPD6KTransform"]
__transformer__ = ["LaPDXYTransform", "LaPD6KTransform"]

import numpy as np

from typing import Any, Dict, Tuple, Union
from warnings import warn

from bapsf_motion.transform import base
from bapsf_motion.transform.helpers import register_transform
from bapsf_motion.transform.lapd_droop import LaPDXYDroopCorrect, DroopCorrectABC


@register_transform
class LaPDXYTransform(base.BaseTransform):
    """
    Class that defines a coordinate transform for a :term:`LaPD` XY
    :term:`probe drive`.

    **transform type:** ``'lapd_xy'``

    Parameters
    ----------
    drive: |Drive|
        The instance of |Drive| the coordinate transformer will be
        working with.

    pivot_to_center: `float`
        Distance from the center of the :term:`LaPD` to the center
        "pivot" point of the ball valve.  A positive value indicates
        the probe drive is set up on the East side of the LaPD and a
        negative value indicates the West side.

    pivot_to_drive: `float`
        Distance from the center line of the :term:`probe drive`
        vertical axis to the center "pivot" point of the ball valve.

    pivot_to_feedthru: `float`
        Distance from the center "pivot" point of the ball valve to the
        nearest face of the probe drive feed-through.

    probe_axis_offset: `float`
        Perpendicular distance from the center line of the probe shaft
        to the :term:`probe drive` pivot point on the vertical axis.

    drive_polarity: 2D tuple, optional
        A two element tuple of +/- 1 values indicating the polarity of
        the probe drive motion to how the math was done for the
        underlying matrix transformations.  For example, a value
        of ``(1, 1)`` would indicate that positive movement (in
        probe drive coordinates) of the drive would be inwards and
        downwards.  However, this is inconsistent if the vertical axis
        has the motor mounted to the bottom of the axis.  In this case
        the ``drive_polarity`` would be ``(1, -1)``.
        (DEFAULT: ``(1, 1)``)

    mspace_polarity: 2D tuple, optional
        A two element tuple of +/- 1 values indicating the polarity of
        the motion space motion to how the math was done for the
        underlying matrix transformations.  For example, a value
        of ``(-1, 1)`` for a probe mounted on an East port would
        indicate that inward probe drive movement would correspond to
        a LaPD -X movement and downward probe drive movement
        would correspond to LaPD +Y.  If the probe was mounted on a
        West port then the polarity would need to be ``(1, 1)`` since
        inward probe drive movement corresponds to +X LaPD coordinate
        movement.  (DEFAULT: ``(-1, 1)``)

    droop_correct : bool
        Set `True` for the coordinate transform to correct for the
        droop of a probe shaft.  This will use
        `~bapsf_motion.transform.lapd_droop.LaPDXYDroopCorrect` to
        correct for the droop of a stainless steel 304 probe shaft of
        size .375" OD x 0.035" wall.  Set `False` for no droop
        correction.  (DEFAULT: `False`)

    droop_scale : `float`
        (DEFAULT ``1.0``)  A float `>= 0.0` indicating how much to scale
        the droop calculation by.  A value of ``0`` would indicate no
        droop.  A value between ``0`` and ``1`` indicates a droop less
        than the default model.  A value of ``1`` indicates the default
        model droop. A value ``> 1`` indicates more droop.

    Examples
    --------

    Let's set up a :term:`transformer` for a probe drive mounted on
    an east port.  In this case the vertical axis motor is mounted
    at the top of the vertical axis.  (Values are NOT accurate to
    actual LaPD values.)

    .. tabs::
       .. code-tab:: py Class Instantiation

          tr = LaPDXYTransform(
              drive,
              pivot_to_center = 62.94,
              pivot_to_drive = 133.51,
              pivot_to_feedthru = 21.6,
              probe_axis_offset = 20.16,
              drive_polarity = (1, 1),
              mspace_polarity = (-1, 1),
          )

       .. code-tab:: py Factory Function

          tr = transform_factory(
              drive,
              tr_type = "lapd_xy",
              **{
                  "pivot_to_center": 62.94,
                  "pivot_to_drive": 133.51,
                  "pivot_to_feedthru": 21.6,
                  "probe_axis_offset": 20.16,
                  "drive_polarity": (1, 1),
                  "mspace_polarity": (-1, 1),
              },
          )

       .. code-tab:: toml TOML

          [...transform]
          type = "lapd_xy"
          pivot_to_center = 62.94
          pivot_to_drive = 133.51
          pivot_to_feedthru = 21.6
          probe_axis_offset = 20.16
          drive_polarity = [1, 1]
          mspace_polarity = [-1, 1]

       .. code-tab:: py Dict Entry

          config["transform"] = {
              "type": "lapd_xy",
              "pivot_to_center": 62.94,
              "pivot_to_drive": 133.51,
              "pivot_to_feedthru": 21.6,
              "probe_axis_offset": 20.16,
              "drive_polarity": (1, 1),
              "mspace_polarity": (-1, 1),
          }

    Now, let's do the same thing for a probe drive mounted on a West
    port and has the vertical axis motor mounted at the base.

    .. tabs::
       .. code-tab:: py Class Instantiation

          tr = LaPDXYTransform(
              drive,
              pivot_to_center = -62.94,
              pivot_to_drive = 133.51,
              pivot_to_feedthru = 21.6,
              probe_axis_offset = 20.16,
              drive_polarity = (1, -1),
              mspace_polarity = (1, 1),
          )

       .. code-tab:: py Factory Function

          tr = transform_factory(
              drive,
              tr_type = "lapd_xy",
              **{
                  "pivot_to_center": -62.94,
                  "pivot_to_drive": 133.51,
                  "pivot_to_feedthru": 21.6,
                  "probe_axis_offset": 20.16,
                  "drive_polarity": (1, -1),
                  "mspace_polarity": (1, 1),
              },
          )

       .. code-tab:: toml TOML

          [...transform]
          type = "lapd_xy"
          pivot_to_center = -62.94
          pivot_to_drive = 133.51
          pivot_to_feedthru = 21.6
          probe_axis_offset = 20.16
          drive_polarity = [1, -1]
          mspace_polarity = [1, 1]

       .. code-tab:: py Dict Entry

          config["transform"] = {
              "type": "lapd_xy",
              "pivot_to_center": -62.94,
              "pivot_to_drive": 133.51,
              "pivot_to_feedthru": 21.6,
              "probe_axis_offset": 20.16,
              "drive_polarity": (1, -1),
              "mspace_polarity": (1, 1),
          }
    """
    # TODO: confirm polarity descriptions once issue #38 is resolved
    # TODO: review that default polarities are correct
    # TODO: write a full primer on how the coordinate transform was
    #       calculated
    _transform_type = "lapd_xy"
    _dimensionality = 2

    def __init__(
        self,
        drive,
        *,
        pivot_to_center: float,
        pivot_to_drive: float,
        pivot_to_feedthru: float,
        probe_axis_offset: float,
        drive_polarity: Tuple[int, int] = (1, 1),
        mspace_polarity: Tuple[int, int] = (-1, 1),
        droop_correct: bool = False,
        droop_scale: Union[int, float] = 1.0,
    ):
        self._droop_correct_callable = None
        self._deployed_side = None
        super().__init__(
            drive,
            pivot_to_center=pivot_to_center,
            pivot_to_drive=pivot_to_drive,
            pivot_to_feedthru=pivot_to_feedthru,
            probe_axis_offset=probe_axis_offset,
            drive_polarity=drive_polarity,
            mspace_polarity=mspace_polarity,
            droop_correct=droop_correct,
            droop_scale=droop_scale,
        )

    def __call__(self, points, to_coords="drive") -> np.ndarray:
        if self.droop_correct is None:
            return super().__call__(points=points, to_coords=to_coords)

        if to_coords == "drive":
            _sign = 1 if self.deployed_side == "East" else -1
            pivot_to_center = np.abs(self.pivot_to_center)

            # - points is in LaPD motion space coordinates
            # - need to convert motion space coordinates to non-droop
            #   scenario before doing matrix multiplication
            points = self._condition_points(points)

            # 1. convert to ball valve coords
            points[..., 0] = np.absolute(_sign * pivot_to_center - points[..., 0])

            # 2. droop correct to non-droop coords
            points = self.droop_correct(points, to_points="non-droop")

            # 3. back to LaPD coords
            points[..., 0] = _sign * (pivot_to_center - points[..., 0])

        tr_points = super().__call__(points=points, to_coords=to_coords)
            
        if to_coords != "drive":  # to motion space
            _sign = 1 if self.deployed_side == "East" else -1
            pivot_to_center = np.abs(self.pivot_to_center)

            # - tr_points is in LaPD motion space coordinates
            # - need to convert motion space coordinates to droop scenario
            # 1. convert to ball valve coords
            tr_points[..., 0] = np.absolute(
                _sign * pivot_to_center - tr_points[..., 0]
            )

            # 2. droop correct to droop coords
            tr_points = self.droop_correct(tr_points, to_points="droop")

            # 3. back to LaPD coords
            tr_points[..., 0] = _sign * (pivot_to_center - tr_points[..., 0])

        return tr_points

    def _validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:

        for key in {
            "pivot_to_center",
            "pivot_to_drive",
            "pivot_to_feedthru",
            "probe_axis_offset",
            "droop_scale",
        }:
            val = inputs[key]
            if not isinstance(val, (float, np.floating, int, np.integer)):
                raise TypeError(
                    f"Keyword '{key}' expected type float or int, "
                    f"got type {type(val)}."
                )
            elif key == "pivot_to_center":
                self._deployed_side = "East" if val >= 0.0 else "West"
                # do not take the absolute value here, so the config
                # dict properly maintains the negative value
                # val = np.abs(val)
            elif val < 0.0:
                # TODO: HOW (AND SHOULD WE) ALLOW A NEGATIVE OFFSET FOR
                #       "probe_axis_offset"
                val = np.abs(val)
                warn(
                    f"Keyword '{val}' is NOT supposed to be negative, "
                    f"assuming the absolute value {val}."
                )
            inputs[key] = val

        for key in ("drive_polarity", "mspace_polarity"):
            polarity = inputs[key]
            if not isinstance(polarity, np.ndarray):
                polarity = np.array(polarity)

            if polarity.shape != (2,):
                raise ValueError(
                    f"Keyword '{key}' is supposed to be a 2-element "
                    "array specifying the polarity of the axes, got "
                    f"an array of shape {polarity.shape}."
                )
            elif not np.all(np.abs(polarity) == 1):
                raise ValueError(
                    f"Keyword '{key}' is supposed to be a 2-element "
                    "array of 1 or -1 specifying the polarity of the "
                    "axes, array has values not equal to 1 or -1."
                )
            inputs[key] = polarity

        if not isinstance(inputs["droop_correct"], bool):
            raise TypeError(
                f"Keyword 'droop_correct' expected type bool, "
                f"got type {type(inputs['droop_correct'])}."
            )
        elif inputs["droop_correct"]:
            _drive = self._drive if self._drive is not None else self.axes
            self._droop_correct_callable = LaPDXYDroopCorrect(
                drive=_drive,
                pivot_to_feedthru=inputs["pivot_to_feedthru"],
                droop_scale=inputs["droop_scale"]
            )

        return inputs

    def _matrix_to_drive(self, points):
        # given points are in motion space "LaPD" (x, y) coordinates

        # polarity needs to be adjusted first, since the parameters for
        # the following transformation matrices depend on the adjusted
        # coordinate space
        points = self.mspace_polarity * points  # type: np.ndarray
        npoints = points.shape[0]

        pivot_to_center = np.abs(self.pivot_to_center)

        tan_theta = points[..., 1] / (points[..., 0] + pivot_to_center)
        theta = -np.arctan(tan_theta)

        T0 = np.zeros((npoints, 3, 3)).squeeze()
        T0[..., 0, 2] = np.sqrt(
            points[..., 1]**2 + (pivot_to_center + points[..., 0])**2
        ) - pivot_to_center
        T0[..., 1, 2] = (
            self.pivot_to_drive * np.tan(theta)
            + self.probe_axis_offset * (1 - (1 / np.cos(theta)))
        )
        T0[..., 2, 2] = 1.0

        T_dpolarity = np.diag(self.drive_polarity.tolist() + [1.0])
        T_mpolarity = np.diag(self.mspace_polarity.tolist() + [1.0])

        return np.matmul(
            T_dpolarity,
            np.matmul(T0, T_mpolarity),
        )

    def _matrix_to_motion_space(self, points: np.ndarray):
        # given points are in drive (e0, e1) coordinates

        # polarity needs to be adjusted first, since the parameters for
        # the following transformation matrices depend on the adjusted
        # coordinate space
        points = self.drive_polarity * points  # type: np.ndarray
        npoints = points.shape[0]

        pivot_to_center = np.abs(self.pivot_to_center)

        # Angle Defs:
        # - theta = angle between the horizontal and the probe shaft
        # - beta = angle between the horizontal and the probe drive pivot
        #          point on e1 (the vertical axis)
        # - alpha = beta - theta

        sine_alpha = self.probe_axis_offset / np.sqrt(
            self.pivot_to_drive**2
            + (-self.probe_axis_offset + points[..., 1])**2
        )

        tan_beta = (-self.probe_axis_offset + points[..., 1]) / -self.pivot_to_drive

        # alpha = arcsine( sine_alpha )
        # beta = pi + arctan( tan_beta )
        # theta = beta - alpha
        # theta2 = theta - pi

        theta = np.arctan(tan_beta) - np.arcsin(sine_alpha)

        T0 = np.zeros((npoints, 3, 3)).squeeze()
        T0[..., 0, 0] = np.cos(theta)
        T0[..., 0, 2] = -pivot_to_center * (1 - np.cos(theta))
        T0[..., 1, 0] = np.sin(theta)
        T0[..., 1, 2] = pivot_to_center * np.sin(theta)
        T0[..., 2, 2] = 1.0

        T_dpolarity = np.diag(self.drive_polarity.tolist() + [1.0])
        T_mpolarity = np.diag(self.mspace_polarity.tolist() + [1.0])

        return np.matmul(
            T_mpolarity,
            np.matmul(T0, T_dpolarity),
        )

    @property
    def pivot_to_center(self) -> float:
        """
        Distance from the center of the :term:`LaPD` to the center
        "pivot" point of the ball valve.
        """
        return self.inputs["pivot_to_center"]

    @property
    def pivot_to_drive(self) -> float:
        """
        Distance from the center line of the :term:`probe drive`
        vertical axis to the center "pivot" point of the ball valve.
        """
        return self.inputs["pivot_to_drive"]

    @property
    def pivot_to_feedthru(self) -> float:
        return self.inputs["pivot_to_feedthru"]

    @property
    def probe_axis_offset(self) -> float:
        """
        Perpendicular distance from the center line of the probe shaft
        to the :term:`probe drive` pivot point on the vertical axis.
        """
        return self.inputs["probe_axis_offset"]

    @property
    def drive_polarity(self) -> np.ndarray:
        """
        A two element array of +/- 1 values indicating the polarity of
        the probe drive motion to how the math was done for the
        underlying matrix transformations.

        For example, a value of ``[1, 1]`` would indicate that positive
        movement (in probe drive coordinates) of the drive would be
        inwards and downwards.  However, this is inconsistent if the
        vertical axis has the motor mounted to the bottom of the axis.
        In this case the ``drive_polarity`` would be ``(1, -1)``.
        """
        return self.inputs["drive_polarity"]

    @property
    def mspace_polarity(self) -> np.ndarray:
        """
        A two element array of +/- 1 values indicating the polarity of
        the motion space motion to how the math was done for the
        underlying matrix transformations.

        For example, a value of ``(-1, 1)`` for a probe mounted on an
        East port would indicate that inward probe drive movement would
        correspond to a LaPD -X movement and downward probe drive
        movement would correspond to LaPD +Y.  If the probe was mounted
        on a West port then the polarity would need to be ``(1, 1)``
        since inward probe drive movement corresponds to +X LaPD
        coordinate movement.
        """
        return self.inputs["mspace_polarity"]

    @property
    def droop_correct(self) -> Union[DroopCorrectABC, None]:
        return self._droop_correct_callable

    @property
    def droop_scale(self) -> float:
        """
        Scale value for how much to adjust the droop from the default
        model.
        """
        return self.inputs["droop_scale"]

    @property
    def deployed_side(self):
        return self._deployed_side


@register_transform
class LaPD6KTransform(LaPDXYTransform):
    """
    Class that defines a coordinate transform for a :term:`LaPD`
    "6K Compumotor" :term:`probe drive`.

    **transform type:** ``'lapd_6k'``

    Parameters
    ----------
    drive: |Drive|
        The instance of |Drive| the coordinate transformer will be
        working with.

    pivot_to_center: `float`
        Distance from the center of the :term:`LaPD` to the center
        "pivot" point of the ball valve.  A positive value indicates
        the probe drive is set up on the East side of the LaPD and a
        negative value indicates the West side. (DEFAULT: ``58.771`` cm)

    pivot_to_drive: `float`
        Distance from the center line of the :term:`probe drive`
        vertical axis to the center "pivot" point of the ball valve.
        (DEFAULT: ``116.84`` cm)

    pivot_to_feedthru: `float`
        Distance from the center "pivot" point of the ball valve to the
        nearest face of the probe drive feed-through.
        (DEFAULT: ``53.76926`` cm)

    probe_axis_offset: `float`
        Perpendicular distance from the center line of the probe shaft
        to the :term:`probe drive` pivot point on the vertical axis.
        (DEFAULT: ``9.36752`` cm)

    drive_polarity: 2D tuple, optional
        A two element tuple of +/- 1 values indicating the polarity of
        the probe drive motion to how the math was done for the
        underlying matrix transformations.  For example, a value
        of ``(1, 1)`` would indicate that positive movement (in
        probe drive coordinates) of the drive would be inwards and
        downwards.  However, this is inconsistent if the vertical axis
        has the motor mounted to the bottom of the axis.  In this case
        the ``drive_polarity`` would be ``(1, -1)``.
        (DEFAULT: ``(1, -1)``)

    mspace_polarity: 2D tuple, optional
        A two element tuple of +/- 1 values indicating the polarity of
        the motion space motion to how the math was done for the
        underlying matrix transformations.  For example, a value
        of ``(-1, 1)`` for a probe mounted on an East port would
        indicate that inward probe drive movement would correspond to
        a LaPD -X movement and downward probe drive movement
        would correspond to LaPD +Y.  If the probe was mounted on a
        West port then the polarity would need to be ``(1, 1)`` since
        inward probe drive movement corresponds to +X LaPD coordinate
        movement.  (DEFAULT: ``(-1, 1)``)

    six_k_arm_length : `float`
        Length of the vertical pivoting arm of the 6K Compumotor probe
        drive. (DEFAULT: ``93.345`` cm)

    droop_correct : bool
        Set `True` for the coordinate transform to correct for the
        droop of a probe shaft.  This will use
        `~bapsf_motion.transform.lapd_droop.LaPDXYDroopCorrect` to
        correct for the droop of a stainless steel 304 probe shaft of
        size .375" OD x 0.035" wall.  Set `False` for no droop
        correction.  (DEFAULT: `False`)

    droop_scale : `float`
        (DEFAULT ``1.0``)  A float `>= 0.0` indicating how much to scale
        the droop calculation by.  A value of ``0`` would indicate no
        droop.  A value between ``0`` and ``1`` indicates a droop less
        than the default model.  A value of ``1`` indicates the default
        model droop. A value ``> 1`` indicates more droop.

    Examples
    --------

    Let's set up a :term:`transformer` for a probe drive mounted on
    an east port.  In this case the motor for the vertical axis is
    mounted at the base of the probe drive vertical axis.  (Values are
    NOT accurate to actual LaPD values.)

    .. tabs::
       .. code-tab:: py Class Instantiation

          tr = LaPD6KTransform(
              drive,
              pivot_to_center = 58.771,
              pivot_to_drive = 133.51,
              pivot_to_feedthru = 53.22,
              probe_axis_offset = 9.37,
              six_k_arm_length = 93.345,
          )

       .. code-tab:: py Factory Function

          tr = transform_factory(
              drive,
              tr_type = "lapd_6k",
              **{
                  "pivot_to_center": 58.771,
                  "pivot_to_drive": 133.51,
                  "pivot_to_feedthru": 53.22,
                  "probe_axis_offset": 9.37,
                  "six_k_arm_length": 93.345,
              },
          )

       .. code-tab:: toml TOML

          [...transform]
          type = "lapd_6k"
          pivot_to_center = 58.771
          pivot_to_drive = 133.51
          pivot_to_feedthru = 53.22
          probe_axis_offset = 9.37
          six_k_arm_length = 93.345

       .. code-tab:: py Dict Entry

          config["transform"] = {
              "type": "lapd_6k",
              "pivot_to_center": 58.771,
              "pivot_to_drive": 133.51,
              "pivot_to_feedthru": 53.22,
              "probe_axis_offset": 9.37,
              "six_k_arm_length": 93.345,
          }

    Now, let's do the same thing for a probe drive mounted on a West
    port and has the vertical axis motor mounted at the base.

    .. tabs::
       .. code-tab:: py Class Instantiation

          tr = LaPD6KTransform(
              drive,
              pivot_to_center = -62.94,
              pivot_to_drive = 133.51,
              pivot_to_feedthru = 21.6,
              probe_axis_offset = 20.16,
              six_k_arm_length = 93.345,
              mspace_polarity = (1, 1),
          )

       .. code-tab:: py Factory Function

          tr = transform_factory(
              drive,
              tr_type = "lapd_6k",
              **{
                  "pivot_to_center": -62.94,
                  "pivot_to_drive": 133.51,
                  "pivot_to_feedthru": 21.6,
                  "probe_axis_offset": 20.16,
                  "six_k_arm_length": 93.345,
                  "mspace_polarity": (1, 1),
              },
          )

       .. code-tab:: toml TOML

          [...transform]
          type = "lapd_6k"
          pivot_to_center = -62.94
          pivot_to_drive = 133.51
          pivot_to_feedthru = 21.6
          probe_axis_offset = 20.16
          six_k_arm_length = 93.345
          mspace_polarity = [1, 1]

       .. code-tab:: py Dict Entry

          config["transform"] = {
              "type": "lapd_6k",
              "pivot_to_center": -62.94,
              "pivot_to_drive": 133.51,
              "pivot_to_feedthru": 21.6,
              "probe_axis_offset": 20.16,
              "six_k_arm_length": 93.345,
              "mspace_polarity": (1, 1),
          }

    .. note::
        For further details reference the jupyter notebook for
        :ref:`LaPD6KYTransform </notebooks/transform/LaPD6KTransform.ipynb>`.

    """
    _transform_type = "lapd_6k"
    _dimensionality = 2

    def __init__(
        self,
        drive,
        *,
        pivot_to_center: float = 58.771,
        pivot_to_drive: float = 116.84,
        pivot_to_feedthru: float = 53.76926,
        probe_axis_offset: float = 9.36752,
        drive_polarity: Tuple[int, int] = (1, -1),
        mspace_polarity: Tuple[int, int] = (-1, 1),
        six_k_arm_length: float = 93.345,
        droop_correct: bool = False,
        droop_scale: Union[int, float] = 1.0,
    ):
        self._droop_correct_callable = None
        self._deployed_side = None
        self._pivot_to_drive_pinion = None
        self._beta = None
        super(LaPDXYTransform, self).__init__(
            drive,
            pivot_to_center=pivot_to_center,
            pivot_to_drive=pivot_to_drive,
            pivot_to_feedthru=pivot_to_feedthru,
            probe_axis_offset=probe_axis_offset,
            drive_polarity=drive_polarity,
            mspace_polarity=mspace_polarity,
            six_k_arm_length=six_k_arm_length,
            droop_correct=droop_correct,
            droop_scale=droop_scale,
        )

    def _validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        _inputs = super()._validate_inputs(inputs)

        # validate argument six_k_arm_length
        key = "six_k_arm_length"
        val = _inputs[key]
        if not isinstance(val, (float, np.floating, int, np.integer)):
            raise TypeError(
                f"Keyword '{key}' expected type float or int, "
                f"got type {type(val)}."
            )
        elif val < 0.0:
            val = np.abs(val)
            warn(
                f"Keyword '{val}' is NOT supposed to be negative, "
                f"assuming the absolute value {val}."
            )
        _inputs[key] = val

        # calculate distance between ball valve center (pivot) to the
        # pivot (pinion) point on the probe drive arm
        self._pivot_to_drive_pinion = np.sqrt(
            _inputs["pivot_to_drive"]**2 + _inputs["probe_axis_offset"]**2
        )

        # calculate beta - the angular drop from the probe shaft to the
        #   probe drive pinion
        #
        #           ________ pivot_to_drive ________x (ball valve pivot)
        #          |                      _________/
        #  probe_axis_offset   __________/
        #          |__________/     ^-- pivot_to_drive_pinion
        #
        self._beta = np.arctan(_inputs["probe_axis_offset"] / _inputs["pivot_to_drive"])

        return _inputs

    def _matrix_to_drive(self, points: np.ndarray) -> np.ndarray:
        # given points are in motion space "LaPD" (x, y) coordinates

        # polarity needs to be adjusted first, since the parameters for
        # the following transformation matrices depend on the adjusted
        # coordinate space
        points = self.mspace_polarity * points  # type: np.ndarray
        npoints = points.shape[0]

        pivot_to_center = np.abs(self.pivot_to_center)

        # calculate theta ... the angle made by the probe shaft on the
        #  drive side of the ball valve
        tan_theta = points[..., 1] / (points[..., 0] + pivot_to_center)
        theta = -np.arctan(tan_theta)

        # calculate phi .. the angle to the probe drive pinion
        phi = theta - self.beta

        # calculate alpha ... the angle made by the 6K arm and the vertical
        #  axis of the probe drive
        alpha = np.arcsin(
            (self.pivot_to_drive - self.pivot_to_drive_pinion * np.cos(phi))
            / self.six_k_arm_length
        )

        T0 = np.zeros((npoints, 3, 3)).squeeze()  # noqa
        T0[..., 0, 0] = 1 / np.cos(theta)
        T0[..., 0, 2] = pivot_to_center * ((1 / np.cos(theta)) - 1)
        T0[..., 1, 2] = (
            self.six_k_arm_length * (np.cos(alpha) - 1)
            + self.probe_axis_offset
            + self.pivot_to_drive_pinion * np.sin(phi)
        )
        T0[..., 2, 2] = 1.0

        T_dpolarity = np.diag(self.drive_polarity.tolist() + [1.0])  # noqa
        T_mpolarity = np.diag(self.mspace_polarity.tolist() + [1.0])  # noqa

        return np.matmul(
            T_dpolarity,
            np.matmul(T0, T_mpolarity),
        )

    def _matrix_to_motion_space(self, points: np.ndarray) -> np.ndarray:
        # given points are in drive (e0, e1) coordinates

        # polarity needs to be adjusted first, since the parameters for
        # the following transformation matrices depend on the adjusted
        # coordinate space
        points = self.drive_polarity * points  # type: np.ndarray
        npoints = points.shape[0]

        pivot_to_center = np.abs(self.pivot_to_center)

        # calculate the distance between the ball valve pivot point (pivot) to the
        # pivot point on the probe drive vertical axis (vpinion)
        pivot_to_vpinion = np.sqrt(
            self.pivot_to_drive**2
            + (self.six_k_arm_length - self.probe_axis_offset + points[..., 1])**2
        ).squeeze()

        # calculate the angle (gamma) the line intersecting the ball valve
        # pivot (pivot) and probe drive vertical pinion (vpinion) makes
        # with the horizontal plane
        gamma = np.arctan(
            (self.six_k_arm_length - self.probe_axis_offset + points[..., 1])
            / self.pivot_to_drive
        ).squeeze()

        # imagine two circles:
        #   1. circle one located at the ball valve pivot (pivot) with a
        #      radius pivot_to_drive_pinion
        #   2. circle two located at the vpinion with a readius six_k_arm_length
        #
        # The probe drive will be oriented at the lower intersection of these
        # two circles.
        #
        # If we select a coordinate system where the line intersecting
        # pivot and vpinion defines the "x-axis", then circle 1 is located
        # at the origin and circle 2 is on the "x-axis" at an offset of
        # pivot_to_vpinion.
        #
        # Let's calculate the angle (phi) these intersection points make
        # with the above mentioned "x-axis".
        #
        tan_2_phi = (
            2 * pivot_to_vpinion * self.pivot_to_drive_pinion / (
                self.six_k_arm_length**2
                - self.pivot_to_drive_pinion**2
                - pivot_to_vpinion**2
            )
        )**2 - 1
        phi = np.arctan(np.sqrt(tan_2_phi))

        # calculate theta - the angle the probe shaft makes with the
        #  true horizontal ... theta is signed s.t. negative means
        #  the back of the probe is below horizontal and positive means
        #  the back of the probe is above horizontal
        theta = gamma + self.beta - np.abs(phi)

        T0 = np.zeros((npoints, 3, 3)).squeeze()
        T0[..., 0, 0] = np.cos(theta)
        T0[..., 0, 2] = -pivot_to_center * (1 - np.cos(theta))
        T0[..., 1, 0] = np.sin(-theta)
        T0[..., 1, 2] = pivot_to_center * np.sin(-theta)
        T0[..., 2, 2] = 1.0

        T_dpolarity = np.diag(self.drive_polarity.tolist() + [1.0])
        T_mpolarity = np.diag(self.mspace_polarity.tolist() + [1.0])

        return np.matmul(
            T_mpolarity,
            np.matmul(T0, T_dpolarity),
        )

    @property
    def six_k_arm_length(self) -> float:
        return self.inputs["six_k_arm_length"]

    @property
    def pivot_to_drive_pinion(self) -> float:
        return self._pivot_to_drive_pinion

    @property
    def beta(self) -> float:
        # angle swept from the probe shaft to the probe drive pinion with
        # respect to the ball valve pivot
        return self._beta
