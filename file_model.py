import csv
import os
from pathlib import Path

IMAGE_TYPES = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
AUDIO_TYPES = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}
DOCUMENT_TYPES = {'.pdf', '.txt', '.doc', '.docx', '.csv', '.xlsx', '.xls', '.pptx'}


def file_category(path):
    extension = Path(path).suffix.lower()
    if extension in IMAGE_TYPES:
        return 'Images'
    if extension in AUDIO_TYPES:
        return 'Audio'
    if extension in DOCUMENT_TYPES:
        return 'Documents'
    return 'Other'


def readable_size(size):
    if size < 0:
        raise ValueError('File size cannot be negative')
    if size < 1024:
        return f'{size} B'
    if size < 1024 ** 2:
        return f'{size / 1024:.1f} KB'
    if size < 1024 ** 3:
        return f'{size / (1024 ** 2):.1f} MB'
    return f'{size / (1024 ** 3):.1f} GB'


def filter_files(files, search='', selected_type='All files'):
    text = search.strip().casefold()
    return [item for item in files
            if (not text or text in item['name'].casefold())
            and (selected_type == 'All files' or item['type'] == selected_type)]


def scan_directory(folder, on_progress=None, should_cancel=None):
    """Return (records, skipped, cancelled). Does not touch any Qt widgets."""
    if not os.path.isdir(folder):
        raise ValueError('Please select an existing folder.')
    records = []
    skipped = 0
    cancelled = False

    def walk_error(_error):
        nonlocal skipped
        skipped += 1

    for root, dirs, names in os.walk(folder, onerror=walk_error):
        if should_cancel and should_cancel():
            cancelled = True
            break
        for name in names:
            if should_cancel and should_cancel():
                cancelled = True
                break
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                skipped += 1
                continue
            records.append({'name': name, 'type': file_category(path),
                            'size': size, 'location': path})
            if on_progress and len(records) % 25 == 0:
                on_progress(len(records))
        if cancelled:
            break
    records.sort(key=lambda item: (item['name'].casefold(), item['location'].casefold()))
    return records, skipped, cancelled


def save_file_report(destination, files):
    with open(destination, 'w', newline='', encoding='utf-8-sig') as output:
        writer = csv.writer(output)
        writer.writerow(['Name', 'Type', 'Size (bytes)', 'Location'])
        for item in files:
            writer.writerow([item['name'], item['type'], item['size'], item['location']])
