from CoolProp.CoolProp import PropsSI
import numpy as np
from functions_and_datacontainer import functions as func
from matplotlib import pyplot as plt
from functions_and_datacontainer import wood_combustion as wc
import matplotlib.dates as mdates
import matplotlib

matplotlib.use("Qt5Agg")

# CP Wasser, Wasserdampf und Luft mit Coolprop
dT = 273
Temp_exhaust = np.array(range((75 + dT), (125+dT)))  # [K] Abgas
Temp_water = np.array(range(40+dT, 70 + dT))  # [K] Wasserklreislauf
Temp_comb_air = np.array(range(10+dT, 30 + dT))
lam = np.array([1.4, 2.3])
p_amb = 1.01325e5  # [Pa]


# Initialisieren der Vektoren
cp_vapor = np.zeros((lam.size, Temp_exhaust.size))
cp_air = np.zeros(Temp_exhaust.size)
cp_exhaust = np.zeros(Temp_exhaust.size)   # Stöchiometrisch!!
cp_water = np.zeros(Temp_water.size)
density_water = np.zeros(Temp_water.size)
density_air = np.zeros(Temp_comb_air.size)

x_h2o = np.zeros(lam.size)

# Berechne Wasseranteil im Abgas für Partialdruck des Dampfes
pellet = wc.Wood("Pellet", ["C", 0.51, "H", 0.06, "O", 0.43, "N", 0, "S", 0], 0.08)  # Objekt für Rechnung
for i, l in enumerate(lam): x_h2o[i] = pellet.H2O(l)  # [mol/mol] Molbruch
p_vapor = x_h2o * p_amb  # [Pa] Partialdruck des Dampfes im Abgas (Auch Abhänig von Lambda)


# Berechnung der Dichte und der Wärmekapazitäten
for i, T in enumerate(Temp_exhaust):
    # Temperaturbereich hoch (am Ausgang des Kessels)
    for z in range(lam.size): cp_vapor[z, i] = PropsSI("C", "T", T, "P|gas", p_vapor[z], "Water")  # [J/(kg*K)]
    cp_air[i] = PropsSI("C", "T", T, "P", p_amb, "Air")  # [J/(kg*K)]
    cp_exhaust[i] = func.calc_cp_exhaust(1, T)
for i, T in enumerate(Temp_water):
    # Temperaturbereich niedrig (am Eingang des Kessels)
    cp_water[i] = PropsSI("C", "T|liquid", T, "P", p_amb, "Water")  # [J/(kg*K)]
    density_water[i] = PropsSI("D", "T|liquid", T, "P", p_amb, "Water")  # [kg/m3]
for i, T in enumerate(Temp_comb_air):
    density_air[i] = PropsSI("D", "T", T, "P", p_amb, "Air")  # [kg/m3]

"-----------------------Plot----------------------------------------"
color = ["black", "grey"]  # Falls 2 Plotts in einem Graph
"CP Water,Vapor and Air"
fig, axes = plt.subplots(3, 1)
for z in range(lam.size):
    axes[0].plot(Temp_exhaust - 273, cp_vapor[z], color=color[z],
                 label=f"cp vapor, lambda: {lam[z]}")
axes[0].set_ylabel("[J/(kg*K)]")
axes[0].legend()
axes[0].grid()

axes[1].plot(Temp_exhaust - 273, cp_air, color="black", label="cp air")
axes[1].set_ylabel("[J/(kg*K)]")
axes[1].legend()
axes[1].grid()
Tmin, Tmax = 10, 80  # [°C] Plot Bereich für Wasser
axes[2].plot(Temp_water - 273, cp_water, color="black", label="cp water")
# axes[2].set_xlim([10,80])
# axes[2].set_ylim([4170,4200])
axes[2].set_ylabel("[J/(kg*K)]")
axes[2].set_xlabel("Temperatur [°C]")
axes[2].legend()
axes[2].grid()
plt.tight_layout()

"CP Exhaust"
fig1 = plt.figure()
plt.plot(Temp_exhaust - 273, cp_exhaust, color="black", label=f"cp exhaust, Lambda = 1")
plt.ylabel("Wärmekapazität [J/(kg*K]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig1.show()

"Airdensity"
fig2, axes2 = plt.subplots(2, 1)
axes2[0].plot(Temp_comb_air - 273, density_air, color="black", label="air density")
axes2[0].set_ylabel("[kg/m3]")
axes2[0].legend()
axes2[0].grid()

axes2[1].plot(Temp_water - 273, density_water, color="black", label="water density")
axes2[1].set_ylabel("[kg/m3]")
axes2[1].legend()
axes2[1].grid()
axes2[1].set_xlabel("Temperatur [°C]")
plt.tight_layout()

# fig2 = plt.figure()
# plt.plot(Temp-273,density_air,color = "black",label = f"air density")
# plt.ylabel("Density [kg/m3]")
# plt.xlabel("Temperatur [°C]")
# plt.xlim([Tmin,Tmax])
# plt.ylim([1,1.25])
# plt.grid()
# plt.legend()
# plt.tight_layout()
# # fig2.show()

plt.show()

save_fig = False

if save_fig:
    fig_formate = "png"
    fig_name = "cp Water Vaper Air" + "." + fig_formate
    fig_name1 = "cp Exhaust" + "." + fig_formate
    fig_name2 = "Airdensity" + "." + fig_formate
    fig.savefig(fig_name, format=fig_formate)
    fig1.savefig(fig_name1, format=fig_formate)
    fig2.savefig(fig_name2, format=fig_formate)
