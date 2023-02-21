# import pandas as pd
import numpy as np
# import cantera as ct
from datetime import datetime, date, time

def edit_silana_excel(file):
    file.columns = change_header_name(file.columns)
    file = file.drop(0)  # delete column 0, contains units
    file = file.reset_index(drop=True)  # reset index to 0
    file["time_abs"] = time_abs_fun(file.Uhrzeit)
    return file

def change_header_name(header):
    """
    header so bearbeiten, dass nur erster Teil verwendet wird
    Bsp.: Temp [°C] wird zu Temp
    so kann direkt mit den headers ohne [] gearbeitet werden

    Parameters
    ----------
    header = array mit allen namen die Verwendet werden sollen
    """
    names = np.empty(len(header), dtype=object)
    z = 0
    for i in header:
        if ' ' in i:
            temp = i.rsplit()
            names[z] = temp[0]
        else:
            names[z] = i  # header

        if "-" in i:
            tmp = i.replace("-", "_")
            names[z] = tmp

        z += 1
    return names

def time_abs_fun(Uhrzeit):
    start_time = datetime(202, 12, 8, Uhrzeit[0].hour, Uhrzeit[0].minute, Uhrzeit[0].second)  # Referenz erstellen, damit mit Time gerechnet werden kann. Mit datetime.time kann nicht gerechnet werden, da kein 0Punkt vorhanden. Dieser muss erstellt werden
    time_abs = np.zeros(len(Uhrzeit))
    for i in range(0, len(time_abs)):
        time_now = datetime(202, 12, 8, Uhrzeit[i].hour, Uhrzeit[i].minute
                            , Uhrzeit[i].second)
        time_abs[i] = np.timedelta64(time_now - start_time, "s").astype(int)
    return time_abs

def norm_values(x,M, x_O2_dry,O2_bezug):
    """
    Erzeugt norm Werte der Abgasanalyse
    Daten können über self.x_norm abgerufen werden

    Parameters
    ----------

    x: Array mit den Grössen, für welche die Normwerte berechnet werden sollen
    M: Array der Molaren Massen
    x_O2_dry: Array mit den Sauerstoffwerten

    Returns
    -------
    x_norm: Array der berechneten Normgrössen

    """
    p_norm = 101325  # [Pa]
    T_norm = 273.15  # [Ka]
    R = 8.314  # [J/(mol*K)]
    x_norm = []
    x_norm_i = np.zeros(len(x_O2_dry))

    def roh_norm(M):
        roh_norm = p_norm * M / (R * T_norm)
        return roh_norm

    def xi_norm(x_O2_dry, x_i, roh_norm_i,O2_bezug):

        x_norm = np.zeros(len(x_O2_dry))
        for i in range(len(x_O2_dry)):
            if x_O2_dry[i]< 19:
                x_norm[i] = x_i[i] * roh_norm_i * (21 - O2_bezug) \
                        / (21 - x_O2_dry[i]) * 1e-3  # [mg/Nm3]
            else:
                x_norm[i] = np.nan
        return x_norm

    for i,xi in enumerate(x):
        roh_norm_i = roh_norm(M[i])
        x_norm_i = xi_norm(x_O2_dry,xi,roh_norm_i,O2_bezug)
        x_norm.append(x_norm_i)

    return x_norm


def get_index_of_time(Uhrzeit,jahr,monat,tag,stunde,minute,sekunde):
    """
    Sucht in einem datetime typ den Index
    :return: index
    :param Uhrzeit: Array mit Uhrzeiten und Datum aus Silana
    :param jahr: Bsp. 2022
    :param tag:
    :param monat:
    :param stunde:
    :param minute:
    :param sekunde:
    """
    index = np.where(Uhrzeit == np.datetime64(datetime(jahr, monat, tag, stunde, minute, sekunde)))[0][0]

    return index



def delet_rows(self, header, start, end):
    """
    Werte von start bis ende werden gelöscht


    Parameters
    ----------
    header: Array aller Namen die verwendet werden sollen
    start:  Start der zu löschenden Daten, muss int sein
    ende:   End der zulöschenden Daten, muss int sein
    """

    z = 0
    self.df = self.df.drop(self.df.index[start:end])
    self.df = self.df.reset_index(drop=True)
    for i in header:
        # self.df[i] = self.df[i][start:end] # Überschreiben des Parameters i
        delattr(self, '{}'.format(i))
        setattr(self, '{}'.format(i), self.df[i])  # Überschreiben des Parameters i
        z += 1




    # def stat(self, header, start, end):
    #     """
    #     Aus T_Regler wird T_Regler_stat erzeugt
    #     enthält nur die stationären Werte
    #
    #     Parameters
    #     ----------
    #     header: Array aller Namen die verwendet werden sollen
    #     start:  Start Zeitpunkt des stationären Zustands
    #     ende:   Ende des Stationären Zustands
    #     """
    #     names = np.empty(len(header), dtype=object)
    #     z = 0
    #     for i in header:
    #         # locals() [i+'_norm'] = i[start:end]
    #         names[z] = i + '_stat'
    #         tmp = self.df[i][start:end]
    #         tmp = tmp.reset_index(drop=True)
    #
    #         setattr(self, '{}'.format(names[z]),
    #                 tmp)  # setattr(self,'{}'.format(names[z]),self.df[i][start:end]) # Tatsächliche Werte übergen und nciht nur Header
    #         z += 1



