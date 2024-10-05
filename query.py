import astropy.units as u
from astropy.coordinates.sky_coordinate import SkyCoord
from astropy.units import Quantity
from astroquery.gaia import Gaia

import pandas as pd

#matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# Suppress warnings. Comment this out if you wish to see the warning messages
import warnings
warnings.filterwarnings('ignore')

'''
from astroquery.gaia import Gaia
tables = Gaia.load_tables(only_names=True)
for table in (tables):
    print (table.get_qualified_name())
    

job = Gaia.launch_job_async("SELECT * \
FROM gaiadr1.gaia_source \
WHERE CONTAINS(POINT(gaiadr1.gaia_source.ra,gaiadr1.gaia_source.dec),CIRCLE(56.75,24.1167,2))=1;" \
, dump_to_file=True)

print (job)

r = job.get_results()
print (r['source_id'])

plt.scatter(r['pmra'], r['pmdec'], color='r', alpha=0.3)
plt.xlim(-60,80)
plt.ylim(-120,30)

plt.show()

#Retrieve all sources contained in a spherical volume (roughly) 
# centred on the Solar System barycentre, and estimate their distances in light years

dist_lim    = 10.0 * u.lightyear                                # Spherical radius in Light Years
dist_lim_pc = dist_lim.to(u.parsec, equivalencies=u.parallax()) # Spherical radius in Parsec

query = f"SELECT source_id, ra, dec, parallax, distance_gspphot, teff_gspphot, azero_gspphot, phot_g_mean_mag, radial_velocity \
FROM gaiadr3.gaia_source \
WHERE distance_gspphot <= {dist_lim_pc.value}\
AND ruwe <1.4"

job     = Gaia.launch_job_async(query)
results = job.get_results()
print(f'Table size (rows): {len(results)}')

results['distance_lightyear'] = results['distance_gspphot'].to(u.lightyear)
results['radial_velocity_ms'] = results['radial_velocity'].to(u.meter/u.second)
results
'''
# Set Pandas to display all rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

# Define additional columns you want to select
columns_to_select = ["ra", "dec", "phot_g_mean_mag", "parallax", "pmra", "pmdec"]  # Add any other columns you want

# Create a string for the column names to use in the SQL query
columns_string = ", ".join(columns_to_select)

# Your updated SQL query using the specified columns
query = f"""
SELECT TOP 100 {columns_string} FROM gaiadr3.gaia_source  
WHERE has_xp_sampled = 'True'
"""  
# SELECT TOP {} - here you can choose the number of rows shown

# Launch the asynchronous job
job = Gaia.launch_job_async(query)

# Get the results
results = job.get_results()

# Convert results to a Pandas DataFrame
df = results.to_pandas()

# Display the DataFrame
#print(df)

##### filtering by brightness
# Define the brightness lower and upper bounds
lower_bound = 10.0  # Example: stars brighter than magnitude 10
upper_bound = 15.0  # Example: stars fainter than magnitude 15

# Filter the DataFrame for rows where 'phot_g_mean_mag' is between the bounds
filtered_stars_df = df[(df["phot_g_mean_mag"] > lower_bound) & (df["phot_g_mean_mag"] < upper_bound)]

# Display the filtered DataFrame
print(filtered_stars_df)


# Coordinate conversion
import astropy.units as u
import astropy.time
import astropy.coordinates

coord = astropy.coordinates.TETE(
    ra=25 * u.deg,
    dec=45 * u.deg,
    obstime=astropy.time.Time("2023-04-12")
)

coord = coord.transform_to(astropy.coordinates.Galactic())
