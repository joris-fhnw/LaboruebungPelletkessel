"""Für die Laborübung wurde nach geeigneten Betriebspunkten gesucht,
dazu wurde der Kessel erst aufgeheizt beim optimum: Gebläse 50 % bei 100 % Leistung, O2 soll (feucht): 7.5
fett: Gebläse 35 %, O2 soll 4 %
Optimal mit weniger Primärluft (0.3 m3/h anstatt 0.4 m3/h)"""

from functions_and_datacontainer import plots
import pandas as pd
import functions_and_datacontainer.edit_data_frame as ed
from functions_and_datacontainer import betriebspunkte as bet
from tabulate import tabulate
import os



show_plot = False
calculate = True
show_res = True
wirte_excel = True


"import data"
""
path = os.path.dirname(__file__)
# path = "C:\\Users\\{user}\\PycharmProjects\\Laboruebung_Pelletkessel\\Pelletkessel\\Betriebspunkte\\" \
#        "betriebspunkt_fett_04prozO2\\"
excel_name = "Aufz_Rohdaten_TEST_Bafu_OEL_221004090722.xlsx"
excel_name = path +"/" +excel_name
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
    day = 4

    yc,yh,yo,yn,ys = 0.51, 0.06,0.43,0,0
    gamma = ["C",yc,"H",yh,"O",yo,"N",yn,"S",ys]
    w = 0.0849 # [kg wasser/ kg holz nass]

    "Betriebspunkte"
    opt_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 10, 34, 0)
    opt_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 10, 51, 0)
    mager_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 13, 44, 0)
    mager_stop = ed.get_index_of_time(file.Uhrzeit,year, month, day, 14, 39, 0)
    nenn_start = ed.get_index_of_time(file.Uhrzeit,year, month, day, 15, 25, 0)
    nenn_stop = ed.get_index_of_time(file.Uhrzeit, year, month, day, 15, 40, 0)

    opt = bet.Betriebspunkt(file,opt_start,opt_stop,"optimum",gamma,w)
    opt.set_mass_loss_parmeters(file,opt_start,opt_stop)
    opt.n_indirekt_fun(1.0065, 1.873, 1.065)
    mager = bet.Betriebspunkt(file,mager_start,mager_stop,"optimum",gamma,w)
    mager.set_mass_loss_parmeters(file,mager_start,mager_stop)
    mager.n_indirekt_fun(1.0065, 1.873, 1.065)
    nenn = bet.Betriebspunkt(file,nenn_start,nenn_stop,"nenn",gamma,w)
    nenn.set_mass_loss_parmeters(file,nenn_start,nenn_stop)
    nenn.n_indirekt_fun(1.0065, 1.873, 1.065)

    lam_o2_vek = []


if show_res:
    "Resultate"
    opt_res = opt.build_res_vek("optimal")
    mager_res = mager.build_res_vek("fett")
    nenn_res = nenn.build_res_vek("optimal_v_prim_low")
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