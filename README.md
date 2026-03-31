# FileOrganizer
Python File Organizer: Photo Edition
A Python-based automation tool designed to declutter and organize large collections of personal photos. This project sorts files into a logical directory structure based on their creation date (Year/Month), making them easy to browse and search.

## Features
Automated Sorting: Automatically scans a source directory and moves files to a structured destination.
Time-Based Organization: Creates folders based on the year and month (e.g., 2024/05/).
Metadata Accuracy: Uses file system creation time to ensure photos end up in the right place.
Collision Prevention: (Optional/Planned) Handles duplicate filenames to prevent data loss.

## Tech Stack
Language: Python 3.14
Modules: os, shutil, datetime, pathlib

## How It Works
The script follows a simple logic flow to ensure your photos are moved safely:
Scan: Iterates through all files in the designated "Input" folder.
Extract: Retrieves the creation timestamp from each file.
Create: Checks if the corresponding Year/Month folders exist; if not, it creates them.
Move: Transfers the file from the source to its new organized home.
