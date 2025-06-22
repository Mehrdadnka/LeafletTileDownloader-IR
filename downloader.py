import os
import math
import time
import requests
from concurrent.futures import ThreadPoolExecutor

MIN_LAT, MAX_LAT = 24.0, 40.0
MIN_LON, MAX_LON = 44.0, 63.0
MIN_ZOOM = 6
MAX_ZOOM = 8  # توصیه می‌کنم از 8 شروع کنی، چون بالاتر حجم سنگینی داره
TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
TILES_DIR = "tiles"

HEADERS = {
    "User-Agent": "MapTileDownloader/1.0 (+your_email@example.com)"
}

def latlon_to_tilexy(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

def download_tile(z, x, y, max_retries=3):
    url = TILE_URL.format(z=z, x=x, y=y)
    save_path = os.path.join(TILES_DIR, str(z), str(x))
    os.makedirs(save_path, exist_ok=True)
    filepath = os.path.join(save_path, f"{y}.png")
    if os.path.exists(filepath):
        print(f"Tile {z}/{x}/{y} already downloaded.")
        return
    for attempt in range(1, max_retries+1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"Downloaded tile {z}/{x}/{y}")
            time.sleep(0.2)  # وقفه برای احترام به سرور
            return
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 403:
                print(f"Access forbidden for tile {z}/{x}/{y}. Skipping.")
                return
            else:
                print(f"HTTP error on tile {z}/{x}/{y}: {e}")
        except Exception as e:
            print(f"Error downloading tile {z}/{x}/{y} attempt {attempt}: {e}")
        time.sleep(1)  # قبل از تلاش دوباره صبر کن
    print(f"Failed to download tile {z}/{x}/{y} after {max_retries} attempts.")

def main():
    tasks = []
    for z in range(MIN_ZOOM, MAX_ZOOM + 1):
        x_min, y_max = latlon_to_tilexy(MIN_LAT, MIN_LON, z)
        x_max, y_min = latlon_to_tilexy(MAX_LAT, MAX_LON, z)

        x_start, x_end = sorted([x_min, x_max])
        y_start, y_end = sorted([y_min, y_max])

        print(f"Zoom {z}: x from {x_start} to {x_end}, y from {y_start} to {y_end}")

        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                tasks.append((z, x, y))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda t: download_tile(*t), tasks)

if __name__ == "__main__":
    main()
