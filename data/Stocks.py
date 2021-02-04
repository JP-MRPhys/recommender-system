import pandas as pd

#TODO: load all this from a config file


def getstockinfo():

    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    colsNames={0: 'Symbol', 1: 'Security' , 2 : 'SEC filings', 3 : 'GICS Sector', 4 : 'GICS Sub Industry',
               5 : 'Headquarters Location', 6 : 'Date first added' , 7: 'CIK' , 8: 'Founded' }


    df=df.drop([0])  #first rown contains column names do just drop it
    df= df.rename(columns=colsNames)

    return df


if __name__ == '__main__':
    stocks=getstockinfo()


