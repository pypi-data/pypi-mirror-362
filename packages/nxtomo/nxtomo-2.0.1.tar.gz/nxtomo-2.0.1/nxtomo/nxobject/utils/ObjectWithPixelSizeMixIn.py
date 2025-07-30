"""
module for NXobject shared classes
"""

from __future__ import annotations

import logging

import numpy
import pint
from silx.utils.proxy import docstring

from nxtomo.nxobject.nxobject import NXobject
from nxtomo.utils import get_quantity

_logger = logging.getLogger(__name__)
_ureg = pint.get_application_registry()


class _ObjectWithPixelSizeMixIn:
    """
    Class to be shared by NXobject that can define a pixel size
    """

    def __init__(self):
        self._x_pixel_size: pint.Quantity | None = None
        # x 'sample' detector size
        self._y_pixel_size: pint.Quantity | None = None
        # y 'sample' detector size

    @property
    def x_pixel_size(self) -> pint.Quantity | None:
        """
        x pixel size as a field with a unit (get a value and a unit - default unit is SI).
        Know as 'x sample pixel size' in some application
        """
        return self._x_pixel_size

    @x_pixel_size.setter
    def x_pixel_size(self, x_pixel_size: pint.Quantity | None) -> None:
        if not isinstance(x_pixel_size, (type(None), pint.Quantity)):
            raise TypeError(
                f"x_pixel_size is expected ot be an instance of {pint.Quantity} or None. Not {type(x_pixel_size)}"
            )
        self._x_pixel_size = x_pixel_size

    @property
    def y_pixel_size(self) -> pint.Quantity | None:
        """
        y pixel size as a field with a unit (get a value and a unit - default unit is SI).
        Know as 'y sample pixel size' in some application
        """
        return self._y_pixel_size

    @y_pixel_size.setter
    def y_pixel_size(self, y_pixel_size: pint.Quantity | None) -> None:
        if not isinstance(y_pixel_size, (type(None), pint.Quantity)):
            raise TypeError(
                f"y_pixel_size is expected ot be an instance of {pint.Quantity} or None. Not {type(y_pixel_size)}"
            )
        self._y_pixel_size = y_pixel_size

    @docstring(NXobject)
    def to_nx_dict(
        self,
        x_pixel_size_path: str | None,
        y_pixel_size_path: str | None,
    ) -> dict:
        assert isinstance(self, NXobject)

        nx_dict = {}
        # x 'sample' pixel
        if x_pixel_size_path is not None and self.x_pixel_size is not None:
            path_x_pixel_size = x_pixel_size_path  # pylint: disable=E1101
            nx_dict[path_x_pixel_size] = self.x_pixel_size.magnitude
            nx_dict["@".join([path_x_pixel_size, "units"])] = (
                f"{self.x_pixel_size.units:~}"
            )
        # y 'sample' pixel
        if y_pixel_size_path is not None and self.y_pixel_size is not None:
            path_y_pixel_size = y_pixel_size_path
            nx_dict[path_y_pixel_size] = self.y_pixel_size.magnitude
            nx_dict["@".join([path_y_pixel_size, "units"])] = (
                f"{self.y_pixel_size.units:~}"
            )
        return nx_dict

    def _load(
        self,
        file_path: str,
        x_pixel_size_path: str | None,
        y_pixel_size_path: str | None,
    ) -> None:
        # nexus_paths = get_nexus_path(nexus_version)
        # nexus_detector_paths = nexus_paths.nx_detector_paths
        if x_pixel_size_path is not None:
            try:
                self.x_pixel_size = get_quantity(
                    file_path=file_path,
                    data_path=x_pixel_size_path,
                    default_unit=_ureg.meter,
                )
            except TypeError as e:
                # in case loaded pixel size doesn't fit the type (case Diamond dataset)
                _logger.warning(f"Fail to load x pixel size. Error is {e}")
        if y_pixel_size_path is not None:
            try:
                self.y_pixel_size = get_quantity(
                    file_path=file_path,
                    data_path=y_pixel_size_path,  # "/".join([data_path, nexus_detector_paths.Y_PIXEL_SIZE]),
                    default_unit=_ureg.meter,
                )
            except TypeError as e:
                # in case loaded pixel size doesn't fit the type (case Diamond dataset)
                _logger.warning(f"Fail to load y pixel size. Error is {e}")

    @staticmethod
    def concatenate(output_nx_object, nx_objects: tuple):
        """
        Update output_nx_object (expected to be the inheriting class) with the pixel size from 'nx_objects'
        """
        if not isinstance(output_nx_object, _ObjectWithPixelSizeMixIn):
            raise TypeError
        if not isinstance(nx_objects[0], _ObjectWithPixelSizeMixIn):
            raise TypeError
        output_nx_object.x_pixel_size = nx_objects[0].x_pixel_size
        output_nx_object.y_pixel_size = nx_objects[0].y_pixel_size
        for nx_obj in nx_objects[1:]:
            if output_nx_object.x_pixel_size is not None and not numpy.isclose(
                output_nx_object.x_pixel_size, nx_obj.x_pixel_size
            ):
                _logger.warning(
                    f"found different x pixel size value. ({output_nx_object.x_pixel_size} vs {nx_obj.x_pixel_size}). Pick the first one"
                )
            if output_nx_object.y_pixel_size is not None and not numpy.isclose(
                output_nx_object.y_pixel_size, nx_obj.y_pixel_size
            ):
                _logger.warning(
                    f"found different y pixel size value. ({output_nx_object.y_pixel_size} vs {nx_obj.y_pixel_size}). Pick the first one"
                )
