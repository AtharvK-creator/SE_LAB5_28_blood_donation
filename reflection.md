# Lab 5: Static Code Analysis — Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues were formatting violations, naming conventions, and missing docstrings because they involved straightforward changes to code style and documentation.

The harder issues were security-related findings, such as unsafe temporary-file creation and shell command execution. These required understanding the risks and replacing the original implementations without changing the intended program behavior.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Bandit continued to report low-severity warnings B404 and B603 for the use of the subprocess module and subprocess execution. These warnings require review but do not automatically prove that the code is vulnerable.

The updated implementation uses `shell=False`, passes arguments as a list, and resolves the executable path. These measures reduce shell-injection and executable-path risks. However, the remaining warnings should still be considered, and phone-number inputs should be validated before using the SMS helper. I did not confirm a definite false positive during this exercise.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Pylint, Flake8, and Bandit regularly while developing and before committing code. I would also configure GitHub Actions to run these tools automatically whenever changes are pushed or a pull request is opened.

I would prioritize security findings and potential bugs, review warnings before suppressing them, and rerun the tools after applying fixes. This would help detect problems early and maintain consistent code quality.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The code became more readable through consistent naming, docstrings, and formatting. Explicit validation and removal of broad exception handling made error handling clearer. Replacing unsafe temporary-file creation and shell-command construction improved security practices.

The Pylint score increased from 4.81/10 to 10.00/10, and the final Flake8 run reported no violations. The program also ran successfully after the changes and retained its expected demonstration output.
