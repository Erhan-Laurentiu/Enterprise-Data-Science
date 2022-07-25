import pandas as pd
import numpy as np
from scipy import optimize
from scipy import integrate

from constantdata import CASES_DEATHS_RAW_FILE_PATH, \
                        POPULATION_RAW_FILE_PATH,    \
                        SIR_FINAL_FILE_PATH,         \
                        SIR_INTERMEDIARY_FILE_PATH



################################################################
################################################################
######## Helper SIR Functions for DataProcessManager.py ########
################################################################
################################################################


N0 = 0
S0 = 0
I0 = 0
R0 = 0
t = 0


def SIR_model_t(SIR,t,beta,gamma):
    ''' Simple SIR model
        S: susceptible population
        t: time step, mandatory for integral.odeint
        I: infected people
        R: recovered people
        beta: 
        
        overall condition is that the sum of changes (differnces) sum up to 0
        dS+dI+dR=0
        S+I+R= N (constant size of population)
    
    '''
    global N0

    S,I,R=SIR
    dS_dt=-beta*S*I/N0          
    dI_dt=beta*S*I/N0-gamma*I
    dR_dt=gamma*I
    return dS_dt,dI_dt,dR_dt


def fit_odeint(x, beta, gamma):
    '''
    helper function for the integration
    '''
    global S0,I0,R0,t

    return integrate.odeint(SIR_model_t, (S0, I0, R0), t, args=(beta, gamma))[:,1] # we only would like to get dI


def createSIRInitialFile():

    print("SIR::createSIRInitialFile: Started Processing the Intermediary SIR File")

    dataFrame = pd.read_csv(CASES_DEATHS_RAW_FILE_PATH)
    di = (dataFrame.groupby('location')['date', 'total_cases']
    .apply(lambda x: dict(zip(range(len(x)), x.values.tolist())))
    .to_dict())

    df_final = list(dict.fromkeys(dataFrame['date'].tolist()));
    df_final = pd.DataFrame(df_final, columns=['date']).sort_values('date')

    for eachCountry in di:
        each_df = pd.DataFrame.from_dict(di)[eachCountry]
        each_df = each_df[each_df.notna()]
        each_df = pd.DataFrame(each_df.to_list(), columns=['date', eachCountry])
        df_final = pd.merge(df_final, each_df, on='date', how='left')

    df_final.to_csv(SIR_INTERMEDIARY_FILE_PATH, sep = ';', index=False)

    print("SIR::createSIRInitialFile: Finished Processing the Intermediary SIR File")


def createSIRProcessedFile():

    print("SIR::createSIRInitialFile: Started Processing the SIR")

    global S0,I0,R0,N0,t

    df_population = pd.read_csv(POPULATION_RAW_FILE_PATH)
    countryList = df_population['entity']
    populationList = df_population['population'] 
    populationDict = dict(zip(countryList, populationList))

    df_analyse=pd.read_csv(SIR_INTERMEDIARY_FILE_PATH,sep=';', parse_dates=[0])
    ydata = np.array(df_analyse['date'][40::])
    t=np.arange(len(ydata))

    df_final = pd.DataFrame(t, columns=['t'])

    for each in df_analyse:
        if each == 'date' or not(each in populationDict):
            continue

        d = {('t'): np.arange(len(np.array(df_analyse[each][40::]))), 
        ('ydata') : np.array(df_analyse[each][40::])}
        each_df = pd.DataFrame.from_dict(d)
        each_df = each_df.dropna(axis=0, subset=['ydata'])

        ydata = np.array(each_df['ydata'])
        t=np.arange(len(ydata))

        N0 = populationDict[each]*0.125 #we consider 12.5% of population
        I0=ydata[0]
        S0=N0-I0
        R0=0

        try:
            popt, pcov = optimize.curve_fit(fit_odeint, t, ydata)
        except RuntimeError:
            #some of the optimize.curve_fit are not solvable so we skip them
            continue

        perr = np.sqrt(np.diag(pcov))
        fitted=fit_odeint(t, *popt)

        d = {('t'):t, 
            (each+'_ydata_opt1') : ydata, 
            (each+'_fitted_opt1') : np.cumsum(fitted), 
            (each+'_ydata_opt2') : np.ediff1d(ydata, to_begin=ydata[1]-ydata[0]), 
            (each+'_fitted_opt2') : fitted}
        each_df = pd.DataFrame.from_dict(d)

        df_final = pd.merge(df_final,each_df, on='t', how='left')

    df_final.to_csv(SIR_FINAL_FILE_PATH, sep = ';', index=False)

    print("SIR::createSIRInitialFile: Finished Processing the SIR")
