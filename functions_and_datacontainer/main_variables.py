"""Parameter welche in allen Datenauswertungsprogrammen für Oelbrenner Verwendet werden"""

user = "joris.strassburg"

"----------------------------------------Zeitversatz-------------------------------------------------------------------"
uhc_offset = 16  # [s]
co_offset = 40  # [s]
nox_offset = 28  # [s]
staub_offset = 114  # [s]
co2_offset = 44  # [s]
v_abgas_offset = 11  # [s]
valve_open_offset = 50  # [s]

"-------------------------------------------Umrechnen auf Normgrössen--------------------------------------------------"
# Molmassen in [kg/kmol]
M_NO2 = 46.0055  # [kg/m3]
M_CO = 28.01  # [kg/m3]
M_CH4 = 16.04  # [kg/m3]
M_air = 28.964 # trockene Luft
R = 8.31446 # [K/(mol*K)]

