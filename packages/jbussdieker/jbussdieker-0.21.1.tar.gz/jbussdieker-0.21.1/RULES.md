# `RULES.md` — jbussdieker Development Principles

These rules guide any AI developer working on **`python-jbussdieker`** inside Cursor (or any AI code assistant).

---

## ✅ Purpose

**`jbussdieker`** is a **modern Python project generator** for developers who want **zero friction** from `git init` to PyPI.

A generated project must:

- Work out-of-the-box with no additional configuration.
- Automate linting, testing, versioning, changelogs, and publishing.
- Use **release-please** and **Trusted Publishers** only — no manual secrets.
- Produce a **GitHub-native** repo: squash merges, PR-driven, CI/CD-first.

---

## 📌 Core Principles

1. **Zero-to-PyPI, zero tokens:**
   No API tokens or manual uploads — only OIDC + Trusted Publisher.

2. **One source of truth:**
   Project metadata must live in `pyproject.toml` only (PEP 621). No `setup.py`.

3. **Idiomatic & minimal:**
   No unnecessary files, configs, or hidden complexity. Keep `Makefile` simple and clear.

4. **Best-practice CI/CD:**
   Versioning and changelogs come from `release-please` PRs.

5. **Squash merges enforced:**
   Linear history is required to align with `release-please`.

6. **Latest Python support:**
   Support Python 3.9+ and keep pace with new releases.

---

## ✅ Entrypoint & Entrypoint Testing Best Practices

### 📦 Structure

- `__main__.py` must do **nothing** but import and call `main()`.

  ```py
  from jbussdieker.cli import main

  if __name__ == "__main__":  # pragma: no cover
      main()
  ```

* Actual CLI logic **must** live in `cli.py` (or equivalent) for testability.
* Define `main(argv=None)` to allow unit testing with explicit arguments.

### ⚙️ Packaging

* Declare the console script in `pyproject.toml` using `[project.scripts]`:

  ```toml
  [project.scripts]
  jbussdieker = "jbussdieker.cli:main"
  ```

  This guarantees `python -m jbussdieker` and `jbussdieker` do the same thing.

### ✅ Unit Testing

* Unit test the `cli:main()` directly — pass `argv` to simulate user input.
* Use `monkeypatch` to stub `sys.stdout`, env vars, or configs as needed.

### ✅ Integration Testing

* Add a subprocess test that runs `python -m jbussdieker` to confirm:

  * `__main__.py` exists and works.
  * The packaging + entrypoint are wired correctly.
* Example:

  ```py
  subprocess.run([sys.executable, "-m", "jbussdieker", ...])
  ```

### 🟢 Coverage

* The `if __name__ == "__main__"` block must be excluded from coverage checks:

  ```py
  if __name__ == "__main__":  # pragma: no cover
      main()
  ```
* Rely on the subprocess test for runtime coverage.

### 🔒 Key Principle

**Keep logic out of `__main__.py`.**
Use it only as a bridge to real, testable code.
Validate both `-m` execution and installed scripts.

---

## ✅ Allowed Enhancements

Cursor may suggest:

* Improvements to **GitHub Actions workflows** (e.g., caching, fail states).
* New `Makefile` tasks for local dev (keep them simple).
* Better **README** scaffolding for new users.
* Optional plug-ins gated behind flags (e.g., optional `pytest` if `unittest` is disabled).

**Note:** By default, `unittest` is the canonical test framework for generated projects.

---

## 🚫 Disallowed Changes

* No **API key secrets**, `.pypirc`, or legacy publish flows.
* No non-PEP 621 packaging (`setup.py`, `setup.cfg`).
* No large, opinionated frameworks (Flask/Django). Stay framework-agnostic.
* No vendor-specific CD outside **GitHub Actions**.
* Do not add other testing frameworks unless explicitly made optional.

---

## 🪝 Future-Proofing

* Generated projects must be **easily editable**: workflows, metadata, and environments should be trivial to customize.
* Keep **PyPI Trusted Publisher** instructions accurate.
* Any breaking changes in templates must bump the major version.

---

## ⚙️ Local Development

When modifying `jbussdieker` itself, follow these standards:

* Small, atomic PRs only.
* Use semantic commits (`feat:`, `fix:`, `docs:`).
* **Maintain 100% test coverage**, including entrypoints.
* Keep `pyproject.toml`, `Makefile`, and GitHub Actions idiomatic and minimal.

---

## ✅ Examples

**Allowed:**

* `feat: add poetry.lock option if user opts in`
* `feat: add pytest support if user disables unittest`
* `docs: clarify OIDC for release-please`

**Disallowed:**

* `feat: add legacy setuptools support`
* `feat: add PyPI token env var`
* `feat: add custom bash release scripts`

---

## ✨ Final Rule

> **When in doubt: Less is more.**
> The user should spend *zero time* debugging the generated project.
> `jbussdieker` should *just work* — add features only if they uphold that promise.

---

## 📝 Rule Management

This project uses a dual-file approach for AI rules:

* **`.cursor/rules`** — primary source for AI editors (concise, task-oriented).
* **`RULES.md`** — human-readable documentation (detailed explanations and examples).

Always update **both** to keep them in sync.
