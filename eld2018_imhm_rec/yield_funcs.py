import sys
sys.path.append(r"C:\Users\ionac\Documents\python\eld2018\Elderfield2018Model\eld2018_imhm_rec")

from scipy import integrate
from params_funcs import *
import numpy as np

def elderfieldOdeSystem_df(time,X):
    S_df, R_df = X
    dS_df = plantGrowth(time,S_df) - plantSenescence(time)*S_df
    dR_df = plantSenescence(time)*S_df
    return np.array([dS_df, dR_df])

def calcYield_df(time):
    # integrating up until the start of the time
    y0_df = S0,R0 # starting conditions
    time_df_chunk1 = [1,time[0]]
    soln_df_chunk1 = integrate.solve_ivp(fun = elderfieldOdeSystem_df, y0 = y0_df, t_span = time_df_chunk1, t_eval = np.arange(time_df_chunk1[0],time_df_chunk1[1],1))
    y_df_chunk1 = soln_df_chunk1.y
    S_df_chunk1,R_df_chunk1 = y_df_chunk1
    
    # integrating the part we are calculating
    y0_df_chunk2 = S_df_chunk1[-1],R_df_chunk1[-1]
    time_df_chunk2 = [time[0],time[1]]
    soln_df_chunk2 = integrate.solve_ivp(fun = elderfieldOdeSystem_df, y0 = y0_df_chunk2, t_span = time_df_chunk2, t_eval = np.arange(time_df_chunk2[0],time_df_chunk2[1],1))
    y_df_chunk2 = soln_df_chunk2.y
    S_df_chunk2,R_df_chunk2 = y_df_chunk2
    
    # # calulating yield over time frame
    t_df_chunk2 = soln_df_chunk2.t
    dt = np.diff(t_df_chunk2)
    yield_df = np.sum(S_df_chunk2[:-1] * dt)  # Discrete integration
    
    return yield_df

def calcLifetimeYield(percYield_arr, totalYield_arr, dfYield):
    tY_sum = 0
    for i in np.arange(0,len(percYield_arr),1):
        if percYield_arr[i] >= 95:
            tY_sum += totalYield_arr[i]
    ltY = tY_sum / dfYield # defining lifetime yield in terms of multiples of df yield
    return ltY
            