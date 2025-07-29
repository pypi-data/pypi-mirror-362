"""Makkink formula for potential evaporation, implemented for Iris."""

import logging
from pathlib import Path

import iris.analysis.maths
import iris.cube
import numpy as np


logger = logging.getLogger(Path(__file__).name)


def constants():
    """Constants used for the Makkink calculation.

    See:
        Reference crop evapotranspiration determined with a modified Makkink equation,
        H. A. R. de Bruin, W. N. Lablans (1988),
        doi:10.1002/(SICI)1099-1085(19980615)12:7<1053::AID-HYP639>3.0.CO;2-E
    """
    c1 = iris.cube.Cube(
        np.float32(0.65),
        long_name="C1",
        units="",
    )
    gamma = iris.cube.Cube(
        np.float32(0.66),
        long_name="gamma",
        units="mbar degC^-1",
    )
    labda = iris.cube.Cube(
        np.float32(2.45e6),
        long_name="lambda",
        units="joule kg^-1",
    )
    return c1, gamma, labda


def vapor_pressure_slope(tas):
    """Slope of the saturation vapor pressure vs. temperature curve.

    See:
        Reference crop evapotranspiration determined with a modified Makkink equation,
        H. A. R. de Bruin, W. N. Lablans (1988),
        doi:10.1002/(SICI)1099-1085(19980615)12:7<1053::AID-HYP639>3.0.CO;2-E
    """
    a = 6.1078
    b = 17.294
    c = 237.73

    tas.convert_units("degC")

    logger.info(str(tas))

    s = (a * b * c) / (c + tas) ** 2 * iris.analysis.maths.exp((b * tas) / (c + tas))
    s.units = "mbar degC^-1"

    logger.info(str(s))

    return s


def calculate_makkink(tas, rsd):
    """Makkink equation for reference crop evapotranspiration.

    For reference see:
        Reference crop evapotranspiration determined with a modified Makkink equation,
        H. A. R. de Bruin, W. N. Lablans (1988),
        doi:10.1002/(SICI)1099-1085(19980615)12:7<1053::AID-HYP639>3.0.CO;2-E
    """
    tas.convert_units("degC")
    rsd.convert_units("Watt m^-2")

    c1, gamma, labda = constants()
    s = vapor_pressure_slope(tas)

    pet = (c1 * s / (s + gamma) * rsd) / labda
    print("PET units:", pet.units)
    pet.units = "kg m^-2 s^-1"

    pet.var_name = "evspsblpot"
    pet.standard_name = "water_potential_evaporation_flux"
    pet.long_name = "Potential Evapotranspiration"

    return pet
