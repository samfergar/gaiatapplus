import pandas as pd
import numpy as np

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

# Example Cartesian coordinates
cartesian_coords = np.array([[1.0, 2.0, 3.0],  # Example 1
                              [-1.0, -2.0, -3.0],  # Example 2
                              [0.0, 0.0, 1.0]])  # Example 3 (at North Celestial Pole)

# Convert and print the celestial coordinates for each Cartesian coordinate
for coord in cartesian_coords:
    x, y, z = coord
    ra, dec = cartesian_to_celestial(x, y, z)
    print(f"Cartesian: (x={x}, y={y}, z={z}) => Celestial: (RA={ra:.2f}°, Dec={dec:.2f}°)")
