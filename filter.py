import numpy as np
from sklearn import linear_model
reg = linear_model.LinearRegression(fit_intercept=True)
import pandas as pd
from paths import *

from scipy import signal

def get_doubling_time_via_regression(in_array):
    ''' Use a linear regression to approximate the doubling rate

        Parameters:
        ----------
        in_array : pandas.series

        Returns:
        ----------
        Doubling rate: double
    '''

    y = np.array(in_array)
    X = np.arange(-1,2).reshape(-1, 1)

    assert len(in_array)==3
    reg.fit(X,y)
    intercept=reg.intercept_
    slope=reg.coef_

    return intercept/slope


def savgol_filter(df_input,column='confirmed',window=5):
    ''' Savgol Filter which can be used in groupby apply function (data structure kept)

        parameters:
        ----------
        df_input : pandas.series
        column : str
        window : int
            used data points to calculate the filter result

        Returns:
        ----------
        df_result: pd.DataFrame
            the index of the df_input has to be preserved in result
    '''

    degree=1
    df_result=df_input

    filter_in=df_input[column].fillna(0) # attention with the neutral element here

    result=signal.savgol_filter(np.array(filter_in),
                           window, # window size used for filtering
                           1)
    df_result[str(column+'_filtered')]=result
    return df_result

def rolling_reg(df_input,col='confirmed'):
    ''' Rolling Regression to approximate the doubling time'

        Parameters:
        ----------
        df_input: pd.DataFrame
        col: str
            defines the used column
        Returns:
        ----------
        result: pd.DataFrame
    '''
    days_back=3
    result=df_input[col].rolling(
                window=days_back,
                min_periods=days_back).apply(get_doubling_time_via_regression,raw=False)



    return result




def calc_filtered_data(df_input,filter_on='confirmed'):
    '''  Calculate savgol filter and return merged data frame

        Parameters:
        ----------
        df_input: pd.DataFrame
        filter_on: str
            defines the used column
        Returns:
        ----------
        df_output: pd.DataFrame
            the result will be joined as a new column on the input data frame
    '''

    must_contain=set(['state','country',filter_on])
    assert must_contain.issubset(set(df_input.columns)), ' Erro in calc_filtered_data not all columns in data frame'

    df_output=df_input.copy() # we need a copy here otherwise the filter_on column will be overwritten

    pd_filtered_result=df_output[['state','country',filter_on]].groupby(['state','country']).apply(savgol_filter)#.reset_index()

    #print('--+++ after group by apply')
    #print(pd_filtered_result[pd_filtered_result['country']=='Germany'].tail())

    #df_output=pd.merge(df_output,pd_filtered_result[['index',str(filter_on+'_filtered')]],on=['index'],how='left')
    df_output=pd.merge(df_output,pd_filtered_result[[str(filter_on+'_filtered')]],left_index=True,right_index=True,how='left')
    #print(df_output[df_output['country']=='Germany'].tail())
    return df_output.copy()





def calc_doubling_rate(df_input,filter_on='confirmed'):
    ''' Calculate approximated doubling rate and return merged data frame

        Parameters:
        ----------
        df_input: pd.DataFrame
        filter_on: str
            defines the used column
        Returns:
        ----------
        df_output: pd.DataFrame
            the result will be joined as a new column on the input data frame
    '''

    must_contain=set(['state','country',filter_on])
    assert must_contain.issubset(set(df_input.columns)), ' Erro in calc_filtered_data not all columns in data frame'


    pd_DR_result= df_input.groupby(['state','country']).apply(rolling_reg,filter_on).reset_index()

    pd_DR_result=pd_DR_result.rename(columns={filter_on:filter_on+'_DR',
                             'level_2':'index'})

    #we do the merge on the index of our big table and on the index column after groupby
    df_output=pd.merge(df_input,pd_DR_result[['index',str(filter_on+'_DR')]],left_index=True,right_on=['index'],how='left')
    df_output=df_output.drop(columns=['index'])


    return df_output

