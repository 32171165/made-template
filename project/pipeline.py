from kaggle.api.kaggle_api_extended import KaggleApi
import os
import sqlalchemy as sql
import pandas as pd

kaggle_api = KaggleApi()
kaggle_api.authenticate()
directory = '../data'


# informations about datasets were stored in the following dictionary
infos = {'asylum': {'file_name': 'asylum-applications',
                    'url' : 'patrasaurabh/global-asylum-data-2000-present',
                    'required_csv_name' : 'asylum-applications',
                    'columns_to_drop' : ['Country of origin (ISO)', 'Country of asylum (ISO)'],
                    'table_name' : 'asylum_applications'},
         
         'Global': {'file_name': 'GlobalLandTemperaturesByCountry',
                    'url' : 'berkeleyearth/climate-change-earth-surface-temperature-data',
                    'required_csv_name' : 'GlobalLandTemperaturesByCountry',
                    'columns_to_drop' : ['AverageTemperatureUncertainty'],
                    'table_name' : 'global_temperature'}
        }





"""
following function downloads the datasets from Kaggle with the API

param   dataset_url : url of the Kaggle dataset 
param   directory : the path in which files will be downloaded
"""
def download_from_kaggle(dataset_url, directory):
    print(f"Downloading {dataset_url}")
    kaggle_api.dataset_download_files(dataset=dataset_url, path=directory, unzip=True)
    print(f"{dataset_url} has been successfully downloaded")
        



"""      
following function checks if the files downloaded. If not calls the downloading function one more time  
  
param   directory : the path which is supposed to have the csv files
param   file : name of the file we are checking
"""    
def check_file_downloaded(directory, file):
    if f'{file}.csv' in os.listdir(directory):
        print(f'{file} is in {directory}')
        
    else:
        print(f'{file} is NOT found in {directory}. Downloading again from Kaggle...')
        if file[:6] == 'Global':
            download_from_kaggle(dataset_list=infos['Global']['url'], directory=directory)
        if file[:6] == 'asylum':
            download_from_kaggle(dataset_list=['asylum']['url'], directory=directory)



""" 
following function makes the necessary cleanings and transformations on the dataframe  

param   df : pandas dataframe on which we want to transform
param   key : name of the dataset to reach the necessary information from the infos dictionary. Also the first five letter of the csv file
return : cleaned dataframe
""" 
def transformation(df, key):
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
following function turns the csv file into pandas dataframe and after transforming uploads it to sql file

param   file : name of the csv file on which we want to transform
param   engine : sqlite database engine
"""
def csv_to_sql_table(file, engine):
    # first five letters of the file is the key for transformation function
    key = file[:6]
    
    # load the csv file into pandas dataframe
    df = pd.read_csv(filepath_or_buffer=(f'{directory}/{file}.csv'))
    
    # transform the dataframe
    df = transformation(df, key)
    
    print(f"{file} was successfully recorded in {infos[key]['table_name']} table")
    
    #load the dataframe into sql database
    df.to_sql(name=infos[key]['table_name'], con=engine, index=False, if_exists='append')
    
   
   



def main():
    
    engine = sql.create_engine('sqlite:///../data/data.sqlite')
    
    for file in infos:
        download_from_kaggle(dataset_url=infos[file]['url'], directory=directory)
        
    for file in infos:
        check_file_downloaded(directory, infos[file]['file_name'])
        
    for file in infos:
        csv_to_sql_table(file=infos[file]['required_csv_name'], engine=engine)
    
    
    
         
if __name__ == '__main__':
    main()