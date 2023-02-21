"""Für die Laborübung wurde nach geeigneten Betriebspunkten gesucht,
dazu wurde der Kessel erst aufgeheizt beim optimum: Gebläse 50 % bei 100 % Leistung, O2 soll (feucht): 7.5
fett: Gebläse 35 %, O2 soll 4 %
Optimal mit weniger Primärluft (0.3 m3/h anstatt 0.4 m3/h)"""

from Pelletkessel import plots
from Pelletkessel import wood_combustion as wc
import numpy as np
import pandas as pd
import Pelletkessel.edit_data_frame as ed
from Pelletkessel.main_variables import *
# from datetime import datetime
from Pelletkessel.functions import  density_air
from Pelletkessel import betriebspunkte as bet
from tabulate import tabulate
from Pelletkessel.functions import change_dataframe_names
# import matplotlib
# matplotlib.use("qtagg") #qtagg


show_plot = True
calculate = True
show_res = True
wirte_excel = False

# Betriebspunkt 1 (Lambda 1.4, 11 kW): O2 soll: 5.4 Venti: 40%
# Betriespunkt 2 (Lambda 2.3, 11 kW): O2 soll: 11.2 Venti: 72 %

"import data"
path = "C:\\Users\\admin\\PycharmProjects\\Laboruebung_Pelletkessel\\Pelletkessel\\M_HS22\\" \
       "Gruppe6_Neukomm_Renz\\"
MP1 = "Aufz_Rohdaten_Laborubung_Pelletkessel_221020093151.xlsx"
MP2 = "Aufz_Rohdaten_Laborubung_Pelletkessel_221020110237.xlsx"
excel_name1 = path + MP1
excel_name2 = path+MP2
file1 = pd.read_excel(excel_name1,header=1)
file1 = ed.edit_silana_excel(file1)
file1 = change_dataframe_names(file1)

file2 = pd.read_excel(excel_name2,header=1)
file2 = ed.edit_silana_excel(file2)
file2 = change_dataframe_names(file2)

o2_norm = 10
x_norm = ed.norm_values([file1.CO,file1.NO],[M_CO,M_NO2],file1.O2,o2_norm)
file1["CO_norm"]=x_norm[0]
file1["NO_norm"] = x_norm[1]

x_norm2 = ed.norm_values([file2.CO,file2.NO],[M_CO,M_NO2],file2.O2,o2_norm)
file2["CO_norm"]=x_norm2[0]
file2["NO_norm"] = x_norm2[1]
# time_abs = ed.time_abs_fun(file.Uhrzeit) # erstelle absolut Zeit


if calculate:
    year = 2022
    month = 10
    day = 20

    yc,yh,yo,yn,ys = 0.508, 0.059,0.432,0.001,0
    gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
    w = 0.085 # [kg wasser/ kg holz nass]

    "Betriebspunkte"
    fett_start = 0
    fett_stop = -1
    mager_start = 0
    mager_stop = -1
    fett_waage_start = ed.get_index_of_time(file1.Uhrzeit,year, month, day, 9, 40, 0)
    fett_waage_stop = ed.get_index_of_time(file1.Uhrzeit, year, month, day, 10, 15, 0)
    fett = bet.Betriebspunkt(file1,fett_start,fett_stop,"fett",gamma,w)
    fett.set_mass_loss_parmeters(file1,fett_waage_start,fett_waage_stop)
    fett.n_indirekt_fun(1.0065, 1.873, 1.065)

    mager = bet.Betriebspunkt(file2,mager_start,mager_stop,"nenn",gamma,w)
    mager.set_mass_loss_parmeters(file2,mager_start,mager_stop)
    mager.n_indirekt_fun(1.0065, 1.873, 1.065)

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
    plots.emi_raw(file1)
    plots.waage(file1)
    plots.Temperaturen(file1)
    plots.emi_raw(file2)
    plots.waage(file2)
    plots.Temperaturen(file2)

if wirte_excel:
    plots.write_to_excel("Mittelwerte_Laborübung_Pelletkessel",res_dataframe,"Betriebspunkte_Laborübung")