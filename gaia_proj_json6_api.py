import numpy as np
import pandas as pd
from astroquery.gaia import Gaia
import json
import logging
from fastapi import FastAPI, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def recalculate_star_positions(planet_ra, planet_dec, star_catalog_df):
    """
    Adjust star positions relative to the exoplanet's coordinates and recalculate brightness.
    
    Parameters:
    - planet_ra (float): Exoplanet's right ascension in degrees.
    - planet_dec (float): Exoplanet's declination in degrees.
    - star_catalog_df (pd.DataFrame): DataFrame of star catalog with RA, Dec, and magnitude.
    
    Returns:
    - pd.DataFrame: DataFrame with recalculated x, y positions and brightness.
    """
    # Assume the exoplanet is at infinite distance (i.e., it's the reference point)
    exo_x, exo_y, exo_z = celestial_to_cartesian(planet_ra, planet_dec, 1e12)

    # Convert stars' celestial coordinates to Cartesian
    star_catalog_df[['x', 'y', 'z']] = star_catalog_df.apply(
        lambda row: celestial_to_cartesian(row['ra'], row['dec'], row['distance']),
        axis=1,
        result_type='expand'
    )

    # Shift stars' positions to be relative to the exoplanet
    star_catalog_df['x_relative'] = star_catalog_df['x'] - exo_x
    star_catalog_df['y_relative'] = star_catalog_df['y'] - exo_y
    star_catalog_df['z_relative'] = star_catalog_df['z'] - exo_z

    # Project the stars onto the z = R plane
    df_projection = planar_projection(star_catalog_df)
    
    # Calculate the modulus (distance in the x-y plane) for each projected point
    df_projection['modulus'] = np.sqrt(
        df_projection['x_projected']**2 + 
        df_projection['y_projected']**2
    )

    # Find normalization value for scaling
    normalization_value = df_projection['modulus'].mean()

    # Normalize the x and y coordinates
    df_projection['x_normalized'] = df_projection['x_projected'] / normalization_value * 200
    df_projection['y_normalized'] = df_projection['y_projected'] / normalization_value * 200

    # Select reference star (e.g., the first in the DataFrame) for brightness calculation
    reference_magnitude = star_catalog_df.iloc[0]['phot_g_mean_mag']
    
    # Calculate relative brightness
    star_catalog_df['relative_brightness'] = 10**(0.4 * (reference_magnitude - star_catalog_df['phot_g_mean_mag']))

    # Normalize brightness between 0 and 1
    min_brightness = star_catalog_df['relative_brightness'].min()
    max_brightness = star_catalog_df['relative_brightness'].max()
    star_catalog_df['relative_brightness_normalized'] = (
        (star_catalog_df['relative_brightness'] - min_brightness) / (max_brightness - min_brightness)
    )

    # Merge brightness back with projected positions
    df_projection['relative_brightness'] = star_catalog_df['relative_brightness_normalized'].values
    df_projection['source_id'] = star_catalog_df['source_id'].values  # Add the star's ID
    
    return df_projection

@app.get("/star_positions/")
async def get_stars(planet_ra: float, planet_dec: float, limit: int = 10):

    # Set Pandas to display all rows and columns
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Define additional columns to select from Gaia, including source_id for star identification
    columns_to_select = ["source_id", "ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]
    columns_string = ", ".join(columns_to_select)

    # Query Gaia database
    query = f"""
    SELECT {columns_string} FROM gaiadr3.gaia_source
    WHERE has_xp_sampled = 'True'
    AND random_index BETWEEN 50000 AND 70000
    """  

    # Launch the async job
    job = Gaia.launch_job_async(query)
    results = job.get_results()

    # Convert results to a Pandas DataFrame
    df = results.to_pandas()

    # Calculate distance from parallax (in parsecs)
    df["distance"] = 1000 / df["parallax"]

    # Filter to keep only visible stars
    df = df[df['distance'] > 0].head(limit)

    # Recalculate star positions and brightness based on the exoplanet's location
    star_data = recalculate_star_positions(planet_ra, planet_dec, df)

    # Convert to the required dictionary format: {star_id: [x_normalized, y_normalized, relative_brightness]}
    star_data_dict = star_data.set_index('source_id')[['x_normalized', 'y_normalized', 'relative_brightness']].T.to_dict(orient='list')

    return star_data_dict
