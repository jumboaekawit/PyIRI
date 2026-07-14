import sys

import numpy as np
import PyIRI
import PyIRI.sh_library as sh  # Updated PyIRI using spherical harmonics
import matplotlib.pyplot as plt


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
# CM01 18.788 N 98.985 E
lon_res = 0.01
lat_res = 0.01
lon_center = 98.985
lat_center = 18.788
offset = 10
alon_2d, alat_2d = np.mgrid[lon_center - offset*lon_res:lon_center + offset*lon_res:lon_res, lat_center - offset*lat_res:lat_center + offset*lat_res:lat_res]
alon = np.reshape(alon_2d, alon_2d.size)
alat = np.reshape(alat_2d, alat_2d.size)

# Time grid: Universal Time from 0 to 24 in 15-minute steps
hr_res = 1
aUT = np.arange(0, 24, hr_res)

# Height grid: 90 km to 700 km in 1 km steps
alt_res = 1
alt_min = 90
alt_max = 700
aalt = np.arange(alt_min, alt_max, alt_res)

# Coefficient sources and model options
foF2_coeff = 'CCIR'       # Options: 'CCIR' or 'URSI'
hmF2_model = 'SHU2015'    # Options: 'SHU2015', 'AMTB2013', 'BSE1979'
coord = 'GEO'             # Coordinate system: 'GEO', 'QD', or 'MLT'
coeff_dir = None          # Use default coefficient path



# Specify date
# year = 1997
# month = 1
# day = 1
year, month, day = [int(x) for x in sys.argv[1].split("-")]
# ----------------------------------------
# Run PyIRI (Spherical Harmonics version)
# ----------------------------------------
# For each day, compute ionospheric parameters for F2, F1, and E layers
# for day in range(18, 18 + 1):

F2, F1, E, sun, mag, EDP = sh.IRI_density_1day(year,
                                            month,
                                            day,
                                            aUT,
                                            alon,
                                            alat,
                                            aalt,
                                            F107,
                                            coeff_dir=coeff_dir,
                                            foF2_coeff=foF2_coeff,
                                            hmF2_model=hmF2_model,
                                            coord=coord)
# save parameters to zarr
save_as = f'daily_parameters/{year}_{month}_{day}.zarr'
z_root = zarr.create_group(save_as, overwrite=True)
zarr_dict2group(z_root, 'F2', F2)
zarr_dict2group(z_root, 'F1', F1)
zarr_dict2group(z_root, 'E', E)
zarr_dict2group(z_root, 'sun', sun)
zarr_dict2group(z_root, 'mag', mag)
EDP_save = z_root.create_array('EDP', shape = EDP.shape, dtype = EDP.dtype, overwrite=True, compressors=compressor)
EDP_save[:] = EDP
# print(f'Saved daily data to {save_as}')
