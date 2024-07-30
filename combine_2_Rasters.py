import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np

# Open the INPUT1 raster
with rasterio.open('INPUT1.tif') as input1:
    input1_data = input1.read(1)
    input1_meta = input1.meta.copy()

# Open the INPUT2 raster
with rasterio.open('INPUT2.tif') as input2:
    input2_data = input2.read(1)
    # Create an empty array for the reprojected INPUT2
    reprojected_input2_data = np.zeros_like(input1_data, dtype=rasterio.float32)

    # Reproject INPUT2 raster to align with INPUT1
    reproject(
        source=input2,
        destination=reprojected_input2_data,
        src_transform=input2.transform,
        dst_transform=input1.transform,
        src_crs=input2.crs,
        dst_crs=input1_data.crs,
        resampling=Resampling.nearest
    )

    # Add INPUT2 VALUE to the INPUT1 VALUE data where INPUT2 data are present
    mask = reprojected_input2_data > 0  # Assuming INPUT2 raster uses 0 or negative for 'no data'
    input1_data[mask] += reprojected_input2_data[mask]

# Save the result in a new raster file
with rasterio.open('OUTPUT.tif', 'w', **input1_meta) as dest:
    dest.write(input1_data, 1)
