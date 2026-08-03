
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
# F2 = dict((key, np.array(z_root['F2'][key])) for key in z_root['F2'].keys())
# F1 = dict((key, np.array(z_root['F1'][key])) for key in z_root['F1'].keys())
# E = dict((key, np.array(z_root['E'][key])) for key in z_root['E'].keys())
# sun = dict((key, np.array(z_root['sun'][key])) for key in z_root['sun'].keys())
# mag = dict((key, np.array(z_root['mag'][key])) for key in z_root['mag'].keys())

EDP = np.array(z_root['EDP'])

alon_2d, alat_2d, aalt, aUT = [np.array(z_root[f'grid/{key}']) for key in ['alon_2d', 'alat_2d', 'aalt', 'aUT']]
lon_res, lat_res, alt_res, UT_res = [z_root[f'resolution/{key}'][...] for key in ['lon_res', 'lat_res', 'alt_res', 'UT_res']]
foF2_coeff, hmF2_model, coord = [z_root[f'model/{key}'][...] for key in ['foF2_coeff', 'hmF2_model', 'coord']]
F107 = z_root['model/F107'][...]

alon = np.reshape(alon_2d, alon_2d.size)
alat = np.reshape(alat_2d, alat_2d.size)
coord_center_idx = np.ravel_multi_index((alon_2d.shape[0]//2, alon_2d.shape[1]//2), alon_2d.shape)
lon_center = alon[coord_center_idx]
lat_center = alat[coord_center_idx]

# print(alon[coord_center_idx], alat[coord_center_idx])
# lon_min = alon[0]
# lon_max = alon[-1]
# lat_min = alat[0]
# lat_max = alat[-1]


# Calculate vertical TEC from EDP array
TEC = PyIRI.main_library.edp_to_vtec(EDP, aalt, min_alt=0.0, max_alt=350.0)

# Plot vTEC vs UT
plt.figure(figsize=(12, 4), constrained_layout=True)
plt.plot(aUT, TEC[:,coord_center_idx])
plt.title(now.strftime('%Y/%m/%d') + ', ' + str(alon[coord_center_idx]) + '° Lon, ' + str(alat[coord_center_idx]) + '° Lat')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(3))
plt.ylabel('TEC (TECU)')
plt.xlabel('UT (hour)')
plt.show()
