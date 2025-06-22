# LeafletTileDownloader-IR

A Python script to automatically download offline map tiles for the Iran region from OpenStreetMap tile servers.  
Designed for developers and researchers who need offline access to map tiles within specific geographic bounds and zoom levels, usable in Leaflet or other map visualization libraries.

---

## Features

- **Geographic coverage:** Downloads map tiles covering Iran's bounding box (Latitude: 24.0 to 40.0, Longitude: 44.0 to 63.0).
- **Zoom levels:** Supports downloading tiles for zoom levels from 6 to 8 by default (configurable).
- **Concurrent downloads:** Utilizes Python's `ThreadPoolExecutor` for parallel tile downloads, speeding up the process while respecting server load.
- **Retry logic:** Implements retry attempts on network or HTTP errors with graceful handling of forbidden (403) responses.
- **User-Agent header:** Sends a custom User-Agent string with requests to identify the downloader responsibly.
- **Folder structure:** Saves tiles in an organized folder hierarchy `{zoom}/{x}/{y}.png` for easy integration with mapping libraries.
- **Respectful throttling:** Includes configurable delays (`time.sleep`) between requests to avoid overwhelming the tile server.

---

## Requirements

- Python 3.7 or higher
- `requests` library

Install dependencies via pip:

```bash
pip install requests
```

## Usage

- Clone or download the repository:

```bash
git clone https://github.com/YourUsername/LeafletTileDownloader-IR.git
cd LeafletTileDownloader-IR
```

- (Optional) Modify geographic bounds or zoom levels in the script (downloader.py) as needed.

- Run the downloader script:
```bash
python downloader.py

```

-Downloaded tiles will be saved under the tiles/ directory.

## Important Notes

- Server Usage Policy:
Please ensure your usage respects OpenStreetMap's tile usage policy:

OpenStreetMap Tile Usage Policy

Avoid heavy bulk downloads or high-frequency requests.

For large-scale or commercial use, consider setting up your own tile server.

## Respectful Downloading:
- The script includes a small delay (default 0.2 seconds) between tile downloads to reduce server load.

- Adjust this delay in the code if necessary to be more respectful or faster.

## Future Enhancements
- Add command-line arguments to specify custom geographic bounding boxes and zoom ranges.
- Support higher zoom levels with smarter rate limiting and improved error handling.
- Option to compress downloaded tiles to save disk space.
- Resume interrupted downloads to avoid starting over.
- Add a GUI interface for easier configuration and progress monitoring.
- Support other tile servers or map providers (e.g., Mapbox) with proper compliance.
- Implement caching and tile integrity verification.

## Use Case in Archaeological and Geospatial Research
This tool can be invaluable for archaeologists and geospatial analysts working in Iran or surrounding regions, enabling:
- Offline access to base maps for fieldwork in remote or internet-limited locations.
- Integration of downloaded tiles with GIS software for spatial analysis.
- Creation of custom offline maps highlighting archaeological sites.
- Reducing dependency on internet connectivity during research expeditions.

## License
This project is licensed under the MIT License.

Please respect all third-party server terms and conditions when using this script.

## Author

**Mehrdadnka**
Email: *\[mehrdad2762@gmail.com]*
GitHub: *https://github.com/Mehrdadnka*

Feel free to open issues or submit pull requests for improvements!
