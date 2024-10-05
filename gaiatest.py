
#
from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"  # Data Release 3, default

import astropy.units as u
from astropy.coordinates import SkyCoord

coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')
width = u.Quantity(0.1, u.deg)
height = u.Quantity(0.1, u.deg)
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

r.pprint(max_lines=12, max_width=130)

#Gaia.ROW_LIMIT controls the number of rows. -1 for unlimited rows

#Cone search
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia

Gaia.ROW_LIMIT = 50  # Ensure the default row limit.
coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')
#RA (right ascension) and Dec (declination) are the coordinates 
# on the sky that correspond to longitude and latitude on Earth.
j = Gaia.cone_search_async(coord, radius=u.Quantity(1.0, u.deg))

r = j.get_results()
r.pprint()



