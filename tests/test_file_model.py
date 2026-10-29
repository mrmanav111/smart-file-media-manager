import csv
import tempfile
import unittest
from pathlib import Path
from file_model import (file_category, filter_files, readable_size,
                        save_file_report, scan_directory)


class FileModelTests(unittest.TestCase):
    def test_category(self):
        self.assertEqual(file_category('song.MP3'), 'Audio')
        self.assertEqual(file_category('photo.JPG'), 'Images')
        self.assertEqual(file_category('notes.pdf'), 'Documents')
        self.assertEqual(file_category('unknown.xyz'), 'Other')

    def test_sizes_and_boundary(self):
        self.assertEqual(readable_size(0), '0 B')
        self.assertEqual(readable_size(1023), '1023 B')
        self.assertEqual(readable_size(1024), '1.0 KB')
        with self.assertRaises(ValueError):
            readable_size(-1)

    def test_filter(self):
        files = [{'name': 'A.MP3', 'type': 'Audio'},
                 {'name': 'B.JPG', 'type': 'Images'}]
        self.assertEqual(len(filter_files(files)), 2)
        self.assertEqual(len(filter_files(files, 'a', 'Audio')), 1)
        self.assertEqual(filter_files(files, 'missing'), [])
        self.assertEqual(filter_files(files, selected_type='Documents'), [])

    def test_scan_and_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'song.mp3').write_bytes(b'hello')
            Path(folder, 'image.jpg').write_bytes(b'img')
            records, skipped, cancelled = scan_directory(folder)
            self.assertEqual(len(records), 2)
            self.assertEqual(skipped, 0)
            self.assertFalse(cancelled)
            destination = Path(folder, 'report.csv')
            save_file_report(destination, records)
            with destination.open(encoding='utf-8-sig', newline='') as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0][0], 'Name')

    def test_missing_folder(self):
        with self.assertRaises(ValueError):
            scan_directory('some-folder-that-does-not-exist-314159')

    def test_cancelled_scan(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'file.txt').write_text('example')
            records, skipped, cancelled = scan_directory(
                folder, should_cancel=lambda: True)
            self.assertTrue(cancelled)
            self.assertEqual(records, [])


if __name__ == '__main__':
    unittest.main()
