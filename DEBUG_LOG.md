# Task 12 — Debugging and corrections

Record only defects you actually observed and the outcome of retesting.

| Issue | Cause | Correction | Retest status |
|---|---|---|---|
| Start Scan initially showed a placeholder rather than loading files | Starter interface had no real scanner connection | Added folder scanning and table updates | Earlier version: user successfully scanned 350 files; retest final version |
| `ModuleNotFoundError: No module named 'file_model'` | `file_model.py` was not present in the running project folder | Created `file_model.py` beside `main.py` and matched the import name | Final version: to test |
| Additional issues | Add after final testing | Add correction | To test |

For each new problem, note the date, reproduction steps, probable cause, exact code change and result of rerunning the related test. Commit the fix with Git when Task 13 begins.
