# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 00:49:50 2016

@author: ACER
"""
import math
import scipy
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import statsmodels.stats.stattools as stools

#from uncertainties import unumpy
#from uncertainties import ufloat
import win32com.client


"""_____________________________________MARGULES MODEL________________________________________"""

#IMPORTING DATA FROM EXCEL
'''data=pd.read_excel("C:\Users\ACER\Desktop\Therm.xlrd","Sheet1") 
Ge=scipy.array(data["Ge"])
x=scipy.array(data["xb"])'''

xl= win32com.client.gencache.EnsureDispatch("Excel.Application")
wb=xl.Workbooks('Therm.xlsx')#.............work book Data,xlsx
sheet=wb.Sheets('Sheet1')#..................sheet Data
   
def getdata(sheet, Range):
    data= sheet.Range(Range).Value
    data=scipy.array(data)
    data=data.reshape((1,len(data)))[0]
    return data

Ge=getdata(sheet,"O4:O10")#..............importing data from excel
x1=getdata(sheet,"B4:B10")
x1x2=getdata(sheet,"T4:T10")
gb=getdata(sheet,"L4:L10")
gt=getdata(sheet,"M4:M10")
Gem=getdata(sheet,"Q4:Q10")
Gevl=getdata(sheet,"O16:O22")
VL=x1x2/Ge
T= 273.16+55


#DEFINING BASIC FUNCTIONS
def equation(x, A):
    return (A*x)

def residuals(p, y, x):
    A = p
    err = y-equation(x, A)
    return err

def peval(x, p):
    A = p
    return equation(x, A)
    
def equ(x, A, B):
     vl= x*(1-x)/(A+B*x)
     return (vl)
        
def residual(p, y, x):
    A,B = p
    err = y-equ(x, A, B)
    return err

def pevaluate(x, p, q):
    A = p
    B = q
    return equ(x, A, B)
    
def equations(x, A, B,C, D):
     nrtl= x*(1-x)*(A*B/(x+(1-x)*B)+C*D/((1-x)+x*D))
     return (nrtl)
        
def resi(p, y, x):
    A, B,C, D = p
    err = y-equations(x, A, B,C, D)
    return err

def pevaluates(x, p, q, r, s):
    A = p
    B = q
    C = r
    D = s
    return equations(x, A,B,C,D)

p0 = [1000]
I=10
while I>0:
    print (" 1. MARGULES MODEL")
    print (" 2. VAN LAAR MODEL")
    print (" 3. NRTL ")
    print (" 4. FOR A COMPARISION OF FITS")
    inp=input("Select the model to check the fit")
    if inp== 1:
        # Fit equation using least squares optimization
        sol1 = leastsq(residuals, p0, args=(Ge, x1x2))
        P1=sol1[0]
        flfit=P1[0]*x1x2
        
        pv=[0.005,-0.005]
        sol2 = leastsq(residual, pv, args=(Ge, x1)) 
        P2=sol2[0]
        flfi=equ(x1, P2[0], P2[1])
        '''
        plt.plot(x1x2 ,flfit,'r',x1x2,Ge,'b^',x1x2,Gem,'g')
        plt.title('Least square fit')
        plt.show()'''
        
        fig, ax = plt.subplots()
        
        ax.plot(x1, flfit, 'r', label='Margules fit')
        ax.plot(x1, Ge, 'b^', label='Experimental data')
        ax.plot(x1, flfi, 'g--', label='Van Laar fit')
        plt.title('Ge vs x for comparision1')
        # Now add the legend with some customizations.
        legend = ax.legend(loc='upper right', shadow=True)
        
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('large')
        
        for label in legend.get_lines():
            label.set_linewidth(1.5)  # the legend line width
        plt.show()
        popt=sol1[0]
        pcov=sol1[1]
        
        
        def error_fit(Xdata,popt,pcov):
            Y=popt[0]*Xdata
            dY=[]
            for i in xrange(len(popt)):
                p=popt[i]
                dp=abs(p)/1e6+1e-20
                popt[i]+=dp
                Yi=popt[0]*Xdata
                dy=(Yi-Y)/dp
                dY.append(dy)
                popt[i]-=dp
                dY=scipy.array(dY)
                A=scipy.dot(dY.T,pcov)
                B=scipy.dot(A,dY)
                sigma2=B.diagonal()
                mean_sigma2=scipy.mean(sigma2)
                M=len(Xdata)
                N=len(popt)
                avg_stddev_data=scipy.sqrt(M*mean_sigma2/N)
                sigma=scipy.sqrt(sigma2)
                return sigma
        
        sig1=error_fit(x1x2,P1,pcov)
        
        
        M=len(Ge)
        N=len(P1)
        
        Geavg=scipy.mean(Ge)
        
        squares=(flfit-Geavg)
        squaresT=(Ge-Geavg)
        residuals=(flfit-Ge)
        
        SSM=sum(squares**2)
        SSE=sum(residuals**2)
        SST=sum(squaresT**2)
        
        DFM=M-1
        DFE=M-N
        DFT=N
        
        MSM=SSM/DFM
        MSE=SSE/DFE
        MST=SST/DFT
        
        R2=SSM/SST
        R2_adj=1-(1-R2)*(M-1)/(M-N-1)
        print("-------------------------------------------------------------------------------------------")
        print("Result of F Test")
        print R2
        print R2_adj
        
        chisquared=sum(residuals**2)
        Dof=M-N
        chisquared_red=chisquared/Dof
        p_chi2=1-scipy.stats.chi2.cdf(chisquared,Dof)
        stderr_reg=scipy.sqrt(chisquared_red)
        chisquare=(p_chi2,chisquared,chisquared_red,Dof,R2,R2_adj)
        print("Chisquare Test Result")
        print chisquare
        
        
        w,p_shapiro=scipy.stats.shapiro(residuals)
        mean_res=scipy.mean(residuals)
        stddev_res=scipy.sqrt(scipy.var(residuals))
        t_res=mean_res/stddev_res
        p_res=1-scipy.stats.t.cdf(t_res,M-1)
        print("Result Of Shapiro Residuals Test")
        print p_res
         
        F=MSM/MSE
        p_F=1-scipy.stats.f.cdf(F,DFM,DFE)
        
        print("Result Of F Test On Residuals")
        
        dw=stools.durbin_watson(residuals)
        print("Durbin Watson")
        resanal=(p_shapiro,w,mean_res,p_res,F,p_F,dw)
        print dw
        print("-------------------------------------------------------------------------------------------")
        
        
        
        print "VALUE OF MARGULES COEFFICIENT"
        print P1
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (EXPERIMENTAL)"
        print Ge
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (FIT BY MODEL)"
        print flfit
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (FIT BY EXCEL)"
        print Gem
        print ""
        print "----------------------------------------------------------------------------------------------"
        I=-1
    if inp ==2:
        print "_________________________________VAN LAAR MODEL_______________________________________"    
        
            
        pv=[0.005,-0.005]
        
        # Fit equation using least squares optimization
        sol1 = leastsq(residual, pv, args=(Ge, x1)) 
        P1=sol1[0]
        flfit=equ(x1, P1[0], P1[1])
        flfi= []
        for x in range(0,1):
            
            flfi += [equ(x, P1[0], P1[1])]
            x=x+0.1
        print flfi
        i=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        plt.plot(i ,flfi ,'r',x1, Ge ,'b^')
        plt.title('Least-squares fit to data')
        plt.xlim([0,1])
        plt.show()
        popt = P1
        pcov = sol1[1]
        
        
        def error_fit(Xdata,popt,pcov):
            Y=popt[0]*Xdata
            dY=[]
            for i in xrange(len(popt)):
                p=popt[i]
                dp=abs(p)/1e6+1e-20
                popt[i]+=dp
                Yi=popt[0]*Xdata
                dy=(Yi-Y)/dp
                dY.append(dy)
                popt[i]-=dp
                dY=scipy.array(dY)
                A=scipy.dot(dY.T,pcov)
                B=scipy.dot(A,dY)
                sigma2=B.diagonal()
                mean_sigma2=scipy.mean(sigma2)
                M=len(Xdata)
                N=len(popt)
                avg_stddev_data=scipy.sqrt(M*mean_sigma2/N)
                sigma=scipy.sqrt(sigma2)
                return sigma
        
        sig1=error_fit(x1x2,P1,pcov)
        
        
        M=len(Ge)
        N=len(P1)
        
        Geavg=scipy.mean(Ge)
        
        squares=(flfit-Geavg)
        squaresT=(Ge-Geavg)
        residuals=(flfit-Ge)
        
        SSM=sum(squares**2)
        SSE=sum(residuals**2)
        SST=sum(squaresT**2)
        
        DFM=M-1
        DFE=M-N
        DFT=N-1
        
        MSM=SSM/DFM
        MSE=SSE/DFE
        MST=SST/DFT
        
        R2=SSM/SST
        R2_adj=1-(1-R2)*(M-1)/(M-N-1)
        print("-------------------------------------------------------------------------------------------")
        print("Result of F Test")
        print R2
        print R2_adj
        
        chisquared=sum(residuals**2)
        Dof=M-N
        chisquared_red=chisquared/Dof
        p_chi2=1-scipy.stats.chi2.cdf(chisquared,Dof)
        stderr_reg=scipy.sqrt(chisquared_red)
        chisquare=(p_chi2,chisquared,chisquared_red,Dof,R2,R2_adj)
        print("Chisquare Test Result")
        print chisquare
        
        
        w,p_shapiro=scipy.stats.shapiro(residuals)
        mean_res=scipy.mean(residuals)
        stddev_res=scipy.sqrt(scipy.var(residuals))
        t_res=mean_res/stddev_res
        p_res=1-scipy.stats.t.cdf(t_res,M-1)
        print("Result Of Shapiro Residuals Test")
        print p_res
         
        F=MSM/MSE
        p_F=1-scipy.stats.f.cdf(F,DFM,DFE)
        
        print("Result Of F Test On Residuals")
        
        dw=stools.durbin_watson(residuals)
        print("Durbin Watson")
        resanal=(p_shapiro,w,mean_res,p_res,F,p_F,dw)
        print dw
        print("-------------------------------------------------------------------------------------------")
        
        
        
        print "VALUE OF VAN LAAR COEFFICIENT"
        print P1
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (EXPERIMENTAL)"
        print Ge
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (FIT BY MODEL)"
        print flfit
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (FIT BY EXCEL)"
        print Gevl
        print "----------------------------------------------------------------------------------------------"
        I=-1
    if inp==3:
        print "_________________________________NON RANDOM TWO LIQUID THEORY MODEL_______________________________________"    
        
            
        pv=[0.005,-0.005, 0.005, 0.005]
        
        # Fit equation using least squares optimization
        sol1 = leastsq(resi, pv, args=(Ge, x1)) 
        P1=sol1[0]
        
        flfit=equations(x1, P1[0], P1[1], P1[2], P1[3])
        
        
        plt.plot(x1 ,flfit ,'r',x1, Ge ,'b^', )
        plt.title('Least-squares fit to data')
        plt.show()
        popt = P1
        pcov = sol1[1]
        
        
        def error_fit(Xdata,popt,pcov):
            Y=popt[0]*Xdata
            dY=[]
            for i in xrange(len(popt)):
                p=popt[i]
                dp=abs(p)/1e6+1e-20
                popt[i]+=dp
                Yi=popt[0]*Xdata
                dy=(Yi-Y)/dp
                dY.append(dy)
                popt[i]-=dp
                dY=scipy.array(dY)
                A=scipy.dot(dY.T,pcov)
                B=scipy.dot(A,dY)
                sigma2=B.diagonal()
                mean_sigma2=scipy.mean(sigma2)
                M=len(Xdata)
                N=len(popt)
                avg_stddev_data=scipy.sqrt(M*mean_sigma2/N)
                sigma=scipy.sqrt(sigma2)
                return sigma
        
        sig1=error_fit(x1x2,P1,pcov)
        
        
        M=len(Ge)
        N=len(P1)
        
        Geavg=scipy.mean(Ge)
        
        squares=(flfit-Geavg)
        squaresT=(Ge-Geavg)
        residuals=(flfit-Ge)
        
        SSM=sum(squares**2)
        SSE=sum(residuals**2)
        SST=sum(squaresT**2)
        
        DFM=M-1
        DFE=M-N
        DFT=N-1
        
        MSM=SSM/DFM
        MSE=SSE/DFE
        MST=SST/DFT
        
        R2=SSM/SST
        R2_adj=1-(1-R2)*(M-1)/(M-N-1)
        print("-------------------------------------------------------------------------------------------")
        print("Result of F Test")
        print R2
        print R2_adj
        
        chisquared=sum(residuals**2)
        Dof=M-N
        chisquared_red=chisquared/Dof
        p_chi2=1-scipy.stats.chi2.cdf(chisquared,Dof)
        stderr_reg=scipy.sqrt(chisquared_red)
        chisquare=(p_chi2,chisquared,chisquared_red,Dof,R2,R2_adj)
        print("Chisquare Test Result")
        print chisquare
        
        
        w,p_shapiro=scipy.stats.shapiro(residuals)
        mean_res=scipy.mean(residuals)
        stddev_res=scipy.sqrt(scipy.var(residuals))
        t_res=mean_res/stddev_res
        p_res=1-scipy.stats.t.cdf(t_res,M-1)
        print("Result Of Shapiro Residuals Test")
        print p_res
         
        F=MSM/MSE
        p_F=1-scipy.stats.f.cdf(F,DFM,DFE)
        
        print("Result Of F Test On Residuals")
        
        dw=stools.durbin_watson(residuals)
        print("Durbin Watson")
        resanal=(p_shapiro,w,mean_res,p_res,F,p_F,dw)
        print dw
        print("-------------------------------------------------------------------------------------------")
        
        
        
        print "VALUE OF NRTL BINARY INTERACTION COEFFICIENTS"
        print P1
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (EXPERIMENTAL)"
        print Ge
        print ""
        print "VALUES OF THE EXCESS GIBB'S FREE ENERGY (FIT BY MODEL)"
        print flfit
        print ""
        print "----------------------------------------------------------------------------------------------"
        I=-13
    
    

        