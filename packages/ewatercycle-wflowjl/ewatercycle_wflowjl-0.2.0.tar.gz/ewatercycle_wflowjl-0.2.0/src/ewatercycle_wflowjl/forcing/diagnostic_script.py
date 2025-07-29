"""wflow diagnostic."""

import logging
from pathlib import Path

import iris
import numpy as np
import xarray as xr
from esmvalcore.preprocessor import regrid
from esmvaltool.diag_scripts.hydrology.derive_evspsblpot import debruin_pet
from esmvaltool.diag_scripts.shared import ProvenanceLogger
from esmvaltool.diag_scripts.shared import get_diagnostic_filename
from esmvaltool.diag_scripts.shared import group_metadata
from esmvaltool.diag_scripts.shared import run_diagnostic

from ewatercycle_wflowjl.forcing import makkink


logger = logging.getLogger(Path(__file__).name)


def create_provenance_record():
    """Create a provenance record."""
    record = {
        "caption": "Forcings for the Wflow.jl hydrological model.",
        "domains": ["global"],
        "authors": [
            "kalverla_peter",
            "camphuijsen_jaro",
            "alidoost_sarah",
            "aerts_jerom",
            "andela_bouwe",
        ],
        "projects": [
            "ewatercycle",
        ],
        "references": [
            "acknow_project",
        ],
        "ancestors": [],
    }
    return record


def get_input_cubes(metadata):
    """Create a dict with all (preprocessed) input files."""
    provenance = create_provenance_record()
    all_vars = {}
    for attributes in metadata:
        short_name = attributes["short_name"]
        if short_name in all_vars:
            raise ValueError(f"Multiple input files found for variable '{short_name}'.")
        filename = attributes["filename"]
        logger.info("Loading variable %s", short_name)
        cube = iris.load_cube(filename)
        # Make prime meridian contiguous:
        cube.coord("longitude").bounds = None
        cube = cube.intersection(longitude=(-180.0, 180.0))
        cube.coord("longitude").guess_bounds()
        cube.attributes.clear()

        all_vars[short_name] = cube
        provenance["ancestors"].append(filename)

    return all_vars, provenance


def save(cubes, dataset, provenance, cfg):
    """Save cubes to file.

    Output format: "wflow_local_forcing_ERA5_Meuse_1990_2018.nc"
    """
    time_coord = cubes[0].coord("time")
    start_year = time_coord.cell(0).point.year
    end_year = time_coord.cell(-1).point.year
    basename = "_".join(
        [
            "wflow",
            dataset,
            cfg["basin"],
            str(start_year),
            str(end_year),
        ]
    )
    output_file = get_diagnostic_filename(basename, cfg)
    logger.info("Saving cubes to file %s", output_file)
    iris.save(cubes, output_file, fill_value=1.0e20, zlib=True)

    # Store provenance
    with ProvenanceLogger(cfg) as provenance_logger:
        provenance_logger.log(output_file, provenance)


def lapse_rate_correction(height):
    """Temperature correction over a given height interval."""
    gamma = iris.coords.AuxCoord(
        np.float32(0.0065), long_name="Environmental lapse rate", units="K m-1"
    )
    return height * gamma


def regrid_temperature(src_temp, src_height, target_height, scheme):
    """Convert temperature to target grid with lapse rate correction."""
    # Convert 2m temperature to sea-level temperature (slt)
    src_dtemp = lapse_rate_correction(src_height)
    src_slt = src_temp.copy(data=src_temp.core_data() + src_dtemp.core_data())

    # Interpolate sea-level temperature to target grid
    target_slt = regrid(src_slt, target_height, scheme)

    # Convert sea-level temperature to new target elevation
    target_dtemp = lapse_rate_correction(target_height)
    target_temp = target_slt
    target_temp.data = target_slt.core_data() - target_dtemp.core_data()

    return target_temp


def load_dem(filename: str):
    """Load DEM into iris cube."""
    logger.info("Reading digital elevation model from %s", filename)
    da = xr.open_dataset(filename)["wflow_dem"]
    if "lon" in da.dims:  # Deltares is not consistent in the dim naming...
        da = da.rename({"lon": "x", "lat": "y"})
    da["x"].attrs["standard_name"] = "longitude"
    da["y"].attrs["standard_name"] = "latitude"
    da["x"].attrs["axis"] = "X"
    da["y"].attrs["axis"] = "Y"
    da["x"].attrs["units"] = "degrees_east"
    da["y"].attrs["units"] = "degrees_north"
    da = da.drop("spatial_ref")

    cube = da.to_iris()
    for coord in "longitude", "latitude":
        if not cube.coord(coord).has_bounds():
            logger.warning("Guessing DEM %s bounds", coord)
            cube.coord(coord).guess_bounds()

    return cube


