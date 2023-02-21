import numpy as np

from functions_and_datacontainer import wood_combustion as wc
import pandas as pd
from CoolProp import CoolProp as cp
from functions_and_datacontainer.functions import var_exists


class Betriebspunkt(wc.Wood):

    def __init__(self,file,start,stop,name,gamma,w):
        super().__init__(name,gamma,w)
        self.start = start
        self.stop = stop
        self.start_datetime = file.Uhrzeit[start]
        self.stop_datetime = file.Uhrzeit.iloc[stop]
        self.P = file.P_Kessel[start:stop].mean()
        self.o2 = file.O2[start:stop].mean()
        self.o2_wet = self.O2(self.Lamb_O2_tr(self.o2/100))[0]*100
        self.lam_o2_aprox = 21/(21-self.o2)
        self.co2 = file.CO2[start:stop].mean()
        self.co = file.CO[start:stop].mean()
        # self.co_norm = file.CO_norm[start:stop].mean()
        self.NOx = file.NO[start:stop].mean()
        self.T_abgas = file.T_Abgas[start:stop].mean()
        self.T_vl = file.T_K_VL[start:stop].mean()
        self.T_rl = file.T_K_RL[start:stop].mean()
        self.V_prim = file.V_Prim[start:stop].mean()
        self.V_sek = file.V_Sek[start:stop].mean()
        self.V_tot = file.V_tot_corr[start:stop].mean()#self.V_sek+self.V_prim # [m3/h] gemessene Menge Verbrennungsluft
        self.V_tot_SI = self.V_tot/3600  # [m3/s]
        self.m_combust_air_meas = self.V_tot_SI * 1.2041 #  [kg/s]


        if "Temperature" in file and np.isnan(file.Temperature[start:stop].mean()) == False:
            self.T_amb = file.Temperature[start:stop].mean()
            self.p_amb = file.Atm_Druck[start:stop].mean() * 1e-3 #  Umgebungsdruck in [bar]
            self.psat = cp.PropsSI("P","T",self.T_amb+273.15,"Q",1,"water")*1e-5  # sättigungsdruck Wasser [bar]
            self.rel_feuchte = file.Rel_Feuchte[start:stop].mean()*1e-2 # relative feuchte [-]
        else:
            self.T_amb = 298-273 # [°C]
            self.p_amb = 0.9893  # [bar]
            self.psat = cp.PropsSI("P", "T", 298, "Q", 1, "water") * 1e-5  # sättigungsdruck Wasser bei 298 K [bar]
            print("warning: Umbgebungs-Druck und Temperatur wurden nicht gemessen! Die Werte wurden auf 0.98 bar und "
                  "25 °C gesetzt")
        self.x =0.622*0.4*self.psat/(self.p_amb-self.psat)
        self.m_combust_air_meas_dry = self.m_combust_air_meas/ (1+self.x)


    def set_mass_loss_parmeters(self,file,start_waage,stop_waage):
        """
        Berechnet den Massenverlust, Massenstrom trocken und nass und setzt die Variablen in self.
        :param start_waage:
        :param stop_waage:
        :param file:
        """
        self.dm_wet = file.Gewicht[start_waage] - file.Gewicht.iloc[stop_waage]
        self.dt = file.time_abs.iloc[stop_waage] - file.time_abs[start_waage]
        self.mdot_wet = self.dm_wet / self.dt  # [kg/s]
        self.dm_dry = self.dm_wet * (1 - self.w)  # [kg]
        self.mdot_dry = self.mdot_wet * (1 - self.w)  # [kg/s]
        self.lam_mass = self.m_combust_air_meas_dry/(self.lmin_dry()*self.mdot_dry)
        self.n_direkt = self.P*1e-3 / (self.mdot_wet * self.Hu_nass())
        self.V_tot_real = self.Lamb_O2_tr(self.o2 / 100)[0] * self.lmin_dry() * self.mdot_dry * 3600 / 1.2041  # [m3/h] Tatsächliche Menge Verbrennungsluft über Lambda O2 Bestimmt

    def n_indirekt_fun(self,cp_air,cp_water,cp_exhaust):
        dT = (self.T_abgas - self.T_amb)
        mue_v = 1 + self.lmin()
        # cp_v = 1.065  # [kJ/ (kg*K)]
        # cp_l = 1.0065  # [kJ/ (kg*K)]
        # cp_w = 1.873  # [kJ/ (kg*K)]
        qvv = (mue_v * cp_exhaust * dT + self.u * cp_water * dT + (
                    self.Lamb_O2_tr(self.o2 / 100)[0] - 1) * self.lmin() * cp_air * dT) * 1e-3  # [kJ]

        self.n_indirekt = 1 - (qvv / ((self.u + 1) * self.Hu_nass())) - 0.01


    def build_res_vek(self,betriebsart):
        column_names = ["Betriebspunkt","start [hh:mm:ss]","stopp [hh:mm:ss]","Leistung [kW]","n_direkt [-]",
                        "n_indirekt [-]","lambda_mass [-]","lamda_o2 [-]","lambda_o2_approx [-]","O2 [Vol %]","O2_wet [Vol %]",
                        "CO [mg/Nm3]","T_Abgas [°C]","T_V [°C]","T_Rl [°C]","V_tot_meas[m3/h]","V_tot_real[m3/h]"]
        res = [[betriebsart,self.start_datetime.time(),self.stop_datetime.time(),round(self.P,2),round(self.n_direkt,2),round(self.n_indirekt,2),
                round(self.lam_mass,2),round(self.Lamb_O2_tr(self.o2/100)[0],2),round(self.lam_o2_aprox,2),round(self.o2,2),round(self.o2_wet,2),round(self.co_norm,2),
                round(self.T_abgas,2),round(self.T_vl,2),round(self.T_rl,2),round(self.V_tot,2),round(self.V_tot_real,2)]]
        res_vek = pd.DataFrame(res, columns=column_names)
        return res_vek
