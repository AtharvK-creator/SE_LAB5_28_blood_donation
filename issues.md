# Lab 5: Static Code Analysis — Issues and Fixes

**Project:** Blood Donation Management System

Note: Line numbers below refer to the original code before fixes.

## Identified Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command execution — B605 | Security: High | 65 | `os.system()` executed a shell command constructed from phone numbers, creating a potential command-injection vulnerability. | Replaced shell execution with `subprocess.run()` using a list of arguments and `shell=False`. The executable path is resolved using `shutil.which()`. |
| Insecure temporary-file creation — B306 | Security: Medium | 60 | `tempfile.mktemp()` generated a filename without securely creating the file, introducing a potential race condition. | Replaced it with `tempfile.NamedTemporaryFile()` and `delete=False`. |
| Hardcoded password — B105 | Security: Low | 5 | A password string was hardcoded in the source code. | Removed the unused password constant. |
| Assertion used for validation — B101 | Security / Reliability: Low | 18 | An assertion was used to validate a blood group. Assertions can be disabled when Python runs with optimization. | Replaced the assertion with explicit validation using `ValueError`. |
| Mutable default argument — W0102 | Code quality | 17 | Using `notes=[]` could retain state between function calls because the same default list is reused. | Changed the default to `None` and initialized the list inside the function. |
| Broad exception handling — W0718 | Reliability | 45 | Catching `Exception` could conceal unexpected errors. | Added explicit blood-group validation and removed broad exception handling from the lookup function. |
| Function and parameter naming — C0103 | Code style | Multiple | CamelCase names did not follow Python's snake_case naming convention. | Renamed functions and parameters consistently and updated their call sites. |
| Missing docstrings — C0114/C0116 | Code quality | Multiple | The module and functions lacked documentation strings. | Added module and function docstrings. |
| Formatting violations — E501/E303/E261/E225 | Code style | Multiple | The original file contained a long line, excess blank lines, incorrect inline-comment spacing, and missing operator whitespace. | Reformatted the code to follow the configured Flake8 style rules. |

## Verification Results

- Initial Pylint score: 4.81/10.
- Intermediate Pylint score: 6.21/10.
- Later Pylint score: 9.84/10.
- Final Pylint score: 10.00/10.
- Final Flake8 run: no reported violations.
- Final program execution: successful, with the expected demonstration output.
- Bandit: no high- or medium-severity findings in the latest run; two low-severity subprocess-related warnings remain.

The changes improved code style, maintainability, and security practices while preserving the demonstration's behavior.
