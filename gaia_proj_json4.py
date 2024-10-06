import numpy as np
import pandas as pd
from astroquery.gaia import Gaia
import json
import logging

# Suppress INFO log messages from astroquery
logging.getLogger('astroquery').setLevel(logging.WARNING)

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
    Create a planar projection of celestial points onto the plane z = R.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing celestial coordinates and distances.
    
    Returns:
    - pd.DataFrame: DataFrame containing the projected coordinates (x_projected, y_projected).
    """
    # Maximum distance from the reference point (the first entry)
    R = df['distance'].max()
    
    # Create new DataFrame for projected points using original coordinates
    df_projection = pd.DataFrame()
    
    # Perform projection for each point
    df_projection['x_projected'] = df['x'] * (R / df['z'])
    df_projection['y_projected'] = df['y'] * (R / df['z'])
    
    return df_projection

# Set Pandas to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define additional columns you want to select
columns_to_select = ["ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]
columns_string = ", ".join(columns_to_select)

# Your updated SQL query using the specified columns
query = f"""
SELECT {columns_string} FROM gaiadr3.gaia_source_lite
WHERE has_xp_sampled = 'True'
AND random_index BETWEEN 0 AND 200000
"""  

# Launch the asynchronous job
job = Gaia.launch_job_async(query)

# Get the results
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Calculate distance from parallax (in parsecs)
df["distance"] = 1000 / df["parallax"]

# Convert celestial coordinates to Cartesian coordinates
df[['x', 'y', 'z']] = df.apply(
    lambda row: celestial_to_cartesian(row['ra'], row['dec'], row['distance']),
    axis=1,
    result_type='expand'
)

# Filter to keep only rows with positive z values (visible hemisphere)
df = df[df['z'] > 0]

# Call the planar_projection function
df_projection = planar_projection(df)

# Drop NaN values if any
df_projection = df_projection.dropna()

# Create a DataFrame for x, y, and their modulus
projected_values = df_projection[['x_projected', 'y_projected']].copy()

# Calculate the modulus for each projected point
projected_values['modulus'] = np.sqrt(
    projected_values['x_projected']**2 + 
    projected_values['y_projected']**2
)

# Find the normalization value (mean of modulus)
normalization_value = projected_values['modulus'].mean()

# Normalize x and y by dividing them by normalization_value and multiplying by 200
projected_values['x_normalized'] = projected_values['x_projected'] / normalization_value * 200
projected_values['y_normalized'] = projected_values['y_projected'] / normalization_value * 200

# Normalize phot_g_mean_mag from 0 to 1
# Assuming 'phot_g_mean_mag' is part of df and aligns with df_projection
min_mag = df['phot_g_mean_mag'].min()
max_mag = df['phot_g_mean_mag'].max()

# Add the normalized magnitude to projected_values
projected_values['phot_g_mean_mag'] = (df['phot_g_mean_mag'] - min_mag) / (max_mag - min_mag)

# Convert projected values to a list of lists for JSON
normalized_values = projected_values[['x_normalized', 'y_normalized', 'phot_g_mean_mag']].values.tolist()

# Convert to JSON format
projected_json = json.dumps(normalized_values)

# Display the JSON result
print(projected_json)
