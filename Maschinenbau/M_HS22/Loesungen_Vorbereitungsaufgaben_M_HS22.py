from functions_and_datacontainer import wood_combustion as wc

M_C = 12.0001
M_O = 15.999
M_N = 14.007
M_H = 1.008
M_S = 32.08

yc, yh, yo, yn, ys = 0.508, 0.059, 0.432, 0.001, 0
x = yc/M_C+yh/M_H+yo/M_O+yn/M_N+ys/M_S
xc,xh,xo,xn,xs = yc/M_C/x,yh/M_H/x,yo/M_O/x,yn/M_N/x,ys/M_S/x
M_B = xc*M_C+xh*M_H+xo*M_O+xn*M_N+xs*M_S
gamma = ["C", yc, "H", yh, "O", yo, "N", yn, "S", ys]
w = (3.181-2.949)/3.181  # [kg wasser/ kg holz nass]
lam_soll = 1.4 # sollwert des lambda
P_soll = 11
Hu_dry = 18.7
pellet = wc.Wood("Holz",gamma,w,Hu_dry=Hu_dry)
Hu_nass = Hu_dry*(1-w)-2.443*w
omin = 2.664*yc+7.937*yh+0.998*ys-yo
lmin = omin/0.2314
a = (2*xc+0.5*xh+2*xs-xo)/2
b = xc
g = pellet.u*M_B/(2*M_H+M_O)
c = 0.5*xh+g
d = xs
e = a*3.73
f = 0.5*xn
x_o2_tr = (lam_soll-1)*a/(b+d+(lam_soll*e+f)+(lam_soll-1)*a)*100
x_o2_nass = (lam_soll-1)*a/(b+c+d+(lam_soll*e+f)+(lam_soll-1)*a)*100
m_br_dry = P_soll/(Hu_dry*1e3)*3600 # [kg/h]
V_luft_soll = m_br_dry*lmin*lam_soll/1.2041 # [m3/h]