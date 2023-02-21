from Betriebspunkte.betriebspunkt_fett_04prozO2 import betriebspunkt_fett as fett
from Betriebspunkte.betriebspunkt_mager_12prozO2 import betriebspunkt_mager as mager
from functions_and_datacontainer.plots import *
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from functions_and_datacontainer.main_variables import *
from tabulate import tabulate
import matplotlib
matplotlib.use("Qt5Agg") #qtagg

color = "darkgreen"
plt.plot(mager.file.O2[mager.mager_start:mager.mager_stop],mager.file.CO[mager.mager_start:mager.mager_stop],
         "x",color = color,label = "mager")

fett.mager_start = fett.mager_start+2500
plt.plot(fett.file.O2[fett.mager_start:fett.mager_stop],fett.file.CO[fett.mager_start:fett.mager_stop],
         "x",color = color,label = "fett")

plt.plot(fett.file.O2[fett.opt_start:fett.opt_stop],fett.file.CO[fett.opt_start:fett.opt_stop],
         "x",color = color,label = "opt")
# plt.plot(mager.file.O2[mager.opt_start:mager.opt_stop],fett.file.CO[mager.opt_start:mager.opt_stop],
#          "x",label = "opt")
# plt.legend(fontsize=label_size)
plt.xlabel("O2 [Vol %]",fontsize=label_size)
plt.ylabel("CO [ppm]",fontsize=label_size)
plt.xticks(fontsize = tick_size)
plt.yticks(fontsize = tick_size)
plt.show()

