import pandas as pd
import matplotlib.dates as mdates
# from Prüfstelle.Datenanalyse_oop import data_analyse as da
import P6_Grütter.edit_data_frame as ed
from matplotlib import pyplot as plt
import P6_Grütter.wood_combustion as wc
import datetime
from datetime import datetime, date, time
import numpy as np
from tabulate import tabulate
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')#plot in eigenem Fenster und nicht inline

# txt = pd.read_csv("Aufz_Rohdaten_Gruetter_220624093958.txt",header=1)

"import data"
excel_name = "Aufz_Rohdaten_TEST_Bafu_OEL_220808105805.xlsx"
file = pd.read_excel(excel_name,header=1)
file = ed.edit_silana_excel(file)
file["T_Abgas"] = file.TIR_401 # damit direkt mit T_Abgas gearbeitet werden kann
o2_norm = 13
x_norm = ed.norm_values([file.CO_low_Emi1,file.NOx_Emi1],[12+16,14+16],file.O2_Emi1,o2_norm)
time_abs = ed.time_abs_fun(file.Uhrzeit) # erstelle absolut Zeit
"---------------------Berechnungen---------------------------------------------------"
def wet_species(pellet,lam):
    """Funktion nicht nötig, selbes kann mit pellet.O2_tr(lambda) und pellet.O2(lambda) berechnet werden"""
    sum_wet = pellet.b + pellet.c + pellet.d + pellet.a*(lam-1) + (pellet.e*lam+pellet.f)
    sum_dry = pellet.b+pellet.d+pellet.a*(lam-1)+(pellet.e*lam+pellet.f)
    co2_wet = pellet.b/sum_wet
    co2_dry = pellet.b/sum_dry
    o2_wet = (lam-1)*pellet.a/sum_wet
    o2_dry = (lam-1)*pellet.a/sum_dry
    return {"co2_wet":co2_wet,"co2_dry":co2_dry,"o2_wet":o2_wet,"o2_dry":o2_dry}


def n_direkt_fun(Q_nutz,mdot_bf,H_uf):
    n = Q_nutz/(mdot_bf*H_uf)
    return n
# def n_indirekt(T_Abgas,H_uf,lmin,lam,u):
#     T_um = 21 # umgebungstemperatur [°C]
#     cp_water = 4.195 # Wärmekapazität von Wasser bei 85 °C [kJ/(kg K)]
#     cp_air = 1.0057 # Wärmekapazität von Luft bei 80 °C [kJ/(kg K)]
#     cp_stoech = 1.07
#     # Abgasverluste
#     mu_stoch = 1 + lmin
#     exhaust_losses = mu_stoch * cp_stoech*(T_Abgas-T_um) + u * cp_water * (T_Abgas-T_um) + \
#                      (lam-1)*lmin*cp_air*(T_Abgas-T_um)
#     # burning_gases_losses = #q_co + q_ogc
#     return exhaust_losses
# Input
yc,yh,yo,yn,ys = 0.51, 0.06,0.43,0,0
gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
w = 0.0849 # [kg wasser/ kg holz nass]
pellet = wc.Wood("Pellet",gamma,w)

# Hu_dry = 18090e-3 #[MJ/kg]
# Hu_wet = 16427e-3 #[MJ/kg]
# Messpunkt 1
start = np.where(file.Uhrzeit == np.datetime64(datetime(2022, 8, 8, 12, 45, 0)))[0][0]
stop = np.where(file.Uhrzeit == np.datetime64(datetime(2022, 8, 8, 13, 45, 0)))[0][0]
# Gewichtsabnahme für Wirkungsgradbestimmung
start_waage = np.where(file.Uhrzeit == np.datetime64(datetime(2022, 8, 8, 13, 15, 0)))[0][0]
stop_waage = np.where(file.Uhrzeit == np.datetime64(datetime(2022, 8, 8, 13, 45, 0)))[0][0]
dm_wet = file.Gewicht_W_600[start_waage]-file.Gewicht_W_600[stop_waage]
dt = time_abs[stop_waage]-time_abs[start_waage]
mdot_wet = dm_wet/dt  # [kg/s]
dm_dry = dm_wet *(1-w)  # [kg]
mdot_dry = mdot_wet*(1-w) # [kg/s]

# Mittelwerte
o2_tr = file.O2_Emi1[start:stop].mean()  #  [Vol %]
co2_tr = file.CO2_Emi1[start:stop].mean()  #  [Vol %]
T_Abgas = file.T_Abgas[start:stop].mean()

# Berechnungen
lam_o2_calc_dry = pellet.Lamb_O2_tr(o2_tr*1e-2)[0]
lam_co2_calc_dry = pellet.Lamb_CO2_tr(co2_tr*1e-2)[0]
mdot_air_dry = pellet.lmin_dry() * lam_o2_calc_dry * mdot_dry
mass_air_dry = mdot_air_dry*dt
lam_mass = mdot_air_dry/(mdot_dry*pellet.lmin_dry())

q_nutz = file.P_Kessel[start:stop].mean()  #mdot_wet*dm_wet*1e3 # [kW]
n_direkt = n_direkt_fun(q_nutz/1000,mdot_wet,pellet.Hu_nass())
# n_indirekt(T_Abgas,pellet.Hu_nass(),pellet.lmin(),lam_o2_calc_dry,pellet.u)
P = q_nutz




