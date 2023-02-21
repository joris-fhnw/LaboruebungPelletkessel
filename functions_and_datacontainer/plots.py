from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from functions_and_datacontainer.main_variables import *
from tabulate import tabulate
import matplotlib
matplotlib.use("Qt5Agg") #qtagg
from openpyxl import load_workbook
from pandas import ExcelWriter
# import os
# import openpyxl

"------------------------------Plot Parameter------------------------------------------------------------------------"
show_res = 0 # Print der Resultate oder nicht

color = {"O2":"darkblue","CO": "green", "UHC":"salmon","NOx":"purple","CO2":"orange","v_abgas":"grey","Staub":"black",
         "burn_on":"violet","valve_open":"darkblue","P":"chocolate"}  # colors for the plots
color_Temp = {"T_PAK": "green", "T_vorlauf":"salmon","T_rücklauf":"darkblue","T_abgas":"crimson","v_abgas":"grey","Staub":"black",
         "burn_on":"violet","valve_open":"darkblue"}  # colors for the plots

fakt_staub = 0
label_mass = {"CO":"CO [$\mu$g/s]","NOx": "$NO_x$ [$\mu$g/s]", "Staub": f"staub*{fakt_staub} [x/$cm^3$]",
              "UHC": "OGC [$\mu$g/s]","v_abgas": "v_Abgas [m/s]"}
label = {"O2":"O2 [Vol %]","CO":"CO [ppm]","NOx": "$NO_x$ [ppm]", "Staub": f"Staub*{fakt_staub} [x/$cm^3$]", "UHC": "OGC [ppm]",
               "v_abgas": "v_Abgas [m/s]", "CO2": "$CO_2$ [Vol %]","P": "Leistung [kW]"}

y1_lim_mass = [0,1000]
y2_lim_mass = [0,10.5]
y1_lim = [0,100]
y2_lim = [0,14]

size = 15
tick_size = 12
label_size = 15

fig_width_size = 15
fig_height_size = 4
"----------------Plots---------------------------------------------------------------"


def emi_raw(file,start = 0, stop = -1):
    """
    Plottet die Emissionen unbearbeitet ohne Zeitversatz in ppm und VOl%
    :param file:
    """
    fig1, ax = plt.subplots()
    # Set the format of the x-axis to hh:mm:ss
    xformatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xformatter)
    ax.plot(file.Uhrzeit[start:stop], file.CO[start:stop], color=color["CO"], label=label["CO"])

    ax.plot(file.Uhrzeit[start:stop], file.NO[start:stop], color=color["NOx"], label=label["NOx"])
    # ax.plot(file.Uhrzeit, file.P_Kessel,label = "P_Kessel [kW]")
    # ax.plot(file.Uhrzeit[start:stop], file.CH4[start:stop], color=color["UHC"], label=label["UHC"])
    # ax.plot(file.Uhrzeit,file.d,label = "durchmesser Partikel")
    ax2 = ax.twinx()
    ax2.plot(file.Uhrzeit[start:stop], file.O2[start:stop], color=color["O2"], label=label["O2"])
    ax2.plot(file.Uhrzeit[start:stop], file.P_Kessel[start:stop], color=color["P"], label=label["P"])
    # ax.plot(file.Uhrzeit[start:stop], file.v_prim[start:stop], color=color["v_abgas"], label=label["v_abgas"])
    ax.set_ylabel('Emissionen [ppm]', fontsize=size)
    ax2.set_ylabel(' Vol %, kW', fontsize=size)
    ax.set_xlabel('Time [hh,mm,ss]', fontsize=size)
    ax.grid(True)
    fig1.set_figwidth(fig_width_size)
    fig1.set_figheight(fig_height_size)
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='best', fontsize = size)
    ax.tick_params(labelsize=tick_size)
    ax2.tick_params(labelsize=tick_size)
    plt.tight_layout()
    fig1.show()

# def Badewanne(file1,file2):


def Temperaturen(file,start=0,stop=-1):
    fig1, ax = plt.subplots()
    # Set the format of the x-axis to hh:mm:ss
    xformatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xformatter)

    ax.plot(file.Uhrzeit[start:stop], file.T_K_RL[start:stop],color = color_Temp["T_rücklauf"] ,label="Rücklauf [°C]")
    ax.plot(file.Uhrzeit[start:stop], file.T_K_VL[start:stop],color = color_Temp["T_vorlauf"], label=f"Vorlauf [°C]")
    ax.plot(file.Uhrzeit[start:stop], file.T_Abgas[start:stop],color = color_Temp["T_abgas"], label=f"Abgas [°C]")
    # fakt_staub = 1e-5
    # ax.plot(file.Uhrzeit, file.N*fakt_staub,label = f"$Staub [x/cm^3] * {fakt_staub}$")

    ax.set_ylabel('Temperatur [°C]', fontsize=size)
    ax.set_xlabel(' Time [hh,mm,ss]', fontsize=size)
    ax.grid(True)
    fig1.set_figwidth(fig_width_size)
    fig1.set_figheight(fig_height_size)
    plt.legend(loc='best', fontsize=size)
    ax.tick_params(labelsize=tick_size)
    plt.tight_layout()
    fig1.show()


def waage(file,start=0,stop=-1):
    fig1, ax = plt.subplots()
    # Set the format of the x-axis to hh:mm:ss
    xformatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xformatter)

    ax.plot(file.Uhrzeit[start:stop], file.Gewicht[start:stop], label="Gewicht Waage ")

    ax.set_ylabel('Gewicht [kg]', fontsize=size)
    ax.set_xlabel(' Time [hh,mm,ss]', fontsize=size)
    ax.tick_params(labelsize=tick_size)
    ax.grid(True)
    fig1.set_figwidth(fig_width_size)
    fig1.set_figheight(fig_height_size)
    plt.legend(loc='best', fontsize=size)
    ax.tick_params(labelsize=tick_size)
    plt.tight_layout()
    fig1.show()

def write_to_excel(excel_name,data,Sheet_Name,index=False):
    """
    Schreibt data in ein Excel file, wenn dieses bereits existiert wird es überschrieben, ansonsten wird ein neues erstellt
    :param excel_name: str, Name des Excels
    :param data: pandas Dataframe, Daten welche in das Excel geschrieben werden
    :param Sheet_Name: str, Name des Excel sheets
    :param index:
    """
    excel_name = excel_name+'.xlsx'

    try:
        "Versuche Excel zu laden"
        ExcelWorkbook = load_workbook(excel_name)
        writer = ExcelWriter(excel_name, engine='openpyxl')
        writer.book = ExcelWorkbook
        data.to_excel(writer,Sheet_Name,index= index)
        writer.close()
        writer.book.close()

    except:
        "Wenn das Excel nicht existiert wird es erstellt"
        writer = ExcelWriter(excel_name, engine='openpyxl')
        data.to_excel(writer,Sheet_Name,index= index)
        writer.close()

"""
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

"""