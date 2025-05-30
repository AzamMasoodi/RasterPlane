import numpy as np
import rasterio
from rasterio.transform import from_origin

def cal_circle_params(points):
    """
    Calculates the circle parameters (center and radius) given three points on the circle.
    """
    A = 2 * (points[1][0] - points[0][0])
    B = 2 * (points[1][1] - points[0][1])
    C = points[1][0]**2 + points[1][1]**2 - points[0][0]**2 - points[0][1]**2
    D = 2 * (points[2][0] - points[1][0])
    E = 2 * (points[2][1] - points[1][1])
    F = points[2][0]**2 + points[2][1]**2 - points[1][0]**2 - points[1][1]**2

    h = (C * E - F * B) / (A * E - D * B)
    k = (A * F - D * C) / (A * E - D * B)
    r = np.sqrt((points[0][0] - h)**2 + (points[0][1] - k)**2)
    
    return h, k, r

def RasterPlane(slopetype, X0, Y0, Z0, Xend, Yend, slopeX, slopeY, cellSize, noise_range=(-0.02, 0.02)):
    """
    Creates a plane in raster format with optional random noise.

    Parameters
    ----------
    slopetype : float
    X0, Y0, Z0 : float
        Coordinates of the first point 
    Xend, Yend : float
        Coordinates of the end point 
    slopeX, slopeY : float
        Slope of the plane in direction X, Y
    cellSize: float
        Size of each cell in the raster
    noise_range : tuple of float
        Range of the uniform distribution for random noise to be added to Z values.
    """
    # Create arrays for X and Y coordinates
    X = np.arange(X0, Xend, cellSize)
    Y = np.arange(Y0, Yend, cellSize)
    X, Y = np.meshgrid(X, Y)
    
    
    # Create initial Z values for the additional rows
    additional_rows = 2  # Number of additional rows
    Z = np.full((additional_rows, X.shape[1]), -0.02, dtype=np.float32)  # Start with -0.02 for 0.5plan and 0.03 for 2 plan
    Z[0, :] = -0.05  # Set the first additional row to -0.05
    
    # Surface: Calculate Z values based on the slope type
    if slopetype == 5:  # even X, even Y
        Z = np.vstack((Z, Z0 + slopeY * (Y - Y0) + slopeX * (X - X0)))

    elif slopetype == 4:  # even X, convex Y
        points = np.array([[0, 0], [12.5, 3.75], [25, 5]])
        h, k, r = cal_circle_params(points)
        Z = np.vstack((Z, Z0 + np.sqrt(r**2 - (Y - h)**2) + k))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
        
    elif slopetype == 6:  # even X, concave Y
        points = np.array([[0, 0], [12.5, 1.25], [25, 5]])
        h, k, r = cal_circle_params(points)
        Z = np.vstack((Z, Z0 - np.sqrt(r**2 - (Y - h)**2) + k))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
        
    elif slopetype == 8:  # convex X, even Y
        points = np.array([[0, 0], [6.25, 0.25], [12.5, 0]])
        h, k, r = cal_circle_params(points)
        Z = np.vstack((Z, Z0 + np.sqrt(r**2 - (X - h)**2) + k + slopeY * (Y - Y0)))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero

    elif slopetype == 2:  # concave X, even Y
        points = np.array([[0, 0.25], [6.25, 0], [12.5, 0.25]])
        h, k, r = cal_circle_params(points)
        Z = np.vstack((Z, Z0 - np.sqrt(r**2 - (X - h)**2) + k + slopeY * (Y - Y0)))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
        
    elif slopetype == 7:  # convex X, convex Y
        points = np.array([[0, 0], [6.25, 0.25], [12.5, 0]])
        marks = np.array([[0, 0], [12.5, 3.75], [25, 5]])
        h, k, r = cal_circle_params(points)
        hY, kY, rY = cal_circle_params(marks)
        Z = np.vstack((Z, Z0 + np.sqrt(r**2 - (X - h)**2) + k + np.sqrt(rY**2 - (Y - hY)**2) + kY))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero 
        
    elif slopetype == 3:  # concave X, concave Y
        points = np.array([[0, 0.25], [6.25, 0], [12.5, 0.25]])
        marks = np.array([[0, 0], [12.5, 1.25], [25, 5]])
        h, k, r = cal_circle_params(points)
        hY, kY, rY = cal_circle_params(marks)
        Z = np.vstack((Z, Z0 - np.sqrt(r**2 - (X - h)**2) + k - np.sqrt(rY**2 - (Y - hY)**2) + kY))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
        
    elif slopetype == 9:  # convex X, concave Y
        points = np.array([[0, 0], [6.25, 0.25], [12.5, 0]])
        marks = np.array([[0, 0], [12.5, 1.25], [25, 5]])
        h, k, r = cal_circle_params(points)
        hY, kY, rY = cal_circle_params(marks)
        Z = np.vstack((Z, Z0 + np.sqrt(r**2 - (X - h)**2) + k - np.sqrt(rY**2 - (Y - hY)**2) + kY))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
  
    elif slopetype == 1:  # concave X, convex Y
        points = np.array([[0, 0.25], [6.25, 0], [12.5, 0.25]])
        marks = np.array([[0, 0], [12.5, 3.75], [25, 5]])
        h, k, r = cal_circle_params(points)
        hY, kY, rY = cal_circle_params(marks)
        Z = np.vstack((Z, Z0 - np.sqrt(r**2 - (X - h)**2) + k + np.sqrt(rY**2 - (Y - hY)**2) + kY))
        Z[-1, :] -= np.min(Z)  # Ensure minimum Z starts from zero
        
    else:
        raise ValueError("Invalid slope type. Use 0 for flat, 1 for concave, -1 for convex.")
    
    # Add random noise to the Z values if noise_range is defined
    if noise_range:
        noise = np.random.uniform(noise_range[0], noise_range[1], Z[2:, :].shape)
        Z[2:, :] += noise


    # Define the transform for the raster
    transform = from_origin(X0, Y0, cellSize, cellSize)

    # Create a new raster file
    with rasterio.open(
        'RasterPlane9.tif',
        'w',
        driver='GTiff',
        height=Z.shape[0],
        width=Z.shape[1],
        count=1,
        dtype=Z.dtype,
        crs='+proj=latlong',
        transform=transform
    ) as new_raster:
        new_raster.write(Z, 1)

# Example usage
X0, Y0, Z0 = 0, 0, 0
Xend = X0 + 12.5  # 100 cells with 0.5 cell size
Yend = Y0 + 25  # 200 cells with 0.5 cell size
cellSize = 0.5
slopeX, slopeY = 0, 0.2  # Example slopes for each cell
noise_range = (-0.02, 0.02)  # Uniform noise range between -0.02 and 0.02

RasterPlane(9, X0, Y0, Z0, Xend, Yend, slopeX, slopeY, cellSize, noise_range)
