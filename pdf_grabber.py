import os
import time
from pathlib import Path
from urllib.parse import unquote
import requests

BASE_URL = "https://www.grc.com/sn/"
OUTPUT_DIR = "securitynow_pdfs"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def download_file(url, folder):
    local_filename = os.path.join(folder, unquote(Path(url).name))
    if os.path.exists(local_filename):
        print(f"Skipping {local_filename} (already exists)")
        return True

    try:
        with requests.get(url, stream=True, timeout=30, headers={'User-Agent': USER_AGENT}) as r:
            if r.status_code == 200:
                print(f"Downloading {url}...")
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            elif r.status_code == 404:
                return False
            else:
                print(f"Failed to download {url} (Status: {r.status_code})")
                return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Episode ranges by year. 2026 uses 9999 as a sentinel — the consecutive-failure
    # guard (max_consecutive_failures) terminates the loop once episodes run out.
    year_map = {
        2005: (1, 19), 2006: (20, 71), 2007: (72, 123), 2008: (124, 175),
        2009: (176, 227), 2010: (228, 279), 2011: (280, 331), 2012: (332, 383),
        2013: (384, 435), 2014: (436, 487), 2015: (488, 539), 2016: (540, 591),
        2017: (592, 643), 2018: (644, 695), 2019: (696, 747), 2020: (748, 799),
        2021: (800, 851), 2022: (852, 903), 2023: (904, 954), 2024: (955, 1005),
        2025: (1006, 1058), 2026: (1059, 9999)
    }

    try:
        user_input = input("Enter the year you would like to download (2005-2026): ").strip()
        year = int(user_input)
        if year not in year_map:
            print("Year must be between 2005 and 2026.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid year.")
        return

    start_ep, end_ep = year_map[year]
    episode = start_ep
    consecutive_failures = 0
    max_consecutive_failures = 5

    print(f"Starting download for year {year} (Episodes {start_ep} to {end_ep if end_ep < 9999 else '...'}) to '{OUTPUT_DIR}'...")

    while episode <= end_ep and consecutive_failures < max_consecutive_failures:
        # zfill(3) pads single/double-digit episodes; numbers >= 1000 are unaffected
        ep_str = str(episode).zfill(3)

        urls_to_try = [
            f"{BASE_URL}sn-{ep_str}.pdf",
            f"{BASE_URL}sn-{ep_str}-notes.pdf",
            f"{BASE_URL}sn-{ep_str}-transcript.pdf"
        ]

        # found_any stays True if any variant (main pdf, notes, or transcript) downloaded
        found_any = False
        for url in urls_to_try:
            if download_file(url, OUTPUT_DIR):
                found_any = True

        if found_any:
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            if consecutive_failures > 1:
                print(f"Episode {episode} not found (Consecutive misses: {consecutive_failures})")

        episode += 1
        time.sleep(0.1) # Be nice to the server

    print("Download finished.")

if __name__ == "__main__":
    main()
