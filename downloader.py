import os                      # For directory and file handling
import math                    # For mathematical functions, like radians and log
import time                    # For delays between requests
import requests                # For HTTP requests to download tiles
from concurrent.futures import ThreadPoolExecutor  # For parallel downloads using threads

# Define geographic bounding box for Iran region (latitude and longitude)
MIN_LAT, MAX_LAT = 24.0, 40.0
MIN_LON, MAX_LON = 44.0, 63.0

# Define minimum and maximum zoom levels for tile downloads
MIN_ZOOM = 6
MAX_ZOOM = 8  # Higher zooms are heavier and need faster internet

# URL template for OpenStreetMap tiles
TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

# Directory where downloaded tiles will be saved
TILES_DIR = "tiles"

# HTTP headers including a custom User-Agent to identify the downloader responsibly
HEADERS = {
    "User-Agent": "MapTileDownloader/1.0 (+your_email@example.com)"
}

def latlon_to_tilexy(lat, lon, zoom):
    """
    Convert latitude and longitude to tile X and Y coordinates at a given zoom level.
    Uses the standard Web Mercator projection formulas.
    """
    lat_rad = math.radians(lat)  # Convert latitude to radians
    n = 2.0 ** zoom              # Number of tiles in one direction at this zoom level
    xtile = int((lon + 180.0) / 360.0 * n)  # Calculate tile X coordinate
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)  # Calculate tile Y coordinate
    return xtile, ytile          # Return tile coordinates as integers

def download_tile(z, x, y, max_retries=3):
    """
    Download a single map tile at zoom z and tile coordinates (x, y).
    Tries up to max_retries times in case of network or HTTP errors.
    """
    url = TILE_URL.format(z=z, x=x, y=y)  # Format tile URL
    save_path = os.path.join(TILES_DIR, str(z), str(x))  # Construct directory path for this zoom and x
    os.makedirs(save_path, exist_ok=True)  # Create directories if they don't exist
    filepath = os.path.join(save_path, f"{y}.png")  # Full path for the tile image file

    if os.path.exists(filepath):  # Skip download if file already exists
        print(f"Tile {z}/{x}/{y} already downloaded.")
        return

    for attempt in range(1, max_retries + 1):  # Retry loop
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)  # HTTP GET with timeout and headers
            resp.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)
            with open(filepath, 'wb') as f:  # Write response content to file
                f.write(resp.content)
            print(f"Downloaded tile {z}/{x}/{y}")
            time.sleep(0.2)  # Sleep briefly to respect server load
            return  # Successful download, exit function

        except requests.exceptions.HTTPError as e:  # Handle HTTP errors separately
            if resp.status_code == 403:
                print(f"Access forbidden for tile {z}/{x}/{y}. Skipping.")  # Forbidden - don't retry
                return
            else:
                print(f"HTTP error on tile {z}/{x}/{y}: {e}")  # Other HTTP errors

        except Exception as e:  # Handle other exceptions like connection errors
            print(f"Error downloading tile {z}/{x}/{y} attempt {attempt}: {e}")

        time.sleep(1)  # Wait before retrying download

    print(f"Failed to download tile {z}/{x}/{y} after {max_retries} attempts.")  # Final failure message

def main():
    tasks = []  # List to hold all tile download tasks

    # Loop over each zoom level in the defined range
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        # Convert geographic bounding box corners to tile coordinates
        x_min, y_max = latlon_to_tilexy(MIN_LAT, MIN_LON, z)
        x_max, y_min = latlon_to_tilexy(MAX_LAT, MAX_LON, z)

        # Sort tile coordinate ranges to ensure correct iteration order
        x_start, x_end = sorted([x_min, x_max])
        y_start, y_end = sorted([y_min, y_max])

        print(f"Zoom {z}: x from {x_start} to {x_end}, y from {y_start} to {y_end}")

        # Append every tile coordinate within bounding box to the task list
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                tasks.append((z, x, y))

    # Use ThreadPoolExecutor to download tiles concurrently (max 4 threads)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda t: download_tile(*t), tasks)  # Map each task tuple to download_tile function

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
