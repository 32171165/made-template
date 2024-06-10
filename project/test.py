from kaggle.api.kaggle_api_extended import KaggleApi
import os
import sqlalchemy as sql
import pandas as pd
from pipeline import transformation

kaggle_api = KaggleApi()
kaggle_api.authenticate()
directory = '../data'

infos = {'df1': {'columns_to_drop' : ['drop1', 'drop2']}}

""" 
following function makes the necessary cleanings and transformations on the dataframe  

param   df : pandas dataframe on which we want to transform
param   key : name of the dataset to reach the necessary information from the infos dictionary. Also the first five letter of the csv file
param   infos : dictionary that contains which columns to drop
return : cleaned dataframe

def transformation(df, key, infos):
    # drop the columns which is not necessary
    df = df.drop(columns=infos[key]['columns_to_drop'])
    
    # if the column 'dt' exists create new column 'Year' to store the year
    # convert column 'dt' from string to date
    if 'dt' in df.columns:
        df['Year'] = pd.to_datetime(df['dt'], yearfirst=True, format='%Y-%m-%d').dt.year
        df['dt'] = pd.to_datetime(df['dt'], yearfirst=True, format='%Y-%m-%d').dt.date
        
    # limit the years between 2000-2012
    df = df[df['Year'] < 2013]
    df = df[df['Year'] > 1999]
    
    return df
"""
def main():
    
    #creating a df for transformation
    #after transformation 'drop1' and 'drop2' columns should be dropped
    #'dt' column should have datetime data type
    #another yolumn 'Year' should be created
    df_to_drop = pd.DataFrame([[1,2,"2012-01-01"],[4,5,"2013-01-02"],[7,8,"1999-02-03"],[4,5,"2000-05-04"]], columns=['drop1', 'drop2', 'dt'])
    
    
    #creating desired dataframe to check
    df_check = pd.DataFrame([["2012-01-01", 2012],["2000-05-04",2000]], columns=['dt','Year']).reset_index(drop=True)
    df_check['Year'] = pd.to_datetime(df_check['Year'], format='%Y').dt.year
    df_check['dt'] = pd.to_datetime(df_check['dt']).dt.date
    
    
    df_result = transformation(df=df_to_drop, key="df1", infos=infos).reset_index(drop=True)
    
    
    print("transformation function is being tested")
    
    assert df_check.equals(df_result), "transformation function doesn't work as intended"
    
    
    
    
         
if __name__ == '__main__':
    main()
    
    