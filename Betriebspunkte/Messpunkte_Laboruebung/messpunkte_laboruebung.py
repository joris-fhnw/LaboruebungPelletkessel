"""Für die Laborübung wurde nach geeigneten Betriebspunkten gesucht,
dazu wurde der Kessel erst aufgeheizt beim optimum: Gebläse 50 % bei 100 % Leistung, O2 soll (feucht): 7.5
fett: Gebläse 35 %, O2 soll 4 %
Optimal mit weniger Primärluft (0.3 m3/h anstatt 0.4 m3/h)"""
from Pelletkessel import plots
from Pelletkessel import wood_combustion as wc
import numpy as np
import pandas as pd
import Pelletkessel.edit_data_frame as ed
# from Pelletkessel.main_variables import *
# from datetime import datetime
from Pelletkessel.functions import  density_air
from Pelletkessel import betriebspunkte as bet
from tabulate import tabulate
# import matplotlib
# matplotlib.use("qtagg") #qtagg


show_plot = True
calculate = True
show_res = True
wirte_excel = False

# Betriebspunkt 1 (Lambda 1.4, 11 kW): O2 soll: 5.4 Venti: 40%
# Betriespunkt 2 (Lambda 2.3, 11 kW): O2 soll: 11.2 Venti: 72 %

"import data"
path = "C:\\Users\\admin\\PycharmProjects\\Laboruebung_Pelletkessel\\Pelletkessel\\Betriebspunkte\\" \
       "Messpunkte_Laboruebung\\"
excel_name = "Aufz_Rohdaten_Laborubung_Pelletkessel_221018085133.xlsx"
excel_name = path + excel_name
file = pd.read_excel(excel_name,header=1)
file = ed.edit_silana_excel(file)
file["T_Abgas"] = file.T_Ab # damit direkt mit T_Abgas gearbeitet werden kann
file["P_Kessel"] = file.P_Kessel_Silana
file["CO"] = file.CO_VP
file["O2"] = file.O2_VP
file["CO2"] = file.CO2_VP
file["NO"]= file.NO_VP
file["CH4"]= file.CH4_VP

o2_norm = 13
# x_norm = ed.norm_values([file.CO_low_Emi1,file.NOx_Emi1],[M_CO,M_NO2],file.O2_Emi1,o2_norm)
time_abs = ed.time_abs_fun(file.Uhrzeit) # erstelle absolut Zeit


if calculate:
    year = 2022
    month = 10
    day = 18

    yc,yh,yo,yn,ys = 0.51, 0.06,0.43,0,0
    gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
    w = 0.0849 # [kg wasser/ kg holz nass]

    "Betriebspunkte"
    fett_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 10, 26, 0)
    fett_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 11, 19, 0)
    mager_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 13, 0, 0)
    mager_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 14, 42, 0)

    fett = bet.Betriebspunkt(file,fett_start,fett_stop,"optimum",gamma,w)
    fett.set_mass_loss_parmeters(file,fett_start,fett_stop)
    fett.n_indirekt_fun(1.0065, 1.873, 1.065)
    mager = bet.Betriebspunkt(file,mager_start,mager_stop,"nenn",gamma,w)
    mager.set_mass_loss_parmeters(file,mager_start,mager_stop)
    mager.n_indirekt_fun(1.0065, 1.873, 1.065)

    lam_o2_vek = []


if show_res:
    "Resultate"

    fett_res = fett.build_res_vek("fett")
    mager_res = mager.build_res_vek("mager")
    res_vek = [fett_res.values[0],mager_res.values[0]]
    res_dataframe = pd.DataFrame(res_vek,columns=mager_res.columns)
    print(tabulate(res_vek,headers = mager_res.columns))
    # print("\n", "Optimum:", "\n\n",tabulate(opt_res,headers = opt_res.columns))
    # print("\n", "Mager:", "\n\n",tabulate(mager_res,headers = mager_res.columns))


if show_plot:
    "Plots"
    plots.emi_raw(file)
    plots.waage(file)
    plots.Temperaturen(file)


if wirte_excel:
    plots.write_to_excel("Mittelwerte_Laborübung_Pelletkessel",res_dataframe,"Betriebspunkte_Laborübung")