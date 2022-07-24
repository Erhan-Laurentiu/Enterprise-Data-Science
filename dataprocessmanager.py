import numpy as np
import pandas as pd

from constantdata import VACCINATION_RAW_FILE_PATH,         \
                         CASES_DEATHS_RAW_FILE_PATH,        \
                         POPULATION_RAW_FILE_PATH,          \
                         PROCESSED_RELATIONAL_INTERMEDIARY, \
                         PROCESSED_RELATIONAL_FINAL 

from filter import calc_filtered_data, calc_doubling_rate


def createProcessedFile():

    print("DataProcessManager::createProcessedFile: Started Processing the Raw Data")
    
    df_vaccination = pd.read_csv(VACCINATION_RAW_FILE_PATH)

    df_vaccination = df_vaccination.loc[:,['date','location','people_fully_vaccinated']]

    df_cases_deaths = pd.read_csv(CASES_DEATHS_RAW_FILE_PATH)
    df_cases_deaths = df_cases_deaths.loc[:,['date','location','total_cases','total_deaths']]

    df_final = pd.merge(df_vaccination, df_cases_deaths, on=['date','location'], how='right')

    del(df_vaccination)
    del(df_cases_deaths)

    df_population = pd.read_csv(POPULATION_RAW_FILE_PATH)
    df_population = df_population.loc[:,['entity','population']]
    df_population = df_population.rename(columns={'entity':'location'});

    df_final = pd.merge(df_final, df_population, on='location', how='right')
    
    casesPerPop=(df_final.loc[:,'total_cases'].values)/(df_final.loc[:,'population'].values)
    df_final["total_cases_per_pop"] = casesPerPop.tolist()

    deathsPerPop=(df_final.loc[:,'total_deaths'].values)/(df_final.loc[:,'population'].values)
    df_final["total_deaths_per_pop"] = deathsPerPop.tolist()

    fullyVaccinatedPerPop=(df_final.loc[:,'people_fully_vaccinated'].values)/(df_final.loc[:,'population'].values)
    df_final["total_fully_vaccinated_per_pop"] = fullyVaccinatedPerPop.tolist()

    df_final = df_final.rename(columns={'location' : 'country'})
    df_final.insert(2, 'state', 'no')
    df_final = df_final.dropna(axis=0, subset=['date'])

    df_final['date']=df_final.date.astype('datetime64[ns]')

    df_final.to_csv(PROCESSED_RELATIONAL_INTERMEDIARY,sep=';',index=False)

    #Memory Cleaning Because the DataSets are quite large
    del(casesPerPop)
    del(deathsPerPop)
    del(fullyVaccinatedPerPop)
    del(df_population)
    del(df_final)

    print("DataProcessManager::createProcessedFile: Finished Processing the Raw Data")


def appendFilterData():

    print("DataProcessManager::appendFilterData: Started Processing the Filter Data")
    
    pd_JH_data=pd.read_csv(PROCESSED_RELATIONAL_INTERMEDIARY,sep=';',parse_dates=[0])
    pd_JH_data=pd_JH_data.sort_values('date',ascending=True).copy()
    pd_JH_data=pd_JH_data.rename(columns={'total_cases' : 'confirmed', 'total_cases_per_pop' : 'confirmed_per_pop'})

    pd_result_larg=calc_filtered_data(pd_JH_data)
    pd_result_larg=calc_doubling_rate(pd_result_larg)
    pd_result_larg=calc_doubling_rate(pd_result_larg,'confirmed_filtered')

    mask=pd_result_larg['confirmed']>100
    pd_result_larg['confirmed_filtered_DR']=pd_result_larg['confirmed_filtered_DR'].where(mask, other=np.NaN)
    pd_result_larg.to_csv(PROCESSED_RELATIONAL_FINAL,sep=';',index=False)

    #Memory Cleaning Because the DataSets are quite large
    del(mask)
    del(pd_JH_data)
    del(pd_result_larg)

    print("DataProcessManager::appendFilterData: Finished Processing the Filter Data")

def processAllData():
    print("DataProcessManager::processAllData: Data Started Being Processing")
    createProcessedFile()
    appendFilterData()
    print("DataProcessManager::processAllData: Data Finished Being Processing")