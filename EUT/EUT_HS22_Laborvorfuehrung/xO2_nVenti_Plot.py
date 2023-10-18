import numpy as np
from matplotlib import pyplot as plt
from functions_and_datacontainer import wood_combustion as wc
from CoolProp import CoolProp as cp
import matplotlib
matplotlib.use("Qt5Agg") #qtagg

"------------------Funktionen-----------------------------------------------"
def n_venti(Vdot_air_wet):
    # Berechnet die eingestellte Ventilatordrehzahl in Prozent anhand des Berechneten Luftmassenstrom
    # y = 0.2468x+5.1442 # x: Eingestellte Ventilatordrehzahl in Prozent, y: Luftmassenstrom gemessen in m3/h
    # x = (y-5.1442)/0.2468
    return (Vdot_air_wet-5.1422)/0.2468


def V_air_wet(V_air_dry,T_amb,p_amb,rel_hum):
    """
    Berechnet aus dem trockenen Luftvolumenstrom den feuchten
    :param V_air_dry: trockener Luftvolumenstrom
    :param T_amb: Temperatur der Luft [K]
    :param p_amb: Luftdruck [bar]
    :param rel_hum: relative Luftfeuchte [-]
    :return: feuchter Luftstrom
    """
    p_sat = cp.PropsSI("P", "T", T_amb, "Q", p_amb, "water") * 1e-5  # sättigungsdruck Wasser bei T_amb [K] und P_amb [bar]
    x = 0.622 * rel_hum * p_sat / (p_amb - p_sat)
    return V_air_dry*(1+x)


"-----------------Definieren der Parameter für die Berechnungen--------------------"
# Brennstoffeigenschaften
yc, yh, yo, yn, ys = 0.51, 0.06, 0.43, 0, 0
gamma = ["C", yc, "H", yh, "O", yo, "N", yn, "S", ys]
w = 0.0849  # [kg wasser/ kg holz nass]
calc = wc.Wood("Holz",gamma,w)  # erstellen des Objekts, wird später für die Berechnung der Mindestluftmenge etc. benötigt
P_soll = [8,11,15] # [kW] Sollleistung, wird für die Berechnung des Brennstoffmassenstroms Verwendet

# Umgebungsbedingungen
T_amb = 298  # [°C]
p_amb = 0.9893  # [bar]
rel_hum = 0.4 # relative Luftfeuchtigkeit

# Definieren der Lambda-Range für die Berechnungen und den Plot
start_lam = 1
end_lam = 3
step = .1 # Auflösung

"------------------------------Berechnungen-------------------------------------"

# Initialisieren der Vektoren
length = int((end_lam-start_lam)/step)
height = len(P_soll)
lamda_vec = np.zeros((height,length))
x_o2_wet_vec = np.zeros((height,length))
Vdot_air_wet_vec = np.zeros((height,length))
Vdot_air_dry_vec = np.zeros((height,length))
n_venti_vec = np.zeros((height,length))
m_br_dry_vec = np.zeros(height)
# Berechne o2_wet und den Verbrennungsluftmassenstrom anhand von Lambda
for z,P in enumerate(P_soll):
    m_br_dry_vec[z] = P / (calc.Hu_tr() * 1e3) * 3600  # [kg/h]
    for i,lam in enumerate(np.arange(start_lam,end_lam,step)):
        lamda_vec[z,i]= lam
        x_o2_wet_vec[z,i] = calc.O2(lam)
        Vdot_air_dry_vec[z,i] = lam*calc.lmin_dry()*m_br_dry_vec[z]/1.2041 # [m3/h]
        Vdot_air_wet_vec[z,i] = V_air_wet(Vdot_air_dry_vec[z,i],T_amb,p_amb,rel_hum)
        n_venti_vec[z,i] = n_venti(Vdot_air_wet_vec[z,i])

"---------------------Plots-------------------------------------------------"
font_size = 15

for z in range(len(P_soll)):
    plt.figure(1)
    plt.plot(lamda_vec[z], x_o2_wet_vec[z] * 100, label = f"P: {P_soll[z]} kW")

    plt.figure(2)
    plt.plot(Vdot_air_wet_vec[z], x_o2_wet_vec[z] * 100, label = f"P: {P_soll[z]} kW")


    plt.figure(3)
    plt.plot(n_venti_vec[z], x_o2_wet_vec[z] * 100, label = f"P: {P_soll[z]} kW")

# dot = '\u0307'
# Vdot = "V"+dot
y_label = "x_$O_{2}$_wet [Vol %]"
plt.figure(1)
plt.xlabel("Lambda [-]", fontsize=font_size)
plt.ylabel(y_label, fontsize=font_size)
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.legend(fontsize=font_size)
plt.grid()
plt.tight_layout()

plt.figure(2)
plt.xlabel(r"$\dot{V}_{air-wet} \left[\frac{m^3}{h}\right]$", fontsize=font_size)
plt.ylabel(y_label, fontsize=font_size)
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.legend(fontsize=font_size)
plt.grid()
plt.tight_layout()

plt.figure(3)
plt.xlabel("Ventilatordrehzahl [%]", fontsize=font_size)
plt.ylabel(y_label, fontsize=font_size)
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.legend(fontsize=font_size)
plt.grid()
plt.tight_layout()


# plt.figure()
# plt.plot(lamda_vec,x_o2_wet_vec*100,'x')
# plt.xlabel("Lambda [-]",fontsize=font_size)
# plt.ylabel("x_O2_wet [Vol %]",fontsize=font_size)
# plt.xticks(fontsize=font_size)
# plt.yticks(fontsize=font_size)
# plt.grid()
#
# plt.figure()
# plt.plot(Vdot_air_wet_vec,x_o2_wet_vec*100,'x')
# plt.xlabel("V_dot_air [m3/h]",fontsize=font_size)
# plt.ylabel("x_O2_wet [Vol %]",fontsize=font_size)
# plt.xticks(fontsize=font_size)
# plt.yticks(fontsize=font_size)
# plt.grid()
#
# plt.figure()
# plt.plot(n_venti_vec,x_o2_wet_vec*100)
# plt.xlabel("Ventilatordrehzahl [%]",fontsize=font_size)
# plt.ylabel("x_O2_wet [Vol %]",fontsize=font_size)
# plt.xticks(fontsize=font_size)
# plt.yticks(fontsize=font_size)
# plt.grid()