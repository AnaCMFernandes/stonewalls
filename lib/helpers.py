
import sklearn.linear_model as LinearRegression
import numpy as np
import math
from matplotlib import pyplot as plt
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

def vague_case(geom):

    elevs = [p.z for p in geom]

    x = np.arange(len(elevs))
    y = np.array(elevs)

    xr = x.reshape(-1, 1)

    model = LinearRegression.LinearRegression().fit(xr, y)
    score = model.score(xr, y)
    print(score)
    if (score < 0.90):
        return True
    else: return False

def wall_tests(geom):
    if large_wall_test(geom): return '1'
    if small_wall_test(geom): return '2'
    if onesided_wall_test(geom): return '3'
    # if vague_case(geom): return '4'
    else: return '0'

def large_wall_test(geom):
    peaks = large_peaks_finder(geom)
    # print('++++large peaks', peaks)
    if (len(peaks) > 0): return True
    else: return False

def large_peaks_finder(geom):
    z = [p.z for p in geom]
    ### TODO change here for adjustment
    peaks, _ = signal.find_peaks(z, prominence=0.35)
    return peaks

def small_wall_test(geom):
    peaks = small_peaks_finder(geom)
    # print('---small peaks', peaks)
    if (len(peaks) > 0): return True
    else: return False

def small_peaks_finder(geom):
    z = [p.z for p in geom]
    ### TODO change here for adjustment
    peaks, _ = signal.find_peaks(z, prominence=0.22)
    return peaks

def onesided_wall_test(geom):
    ##elevations
    peaks = onesided_peaks_finder(geom)
    if (len(peaks) > 0):
        return True
    else: return False
    return True

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
        #print(large_peaks)
        return (large_peaks, '1')
    small_peaks = small_peaks_finder(geom)
    if (len(small_peaks) > 0):
        #print('small peak')
        return (small_peaks, '2')
    onesided_peaks = onesided_peaks_finder(geom)
    if (len(onesided_peaks) > 0):
        #print('onesided peak')
        return (onesided_peaks, '3')
    # print('no wall no peak no chance')
    # vague_peaks = vague_case(geom)
    # if vague_peaks:
    #     return ([25], '4')
    return ([], '0')
    
def plot_profiles(profile, wall_type):    
    if (wall_type=='1'):     
        just_plot(profile, 'green')
    elif (wall_type=='2'):     
        just_plot(profile, 'orange')
    elif (wall_type=='3'):     
        just_plot(profile, 'red')
    elif(wall_type=='4'):
        just_plot(profile, 'purple')
    else:     
        just_plot(profile, 'blue')
    return 1