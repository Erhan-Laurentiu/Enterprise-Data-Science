from cmath import nan
from curses import newpad
import pandas as pd
import numpy as np
from datetime import datetime

from paths import *

populationDict = {}

def createPopulationFile():
    dataFrame = pd.read_csv(POPULATION_RAW_FILE_PATH)
    countryList = dataFrame['entity']
    populationList = dataFrame['population']

    pd.DataFrame(
        {
            'Country'   :countryList,
            'Population':populationList
        }
        ).to_csv(POPULATION_PROCESSED_FILE_PATH, sep=';')

    global populationDict
    populationDict = dict(zip(countryList, populationList))
    
    # print(populationDict)

def createVaccinationFile():
    dataFrame = pd.read_csv(VACCINATION_RAW_FILE_PATH)

    di = (dataFrame.groupby('location')['date','people_vaccinated']
        .apply(lambda x: dict(zip(range(len(x)),x.values.tolist())))
        .to_dict())

    listOfDf = []
    listOfDfWithPopulation = []

    for eachCountry in di:
        dateList = []
        valuesList = []
        countryName = eachCountry
        if countryName not in populationDict:
            continue
        countryPopulation = populationDict[eachCountry]
        # print(countryPopulation)
        for i in range(len(di[eachCountry])):
            dateList.append(di[eachCountry][i][0])
            valuesList.append(di[eachCountry][i][1])

        listOfDf.append( pd.DataFrame(
        {
            'Date'      :      dateList,
             countryName:      valuesList
        }))
        
        listOfDfWithPopulation.append( pd.DataFrame(
        {
            'Date'      :       dateList,
             countryName:       100*np.array(valuesList)/countryPopulation #percentage of population vaccinated
        }))

        dateList.clear()
        valuesList.clear()
        

    pd.concat(listOfDf,                 axis=0, ignore_index=True).to_csv(VACCINATION_PROCESSED_FILE_PATH,     sep = ';')
    pd.concat(listOfDfWithPopulation,   axis=0, ignore_index=True).to_csv(VACCINATION_POP_PROCESSED_FILE_PATH, sep = ';')

  
def createCasesDeathsFiles():
    dataFrame = pd.read_csv(CASES_DEATHS_RAW_FILE_PATH)
    di = (dataFrame.groupby('location')['date', 'total_cases', 'total_deaths']
    .apply(lambda x: dict(zip(range(len(x)),x.values.tolist())))
    .to_dict())

    listOfCasesDf = []
    listOfCasesDfWithPopulation = []
    listOfDeathsDf = []
    listOfDeathsDfWithPopulation = []
    

    for eachCountry in di:
        dateList = []
        casesList = []
        deathsList = []
        
        countryName = eachCountry
        if countryName not in populationDict:
            #skip countries that don't have the population provided in this data set
            continue
        countryPopulation = populationDict[eachCountry]
        # print(countryPopulation)
        for i in range(len(di[eachCountry])):
            dateList.append(di[eachCountry][i][0])
            casesList.append(di[eachCountry][i][1])
            deathsList.append(di[eachCountry][i][1])

        listOfCasesDf.append( pd.DataFrame(
        {
            'Date'      :   dateList,
            countryName :   casesList
        }))
        
        listOfCasesDfWithPopulation.append( pd.DataFrame(
        {
            'Date'      :   dateList,
            countryName :   np.array(casesList)/countryPopulation #percentage of population vaccinated
        }))

        listOfDeathsDf.append( pd.DataFrame(
        {
            'Date'      :   dateList,
            countryName :   deathsList
        }))
        
        listOfDeathsDfWithPopulation.append( pd.DataFrame(
        {
            'Date'      :   dateList,
            countryName :   np.array(deathsList)/countryPopulation #percentage of population vaccinated
        }))

        dateList.clear()
        casesList.clear()
        deathsList.clear()
    
    
    pd.concat(listOfCasesDf,                axis=0, ignore_index=True).to_csv(CASES_PROCESSED_FILE_PATH,        sep = ';')
    pd.concat(listOfCasesDfWithPopulation,  axis=0, ignore_index=True).to_csv(CASES_POP_PROCESSED_FILE_PATH,    sep = ';')
    pd.concat(listOfDeathsDf,               axis=0, ignore_index=True).to_csv(DEATHS_PROCESSED_FILE_PATH,       sep = ';')
    pd.concat(listOfDeathsDfWithPopulation, axis=0, ignore_index=True).to_csv(DEATHS_POP_PROCESSED_FILE_PATH,   sep = ';')

def processAllData():
    createPopulationFile()
    createVaccinationFile()
    createCasesDeathsFiles()