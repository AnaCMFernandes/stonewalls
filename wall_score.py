
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

    slope = LR.coef_[0]
    intercept = LR.intercept_

    return (slope, intercept)
## set to work for multipoint
def just_plot(geom, color='green', title=''):
    try:
        elevs = [p.z for p in geom]
    except:
        elevs = [p.y for p in geom]

    x = np.arange(len(elevs))
    y = np.array(elevs)

    plt.figure()
    plt.scatter(x, y, label="elevations", color=color, alpha=0.7)
    plt.title(title)
    plt.yticks(np.arange(1.5,step=0.2))
    plt.legend()
    plt.show()
    return True

def rise_run_to_angle(rise, run):
   return math.degrees(math.atan(rise/run))

def large_wall_test(geom):
    peaks = large_peaks_finder(geom)
    # print('++++large peaks', peaks)
    if (len(peaks) > 0): return True
    else: return False

def small_wall_test(geom):
    peaks = small_peaks_finder(geom)
    # print('---small peaks', peaks)
    if (len(peaks) > 0): return True
    else: return False

def onesided_wall_test(geom):
    ##elevations
    peaks = onesided_peaks_finder(geom)
    if (len(peaks) > 0):
        return True
    else: return False
    return True

def wall_tests(geom):
    if large_wall_test(geom): return '1'
    if small_wall_test(geom): return '2'
    if onesided_wall_test(geom): return '3'
    else: return '0'

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

def large_peaks_finder(geom):
    z = [p.z for p in geom]
    ### TODO change here for adjustment
    peaks, _ = signal.find_peaks(z, prominence=0.30)
    return peaks
def small_peaks_finder(geom):
    z = [p.z for p in geom]
    ### TODO change here for adjustment
    peaks, _ = signal.find_peaks(z, prominence=0.20)
    return peaks

def onesided_peaks_finder(geom):
    z = [p.z for p in geom]
    ## steps in x direction
    x = list(np.arange(0, 20.01, step=0.4))
    coords = []
    for i in range(len(z)):
        coord = (x[i], z[i])
        coords.append(coord)

    #### calculate rotations and transformation
    rise, intercept = linear_regression_score3D(geom)

    origin = (0,intercept)

    run = 0.4

    rotation = rise_run_to_angle(rise, run)

    new_geom = affinity.rotate(MultiPoint(coords), -rotation, origin = origin)
    # just_plot(new_geom, 'purple', 'rotated')
    # new_x = np.array([p.x for p in new_geom])
    new_z = np.array([p.y for p in new_geom])
    ### TODO change here for adjustment
    peaks, _ = signal.find_peaks(new_z, prominence=0.20)
    return peaks


def find_wall_peak(geom):
    large_peaks = large_peaks_finder(geom)
    if (len(large_peaks) > 0):
        # print('large peak')
        return (large_peaks, '1')
    onesided_peaks = onesided_peaks_finder(geom)
    if (len(onesided_peaks) > 0):
        # print('onesided peak')
        return (onesided_peaks, '3')
    small_peaks = small_peaks_finder(geom)
    if (len(small_peaks) > 0):
        # print('small peak')
        return (small_peaks, '2')
    # print('no wall no peak no chance')
    return ([], '0')
    
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

