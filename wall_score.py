import sklearn.linear_model as LinearRegression
import numpy as np
from matplotlib import pyplot as plt


def linear_regression_score(elevs, showplots=False):
    x = np.arange(len(elevs))
    y = np.array(elevs)

    xr = x.reshape(-1, 1)

    LR = LinearRegression.LinearRegression()
    LR.fit(xr, y)
    score = LR.score(xr, y)

   #  prediction = LR.predict(xr)

   #  plt.figure()
   #  plt.plot(x, prediction, label="linear regression", color="b")
   #  plt.scatter(x, y, label="elevations", color="g", alpha=0.7)
   #  plt.title(score)
   #  plt.legend()
   #  plt.show()
   
    return score

def linear_regression_score3D(multipoint):

    elevs = [p.z for p in multipoint]

    x = np.arange(len(elevs))
    y = np.array(elevs)

    xr = x.reshape(-1, 1)

    LR = LinearRegression.LinearRegression()
    LR.fit(xr, y)

    score = LR.score(xr, y)

    prediction = LR.predict(xr)

    plt.figure()
    plt.plot(x, prediction, label="linear regression", color="b")
    plt.scatter(x, y, label="elevations", color="g", alpha=0.7)
    plt.title(score)
    plt.legend()
    plt.show()

    return score


