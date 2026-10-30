# Smart File & Media Manager — Distribution Guide

## 1. Distribution Method

The Smart File & Media Manager application was packaged using PyInstaller 6.22.3 on Windows 11 with Python 3.13.0.

A one-folder (`--onedir`) distribution method was selected. This includes the executable and its required supporting files in one folder.

## 2. Build Command

```powershell
py -m PyInstaller --noconfirm --clean --windowed --onedir --name SmartFileMediaManager main.py
```

The build completed successfully and generated the application inside `dist/SmartFileMediaManager/`.

## 3. How to Run

1. Extract the distribution ZIP file.
2. Open the `SmartFileMediaManager` folder.
3. Double-click `SmartFileMediaManager.exe`.
4. Choose a folder, scan files and use the application.

The user does not need to install Python separately. The complete distribution folder must be kept together.

## 4. Packaged Application Testing

The packaged application was tested on the development computer.

| Test | Result |
|---|---|
| Launch the EXE | Pass |
| Select and scan a folder | Pass |
| Search and filter files | Pass |
| Play and pause MP3 audio | Pass |
| Preview an image | Pass |
| Export a CSV report | Pass |
| Cancel an active scan | Pass |
| Close and reopen the application | Pass |

**Result:** All 8 tests passed.

## 5. Limitations

The application was packaged for Windows. Compatibility with other operating systems was not tested. Testing on another Windows computer without Python installed is still recommended.

## 6. Conclusion

The Windows executable was successfully built and tested. The application can be launched directly, and its main features worked during packaged application testing.