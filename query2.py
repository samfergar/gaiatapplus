import pandas as pd
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Data Release 3, default


# Set Pandas to display all rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

def convert_and_calculate_distance(df, index1, index2):
    """
    Convert celestial coordinates to Cartesian coordinates and calculate distance between two points.

    Parameters:
    - df (DataFrame): DataFrame containing 'ra', 'dec', 'parallax' columns.
    - index1 (int): Index of the first point (P1).
    - index2 (int): Index of the second point (P2).

    Returns:
    - P1_coords (array): Cartesian coordinates of P1.
    - P2_coords (array): Cartesian coordinates of P2.
    - distance (float): Distance between P1 and P2 in parsecs.
    """
    
    # Calculate distance from parallax (in parsecs)
    df["distance"] = 1000 / df["parallax"]  # Convert parallax from mas to parsecs
    
    # Debugging: Print parallax and calculated distances
    print("Parallax (mas):", df["parallax"].values)
    print("Distances (parsecs):", df["distance"].values)

    # Convert RA and Dec from degrees to radians for calculations
    df["ra_rad"] = np.radians(df["ra"])
    df["dec_rad"] = np.radians(df["dec"])

    # Convert to Cartesian coordinates (x, y, z)
    df["x"] = df["distance"] * np.cos(df["dec_rad"]) * np.cos(df["ra_rad"])
    df["y"] = df["distance"] * np.cos(df["dec_rad"]) * np.sin(df["ra_rad"])
    df["z"] = df["distance"] * np.sin(df["dec_rad"])

    # Debugging: Print the calculated Cartesian coordinates
    print("Calculated Cartesian Coordinates (x, y, z):")
    print(df[["x", "y", "z"]])

    # Select points P1 and P2
    P1 = df.iloc[index1]
    P2 = df.iloc[index2]

    # Calculate the distance vector from P1 to P2
    delta_x = P2["x"] - P1["x"]
    delta_y = P2["y"] - P1["y"]
    delta_z = P2["z"] - P1["z"]

    # Calculate the Euclidean distance between P1 and P2
    distance_between_P1_and_P2 = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    # Output the coordinates of P1 and P2
    P1_coords = P1[["x", "y", "z"]].values
    P2_coords = P2[["x", "y", "z"]].values

    return P1_coords, P2_coords, distance_between_P1_and_P2

# Your updated SQL query using the specified columns
columns_to_select = ["ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]  # Add any other columns you want
columns_string = ", ".join(columns_to_select)

query = f"""
SELECT TOP 100 {columns_string} FROM gaiadr3.gaia_source  
WHERE has_xp_sampled = 'True'
"""  

# Launch the asynchronous job
job = Gaia.launch_job_async(query)

# Get the results
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Calculate distance and coordinates
P1_coords, P2_coords, distance = convert_and_calculate_distance(df, index1=0, index2=1)

# Output the results with all coordinates included
print("Coordinates of P1 (x, y, z):", P1_coords)  # Show x, y, z for P1
print("Coordinates of P2 (x, y, z):", P2_coords)  # Show x, y, z for P2
print("Distance between P1 and P2 (in parsecs):", distance)

# Display the updated DataFrame with the new calculations
print(df[["ra", "dec", "parallax", "distance", "x", "y", "z"]])  # Display relevant columns
