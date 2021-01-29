import matplotlib.pyplot as plt
from qutip import *
import numpy as np
from ParameterEstimation.control import grape_CramerRao

t = qload("time_span")
c = qload("controls")

plt.plot(t, c[0],label="x")
plt.plot(t, c[1],label="y")
plt.plot(t, c[2],label="z")
plt.title("controls of single parameter estimation")
plt.xlabel("time span")
plt.ylabel("controls")
plt.savefig("controls.png")

rho_initial = Qobj(np.array([[0.5, 0.5], [0.5, 0.5]]))

M0 = Qobj(0.5 * np.array([[1.0, 1.], [1., 1.]]))
M1 = Qobj(0.5 * np.array([[1.0, -1.], [-1., 1.]]))
M = [M0, M1]

times = np.linspace(0, 10, 100)

epsilon = 0.1

w = 1.
H0 = 0.5 * w * sigmaz()
dH = [0.5 * sigmaz()]

Lvec = [sigmam()]
gamma = [0.1]

Hc = [sigmax(), sigmay(), sigmaz()]

ctrlgrape = grape_CramerRao.control(H0, rho_initial, times, Lvec, gamma, dH, Hc, c, epsilon)
ctrlgrape.propagation_single()

def rrep(rho):
    return [rho[1][0]+rho[2][0],(rho[2][0]-rho[1][0])/(1.j),rho[0][0]-rho[3][0]]

r= [rrep(ctrlgrape.rho[i]) for i in range(len(t))]

xx = [r[i][0][0].real for i in range(len(t))]
yy = [r[i][1][0].real for i in range(len(t))]
zz = [r[i][2][0].real for i in range(len(t))]


b = Bloch()
b.vector_color = ['r']
b.view = [-40,30]
for i in range(len(t)):
    b.clear()
    b.add_points([xx,yy,zz])
    b.add_vectors([xx[i],yy[i],zz[i]])
    b.save(dirc='temp') #saving images to temp directory in current working directory

b.clear()
b.add_points([xx,yy,zz])
b.save()
