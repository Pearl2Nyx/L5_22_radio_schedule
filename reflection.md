# Reflection - Lab 5: Static Code Analysis

## 1. Which tool did you find most useful, and why?
Bandit gave the most valuable results, because it actally found the three problems that could actually hurt a real system: the SQL injection, `eval()` and the hardcoded password. Pylint found the most issues overall (21 messages, 2.41/10) and also caught design problems such as the `global` counter. Flake8 only reported formatting, which matters for readability but not for correctness.

## 2. Did any tool report something that was a false positive or not worth fixing?
The hardcoded-password warning  is arguably a false positive here, because the constant is never actually used. It still shows a real habit to avoid, so I moved it to an environment variable. The line-length and docstring messages are style rules rather than bugs, so they are less urgent than the security findings. I didnt find a truly wrong report

## 3. How did fixing the issues change the code?
The security and design fixes changed behaviour. Queries are parameterised, `eval` is gone, and bad input raises a clear `ValueError`. Removing the global counter fixed a hidden bug, because `removeSlot` never updated it. The demo output stayed identical, and the final results were Pylint 10.00/10, Bandit is clean and Flake8 clean.

## 4. How would you use static analysis in future projects?
I would run Flake8, Pylint and Bandit automatically in CI and as a pre-commit hook, so problems are caught on every commit instead of at the end. I would fail the build on Bandit High and Medium findings and set a minimum Pylint score. Static analysis cannot prove the code is correct, so I would still write tests, for example one that tries an injection string and invalid hours.
