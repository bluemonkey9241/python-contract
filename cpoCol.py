# Using the magic encoding
# -*- coding: utf-8 -*-

# función cpoCol(x0,param)
import numpy as np

def cpoCol(x0,param):
    beta = param[0]
    m0 = param[1]
    T = param[2]
    L = param[3]
    w = param[4]
    l = param[5]
    q = param[6]
    
    #Pass the seed
    c = x0

    #Inicialización de variables
    m = np.zeros(T)
    f =  np.zeros(T) 
    
    #Use the budget contraint to compute m_{t} given the guess
    m[0] = w[0]*l[0]+q[0]*w[0]*(L-l[0])+m0-q[0]*c[0]
    for t in list(range(1,T)):
        m[t] = w[t]*l[t]+m[t-1]-q[t]*c[t]
    
    #Ecuación de Euler        
    for t in list(range(T-1)):
        f[t] = q[t]/q[t+1]-c[t+1]/(beta*c[t])
        f[T-1] = m[T-1]-m[T-2]
    return f
