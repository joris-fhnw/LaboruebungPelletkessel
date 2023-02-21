import numpy as np
from datetime import datetime
from functions_and_datacontainer.main_variables import *


def lambda_O2_approx(o2_tr):
    lam_o2 = 0.21


def velocity_to_mass_flow(velocity, temperature, radius):
    area = radius ** 2 * np.pi
    volume_flow = area * velocity
    density_air = .985e5 / (R / M_air * temperature)
    mass_flow = density_air * volume_flow
    return mass_flow


def density_air(temperature, pressure):
    return pressure / (temperature * R / M_air) * 1e-3  # [kg/m3]


def var_exists(var):
    try:
        var
    except NameError:
        var_exists = False
    else:
        var_exists = True
    return var_exists


def change_dataframe_names(file):
    file["T_Abgas"] = file.T_Ab  # damit direkt mit T_Abgas gearbeitet werden kann
    file["P_Kessel"] = file.P_Kessel_Silana
    file["CO"] = file.CO_VP
    file["O2"] = file.O2_VP
    file["CO2"] = file.CO2_VP
    file["NO"] = file.NO_VP
    file["CH4"] = file.CH4_VP

    return file


def calc_cp_exhaust(lam, Temp):
    """
    Berechnet die Wärmekapazität des Abgases nach einer Fit Formel:

April 2006 Methodology for identifying parameters for the TRNSYS model Type 210 -wood pellet
stoves and boilers, Tomas Persson, Frank Fiedler and Svante Nordlander
    :param lam: [-] Lambda
    :param Temp: [K]
    :return: [J/(kg*K)]
    """
    cp = (0.01382 * Temp + 3.188) * (np.log(lam)) ** 2 - (0.07622 * Temp + 17.693) * np.log(
        lam) + 0.0002785 * Temp ** 2 + 0.008727 * Temp + 1043.1

    return cp
