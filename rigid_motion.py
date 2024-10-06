import numpy as np

def celestial_to_cartesian(ra, dec, distance):
    """Convert celestial coordinates (RA, Dec) to Cartesian coordinates (x, y, z)."""
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)
    return x, y, z

def recalculate_star_brightness(planet_ra, planet_dec, planet_distance, star_catalog_df):
    """
    Recalculate the relative brightness of stars from the point of view of a given exoplanet.
    
    Parameters:
    - planet_ra (float): Right Ascension (RA) of the exoplanet in degrees.
    - planet_dec (float): Declination (Dec) of the exoplanet in degrees.
    - planet_distance (float): Distance to the exoplanet in parsecs.
    - star_catalog_df (pd.DataFrame): DataFrame containing the star catalog with RA, Dec, and phot_g_mean_mag.
    
    Returns:
    - star_data_dict (dict): A dictionary containing recalculated star positions and relative brightness.
    """
    # Convert the exoplanet's celestial coordinates (RA, Dec, distance) to Cartesian coordinates
    planet_x, planet_y, planet_z = celestial_to_cartesian(planet_ra, planet_dec, planet_distance)
    
    # Convert stars' celestial coordinates to Cartesian coordinates
    star_catalog_df[['x', 'y', 'z']] = star_catalog_df.apply(
        lambda row: celestial_to_cartesian(row['ra'], row['dec'], row['distance']),
        axis=1,
        result_type='expand'
    )

    # Shift star positions to be relative to the exoplanet's coordinates
    star_catalog_df['x_relative'] = star_catalog_df['x'] - planet_x
    star_catalog_df['y_relative'] = star_catalog_df['y'] - planet_y
    star_catalog_df['z_relative'] = star_catalog_df['z'] - planet_z
    
    # Project the stars onto the same z = R plane as before (for consistency)
    R = star_catalog_df['distance'].max()  # Maximum distance
    star_catalog_df['x_projected'] = star_catalog_df['x_relative'] * (R / star_catalog_df['z_relative'])
    star_catalog_df['y_projected'] = star_catalog_df['y_relative'] * (R / star_catalog_df['z_relative'])
    
    # Calculate the modulus (distance in the x-y plane) for each projected point
    star_catalog_df['modulus'] = np.sqrt(
        star_catalog_df['x_projected']**2 + star_catalog_df['y_projected']**2
    )
    
    # Find the normalization value (mean of modulus) for scaling purposes
    normalization_value = star_catalog_df['modulus'].mean()
    
    # Normalize x and y coordinates using the normalization value
    star_catalog_df['x_normalized'] = star_catalog_df['x_projected'] / normalization_value * 200
    star_catalog_df['y_normalized'] = star_catalog_df['y_projected'] / normalization_value * 200
    
    # Select a reference star (e.g., the first star in the list)
    reference_magnitude = star_catalog_df.iloc[0]['phot_g_mean_mag']
    
    # Recalculate the relative brightness with respect to the reference star
    star_catalog_df['relative_brightness'] = 10**(0.4 * (reference_magnitude - star_catalog_df['phot_g_mean_mag']))
    
    # Normalize relative brightness between 0 and 1
    min_brightness = star_catalog_df['relative_brightness'].min()
    max_brightness = star_catalog_df['relative_brightness'].max()
    star_catalog_df['relative_brightness_normalized'] = (
        (star_catalog_df['relative_brightness'] - min_brightness) / (max_brightness - min_brightness)
    )
    
    # Prepare the output dictionary
    star_data_dict = {}
    for idx, row in star_catalog_df.iterrows():
        star_data_dict[idx] = {
            "position": {
                "x_normalized": row['x_normalized'],
                "y_normalized": row['y_normalized']
            },
            "normalization_value": normalization_value,
            "relative_brightness": row['relative_brightness_normalized']
        }
    
    return star_data_dict
