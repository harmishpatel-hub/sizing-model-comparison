import pandas as pd
import numpy as np
from itertools import product

def create_df():
    length = np.arange(0.1, 3.05, 0.05)
    width = np.arange(0.1, 3.05, 0.05)
    peak_value = np.arange(0, -4000, -20)
    wt = np.arange(0.1, 1.05, 0.05)
    dimensionsCombination = pd.DataFrame(
        list(
            product(length, width, peak_value, wt)
            ), 
            columns=['length', 'width', 'peak_value', 'wt']
            )
    print(dimensionsCombination.shape)
    print(dimensionsCombination.head())

create_df()