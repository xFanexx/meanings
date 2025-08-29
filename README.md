# 🤖 Meanings Bot

<p align="center">
  <img src="https://img.shields.io/github/license/xFanexx/meanings?style=for-the-badge&color=6f42c1&logo=github" alt="License" />
  <img src="https://img.shields.io/github/last-commit/xFanexx/meanings?style=for-the-badge&color=2ea043&logo=git" alt="Last Commit" />
  <img src="https://img.shields.io/github/languages/top/xFanexx/meanings?style=for-the-badge&color=f1e05a&logo=python" alt="Top Language" />
  <img src="https://img.shields.io/github/repo-size/xFanexx/meanings?style=for-the-badge&color=ff6f00&logo=database" alt="Repo Size" />
  <img src="https://img.shields.io/github/languages/code-size/xFanexx/meanings?style=for-the-badge&color=6f42c1&logo=code" alt="Code Size" />
  <img src="https://img.shields.io/github/commit-activity/y/xFanexx/meanings?style=for-the-badge&color=red&logo=githubactions" alt="Commit Activity" />
</p>

A sleek Discord bot to manage and explore slang meanings, built with Python. Offers public commands for all and admin tools for whitelisted users. Runs on Linux with systemd support!

## ✨ Features
- **Public Commands**: `?meaning`, `?list`, `?stats`, `?ping`
- **Admin Commands**: `?addmeaning`, `?deletemeaning`, `?yes`, `?no` (whitelisted only)
- **DND Status**: Watches servers with a "Do Not Disturb" flair
- **Scalable**: Handles multiple servers effortlessly
- [Commands](commands.md) Check this for all commands
- **Async file** handling with `aiofiles`
- Fully **Poetry-managed** project with isolated dependencies

## Requirements

- **Python** 3.12+
- **Poetry** 2.x
- **Discord bot token** (`.env` file)
- **Curl** 8.15.x
- **Git**

## 🚀 Getting Started
1. Clone the repo:
   ```sh
   git clone https://github.com/xFanexx/meanings.git
   ```
## Install Poetry (if not installed)
1. From offical site:
  - Linux, macOS, Windows (WSL)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

  - Windows (Powershell)

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> [!NOTE]
> If you have installed Python through the Microsoft Store, replace `py` with `python` in the command above.

Check their offical **Documentation** for more information. [Python-Poerty](https://python-poetry.org/docs/#installing-with-the-official-installer)

2. With **PIP**:
```py
pip install poetry
```

> [!IMPORTANT]
> When you are installing **Poetry** via `pip`, always check if **Rust** is installed in your system because one of its dependencies (`maturin`) needs Rust to build and top of that do not forget to update `pip` or its **prebuilt wheels**. So, you don't get any errors.

## Install dependencies

```py
poetry install
```

> [!NOTE]
> This installs all dependencies listed in `pyproject.toml` inside a virtual environment.
>
>
> Since this project is a **Discord bot** (not a distributed Python package), we set:
>
> ```toml
> [tool.poetry]
> package-mode = false
> ```
>
> This ensures that `poetry install` only installs dependencies and does not fail with a *“No file/folder found for package”* error.


# For Non-Poetry Users

If you don’t have **Poetry** installed, you can still run this project using only `pip` and `requirements.txt`.

### Installation

```py
pip install --no-deps -r requirements.txt
```

> [!NOTE]
> When using `requirements.txt` exported from Poetry, the `--no-deps` flag is required.
>
> This is because the exported file already includes **all direct and transitive dependencies** with exact versions or resolved hashes.
> Running pip without `--no-deps` may cause it to try **re-resolving dependencies**, which can lead to conflicts or errors—especially for Git-based dependencies.

## Updating Dependencies (PIP)

1. Upgrade a single dependency:

```py
pip install --upgrade <package-name>
```
**Example**:

```py
pip install --upgrade discord.py
```

**Then regenerate `requirements.txt`**:

- Create a virtual environment:

  - Linux / MacOS

```bash
python3 -m venv venv
```

  - Windows (Powershell and CMD)

```bash
python -m venv venv
```

This creates a folder called venv in your project.

- Activate the virtual environment:

  - Linux / MacOS

```bash
source venv/bin/activate
```

**Replace `venv` with the name of your virtual environment folder**.

  - Windows (Powershell and CMD)

```bash
# Powershell
.\venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

> [!NOTE]
> If you encounter a "cannot be loaded because running scripts is disabled" error, you may need to run `Set-ExecutionPolicy RemoteSigned -Scope Process` in your PowerShell window to temporarily allow script execution.

Then regenerate the `.txt`:

```py
pip freeze > requirements.txt
```

After that deactivate it:

```bash
# Linux, MacOS and Windows
deactivate
```

2. Upgrade all dependencies:

```py
pip install --upgrade -r requirements.txt
```

> [!WARNING]
> This respects the pinned versions in `requirements.txt`. If you want latest versions, remove version numbers from the file before running.


### Regenerate requirements.txt

After any upgrade activate the virtual environment and update it:

```py
pip freeze > requirements.txt
```

> [!TIP]
> Using `pyproject.toml` with **Poetry** is recommended for consistent, reproducible environments — but `requirements.txt` works for quick installs and deployment.

# Environment Variables
Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_token_here
```

> [!IMPORTANT]
> Do not commit `.env` to version control.

# Updating Dependencies

- To update a single dependency:

```py
poetry update discord-py
```

- To update all dependencies:

```py
poetry update
```

- Regenerate requirements.txt after updates:

```bash
source $(poetry env info --path)/bin/activate && pip freeze > requirements.txt && deactivate
```

---

# Contributing

- Fork the Repo.

- Make sure `.env` and `.venv/` are ignored in **Git** (`.gitignore` is included).

- Commit `pyproject.toml` and `poetry.lock` to track dependencies.

- PR should be **clean**, **concise** and **descriptive**.

- Use **Poetry** for adding new packages in your project:

```bash
poetry add <package-name>      # normal dependency
poetry add --dev <package-name> # dev dependency
```


> [!WARNING]
> THIS MIGHT BE PRODUCTION READY, BUT YOU MIGHT CONSIDER RE-WRITING THE CODE AND SWITCHING TO A SQLITE OR POSTGRESQL DB.

> [!NOTE]
> THIS IS A PURE HOBBY BOT INTENDED TO HAVE SOME FUN IN DISCORD CHANNELS.

## 👥 Contributors

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/Sacul0457">
        <img src="https://github.com/Sacul0457.png" width="100px;" style="border-radius:10px;" alt="Sacul0457"/>
        <br />
        <b>Sacul0457</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/xFanexx">
        <img src="https://github.com/xFanexx.png" width="100px;" style="border-radius:10px;" alt="xFanexx"/>
        <br />
        <b>xFanexx</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Chandramauli-Arm64">
        <img src="https://github.com/Chandramauli-Arm64.png" width="100px;" style="border-radius:10px;" alt="Chandramauli"/>
        <br />
        <b>Chandramauli</b>
      </a>
    </td>
  </tr>
</table>

![Alt](https://repobeats.axiom.co/api/embed/829d921b5850e576b4837cd5f4c9f6497010a54b.svg "Repobeats analytics image")
