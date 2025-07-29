"""Wflow.jl eWaterCycle Model."""

import datetime
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import toml
import xarray as xr
from ewatercycle.base.model import ContainerizedModel
from ewatercycle.base.model import eWaterCycleModel
from ewatercycle.base.parameter_set import ParameterSet
from ewatercycle.container import ContainerImage
from ewatercycle.util import geographical_distances
from ewatercycle.util import get_time
from pydantic import PrivateAttr
from pydantic import model_validator

from ewatercycle_wflowjl.forcing.forcing import WflowJlForcing


def _iso_to_wflow(time: str):
    dt = get_time(time)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def _wflow_to_dt(time: str):
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")


def get_value_as_xarray(model: "eWaterCycleModel", name: str) -> xr.DataArray:
    """get_value method, but returns full xarray object."""
    grid = model._bmi.get_var_grid(name)
    grid_type = model._bmi.get_grid_type(grid)

    if grid_type in ["rectilinear", "uniform_rectilinear"]:
        lat, lon, shape = model.get_latlon_grid(name)
        da = xr.DataArray(
            data=np.reshape(model.get_value(name), (1, shape[0], shape[1])),
            coords={"longitude": lon, "latitude": lat},
            dims=["latitude", "longitude"],
            name=name,
        )
        da = da.where(da != -999)

    if grid_type in ["unstructured", "points"]:
        if not model._bmi.get_var_location(name) == "node":
            msg = "This method is only implemented for nodes in unstructured grids."
            raise NotImplementedError(msg)

        rank = model._bmi.get_grid_rank(grid)
        node_count = model._bmi.get_grid_node_count(grid)
        locs = [model._bmi.get_grid_x(grid, np.zeros(node_count))]
        loc_names = ["lon"]
        if rank > 1:
            locs.append(model._bmi.get_grid_y(grid, np.zeros(node_count)))
            loc_names.append("lat")
        if rank > 2:
            locs.append(model._bmi.get_grid_z(grid, np.zeros(node_count)))
            loc_names.append("z")

        da = xr.DataArray(data=model.get_value(name), dims="loc", name=name)
        da["loc"] = pd.MultiIndex.from_arrays(locs, names=loc_names)

    else:
        msg = (
            "This method is only implemented for rectilinear and unstructured grids.\n"
            f"Not grid type '{grid_type}'"
        )
        raise ValueError(msg)

    da.attrs["units"] = model._bmi.get_var_units(name)
    da = da.expand_dims(
        dim={
            "time": [model.time_as_datetime],
        }
    )
    return da


def coords_to_indices(
    model: eWaterCycleModel, name: str, lat: Iterable[float], lon: Iterable[float]
) -> np.ndarray:
    """Turn location coordinates (lat, lon) to indices."""
    locs = list(zip(lat, lon, strict=True))

    grid = model._bmi.get_var_grid(name)
    grid_type = model._bmi.get_grid_type(grid)

    if grid_type not in ["unstructured", "points"]:
        msg = (
            "This method is only implemented for unstructured grids.\n"
            f"Not grid type '{grid_type}'"
        )
        raise ValueError(msg)

    if not model._bmi.get_var_location(name) == "node":
        msg = "This method is only implemented for nodes in unstructured grids."
        raise NotImplementedError(msg)

    node_count = model._bmi.get_grid_node_count(grid)
    x_coords = model._bmi.get_grid_x(grid, np.zeros(node_count))
    y_coords = model._bmi.get_grid_y(grid, np.zeros(node_count))

    indices = np.zeros(len(locs), dtype=int)
    for index, (point_lon, point_lat) in enumerate(locs):
        distances = geographical_distances(point_lat, point_lon, x_coords, y_coords)
        indices[index] = distances.argmin()

    return indices


