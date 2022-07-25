import numpy as np
import pandas as pd

from filter import calc_filtered_data, calc_doubling_rate
from sir import createSIRInitialFile, createSIRProcessedFile

from constantdata import *



def createProcessedFile():

    print("DataProcessManager::createProcessedFile: Started Processing the Raw Data")
    
    df_vaccination = pd.read_csv(VACCINATION_RAW_FILE_PATH)

    df_vaccination = df_vaccination.loc[:,[DATE_KEY,LOCATION_KEY,FULLY_VACCINATED_KEY]]

    df_cases_deaths = pd.read_csv(CASES_DEATHS_RAW_FILE_PATH)
    df_cases_deaths = df_cases_deaths.loc[:,[DATE_KEY,LOCATION_KEY,'total_cases',DEATHS_KEY]]

    df_final = pd.merge(df_vaccination, df_cases_deaths, on=[DATE_KEY,LOCATION_KEY], how='right')

    df_population = pd.read_csv(POPULATION_RAW_FILE_PATH)
    df_population = df_population.loc[:,['entity',POPULATION_KEY]]
    df_population = df_population.rename(columns={'entity':LOCATION_KEY});

    df_final = pd.merge(df_final, df_population, on=LOCATION_KEY, how='right')
    
    casesPerPop=(df_final.loc[:,'total_cases'].values)/(df_final.loc[:,POPULATION_KEY].values)
    df_final["total_cases_per_pop"] = casesPerPop.tolist()

    deathsPerPop=(df_final.loc[:,DEATHS_KEY].values)/(df_final.loc[:,POPULATION_KEY].values)
    df_final[DEATHS_POP_KEY] = deathsPerPop.tolist()

    fullyVaccinatedPerPop=(df_final.loc[:,FULLY_VACCINATED_KEY].values)/(df_final.loc[:,POPULATION_KEY].values)
    df_final[FULLY_VACCINATED_POP_KEY] = fullyVaccinatedPerPop.tolist()

    df_final = df_final.rename(columns={LOCATION_KEY : COUNTRY_KEY})
    df_final.insert(2, 'state', 'no')
    df_final = df_final.dropna(axis=0, subset=[DATE_KEY])

    df_final[DATE_KEY]=df_final.date.astype('datetime64[ns]')

    df_final.to_csv(PROCESSED_RELATIONAL_INTERMEDIARY_FILE_PATH,sep=';',index=False)

    print("DataProcessManager::createProcessedFile: Finished Processing the Raw Data")


def appendFilterData():

    print("DataProcessManager::appendFilterData: Started Processing the Filter Data")
    
    pd_JH_data=pd.read_csv(PROCESSED_RELATIONAL_INTERMEDIARY_FILE_PATH,sep=';',parse_dates=[0])
    pd_JH_data=pd_JH_data.sort_values(DATE_KEY,ascending=True).copy()
    pd_JH_data=pd_JH_data.rename(columns={'total_cases' : CASES_KEY, 'total_cases_per_pop' : CASES_POP_KEY})

    pd_result_larg=calc_filtered_data(pd_JH_data)
    pd_result_larg=calc_doubling_rate(pd_result_larg)
    pd_result_larg=calc_doubling_rate(pd_result_larg, CASES_FILTERED_KEY)

    mask=pd_result_larg[CASES_KEY]>100
    pd_result_larg[CASES_FILTERED_DR_KEY]=pd_result_larg[CASES_FILTERED_DR_KEY].where(mask, other=np.NaN)
    pd_result_larg.to_csv(PROCESSED_RELATIONAL_FINAL_FILE_PATH,sep=';',index=False)

    print("DataProcessManager::appendFilterData: Finished Processing the Filter Data")


def processAllData():
    
    print("DataProcessManager::processAllData: Data Started Being Processing")

    createProcessedFile()
    appendFilterData()
    createSIRInitialFile()
    createSIRProcessedFile()

    print("DataProcessManager::processAllData: Data Finished Being Processing")
