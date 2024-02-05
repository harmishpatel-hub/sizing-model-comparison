import pandas as pd
import numpy as np
from src.dataset_preprocessing import getMetalLossClass, labelEncoding 

def create_df(length, widthList, peakValue, wallThickness, externalOrinternal, speed = 2):
    dimensionDF = pd.DataFrame()
    dimensionDF['width'] = widthList
    dimensionDF['length'] = length
    dimensionDF['peak_value'] = peakValue
    dimensionDF['wt'] = wallThickness
    dimensionDF['Ext/Int'] = externalOrinternal
    dimensionDF['Ext/Int'] = dimensionDF['Ext/Int'].apply(lambda x: 1 if x=='External' else 0)
    dimensionDF['speed'] = speed
    dimensionDF['ml_class'] = dimensionDF.apply(
        lambda x: getMetalLossClass(
                                    x['length'],
                                    x['width'],
                                    x['wt']), axis=1)
    dimensionDF = labelEncoding(dimensionDF, 'ml_class')
    cols = ['ml_class', 'Ext/Int', 'length', 'width', 'wt', 'peak_value', 'speed']
    dimensionDF = dimensionDF[cols]
    return dimensionDF
    
def createListfromRange(startingElement, lastElement, steps, decimal = 3):
        _list = np.arange(startingElement, lastElement, steps).tolist()
        _list = np.round(_list, decimal).tolist()
        return _list