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
path = "C:\\Users\\admin\\PycharmProjects\\Laboruebung_Pelletkessel\\Pelletkessel\\Betriebspunkte\\" \
       "betriebspunkt_mager_12prozO2\\"
excel_name = "LÜ_Pelletkessel_Messpunkte220926112917.xlsx"
excel_name = path+excel_name
file = pd.read_excel(excel_name,header=1)
file = ed.edit_silana_excel(file)
file["T_Abgas"] = file.T_Ab # damit direkt mit T_Abgas gearbeitet werden kann
o2_norm = 13
# x_norm = ed.norm_values([file.CO_low_Emi1,file.NOx_Emi1],[M_CO,M_NO2],file.O2_Emi1,o2_norm)
time_abs = ed.time_abs_fun(file.Uhrzeit) # erstelle absolut Zeit

start = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 14, 57, 0)
stop = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 15, 16, 0)
start_waage = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 14, 20, 0)
stop_waage = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 15, 16, 0)

yc,yh,yo,yn,ys = 0.51, 0.06,0.43,0,0
gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
w = 0.0849 # [kg wasser/ kg holz nass]

"Betriebspunkte"
opt_start = start
opt_stop = stop
mager_start = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 16, 20, 0)
mager_stop = ed.get_index_of_time(file.Uhrzeit,2022, 9, 26, 16, 50, 0)

opt = bet.Betriebspunkt(file,opt_start,opt_stop,"optimum",gamma,w)
opt.set_mass_loss_parmeters(file,start_waage,stop_waage)
opt.n_indirekt_fun(1.0065,1.873,1.065)
mager = bet.Betriebspunkt(file,mager_start,mager_stop,"optimum",gamma,w)
mager.set_mass_loss_parmeters(file,mager_start,mager_stop)
mager.n_indirekt_fun(1.0065,1.873,1.065)

if show_res:
    "Resultate"
    opt_res = opt.build_res_vek("optimal")
    mager_res = mager.build_res_vek("mager")
    res_vek = [opt_res.values[0],mager_res.values[0]]
    res_dataframe = pd.DataFrame(res_vek, columns=opt_res.columns)
    print(tabulate(res_vek,headers = opt_res.columns))
    # print("\n", "Optimum:", "\n\n",tabulate(opt_res,headers = opt_res.columns))
    # print("\n", "Mager:", "\n\n",tabulate(mager_res,headers = mager_res.columns))


if show_plot:
    "Plots"
    plots.emi_raw(file)
    plots.waage(file)
    plots.Temperaturen(file)



if wirte_excel:
    plots.write_to_excel("Mittelwerte_Laborübung_Pelletkessel_2",res_dataframe,"mittelwerte_fett")
