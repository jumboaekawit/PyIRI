
# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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
F107 = 100

# Create horizontal grid
lon_res = 0.01
lat_res = 0.01
lon_center = 98.985
lat_center = 18.788
offset = 10
alon_2d, alat_2d = np.mgrid[lon_center - offset*lon_res:lon_center + offset*lon_res:lon_res, lat_center - offset*lat_res:lat_center + offset*lat_res:lat_res]
alon = np.reshape(alon_2d, alon_2d.size)
alat = np.reshape(alat_2d, alat_2d.size)

lon_min = lon_center - offset*lon_res
lon_max = lon_center + offset*(lon_res-1)
lat_min = lat_center - offset*lat_res
lat_max = lat_center + offset*(lat_res-1)

# Time grid: Universal Time from 0 to 24 in 15-minute steps
hr_res = 1
aUT = np.arange(0, 24, hr_res)

# Height grid: 90 km to 700 km in 1 km steps
alt_res = 1
alt_min = 90
alt_max = 700
aalt = np.arange(alt_min, alt_max, alt_res)

filename = 'D:/DATA/IRI_from_TP/result/1997_1_1.zarr'

z_root = zarr.open_group(filename, mode='r')
# load each dictionary from group
F2 = dict((key, np.array(z_root['F2'][key])) for key in z_root['F2'].keys())
F1 = dict((key, np.array(z_root['F1'][key])) for key in z_root['F1'].keys())
E = dict((key, np.array(z_root['E'][key])) for key in z_root['E'].keys())
sun = dict((key, np.array(z_root['sun'][key])) for key in z_root['sun'].keys())
mag = dict((key, np.array(z_root['mag'][key])) for key in z_root['mag'].keys())

# load numpy array directly
EDP = np.array(z_root['EDP'])


# Select a time frame to plot
UT_plot = 10

ind_time = np.where(aUT == UT_plot)

# Plot foF2
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F2['fo'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=2, vmax=14)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$fo$F2 (MHz)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_foF2.png', format='png', bbox_inches='tight')


# Plot hmF2
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F2['hm'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=200, vmax=360)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$hm$F2 (km)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_hmF2.png', format='png', bbox_inches='tight')


# Plot B0
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F2['B0'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=60, vmax=220)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$B0$ (km)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_B0.png', format='png', bbox_inches='tight')


# Plot B1
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F2['B1'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=5)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$B1$ (unitless)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_B1.png', format='png', bbox_inches='tight')


# Plot B_top
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F2['B_top'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=36, vmax=46)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$B_{top}$ (km)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_B_top.png', format='png', bbox_inches='tight')

# Plot probability of F1 to occurre
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F1['P'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=1)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('Probability of F1')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_P.png', format='png', bbox_inches='tight')


# Plot thickness of F1
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F1['B_bot'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=50)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('B$_{bot}^{F1}$ (km)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_B_F1_bot.png', format='png', bbox_inches='tight')


# Plot foF1
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F1['fo'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=10)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$fo$F1 (MHz)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_foF1.png', format='png', bbox_inches='tight')


# Plot hmF1
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(F1['hm'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=100, vmax=200)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$hm$F1 (km)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_hmF1.png', format='png', bbox_inches='tight')

# Plot results for E region


# Plot foE
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(E['fo'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=4)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$fo$E (MHz)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_foE.png', format='png', bbox_inches='tight')


# Calculate vertical TEC from EDP array
TEC = PyIRI.main_library.edp_to_vtec(EDP, aalt, min_alt=0.0, max_alt=202000.0)

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
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=60)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('vTEC (TECU)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_vTEC.png', format='png', bbox_inches='tight')

# Plot electron density vertical profiles from one location


# Select location to plot EDP
lon_plot = 10
lat_plot = 10


fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(4, 4),
                           constrained_layout=True)
ax.set_xlabel('Electron Density (m$^{-3}$)')
ax.set_ylabel('Altitude (km)')
ax.set_facecolor("lightgrey")
ax.set_xlim(0, 1.4e12)
ax.set_ylim(0, 700)
ind_grid = np.zeros_like(alat, dtype=bool)
ind_grid[ind_grid.shape[0]//2, ind_grid.shape[1]//2] = True
ind_time = np.where(aUT == UT_plot)
ind_vert = np.where(aalt >= 0)
ind = ind_time, ind_vert, ind_grid
x = np.reshape(EDP[ind], aalt.shape)
ax.plot(x, aalt, c='black', linewidth=1)
plt.title(str(lon_plot) + '° Lon, ' + str(lat_plot) + '° Lat, ' + str(UT_plot) + ' UT')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_EDP.png', format='png', bbox_inches='tight')

# ### Compute the sporadic E layer critical frequency
# 
# Because the sporadic E layer contains sharper density gradients, a higher number of spherical harmonic coefficients is needed to reconstruct it accurately. The sporadic E layer parameter functions are therefore decoupled from the ionospheric parameter computation of the F2, F1, and E layers.


# Compute ionospheric parameters for sporadic E layer
Es = sh.sporadic_E_1day(year,
                        month,
                        day,
                        aUT,
                        alon,
                        alat,
                        F107,
                        coeff_dir=coeff_dir,
                        coord=coord)

# Plot foEs
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(5, 3),
                        constrained_layout=True)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(lon_res))
ax.yaxis.set_major_locator(ticker.MultipleLocator(lat_res))
ax.set_facecolor('grey')
ax.set_xlabel('Geo Lon (°)')
ax.set_ylabel('Geo Lat (°)')
z = np.reshape(Es['fo'][ind_time, :], alon_2d.shape)
mesh = ax.pcolormesh(alon_2d, alat_2d, z, vmin=0, vmax=10)
ax.scatter(sun['lon'][ind_time], sun['lat'][ind_time],
                    c='red', s=20, edgecolors="black", linewidths=0.5)
cbar = fig.colorbar(mesh, ax=ax)
cbar.set_label('$fo$Es (MHz)')
# Save figure
plot_dir = 'figure/'
plt.savefig(plot_dir + 'PyIRI_sh_foEs.png', format='png', bbox_inches='tight')


