import numpy as np
import rasterio
def RasterPlane(X0,Y0,Z0,Xend,Yend,slopeX,slopeY,cellSize):
    """
    Creates a plane in raster format
    by Azam Masoodi

    Parameters
    ----------
    X0,Y0,Z0 : float
        coordination of first point 
    Xend,Yend : float
        coordination of end point 
    slopeX, slopeY : float
        slope of plane in direction X, Y
    cellSize: cellSize of Raster
    """
    X =np.arange(X0, Xend, cellSize)
    Y=np.arange(Y0, Yend, cellSize)
    X,Y= np.meshgrid(X,Y)
    Z=Z0+slopeY*(Y-Y0)+slopeX*(X-X0)
    new_raster = rasterio.open(

        'RasterPlane.tif',

        'w',

        driver='GTiff',

        height=Z.shape[0],

        width=Z.shape[1],

        count=1,

        dtype=Z.dtype,

        crs='+proj=latlong'

    )
    new_raster.write(Z, 1)
    new_raster.close()

RasterPlane(0,0,0,1000,1000,0,0.0001,1)
