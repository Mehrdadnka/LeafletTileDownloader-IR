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
