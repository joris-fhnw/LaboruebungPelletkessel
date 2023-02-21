from CoolProp.CoolProp import PropsSI
import numpy as np
from functions_and_datacontainer import functions as func
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use("Qt5Agg") #qtagg

# CP Wasser, Wasserdampf und Luft mit Coolprop
Temp = np.array(range(300,450))  # [K]
cp_vapor = np.zeros(Temp.size)
cp_water = np.zeros(Temp.size)
cp_air = np.zeros(Temp.size)
density_air = np.zeros(Temp.size)

p_amb = 1.01325e2  # [hPa]
for i,T in enumerate(Temp):
    cp_vapor[i] = PropsSI("C","T",T,"P|gas",p_amb,"Water")   # [J/(kg*K)]
    cp_water[i] = PropsSI("C", "T|liquid", T, "P", p_amb, "Water")  # [J/(kg*K)]
    cp_air[i] = PropsSI("C", "T", T, "P", p_amb, "Air")  # [J/(kg*K)]
    density_air[i] = PropsSI("D", "T", T, "P", p_amb, "Air")*1e3  # [kg/K]

# CP Abgas ist von Lambda und Temperatur abhängig, wird mit Fitformel berechnet
lam = np.array([1.4,2.3])
cp_exhaust = np.zeros((lam.size,Temp.size))
for z,l in enumerate(lam):
    for i,T in enumerate(Temp):
        cp_exhaust[z,i] = func.calc_cp_exhaust(l,T)  # [J/(kg*K)]


"-----------------------Plot----------------------------------------"

"CP Water,Vapor and Air"
fig, axes = plt.subplots(3,1)
axes[0].plot(Temp-273,cp_vapor,color = "black",label = "cp vapor")
axes[0].set_ylabel("[J/(kg*K)]")
# axes[0].set_xlabel("Temperatur [°C]")
axes[0].legend()
axes[0].grid()
axes[1].plot(Temp-273,cp_water,color = "black",label = "cp water")
axes[1].set_ylabel("[J/(kg*K)]")
# axes[1].set_xlabel("Temperatur [°C]")
axes[1].legend()
axes[1].grid()
axes[2].plot(Temp-273,cp_air,color = "black",label = "cp air")
axes[2].set_ylabel("[J/(kg*K)]")
axes[2].set_xlabel("Temperatur [°C]")
axes[2].legend()
axes[2].grid()
# fig.text(0.06, 0.5, 'Wärmekapazität [J/(kg*K)]', ha='center', va='center', rotation='vertical')
plt.tight_layout()
# fig.show()

"CP Exhaust"
color = ["black","grey"]
fig1 = plt.figure()
for i,l in enumerate(lam):
    plt.plot(Temp-273,cp_exhaust[i], color=color[i], label=f"Lambda = {l}")
plt.ylabel("Wärmekapazität [J/(kg*K]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig1.show()

"Airdensity"
fig2 = plt.figure()
plt.plot(Temp-273,density_air,color = "black",label = f"air density")
plt.ylabel("Density [kg/m3]")
plt.xlabel("Temperatur [°C]")
plt.grid()
plt.legend()
plt.tight_layout()
# fig2.show()

plt.show()

save_fig = True

if save_fig:
    fig_formate = "png"
    fig_name = "cp Water Vaper Air" + "." + fig_formate
    fig_name1 = "cp Exhaust" + "." + fig_formate
    fig_name2 = "Airdensity" + "." + fig_formate
    fig.savefig(fig_name, format=fig_formate)
    fig1.savefig(fig_name1, format=fig_formate)
    fig2.savefig(fig_name2, format=fig_formate)

