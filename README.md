# Security Now PDF Downloader

This script was Vibe Coded with Gemini Pro

A Python script to download "Security Now" podcast PDFs (Show Notes, Transcripts, etc.) from GRC.com, organized by year.

## Features

- **Year Selection:** Allows users to choose a specific year (2005-2026) to download content for.
- **Smart Mapping:** Automatically maps years to the correct episode ranges.
- **Resumable:** Checks if a file already exists before downloading to avoid duplicates.
- **Variety:** Attempts to download standard PDFs, show notes, and transcripts for each episode.
- **Polite:** Includes a small delay between requests to reduce load on the GRC servers.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone or download this repository.
2. Install the required Python dependency:

   ```bash
   pip install requests
   ```

## Usage

Run the script from your terminal:

```bash
python3 pdf_grabber.py
```

When prompted, enter the year you wish to download (between 2005 and 2026).

Example interaction:
```text
Enter the year you would like to download (2005-2026): 2023
Starting download for year 2023 (Episodes 904 to 954) to 'securitynow_pdfs'...
Downloading https://www.grc.com/sn/sn-904.pdf...
...
```

The files will be saved in the `securitynow_pdfs` directory within the same folder.

## Disclaimer

This script is for personal archiving purposes. Please respect the bandwidth of the host (GRC.com). The script includes a built-in delay to be polite to the server.