class WflowJlMixins(eWaterCycleModel):
    """Functionality for the Wflow.jl model."""

    forcing: WflowJlForcing | None = None
    parameter_set: ParameterSet

    _config: dict = PrivateAttr()

    @model_validator(mode="after")
    def _initialize_config(self):
        """Load config from parameter set and update with forcing info."""
        cfg = toml.load(self.parameter_set.directory / self.parameter_set.config)

        self._config = cfg

    def _make_cfg_file(self, **kwargs) -> Path:
        """Create a new wflow config file and return its path."""
        if "start_time" in kwargs:
            self._config["starttime"] = _iso_to_wflow(kwargs["start_time"])
        if "end_time" in kwargs:
            self._config["endtime"] = _iso_to_wflow(kwargs["end_time"])

        # Get time specs from forcing
        if self.forcing is not None:
            if self.forcing.directory is not None:
                forcing_path = self.forcing.directory / self.forcing.netcdfinput
            else:
                forcing_path = Path(self.forcing.netcdfinput)

            ds = xr.open_dataset(forcing_path)
            calendar_type = ds["time"].attrs.get("calendar_type")
            if calendar_type is not None:
                self._config["calendar"] = calendar_type
            self._config["timestepsecs"] = int(
                np.timedelta64(ds["time"].to_numpy()[1] - ds["time"].to_numpy()[0])
                / np.timedelta64(1, "s")
            )
            if "start_time" not in kwargs:
                self._config["starttime"] = _iso_to_wflow(self.forcing.start_time)
            if "end_time" not in kwargs:
                self._config["endtime"] = _iso_to_wflow(self.forcing.end_time)

        config_file = self._cfg_dir / "wflow_ewatercycle.toml"

        # Input paths
        self._config["state"]["path_input"] = str(
            Path(self.parameter_set.directory) / self._config["state"]["path_input"]
        )
        self._config["input"]["path_static"] = str(
            Path(self.parameter_set.directory) / self._config["input"]["path_static"]
        )
        if self.forcing is None:
            self._config["input"]["path_forcing"] = str(
                Path(self.parameter_set.directory)
                / self._config["input"]["path_forcing"]
            )
        else:
            self._config["input"]["path_forcing"] = str(forcing_path)

        # Output paths
        self._config["state"]["path_output"] = str(
            self._cfg_dir / self._config["state"]["path_output"]
        )
        self._config["output"]["path"] = str(
            self._cfg_dir / self._config["output"]["path"]
        )
        self._config["csv"]["path"] = str(self._cfg_dir / self._config["csv"]["path"])
        self._config["netcdf"]["path"] = str(
            self._cfg_dir / self._config["netcdf"]["path"]
        )

        # Enable the following variables for the BMI:
        if "API" not in self._config:
            self._config["API"] = {}
        self._config["API"]["components"] = [
            "vertical",
            "lateral.subsurface",
            "lateral.land",
            "lateral.river",
            "lateral.river.reservoir",
        ]

        with config_file.open(mode="w") as f:
            f.write(toml.dumps(self._config))

        return config_file


class WflowJl(WflowJlMixins, ContainerizedModel):
    """Wflow.jl eWaterCycle LocalModel."""

    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/ewatercycle/wflowjl-remotebmi:0.2.0"
    )
    protocol: Literal["grpc", "openapi"] = "openapi"

    def get_latlon_grid(self, name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Grid latitude, longitude and shape for variable.

        The default implementation takes Bmi's x as longitude and y as latitude.
        See bmi.readthedocs.io/en/stable/model_grids.html#structured-grids.

        Some models may deviate from this default. They can provide their own
        implementation or use a BMI wrapper as in the wflow and pcrglob examples.

        Args:
            name: Name of the variable
        """
        grid_id = self._bmi.get_var_grid(name)
        grid_type = self._bmi.get_grid_type(grid_id)

        if grid_type in ["rectilinear", "uniform_rectilinear"]:
            shape = self._bmi.get_grid_shape(grid_id)
            grid_lon = self._bmi.get_grid_x(grid_id)
            grid_lat = self._bmi.get_grid_y(grid_id)
        elif grid_type in ["unstructured", "points"]:
            node_count = self._bmi.get_grid_node_count(grid_id)
            grid_lat = self._bmi.get_grid_x(grid_id, np.zeros(node_count))
            grid_lon = self._bmi.get_grid_y(grid_id, np.zeros(node_count))
            shape = np.array([node_count])
        else:
            msg = f"Grid type '{grid_type}' is not supported by this method."
            raise ValueError(msg)

        return grid_lat, grid_lon, shape

    def get_value_as_xarray(self, name: str) -> xr.DataArray:
        """get_value method, but returns an xarray object with dims and coords."""
        return get_value_as_xarray(self, name)

    def _coords_to_indices(
        self, name: str, lat: Iterable[float], lon: Iterable[float]
    ) -> np.ndarray:
        """Turn location coordinates (lat, lon) to indices."""
        return coords_to_indices(self, name, lat, lon)

    def get_value_at_coords(
        self, name, lat: Iterable[float], lon: Iterable[float]
    ) -> np.ndarray:
        """get_value_at_indices method, but with actual coordinates instead."""
        return super().get_value_at_coords(name, lat, lon)

    @property
    def start_time_as_datetime(self) -> datetime.datetime:
        """Start time of the model as a datetime object."""
        if isinstance(self._config["starttime"], str):
            return _wflow_to_dt(self._config["starttime"])
        return self._config["starttime"]

    @property
    def end_time_as_datetime(self) -> datetime.datetime:
        """End time of the model as a datetime object'."""
        if isinstance(self._config["endtime"], str):
            return _wflow_to_dt(self._config["endtime"])
        return self._config["endtime"]

    @property
    def time_as_datetime(self) -> datetime.datetime:
        """Current time of the model as a datetime object'."""
        lookup = {"s": "seconds", "min": "minutes", "h": "hours", "d": "days"}
        td = datetime.timedelta(
            **{
                lookup[self._bmi.get_time_units()]: self._bmi.get_current_time(),
            }
        )
        return self.start_time_as_datetime + td
