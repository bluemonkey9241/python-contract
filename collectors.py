#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
%This is the general equilibrium alternative to the Optimal Control
%model sketched in path2ss.m
%The problem is explained as:

%Collectors
%Max \sum_{t=1}^{\infty} \beta^{t} log(c_{t})
%s.t.
%s_{t}+(m_{t}^{d}-m_{t-1}) = w_{t}l_{t} 
%
%and
%
%c_{t} = s_{t}/q_{t}
%
%Where l_{t} = A*Fx(t) is labor dedicated
%to the production of output in parcels using Neiblock

%Output
%Total output is produced in a distant place. Its quantity y_{t} is
%determined by y_{t} = A min{l_{t}, alpha* k_{t}} in eq. y_{t}=Fx_{t}
%
%Whete l_{t} is given and the sequence of k is computed
%The exchage rate is defined as q_{1} = 100 pela/euro y q_{T} = 1 pela/euro """

import numpy as np
#import pylab as pl
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import timeit
from cpoCol import cpoCol

# Definición de parámetros del modelo
# Thechnology
A = 10
alpha = 0.9

# Preferences
beta = 0.96

# Adoption
T = 100
x = np.linspace(0,1,T)
mu = 0.3
sigma = 0.1
Fx = 100*((1/2)+ 1*np.sign(x-mu)/2 * (1-np.exp(-np.sqrt(2)/sigma *np.abs(x-mu))))
L = Fx[T-1]/A # Max number of workers

#Given total revaluation, we compute the initial value of the token in
#the ICO, and the end value.
q = np.zeros(T)
qinit = 100
q[0] = qinit
qr = 1.09 #Revaluation rate
cnt = 1-1/qr #Constant to guarrantee that q(T) = 1
for t in list(range(T-1)):
    q[t+1] = q[t]/qr+cnt

#Use technology to compute the wage of the collector
dif2qr = 0.05
r = (qr-dif2qr)*np.ones(T);
k = Fx/(A*alpha);
l = Fx/A;
w = (Fx-r*k)/l;

#Initial pela holdings
m0 = 0;

#Prepare to pass values to the Newton-Raphson algorithm
param = [beta, m0, T, L, w, l, q] #Parameters
crit = 1e-6 #Exit flag
maxit = 1000 #Max. num. of iterations
x0 = (0.8*w*l) #Seed for the algorith

#Check for performance
tic=timeit.default_timer()

def g(x):
    return cpoCol(x,param)

c = fsolve(g, x0,  xtol=1.e-06,)
toc=timeit.default_timer()
print("time=%f" % (toc - tic )) 

#Resultados
#Use the budget contraint to compute m_{t} given the guess
m = np.zeros(T)
qReturn = np.zeros(T-1)
m[0] = w[0]*l[0]+q[0]*w[0]*(L-l[0])+m0-q[0]*c[0]
for t in list(range(1,T)):
    m[t] = w[t]*l[t]+q[t]*w[t]*(L-l[t])+m[t-1]-q[t]*c[t]
    qReturn[t-1] = q[t-1]/q[t]

#plt.rc('text', usetex=True)
plt.figure(figsize=(8, 8))
plt.subplot(2, 2, 1)
plt.xlim(0,T)
#plt.xticks([0,50,100])
#plt.ylim(180,240)
#plt.yticks([180,200,220,240])
plt.plot(qReturn)
plt.plot((1/beta)*np.ones(T))
plt.title(r'Pelas appreciation rate (blue) and $1/\beta$ (orange)')

plt.subplot(2, 2, 2)
plt.xlim(0,T)
#plt.xticks([0,50,100])
#plt.ylim(62,68)
#plt.yticks([62,64,66,68])
plt.plot(q)
plt.title('Exchange rate')

plt.subplot(2, 2, 3)
plt.xlim(0,T)
#plt.xticks([0,50,100])
#plt.ylim(13,17)
#plt.yticks([13,14,15,16,17])
plt.plot(c[0:T-2])
plt.title(r'Consumption')

plt.subplot(2, 2, 4)
plt.xlim(0,T)
#plt.xticks([0,50,100])
#plt.ylim(45,55)
#plt.yticks([45,50,55])
plt.plot(m)
plt.title('Pela ($\wp$) holdings')

plt.show()
