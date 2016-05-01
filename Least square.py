# -*- coding: utf-8 -*-
"""
Created on Sun May 01 23:22:44 2016

@author: aditya
"""
import math
import scipy
import numpy.random as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import statsmodels.stats.stattools as stools

t=scipy.array([0,10,20,30,40])
yexpt=scipy.array([40,30,25,20,15])

def function(a,d,t):
    ymodel=a*t*+d
    return ymodel
def residuals(p,yexpt,t):
    [a,d]=p
    
    m=yexpt-function(a,d,t)
    return m
p=[0,0]


soln1=leastsq(residuals,p,args=(yexpt,t))
print soln1[1]
    
       

    
    