# Bolt's Journal

## 2025-12-18 - Python String Concatenation and Git Hygiene
**Learning:** Python string concatenation using `+=` in loops can be inefficient ($O(N^2)$) for large strings. Using list accumulation and `''.join()` is preferred ($O(N)$). Also, executing Python scripts generates `__pycache__` artifacts which must be ignored in `.gitignore`.
**Action:** Always prefer `list.append()` and `''.join()` for building large strings in loops. Ensure `.gitignore` includes `__pycache__/` and `*.pyc` before running Python scripts.
