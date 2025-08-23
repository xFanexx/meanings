# 🤖 Meanings Bot

<p align="center">
  <img src="https://img.shields.io/github/license/xFanexx/meanings?style=flat-square&color=purple" alt="License" />
  <img src="https://img.shields.io/github/last-commit/xFanexx/meanings?style=flat-square&color=green" alt="Last Commit" />
  <img src="https://img.shields.io/github/languages/top/xFanexx/meanings?style=flat-square&color=yellow" alt="Top Language" />
  <img src="https://img.shields.io/github/repo-size/xFanexx/meanings?style=flat-square&color=orange" alt="Repo Size" />
  <img src="https://img.shields.io/github/languages/code-size/xFanexx/meanings?style=flat-square&color=purple" alt="Code Size" />
  <img src="https://img.shields.io/github/commit-activity/y/xFanexx/meanings?style=flat-square&color=red" alt="Commit Activity" />
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
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
  - Windows (Powershell)
    ```sh
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
>
> This ensures that `poetry install` only installs dependencies and does not fail with a *“No file/folder found for package”* error.


# For Non-Poetry Users

If you don’t have **Poetry** installed, you can still run this project using only `pip` and `requirements.txt`.

### Installation

```py
pip install -r requirements.txt
```

## Updating Dependencies (PIP)

1. Upgrade a single dependency:

```py
pip install --upgrade <package-name>
```
**Example**:

```py
pip install --upgrade discord.py
```

Then regenerate `requirements.txt`:

```py
pip freeze > requirements.txt
```

2. Upgrade all dependencies:

```py
pip install --upgrade -r requirements.txt
```

> [!WARNING]
> This respects the pinned versions in `requirements.txt`. If you want latest versions, remove version numbers from the file before running.


### Regenerate requirements.txt

After any upgrade:

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
source $(poetry env info --path)/bin/activate
pip freeze > requirements.txt
deactivate
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
