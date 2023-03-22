from CoolProp.CoolProp import PropsSI
import numpy as np
from functions_and_datacontainer import functions as func
from matplotlib import pyplot as plt
import matplotlib
from functions_and_datacontainer import wood_combustion as wc
import cantera as ct
matplotlib.use("Qt5Agg")

"Berechnen des Stöchiometrischen Abgases"
yc, yh, yo, yn, ys = 0.51, 0.06, 0.43, 0, 0
gamma = ["C", yc, "H", yh, "O", yo, "N", yn, "S", ys]
w = 0.08  # [kg wasser/ kg holz nass]
wood = wc.Wood("Holz",gamma,w)
x = {"H2O": wood.H2O(1), "CO2": wood.CO2(1), "N2": wood.N2(1)}  # Molanteile des stöchiometrischen Abgases, Lambda = 1
exhaus_stoech = ct.Solution("gri30.yaml")
exhaus_stoech.TPX = 300,ct.one_atm,x


# CP Wasser, Wasserdampf und Luft mit Coolprop
dT = 273
Temp_exhaust = np.array(range((75 + dT), (125+dT)))  # [K] Abgas
Temp_water = np.array(range(40+dT, 70 + dT))  # [K] Wasserkreislauf
Temp_comb_air = np.array(range(10+dT, 30 + dT))
lam = np.array([1.4, 2.3])
p_amb = 1.01325e5  # [Pa]


# Initialisieren der Vektoren
cp_vapor = np.zeros((lam.size, Temp_exhaust.size))
cp_air = np.zeros(Temp_exhaust.size)
cp_exhaust = np.zeros(Temp_exhaust.size)
cp_water = np.zeros(Temp_water.size)
density_water = np.zeros(Temp_water.size)
density_air = np.zeros(Temp_comb_air.size)

x_h2o = np.zeros(lam.size)

# Berechne Wasseranteil im Abgas für Partialdruck des Dampfes
for i, l in enumerate(lam): x_h2o[i] = wood.H2O(l)  # [mol/mol] Molbruch
p_vapor = x_h2o * p_amb  # [Pa] Partialdruck des Dampfes im Abgas (Auch abhängig von Lambda)

# Berechnung der Dichte und der Wärmekapazitäten
for i, T in enumerate(Temp_exhaust):
    # Temperaturbereich hoch (am Ausgang des Kessels)
    for z in range(lam.size): cp_vapor[z, i] = PropsSI("C", "T", T, "P|gas", p_vapor[z], "Water")  # [J/(kg*K)]
    cp_air[i] = PropsSI("C", "T", T, "P", p_amb, "Air")  # [J/(kg*K)]
    exhaus_stoech.TP = T,p_amb
    cp_exhaust[i] = exhaus_stoech.cp_mass  # [kJ/(kg*K)] ergibt fast das gleiche, wie wenn mit CoolProp gerechnet wird:
    # über yCO2 * cpCO2 + yN2*cpN2+yH2O*cpH2O
    # cp_exhaust[i] = func.calc_cp_exhaust(1, T)  # Funktion aus Paper ergibt auch sehr ähliche Resultate
for i, T in enumerate(Temp_water):
    # Temperaturbereich niedrig (am Eingang des Kessels)
    cp_water[i] = PropsSI("C", "T|liquid", T, "P", p_amb, "Water")  # [J/(kg*K)]
    density_water[i] = PropsSI("D", "T|liquid", T, "P", p_amb, "Water")  # [kg/m3]
for i, T in enumerate(Temp_comb_air):
    density_air[i] = PropsSI("D", "T", T, "P", p_amb, "Air")  # [kg/m3]

"-----------------------Plot----------------------------------------"
color = ["black", "grey"]  # Falls 2 Plotts in einem Graph
#

"CP Exhaust"
fig1 = plt.figure()
plt.plot(Temp_exhaust - 273, cp_exhaust, color="black", label=f"cp Abgas (stöchiometrisch)")
plt.ylabel("Wärmekapazität [J/(kg*K]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig1.show()

"CP Vapor"
fig2 = plt.figure()
for z in range(lam.size):
    plt.plot(Temp_exhaust - 273, cp_vapor[z], color=color[z],
                 label=f"cp Dampf, lambda: {lam[z]}")
plt.ylabel("Wärmekapazität [J/(kg*K]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig1.show()

"CP Air"
fig3 = plt.figure()
plt.plot(Temp_exhaust - 273, cp_air, color="black", label=f"cp Luft")
plt.ylabel("Wärmekapazität [J/(kg*K]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig1.show()

"Airdensity"
fig4, axes2 = plt.subplots(2, 1)
axes2[0].plot(Temp_comb_air - 273, density_air, color="black", label="Dichte Luft")
axes2[0].set_ylabel("[kg/m3]")
axes2[0].legend()
axes2[0].grid()

axes2[1].plot(Temp_water - 273, density_water, color="black", label="Dichte Wasser")
axes2[1].set_ylabel("[kg/m3]")
axes2[1].legend()
axes2[1].grid()
axes2[1].set_xlabel("Temperatur [°C]")
plt.tight_layout()


plt.show()

save_fig = False

if save_fig:
    fig_formate = "png"
    fig_name1 = "cp Abgas stöchiometrisch" + "." + fig_formate
    fig_name2 = "cp Dampf" + "." + fig_formate
    fig_name3 = "cp Luft" + "." + fig_formate
    fig_name4 = "Dichte Wasser und Luft" + "." + fig_formate

    fig1.savefig(fig_name1, format=fig_formate)
    fig2.savefig(fig_name2, format=fig_formate)
    fig3.savefig(fig_name3, format=fig_formate)
    fig4.savefig(fig_name4, format=fig_formate)

"CP Water,Vapor and Air"
# fig, axes = plt.subplots(3, 1)
# for z in range(lam.size):
#     axes[0].plot(Temp_exhaust - 273, cp_vapor[z], color=color[z],
#                  label=f"cp vapor, lambda: {lam[z]}")
# axes[0].set_ylabel("[J/(kg*K)]")
# axes[0].legend()
# axes[0].grid()
#
# axes[1].plot(Temp_exhaust - 273, cp_air, color="black", label="cp air")
# axes[1].set_ylabel("[J/(kg*K)]")
# axes[1].legend()
# axes[1].grid()
# Tmin, Tmax = 10, 80  # [°C] Plot Bereich für Wasser
# axes[2].plot(Temp_water - 273, cp_water, color="black", label="cp water")
# # axes[2].set_xlim([10,80])
# # axes[2].set_ylim([4170,4200])
# axes[2].set_ylabel("[J/(kg*K)]")
# axes[2].set_xlabel("Temperatur [°C]")
# axes[2].legend()
# axes[2].grid()
# plt.tight_layout()

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
