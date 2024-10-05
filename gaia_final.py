import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Data Release 3, default


def cartesian_to_celestial(x, y, z):
    """
    Convert Cartesian coordinates (x, y, z) to celestial coordinates (RA, Dec).
    
    Parameters:
    - x (float): x coordinate
    - y (float): y coordinate
    - z (float): z coordinate
    
    Returns:
    - ra (float): Right Ascension in degrees
    - dec (float): Declination in degrees
    """
    
    # Calculate the distance from the origin
    distance = np.sqrt(x**2 + y**2 + z**2)
    
    # Calculate Right Ascension (RA)
    ra_rad = np.arctan2(y, x)  # atan2 handles quadrants correctly
    
    # Ensure RA is in the range [0, 2*pi]
    if ra_rad < 0:
        ra_rad += 2 * np.pi
    
    # Calculate Declination (Dec)
    dec_rad = np.arcsin(z / distance)
    
    # Convert radians to degrees
    ra_deg = np.degrees(ra_rad)
    dec_deg = np.degrees(dec_rad)
    
    return ra_deg, dec_deg

def celestial_to_cartesian(ra, dec, distance):
    """
    Convert celestial coordinates (RA, Dec) to Cartesian coordinates (x, y, z).
    
    Parameters:
    - ra (float): Right Ascension in degrees
    - dec (float): Declination in degrees
    - distance (float): Distance from the observer in parsecs
    
    Returns:
    - x (float): x coordinate
    - y (float): y coordinate
    - z (float): z coordinate
    """
    
    # Convert RA and Dec from degrees to radians
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    # Calculate Cartesian coordinates
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)
    
    return x, y, z

def change_reference(star_ref, exoplanet_ref):
    '''
    takes in current coordinates of star and the new reference centre of exoplanet and returns the new reference coordinates
    '''
    curr_ra, curr_dec, curr_distance = star_ref
    ex_ra, ex_dec, ex_distance = exoplanet_ref
    
    star_X, star_Y, star_Z= celestial_to_cartesian(star_ref)
    exo_X, exo_Y, exo_Z = celestial_to_cartesian(exoplanet_ref)
    
    new_cartesians = (star_X - exo_X, star_Y - exo_Y, star_Z - exo_Z)
    new_celestial = cartesian_to_celestial(new_cartesians)
    
    return new_celestial


# Set Pandas to display all rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

# Your updated SQL query using the specified columns
columns_to_select = ["ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]  # Add any other columns you want
columns_string = ", ".join(columns_to_select)

query = f"""
SELECT TOP 1000 {columns_string} FROM gaiadr3.gaia_source  
WHERE has_xp_sampled = 'True'
"""  

# Launch the asynchronous job
job = Gaia.launch_job_async(query)

# Get the results
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Calculate distance from parallax (in parsecs)
# Assuming parallax is in milliarcseconds (mas)
df["distance"] = 1000 / df["parallax"]

# Convert celestial coordinates to Cartesian coordinates and add to DataFrame
df[['x', 'y', 'z']] = df.apply(
    lambda row: celestial_to_cartesian(row['ra'], row['dec'], row['distance']),
    axis=1,
    result_type='expand'
)

# Calculate the Cartesian coordinates of the first entry
first_entry_cartesian = df[['x', 'y', 'z']].iloc[0]

# Calculate new columns for relative coordinates with respect to the first entry
df[['x_relative', 'y_relative', 'z_relative']] = df[['x', 'y', 'z']].subtract(first_entry_cartesian, axis=1)

# Display the updated DataFrame with new coordinates
print(df)