def convertToDesiredFormat():
    pd_raw=pd.read_csv(CASES_PROCESSED_FILE_PATH, sep=';')

    countryListInOrder = list(pd_raw.columns)
    countryListInOrder.remove('date')
    countryListInOrder.remove('Unnamed: 0')
    dateList = pd_raw['date'].tolist()
    numberOfRows = len(dateList)

    bigListWithoutColumnNames =[]


    for x in range(0,numberOfRows):
        for countryName in countryListInOrder:
            bigListWithoutColumnNames.append([dateList[x], np.nan, countryName, pd_raw[countryName][x]])
            # bigListWithoutColumnNames.append([dateList[x], countryName, pd_raw[countryName][x]])

    df=pd.DataFrame(bigListWithoutColumnNames, columns=['date', 'state','country','confirmed'])
    df['state']=df['state'].fillna('no')
    # df=pd.DataFrame(bigListWithoutColumnNames, columns=['date','country','confirmed'])
    # df.set_index(['state','country'])
    # df.stack(level=[0,1]).reset_index()
    df.to_csv(CASES_INTERMEDIARY_FILE_PATH,sep=';',index=False)




def createUIFiles():
    dataFrame = pd.read_csv(CASES_FILTERING_PROCESSED_FILE_PATH, sep=';', index_col=False)
    di = (dataFrame.groupby('country')['date', 'confirmed_filtered', 'confirmed_DR', 'confirmed_filtered_DR']
    .apply(lambda x: dict(zip(range(len(x)),x.values.tolist())))
    .to_dict())

    listOfFiltered = []
    listOfDR = []
    listOfFilteredDR = []
    

    for eachCountry in di:
        dateList = []
        filteredList = []
        drList = []
        drFilteredList = []

        countryName = eachCountry

        for i in range(len(di[eachCountry])):
            dateList.append(di[eachCountry][i][0])
            filteredList.append(di[eachCountry][i][1])
            drList.append(di[eachCountry][i][2])
            drFilteredList.append(di[eachCountry][i][3])

        listOfFiltered.append( pd.DataFrame(
        {
            'date'      :   dateList,
            countryName :   filteredList
        }))
        
        listOfDR.append( pd.DataFrame(
        {
            'date'      :   dateList,
            countryName :   drList
        }))

        listOfFilteredDR.append( pd.DataFrame(
        {
            'date'      :   dateList,
            countryName :   drFilteredList
        }))
        

        dateList.clear()
        filteredList.clear()
        drList.clear()
        drFilteredList.clear()
    
    pd.concat(listOfFiltered,                axis=0, ignore_index=True).to_csv(CASES_FILTERED_PROCESSED_FILE_PATH,        sep = ';')
    pd.concat(listOfDR,                      axis=0, ignore_index=True).to_csv(CASES_DR_PROCESSED_FILE_PATH,    sep = ';')
    pd.concat(listOfFilteredDR,              axis=0, ignore_index=True).to_csv(CASES_FILTERED_DR_PROCESSED_FILE_PATH,       sep = ';')
   

def filterData():
    
    convertToDesiredFormat()
    pd_JH_data=pd.read_csv(CASES_INTERMEDIARY_FILE_PATH,sep=';',parse_dates=[0])
    pd_JH_data=pd_JH_data.sort_values('date',ascending=True).copy()
    pd_result_larg=calc_filtered_data(pd_JH_data)
    pd_result_larg=calc_doubling_rate(pd_result_larg)
    pd_result_larg=calc_doubling_rate(pd_result_larg,'confirmed_filtered')
    mask=pd_result_larg['confirmed']>100
    pd_result_larg['confirmed_filtered_DR']=pd_result_larg['confirmed_filtered_DR'].where(mask, other=np.NaN)
    pd_result_larg.to_csv(CASES_FILTERING_PROCESSED_FILE_PATH,sep=';',index=False)
    createUIFiles()
