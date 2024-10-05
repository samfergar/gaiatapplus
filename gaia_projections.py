import numpy as np
import pandas as pd
from astroquery.gaia import Gaia

Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Data Release 3, default

def cartesian_to_celestial(x, y, z):
    """Convert Cartesian coordinates (x, y, z) to celestial coordinates (RA, Dec)."""
    distance = np.sqrt(x**2 + y**2 + z**2)
    ra_rad = np.arctan2(y, x)  # atan2 handles quadrants correctly
    if ra_rad < 0:
        ra_rad += 2 * np.pi
    dec_rad = np.arcsin(z / distance)
    ra_deg = np.degrees(ra_rad)
    dec_deg = np.degrees(dec_rad)
    return ra_deg, dec_deg

def celestial_to_cartesian(ra, dec, distance):
    """Convert celestial coordinates (RA, Dec) to Cartesian coordinates (x, y, z)."""
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)
    return x, y, z

def planar_projection(df):
    """
    Create a planar projection of celestial points relative to the first entry.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing celestial coordinates and distances.
    
    Returns:
    - pd.DataFrame: DataFrame containing the projected coordinates (x_projected, y_projected).
    """
    # Calculate the Cartesian coordinates of the first entry
    first_entry_cartesian = df[['x', 'y', 'z']].iloc[0]
    
    # Maximum distance from the reference point
    max_distance = df['distance'].max()  
    
    # Planar projection onto the XY-plane at the maximum distance using original coordinates
    projection_factor = max_distance / df['distance']  # Calculate the projection factor

    # Create new DataFrame for projected points using original coordinates
    df_projection = pd.DataFrame()
    df_projection['x_projected'] = df['x'] * projection_factor
    df_projection['y_projected'] = df['y'] * projection_factor
    
    return df_projection

# Set Pandas to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define additional columns you want to select
columns_to_select = ["ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]
columns_string = ", ".join(columns_to_select)

# Your updated SQL query using the specified columns
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

# Calculate distance from parallax (in parsecs)
df["distance"] = 1000 / df["parallax"]

# Convert celestial coordinates to Cartesian coordinates and add to DataFrame
df[['x', 'y', 'z']] = df.apply(
    lambda row: celestial_to_cartesian(row['ra'], row['dec'], row['distance']),
    axis=1,
    result_type='expand'
)

# Call the planar_projection function
df_projection = planar_projection(df)

# Display the updated DataFrame with projected coordinates
print(df_projection)