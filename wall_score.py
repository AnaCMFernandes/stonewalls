import sklearn.linear_model as LinearRegression
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy import signal
from shapely.geometry import MultiPoint
from shapely import affinity

## set to work for multipoint
def linear_regression_score3D(geom):

    elevs = [p.z for p in geom]

    x = np.arange(len(elevs))
    y = np.array(elevs)

    xr = x.reshape(-1, 1)

    LR = LinearRegression.LinearRegression()
    LR.fit(xr, y)

    # score = LR.score(xr, y)

    prediction = LR.predict(xr)

    # plt.figure()
    # plt.plot(x, prediction, label="linear regression", color="b")
    # plt.scatter(x, y, label="elevations", color="g", alpha=0.7)
   
    # plt.legend()
    # plt.show()

    slope = LR.coef_[0]
    intercept = LR.intercept_

    return (slope, intercept)
## set to work for multipoint
def only_plot(geom, title='', color='green'):
    try:
        elevs = [p.z for p in geom]
    except:
        elevs = [p.y for p in geom]

    x = np.arange(len(elevs))
    y = np.array(elevs)

    plt.figure()
    plt.scatter(x, y, label="elevations", color=color, alpha=0.7)
    plt.title(title)
    plt.legend()
    plt.show()
    return True

def rise_run_to_angle(rise, run):
   return math.degrees(math.atan(rise/run))

def large_stonewall_test(geom):
    z = [p.z for p in geom]
    peaks, _ = signal.find_peaks(z, prominence=1.7)
    if (len(peaks) > 1): return True
    else: return False

def small_stonewall_test(geom):
    z = [p.z for p in geom]
    peaks, _ = signal.find_peaks(z, prominence=0.05)
    if (len(peaks) > 1): return True
    else: return False

def earthwall_test(geom):
    ##elevations
    y = [p.z for p in geom]
    ## steps in x direction
    x = list(np.arange(0, 20.01, step=0.4))

    coords = []
    for i in range(len(y)):
        coord = (x[i], y[i])
        coords.append(coord)

    #### calculate rotations and transformation
    rise, intercept = linear_regression_score3D(geom)

    origin = (0,intercept)

    run = 0.4

    rotation = rise_run_to_angle(rise, run)

    new_geom = affinity.rotate(MultiPoint(coords), -rotation, origin = origin)

    new_x = np.array([p.x for p in new_geom])
    new_y = np.array([p.y for p in new_geom])

    return True



def no_wall_test(geom):
    return True

def pnt_from_rtn_arnd_orgn(point, origin, angle):

   p = {'x': point[0], 'y':point[1]}
   o = {'x': origin[0], 'y':origin[1]}

   # if (p['x'] == o['x'] & p['y'] == o['y']): return point

   cos = math.cos(angle)
   sin = math.sin(angle)

   dx = p['x'] - o['x']
   dy = p['y'] - o['y']

   nx = (cos * dx) + (sin * dy) + o['x']
   ny = (cos * dy) - (sin * dx) + o['y']

   return [nx, ny]

def normalise():
    # sbst_gdf = gdf[:500]

# for _,row in sbst_gdf.iterrows():
#    elevs = [p.z for p in row['geometry']]
#    average = sum(elevs) / len(elevs)
#    nrml_elevs = [(p - average) for p in elevs]

#    x = np.arange(len(nrml_elevs))
#    y = np.array(nrml_elevs)

#    peaks = signal.find_peaks(y, height=0.2)
#    print('---peaks----')
#    print(peaks)

#    plt.figure()
#    plt.scatter(x,y)
#    plt.yticks(np.arange(-0.6,.6, step=0.1))
   # plt.show()

# scipy.signal.find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
    return True