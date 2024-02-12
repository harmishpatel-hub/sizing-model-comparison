import pandas as pd 
from os import listdir
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

dim = pd.read_csv("./dim/dim.csv")

def read_csvs(PATH):
    files = [f for f in listdir(PATH) if f.endswith('.csv')]
    combinedDF = pd.DataFrame()
    for file in files:
        df_csv = pd.read_csv(f'{PATH}{file}')
        df_csv['Info'] = file.split('.csv')[0]
        df_csv.columns = df_csv.columns.str.lstrip(" ")
        combinedDF = pd.concat([combinedDF, df_csv])
    # df = pd.concat(pd.read_csv(f'{PATH}{f}') for f in files)
    return combinedDF

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

def getLength(shape):
    return dim[dim['Shape']==shape]['Length [in]'].values[0]

def getWidth(shape):
    return dim[dim['Shape']==shape]['Width [in]'].values[0]

def getMetalLossClass(length, width, wt):
    mmLength = length*25.4
    mmWidth = width*25.4
    mmWT = wt*25.4
    mlClass = ''
    A = 10 if mmWT<10 else mmWT
    ratio = mmLength/mmWidth
    if mmWidth >= 3*A and mmLength >= 3*A:
        mlClass = 'General'
    elif mmWidth >= A and mmWidth < 6*A and mmLength >= A and mmLength >= A and mmLength < 6*A and ratio > 0.5 and ratio < 2:
        mlClass = 'Pitting'
    elif mmWidth >= A and mmWidth < 3 * A and ratio >= 2:
        mlClass = 'Axial Grooving'
    elif mmLength >= A and mmLength < 3 * A and ratio <= 0.5:
        mlClass = "Circ Grooving"
    elif mmWidth > 0 and mmWidth < A and mmLength > 0 and mmLength < A:
        mlClass = "Pinhole"
    elif mmWidth > 0 and mmWidth < A and mmLength >= A:
        mlClass = "Axial Slotting"
    elif mmWidth >= A and mmLength > 0 and mmLength < A:
        mlClass = "Circ Slotting"
    return mlClass

def preprocess_length_width(df):
    df['Length [in]'] = df['Shape'].apply(lambda x: getLength(x))
    df['Width [in]'] = df['Shape'].apply(lambda x: getWidth(x))
    df['ML Class'] = df.apply(lambda x: getMetalLossClass(
                                        x['Length [in]'],
                                        x['Width [in]'],
                                        x['WT [in]']), axis=1)
    return df

def labelEncoding(data, colToEncode):
    le = LabelEncoder()
    data[colToEncode] = le.fit_transform(data[colToEncode])
    return data

def parsed_data(df):
    columns = ['ML Class', 'Ext/Int', 'Length [in]', 'Width [in]', 'WT [in]', 'Peak Value', 'Speed [ft/s]', '% Depth']
    filtered_df = filter_columns(df, columns)
    df_test = filtered_df.rename(
        columns={
            'ML Class': 'ml_class', 
            'Length [in]': 'length', 
            'Width [in]': 'width', 
            'WT [in]': 'wt', 
            'Peak Value': 'peak_value',
            'Speed [ft/s]': 'speed',
            '% Depth': 'depth_old'
            }
        )
    old_depth = df_test['depth_old']
    df_test.drop('depth_old', axis=1, inplace=True)
    df_test['Ext/Int'] = df_test['Ext/Int'].apply(lambda x: 1 if x=='External' else 0)
    df_test = labelEncoding(df_test, 'ml_class')
    # st.dataframe(df_test)
    return df_test

