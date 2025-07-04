import pandas as pd
import re
from data_collection import load_data
from loguru import logger

def prepare_data():
    logger.info("starting up preprocessing pipeline")
    # to prepare dataset we need:
    
    #1. load the dataset
    data = load_data()
    #2. encode columns like balcony, parking etc
    data_encoded = encode_cat_cols(data)
    #3. parse the garden column
    df = parse_garden_col(data_encoded)
    
    return df

def encode_cat_cols(data):
    cols = ['balcony','parking', 'furnished', 'garage', 'storage']
    logger.info(f"encoding categorical columns: {cols}")
    return pd.get_dummies(data,
                          columns = cols,
                          drop_first=True)

def parse_garden_col(data):
    logger.info("parsing garden column")
    
    # Make an explicit copy to avoid SettingWithCopyWarning
    data = data.copy()
    
    for i in range(len(data)):
        if data.loc[i, 'garden'] == 'Not present':
            data.loc[i, 'garden'] = 0
        else:
            data.loc[i, 'garden'] = int(re.findall(r'\d+', data.loc[i, 'garden'])[0])
    
    return data