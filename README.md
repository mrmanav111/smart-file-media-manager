# Smart File & Media Manager

This desktop application helps users scan folders, filter files, preview images, play audio and export CSV reports. It uses Python and PyQt6.

## Setup on Windows

Open this folder in VS Code. Run:

```powershell
py -m pip install -r requirements.txt
py main.py
```

To run automated tests:

```powershell
py -m unittest discover -s tests -v
```

To run the sequential/threaded performance comparison:

```powershell
py performance.py "D:/music"
```

## Files and architecture

- `main.py`: application entry point
- `main_window.py`: View, builds controls and menus
- `controller.py`: Controller, connects events and updates GUI
- `file_model.py`: Model, file information, filtering and CSV logic
- `workers.py`: scans using a QThread, sends Qt signals to GUI, supports cancellation
- `performance.py`: sequential and threaded processing comparison
- `tests/test_file_model.py`: automated model tests
- `TEST_PLAN.md`, `PERFORMANCE_NOTES.md`, `DEBUG_LOG.md`: testing and analysis records

## Thread safety

The worker scans files and creates its own result list. It **does not update Qt widgets directly**. Qt signals deliver progress and complete results to the controller, which updates the table on the main GUI thread. A `threading.Event` is used only to request cancellation safely. The GUI prevents starting a second scan while one is running.

The scan uses an indefinite/busy progress bar because total file count is not known in advance; it changes to 100% on successful completion. The live file count indicates progress during scanning.

## Scope and limitations

Metadata scanning includes subfolders. Some inaccessible files are skipped with a warning. Audio playback depends on codecs available through Qt on the target machine. Very large directories can consume memory because the application stores records and builds a table. Final Windows testing, evidence, Git work, packaging and presentation are separate tasks.
