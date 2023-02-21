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

show_plot = False
calculate = True
show_res = True
wirte_excel = True

"import data"
excel_name = "Aufz_Rohdaten_Laborubung_Pelletkessel_221006102535.xlsx"
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
    day = 6

    yc,yh,yo,yn,ys = 0.51, 0.06,0.43,0,0
    gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
    w = 0.0849 # [kg wasser/ kg holz nass]

    "Betriebspunkte"
    opt_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 11, 45, 0)
    opt_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 12, 36, 0)
    mager_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 13, 10, 0)
    mager_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 13, 35, 0)
    nenn_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 14, 37, 0)
    nenn_stop = ed.get_index_of_time(file.Uhrzeit, year, month, day, 15, 49, 0)

    opt = bet.Betriebspunkt(file,opt_start,opt_stop,"optimum",gamma,w)
    opt.set_mass_loss_parmeters(file,opt_start,opt_stop)
    opt.n_indirekt_fun(1.0065,1.8724,1.06)
    mager = bet.Betriebspunkt(file,mager_start,mager_stop,"optimum",gamma,w)
    mager.set_mass_loss_parmeters(file,mager_start,mager_stop)
    mager.n_indirekt_fun(1.0065,1.8724,1.061)
    nenn = bet.Betriebspunkt(file,nenn_start,nenn_stop,"nenn",gamma,w)
    nenn.set_mass_loss_parmeters(file,nenn_start,nenn_stop)
    nenn.n_indirekt_fun(1.0065,1.873,1.065)


if show_res:
    "Resultate"
    opt_res = opt.build_res_vek("optimal")
    mager_res = mager.build_res_vek("mager_1")
    nenn_res = nenn.build_res_vek("mager_2")
    res_vek = [opt_res.values[0],mager_res.values[0],nenn_res.values[0]]
    res_dataframe = pd.DataFrame(res_vek,columns=opt_res.columns)
    print(tabulate(res_vek,headers = opt_res.columns))
    # print("\n", "Optimum:", "\n\n",tabulate(opt_res,headers = opt_res.columns))
    # print("\n", "Mager:", "\n\n",tabulate(mager_res,headers = mager_res.columns))


if show_plot:
    "Plots"
    plots.emi_raw(file)
    plots.waage(file)
    plots.Temperaturen(file)


if wirte_excel:
    plots.write_to_excel("Mittelwerte_Laborübung_Pelletkessel",res_dataframe,"mittelwerte_fett")

# Verluste im Abgas
dT =  (nenn.T_abgas-nenn.T_amb)
mue_v = 1+nenn.lmin()
cp_v = 1.065  # [kJ/ (kg*K)]
cp_l = 1.0065  # [kJ/ (kg*K)]
cp_w = 1.873  # [kJ/ (kg*K)]
# qvv = (mue_v*cp_v * dT + nenn.u*cp_w*dT + (nenn.Lamb_O2_tr(nenn.o2/100)[0]-1)*nenn.lmin()*cp_l*dT)*1e-3  # [kJ]
#
# n_indirekt = 1-(qvv/((nenn.u+1)*nenn.Hu_nass()))-0.01
# # Verluste durch Wärmeabstrahlung
