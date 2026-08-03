
# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import PyIRI


import numcodecs
numcodecs.blosc.use_threads = False

import zarr
# compressor = zarr.codecs.BloscCodec(
#         cname="zstd",
#         clevel=22,
#         shuffle=zarr.codecs.BloscShuffle.shuffle
#     )

compressor = zarr.codecs.ZstdCodec(level=22)


def zarr_dict2group(zg: zarr.Group, name: str, dict: dict, overwrite: bool = True):
    grp = zg.create_group(name, overwrite=overwrite)
    for key, val in dict.items():
        arr = grp.create_array(key, shape = val.shape, dtype = val.dtype, overwrite=overwrite, compressors=compressor)
        arr[:] = val


# Specify solar activity index (F10.7 in SFU)
# https://kp.gfz.de/en/data#c222
# https://lasp.colorado.edu/lisird/data/noaa_radio_flux
# https://omniweb.gsfc.nasa.gov/form/dx1.html

from datetime import datetime
now = datetime.now()
year = now.year      # int
month = now.month    # int
day = now.day

filename = f'daily_parameters/{year}_{month}_{day}.zarr'

z_root = zarr.open_group(filename, mode='r')
# load each dictionary from group
F2 = dict((key, np.array(z_root['F2'][key])) for key in z_root['F2'].keys())
F1 = dict((key, np.array(z_root['F1'][key])) for key in z_root['F1'].keys())
E = dict((key, np.array(z_root['E'][key])) for key in z_root['E'].keys())
sun = dict((key, np.array(z_root['sun'][key])) for key in z_root['sun'].keys())
mag = dict((key, np.array(z_root['mag'][key])) for key in z_root['mag'].keys())

# load numpy array directly
EDP = np.array(z_root['EDP'])

alon_2d = np.array(z_root['alon_2d'])
alat_2d = np.array(z_root['alat_2d'])
lon_res = float(z_root['lon_res'][...])
lat_res = float(z_root['lat_res'][...])
print(lon_res, lat_res)

alon = np.reshape(alon_2d, alon_2d.size)
alat = np.reshape(alat_2d, alat_2d.size)
coord_center_idx = np.ravel_multi_index((alon_2d.shape[0]//2, alon_2d.shape[1]//2), alon_2d.shape)
lon_center = alon[coord_center_idx]
lat_center = alat[coord_center_idx]

print(alon[coord_center_idx], alat[coord_center_idx])
lon_min = alon[0]
lon_max = alon[-1]
lat_min = alat[0]
lat_max = alat[-1]

aalt = np.array(z_root['aalt'])
aUT = np.array(z_root['aUT'])

# Select a time frame to plot
UT_plot = 10

ind_time = np.where(aUT == UT_plot)

# Calculate vertical TEC from EDP array
TEC = PyIRI.main_library.edp_to_vtec(EDP, aalt, min_alt=0.0, max_alt=350.0)

# Plot vTEC
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(TEC[ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z) #, vmin=0, vmax=60)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('vTEC (TECU)')
fig.show()
# Save figure
# plot_dir = 'figure/'
# plt.savefig(plot_dir + 'PyIRI_sh_vTEC.png', format='png', bbox_inches='tight')

# Plot electron density vertical profiles from one location

fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(4, 4),
                           constrained_layout=True)
ax.set_xlabel('Electron Density (m$^{-3}$)')
ax.set_ylabel('Altitude (km)')
ax.set_facecolor("lightgrey")
# ax.set_xlim(0, 1.4e12)
# ax.set_ylim(0, 700)
ind_grid = np.zeros_like(alat, dtype=bool)
ind_grid[ind_grid.shape[0]//2] = True
ind_time = np.where(aUT == UT_plot)
ind_vert = np.where(aalt >= 0)
ind = ind_time, ind_vert, ind_grid
x = np.reshape(EDP[ind], aalt.shape)
ax.plot(x, aalt, c='black', linewidth=1)
plt.title(str(lon_center) + '° Lon, ' + str(lat_center) + '° Lat, ' + str(UT_plot) + ' UT')
plt.show()
# Save figure
# plot_dir = 'figure/'
# plt.savefig(plot_dir + 'PyIRI_sh_EDP.png', format='png', bbox_inches='tight')