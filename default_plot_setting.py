SMALL_SIZE=14
MEDIUM_SIZE=16
LARGE_SIZE=20

import matplotlib
import matplotlib.pyplot as plt

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=LARGE_SIZE)  # fontsize of the figure title
#x-axis tick width and size(length)
matplotlib.rcParams['xtick.major.size'] = 8
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 5
matplotlib.rcParams['xtick.minor.width'] = 1.5
#y-axis
matplotlib.rcParams['ytick.major.size'] = 8
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rcParams['ytick.minor.size'] = 5
matplotlib.rcParams['ytick.minor.width'] = 1.5

matplotlib.rcParams["figure.figsize"] = [16,9]

#set default background color
# plt.rcParams.update({
#     "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
#     "axes.facecolor":    (0.0, 1.0, 0.0, 0.5),  # green with alpha = 50%
#     "savefig.facecolor": (0.0, 0.0, 1.0, 0.2),  # blue  with alpha = 20%
# })