from sklearn import metrics
import numpy as np

def model_score(Y_test, prediction):
  """
  It will calculate the score based on true and predicted value
  """
  mae = metrics.mean_absolute_error(Y_test, prediction)
  mse = metrics.mean_squared_error(Y_test, prediction)
  rmse = np.sqrt(mse)
  return mae, mse, rmse