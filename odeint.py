# -*- coding: utf-8 -*-
"""
Created on Sun May 01 21:38:31 2016

@author: aditya
"""
import numpy as np

import matplotlib.pyplot as plt
from scipy.integrate import odeint
k=0.5
def firstorder(Ca,t):
    dcadt=-k*Ca
    
    return dcadt
Ca0=49.44
t=np.linspace(0,10,100)
y= odeint (firstorder,Ca0,t)
print Ca0
print t
print y


plt.plot(t,y,'b-')
plt.ylabel('concentration')

plt.xlabel('time')
plt.title('conc vs time')


SECOND ORDER ODE
import numpy as np
from scipy import integrate

def solvr(Y, t):
    return [Y[1], -2 * Y[0]-Y[1]]
    
def main():
    a_t = np.arange(0, 25.0, 0.01)
    asol = integrate.odeint(solvr, [1, 0], a_t)
    print(asol)

if __name__ == '__main__':
    main()
def main():
    a_t = np.arange(0, 25.0, 0.01)
    asol = integrate.odeint(solvr, [1, 0], a_t)
    astack = np.c_[a_t, asol[:,0], asol[:, 1]]
    np.savetxt('approx.csv', astack, delimiter=',', header='t, y, yd', comments='')
    
    
approx <- read.csv('approx.csv')
>plot(y ~ t, data=approx, type='l')
    