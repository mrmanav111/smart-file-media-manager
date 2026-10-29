# Smart File & Media Manager — test plan (Tasks 9 and 10)

The aim is to check that each feature works as expected. Enter the actual result, date and Pass/Fail **after running the final version on your computer**. These are planned tests, not claimed results.

| ID | Requirement | Test input / condition | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| T01 | FR01 | Start Scan before selecting a folder | Warning appears | To test | To test |
| T02 | FR01, FR02 | Select a folder with MP3, PDF and JPG files; scan | File details appear | To test | To test |
| T03 | FR03 | Search for part of an existing name | Matching files only | To test | To test |
| T04 | FR03 | Filter to Audio | Audio rows only | To test | To test |
| T05 | FR04 | Select MP3; Play, Pause, Play | Playback starts, pauses, resumes | To test | To test |
| T06 | FR04 | Select image | Preview appears for supported image | To test | To test |
| T07 | FR04, FR07 | Select PDF or non-audio; click Play if available | Audio button unavailable | To test | To test |
| T08 | FR05, FR06 | Scan a folder with many files | GUI responds and count increases | To test | To test |
| T09 | FR05 | Start large scan, then Cancel | Stops safely, partial results shown | To test | To test |
| T10 | FR08 | Export after successful scan | CSV produced with matching rows | To test | To test |
| T11 | FR08 | Export before any scan | Information message | To test | To test |
| T12 | FR07 | Select folder, remove it before scanning | Folder unavailable warning | To test | To test |
| T13 | FR03 | Search for a name not present | Empty table, no crash | To test | To test |
| T14 | FR02 | Scan an empty folder | Zero rows, scan completes | To test | To test |
| T15 | FR07 | Try exporting to location without write access | Export error message | To test | To test |
| T16 | GUI | Open File > Open Folder; Help > About; File > Exit | Each menu works | To test | To test |
| T17 | Thread safety | Search or resize while background scan is active | GUI stays responsive | To test | To test |

Screenshots to collect: the main application with data, scan progress, export, audio playing, invalid-input warning and automated-test terminal output.

## Automated tests (Task 11)
Run `py -m unittest discover -s tests -v`. Tests cover categories, boundaries, filtering, scanning, cancellation and CSV generation. Audio playback and GUI actions require manual tests because speakers and interface actions depend on the user's Windows machine.
