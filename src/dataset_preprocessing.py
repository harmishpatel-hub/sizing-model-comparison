import pandas as pd 
from os import listdir

def read_excel(PATH):
    files = [f for f in listdir(PATH) if f.endswith('.xlsx')]
    df = pd.concat(pd.read_excel(f'{PATH}{f}') for f in files)
    return df

def filter_columns(df, columns):
    return df[columns]

def preprocess_shape_depth(df):
    df = df[df['Internal Comments'].notnull()]
    df['Internal Comments'] = df['Internal Comments'].astype(str)
    df['Internal Comments'] = df['Internal Comments'].apply(lambda x: x.replace('-',''))
    df['Internal Comments'] = df['Internal Comments'].astype(float).astype(int)
    df['Shape'] = df['Internal Comments'].apply(lambda x: str(x)[:-2])
    df['Shape'] = df['Shape'].astype(int)
    df['Actual Depth'] = df['Internal Comments'].apply(lambda x: str(x)[-2:])
    df['Actual Depth'] = df['Actual Depth'].astype(int)
    return df