headers_input = ["Startzeit", "Endzeit ","Pelletmenge [kg/h]","O2_dry [Vol %]"]
input = [[str(file.Uhrzeit[start]), str(file.Uhrzeit[stop]),round(dm_dry,2),round(o2_tr,2)]]
headers_res = ["Leistung [kW]","lmin_dry [kg/kg]", "lam_o2 [-]","lam_co2 [-]",
                 "Luftmenge trocken [kg/h]"]
res = [[round(P,2),round(pellet.lmin_dry(), 2), \
               round(lam_o2_calc_dry, 2),round(lam_co2_calc_dry, 2), round(mass_air_dry,2)]]
print("\n", "Inputs:", "\n\n", tabulate(input, headers_input))
print("\n", "Berechnungen:", "\n\n", tabulate(res, headers_res))
"----------------Plots---------------------------------------------------------------"
"plot Gasanalyse"
size = 15
tick_size = 12

fig1,ax = plt.subplots()
#Set the format of the x-axis to hh:mm:ss
xformatter = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xformatter)
fakt_CO = 1e-2
fakt_NO = 1e-1
fakt_FID = 1e-2

ax.plot(file.Uhrzeit, file.O2_Emi1, label = "O2_Emi1 [Vol %]")
ax.plot(file.Uhrzeit,file.CO_low_Emi1*fakt_CO,label = f"CO_low_Emi1 [ppm*{fakt_CO}]")
ax.plot(file.Uhrzeit, file.NOx_Emi1*fakt_NO,label = f"NOx_Emi1 [ppm*{fakt_NO}]")
ax.plot(file.Uhrzeit, file.FID_Emi1*fakt_FID,label = f"FID_Emi1 [ppm*{fakt_FID}]")
ax.set_ylabel(' [Vol %] or [ppm]', fontsize = size)
ax.set_xlabel(' Time [hh,mm,ss]', fontsize = size)
ax.grid(True)
fig1.legend(loc='upper right', fontsize = size)
ax.tick_params(labelsize = tick_size)
fig1.show()

"Gas analyse Normgrössen"
size = 15
tick_size = 12

fig1,ax = plt.subplots()
#Set the format of the x-axis to hh:mm:ss
xformatter = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xformatter)
ax.plot(file.Uhrzeit, file.CO2_Emi1, label = "CO2_Emi1 [Vol %]")
ax2 = ax.twinx()
ax2.plot(file.Uhrzeit,x_norm[0]*fakt_CO,label = f"CO_low_Emi1",color ="red")
ax2.plot(file.Uhrzeit, x_norm[1]*fakt_NO,label = f"NOx_Emi1", color = "purple")
# fakt_staub = 1e-5
# ax.plot(file.Uhrzeit, file.N*fakt_staub,label = f"$Staub [x/cm^3] * {fakt_staub}$")

ax.set_ylabel(' [Vol %]', fontsize = size)
ax2.set_ylabel(f'[mg/$Nm^3$ @{o2_norm} Vol % O2 ]', fontsize = size)
ax.set_xlabel(' Time [hh,mm,ss]', fontsize = size)
ax.grid(True)
fig1.legend(loc='upper right', fontsize = size)
ax.tick_params(labelsize = tick_size)
fig1.show()

"Temperaturen"
fig1,ax = plt.subplots()
#Set the format of the x-axis to hh:mm:ss
xformatter = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xformatter)

ax.plot(file.Uhrzeit, file.TIR_112, label = "Rücklauf [°C]")
ax.plot(file.Uhrzeit,file.TIR_111,label = f"Vorlauf [°C]")
ax.plot(file.Uhrzeit, file.TIR_401,label = f"Abgas [°C]")
# fakt_staub = 1e-5
# ax.plot(file.Uhrzeit, file.N*fakt_staub,label = f"$Staub [x/cm^3] * {fakt_staub}$")

ax.set_ylabel('Temperatur [°C]', fontsize = size)
ax.set_xlabel(' Time [hh,mm,ss]', fontsize = size)
ax.grid(True)
fig1.legend(loc='upper right', fontsize = size)
ax.tick_params(labelsize = tick_size)
fig1.show()

"Gewichtsverlust"
"Temperaturen"
fig1,ax = plt.subplots()
#Set the format of the x-axis to hh:mm:ss
xformatter = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xformatter)

ax.plot(file.Uhrzeit, file.Gewicht_W_600, label = "Gewicht Waage ")
# ax.plot(file.Uhrzeit,file.TIR_111,label = f"Vorlauf [°C]")
# ax.plot(file.Uhrzeit, file.TIR_401,label = f"Abgas [°C]")
# fakt_staub = 1e-5
# ax.plot(file.Uhrzeit, file.N*fakt_staub,label = f"$Staub [x/cm^3] * {fakt_staub}$")

ax.set_ylabel('Gewicht [kg]', fontsize = size)
ax.set_xlabel(' Time [hh,mm,ss]', fontsize = size)
ax.grid(True)
fig1.legend(loc='upper right', fontsize = size)
ax.tick_params(labelsize = tick_size)
fig1.show()
# "Badewannenkurve"
#
# fig1,ax = plt.subplots()
# ax.plot(file.O2_Emi1, file.CO_low_Emi1, "o")
# ax.plot(file.O2_Emi1, x_norm[0], "x")
# ax.set_ylabel('CO [ppm] or [mg/Nm3]', fontsize = size)
# ax.set_xlabel(' O2 [Vol %]', fontsize = size)
# ax.grid(True)
# # fig1.legend(loc='upper right', fontsize = size)
# ax.tick_params(labelsize = tick_size)
# fig1.show()
#
# ""