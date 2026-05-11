import numpy as np
import matplotlib.pyplot as plt

dt = 1.0
time = np.arange(0, 10, dt)
mass = 40000      
g = 9.81
rho = 1.225
Cd = 0.6
A = 10.0
Cr = 0.006
theta = 0.03        
SOC_min = 0.3
SOC_max = 0.8
SOC_target = 0.6
SOC = 0.6
Ebat = 50 * 3.6e6   
eta_bat = 0.95
P_FC_max = 150e3   
eta_FC = 0.55
LHV_H2 = 120e6      
acceleration = 0.8 
v0 = 0.0

speeds = []
SOC_list = []
Pbat_list = []
Pfc_list = []
H2_list = []

v = v0
H2_total = 0

for t in time:

    v = v + acceleration * dt
    speeds.append(v)
    F_aero = 0.5 * rho * Cd * A * v**2
    F_roll = Cr * mass * g
    F_grade = mass * g * np.sin(theta)
    F_total = F_aero + F_roll + F_grade
    P_demand = F_total * v

    if SOC < SOC_target:
        P_FC = min(P_demand, P_FC_max)
    else:
        P_FC = 0.7 * P_demand

    P_bat = P_demand - P_FC
    SOC = SOC - (P_bat * dt) / (Ebat * eta_bat)
    SOC = max(SOC_min, min(SOC, SOC_max))
    H2 = (P_FC * dt) / (eta_FC * LHV_H2)
    H2_total += H2

    SOC_list.append(SOC)
    Pbat_list.append(P_bat)
    Pfc_list.append(P_FC)
    H2_list.append(H2_total)

plt.scatter(time, speeds)
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title("Speed vs Time")
plt.grid(True)
plt.show()

plt.scatter(time, SOC_list)
plt.xlabel("Time (s)")
plt.ylabel("SOC")
plt.title("SOC vs Time")
plt.grid(True)
plt.show()

plt.scatter(time, Pfc_list, label="Fuel Cell Power")
plt.scatter(time, Pbat_list, label="Battery Power")
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.title("Power vs Time")
plt.legend()
plt.grid(True)
plt.show()

plt.scatter(time, H2_list)
plt.xlabel("Time (s)")
plt.ylabel("Hydrogen Consumption (kg)")
plt.title("Cumulative Hydrogen Consumption")
plt.grid(True)
plt.show()
