# jbussdieker

**A modern Python development toolkit with a modular plugin architecture — from project scaffolding to AI-powered commits with automated releases.**

## 🚀 What it does

**`jbussdieker`** is your complete Python development toolkit built with a modular plugin system:

**Core CLI Framework:**
- ✅ Lightweight CLI with plugin discovery via entry points
- ✅ Configurable logging and settings management
- ✅ Extensible command system for plugins

**Plugin Ecosystem:**
- ✅ **`jbussdieker-project`** — Project scaffolding and templates
- ✅ **`jbussdieker-commit`** — AI-powered conventional commit messages
- ✅ **`jbussdieker-app`** — Application framework and utilities
- ✅ **`jbussdieker-service`** — Service layer and API utilities
- ✅ **`jbussdieker-storage`** — Data storage and persistence layer
- ✅ **`jbussdieker-config`** — Configuration management (core dependency)

**Modern Python Development:**
- ✅ **release-please** workflow for versioning and changelogs
- ✅ Publish to **PyPI** using [Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- ✅ GitHub Actions CI for linting, typing, tests, and publishing

**No tokens. No manual uploads. Just push, merge, and release.**

## 📦 Install

### Core CLI
```bash
pip install jbussdieker
```

### With all plugins
```bash
pip install jbussdieker[all]
```

### Individual plugins
```bash
# Project scaffolding
pip install jbussdieker[project]

# AI-powered commits
pip install jbussdieker[commit]

# Application framework
pip install jbussdieker[app]

# Service layer
pip install jbussdieker[service]

# Storage layer
pip install jbussdieker[storage]
```

## 🔌 Plugin Ecosystem

### `jbussdieker-project` — Project Scaffolding
Create modern Python projects with zero friction:

```bash
jbussdieker project create myproject
cd myproject
git init
git commit --allow-empty -m "chore: init"
gh repo create --source=. --private --push
git add .
git commit -m "feat: initial commit"
git push
```

**Features:**
- ✅ `pyproject.toml` using **PEP 621**
- ✅ GitHub Actions CI for linting, typing, tests, and publishing
- ✅ `Makefile` with simple install, lint, test commands
- ✅ `.gitignore` for Python best practices
- ✅ **release-please** workflow for versioning and changelogs
- ✅ Publish to **PyPI** using Trusted Publishers

### `jbussdieker-commit` — AI-Powered Commits
Generate conventional commit messages using AI:

```bash
# Stage your changes
git add .

# Generate and edit a commit message
jbussdieker commit

# Or preview the message without committing
jbussdieker commit --dry-run
```

**Features:**
- 📝 Generate conventional commit messages (feat, fix, docs, etc.)
- 🔍 Analyze your staged changes and project context
- ✏️ Open your editor for final review and editing
- 🚀 Create the commit with your approved message

**Requirements:**
- OpenAI API key in `OPENAI_API_KEY` environment variable
- Staged changes in your git repository
- Your preferred editor (defaults to `vim`)

### `jbussdieker-app` — Application Framework
Build modern Python applications with best practices:

```bash
jbussdieker app create myapp
cd myapp
# Start building your application
```

**Features:**
- 🏗️ Application scaffolding with proper structure
- 🔧 Configuration management integration
- 📦 Dependency management and packaging
- 🧪 Testing framework setup
- 🚀 Deployment-ready structure

### `jbussdieker-service` — Service Layer
Build robust service-oriented applications:

```bash
jbussdieker service create myservice
cd myservice
# Build your service layer
```

**Features:**
- 🔌 Service discovery and registration
- 📡 API utilities and middleware
- 🔒 Authentication and authorization helpers
- 📊 Monitoring and health checks
- 🚀 Scalable service architecture

### `jbussdieker-storage` — Data Storage
Manage data persistence across different backends:

```bash
jbussdieker storage create mystorage
cd mystorage
# Configure your storage layer
```

**Features:**
- 💾 Multi-backend storage support
- 🔄 Data migration utilities
- 🔍 Query builders and ORM helpers
- 🛡️ Data validation and sanitization
- 📈 Performance monitoring

### `jbussdieker-config` — Configuration Management
Centralized configuration for all your applications:

```bash
# Configuration is automatically managed
# across all jbussdieker plugins
```

**Features:**
- ⚙️ Environment-based configuration
- 🔐 Secure secret management
- 📝 YAML/TOML/JSON support
- 🔄 Hot-reload capabilities
- 🧪 Test configuration helpers

## ✅ Set up automated releases

1️⃣ **Ensure GitHub Actions has required permissions**

For `release-please` to work, your repository's Actions must have write access and permission to create PRs.

* **Allow workflows to write to your repo:**
   - Go to your repo's **Settings → Actions → General** ([GitHub Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-default-github_token-permissions))
   - Under **Workflow permissions**, select **Read and write permissions**

* **Allow Actions to create PRs:**
   - In the same [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#preventing-github-actions-from-creating-or-approving-pull-requests)
   - Check **Allow GitHub Actions to create and approve pull requests**

2️⃣ **Add a Trusted Publisher on PyPI**

Configure PyPI to trust your GitHub repo for publishing

* Visit [PyPI Publishing](https://pypi.org/manage/account/publishing/)
* Scroll down to add a new pending publisher
* Fill out:

  * **GitHub Owner** → your username or org
  * **Repository Name** → your repo name (`myproject`)
  * **Workflow Name** →

    ```plaintext
    publish.yml
    ```
  * **Environment Name** →

    ```plaintext
    release
    ```
* Click **Add**.

3️⃣ **Push your first tag**

Once `release-please` opens a version bump PR, merging it will automatically publish your package. No API keys needed — PyPI trusts your GitHub Action.

## 🧹 Local development

Your project includes a simple `Makefile`:

```bash
make venv    # create .venv
make install # pip install -e .
make lint    # black + mypy
make format  # run black
make test    # run unittest
make clean   # remove .venv
```

## 🔒 Recommended GitHub repo settings

- ✅ **Use Squash merge only** — keeps your history tidy and is required for a linear commit history.
  [See why release-please recommends this.](https://github.com/googleapis/release-please?tab=readme-ov-file#linear-git-commit-history-use-squash-merge)
- ✅ Enable **Auto-delete branches after merge**

## 📢 Example workflow

```bash
# 1️⃣ Scaffold the project locally
jbussdieker project create myproject
cd myproject

# 2️⃣ Init the repo with an empty commit to push just the structure
git init
git commit --allow-empty -m "chore: init"  # ensures a branch exists for first push
gh repo create --source=. --public --push

# ⏸️ This step ensures your repo exists on GitHub first,
# so you can safely configure required Actions + PyPI before any workflows run!

# 3️⃣ Now pause — go to GitHub and:
#    ✅ Set Workflow permissions to Read & Write
#    ✅ Allow Actions to create & approve PRs
#    ✅ Add PyPI Trusted Publisher if you like

# 4️⃣ Add the actual files
git add .
# Optionally use AI-powered commits:
# jbussdieker commit
# Or traditional commit:
git commit -m "feat: initial code"
git push

# 5️⃣ Merge your first release-please PR 🚀
```

## 🔌 Plugin Development

Want to extend `jbussdieker` with your own plugins? The CLI uses entry points for plugin discovery:

```python
# In your plugin's setup.py or pyproject.toml
[project.entry-points."jbussdieker.cli"]
myplugin = "myplugin.cli:register"
```

```python
# myplugin/cli.py
def register(subparsers):
    parser = subparsers.add_parser("myplugin", help="My plugin command")
    parser.add_argument("--option", help="My option")
    parser.set_defaults(func=myplugin_command)

def myplugin_command(args, config):
    # Your plugin logic here
    pass
```

## 📝 License

This project is licensed under **MIT**.

## 🎉 Ship faster

No config sprawl. No secrets rotation. Just `git push` and publish Python packages the *modern* way with a modular, extensible toolkit.

---

**Enjoy! 🚀**