def check_dem(dem, cube):
    """Check that the DEM and extract_region parameters match."""
    for coord in ("longitude", "latitude"):
        start_dem_coord = dem.coord(coord).cell(0).point
        end_dem_coord = dem.coord(coord).cell(-1).point
        start_cube_coord = cube.coord(coord).cell(0).point
        end_cube_coord = cube.coord(coord).cell(-1).point
        if start_dem_coord < start_cube_coord:
            logger.warning(
                "Insufficient data available, input data starts at %s "
                "degrees %s, but should be at least one grid "
                "cell larger than the DEM start at %s degrees %s.",
                start_cube_coord,
                coord,
                start_dem_coord,
                coord,
            )
        if end_dem_coord > end_cube_coord:
            logger.warning(
                "Insufficient data available, input data ends at %s "
                "degrees %s, but should be at least one grid "
                "cell larger than the DEM end at %s degrees %s.",
                end_cube_coord,
                coord,
                end_dem_coord,
                coord,
            )


def shift_era5_time_coordinate(cube, shift=30):
    """Shift instantaneous variables (default = 30 minutes forward in time).

    After this shift, as an example:
    time format [1990, 1, 1, 11, 30, 0] will be [1990, 1, 1, 12, 0, 0].
    For aggregated variables, already time format is [1990, 1, 1, 12, 0, 0].
    """
    time = cube.coord(axis="T")
    time.points = time.points + shift / (24 * 60)
    time.bounds = None
    time.guess_bounds()
    return cube


def main(cfg):
    """Process data for use as input to the wflow hydrological model."""
    input_metadata = cfg["input_data"].values()

    for dataset, metadata in group_metadata(input_metadata, "dataset").items():
        all_vars, provenance = get_input_cubes(metadata)

        if dataset == "ERA5":
            for var in ["tas", "psl"]:
                all_vars[var] = shift_era5_time_coordinate(all_vars[var])

        # Interpolating variables onto the dem grid
        # Read the target cube, which contains target grid and target elevation
        dem_path = Path(cfg["auxiliary_data_dir"]) / cfg["dem_file"]
        dem = load_dem(dem_path)

        check_dem(dem, all_vars["pr"])

        logger.info("Processing variable precipitation_flux")
        scheme = cfg["regrid"]
        pr_dem = regrid(all_vars["pr"], dem, scheme)

        logger.info("Processing variable temperature")

        tas_dem = regrid_temperature(
            all_vars["tas"],
            all_vars["orog"],
            dem,
            scheme,
        )

        logger.info("Processing variable potential evapotranspiration")
        if dataset == "ERA5":
            logger.info(
                "Potential evapotransporation not available, "
                "deriving with de Bruin equation."
            )
            psl_dem = regrid(all_vars["psl"], dem, scheme)
            rsds_dem = regrid(all_vars["rsds"], dem, scheme)
            rsdt_dem = regrid(all_vars["rsdt"], dem, scheme)
            pet_dem = debruin_pet(
                tas=tas_dem,
                psl=psl_dem,
                rsds=rsds_dem,
                rsdt=rsdt_dem,
            )
        else:
            logger.info(
                "Potential evapotransporation not available, "
                "deriving with Makkink equation."
            )
            rsds_dem = regrid(all_vars["rsds"], dem, scheme)
            pet_dem = makkink.calculate_makkink(
                tas=tas_dem,
                rsd=rsds_dem,
            )

        pet_dem.var_name = "pet"

        logger.info("Converting units")
        pet_dem.units = pet_dem.units / "kg m-3"
        pet_dem.data = pet_dem.core_data() / 1000.0
        pet_dem.convert_units("mm day-1")

        pr_dem.units = pr_dem.units / "kg m-3"
        pr_dem.data = pr_dem.core_data() / 1000.0
        pr_dem.convert_units("mm day-1")

        tas_dem.convert_units("degC")

        pr_dem.var_name = "precip"
        tas_dem.var_name = "temp"
        pet_dem.var_name = "pet"
        cubes = iris.cube.CubeList([pr_dem, tas_dem, pet_dem])
        save(cubes, dataset, provenance, cfg)


if __name__ == "__main__":
    with run_diagnostic() as config:
        main(config)
