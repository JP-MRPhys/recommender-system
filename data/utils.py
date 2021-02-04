import pandas as pd

def getstockspn():

    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    colsNames={0: 'Symbol', 1: 'Security' , 2 : 'SEC filings', 3 : 'GICS Sector', 4 : 'GICS Sub Industry',
               5 : 'Headquarters Location', 6 : 'Date first added' , 7: 'CIK' , 8: 'Founded' }


    df=df.drop([0])  #first rown contains column names do just drop it
    df= df.rename(columns=colsNames)

    return df

def getstockfromiex():

    #extract all stock information from IEX top end points 

    return