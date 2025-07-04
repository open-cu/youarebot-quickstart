# Intro

The goal of today’s session is to explore the key aspects of development, both in general and as they apply specifically to the Python language. We will focus on closing any knowledge gaps necessary for successfully mastering the rest of the course materials and completing the homework assignments. To do this, we will examine some useful tools and see how they integrate into the IDE.

The primary development environment for the course will be [Visual Studio Code](https://code.visualstudio.com/) (VS Code).

Lecture outline:

* Project structure
* Virtual environments
* Running
* Debugging
* Formatting
* Linting
* Git: version-control system
* Command line, shell
* Remote development

## Project structure

We will study the various tools using the **youarebot-quickstart** project as an example. This project is a quickstart template for building bot detection or AI-powered applications.

The project has the following directory structure:

* `app/` – the main application directory containing the service logic

  * `__init__.py` – Python package initialization file
  * `models.py` – data models and structures used by the application
  * `api/` – responsible for the service API
    * `__init__.py` – Python package initialization file
    * `main.py` – main API entry point and route definitions
  * `core/` – core functionality and utilities
    * `__init__.py` – Python package initialization file
    * `logging.py` – logging configuration and utilities
  * `web/` – web interface components
    * `__init__.py` – Python package initialization file
    * `streamlit_app.py` – Streamlit web application
* `materials/` – teaching materials and documentation

  * `day06-intro.md` – introduction and development guide
* `tests/` – test files that verify the correctness of the project
* `.gitignore` – specifies the files and directories that should be ignored by Git. See the [collection of ready-made *gitignore* files](https://github.com/github/gitignore).
* `poetry.lock` – lock file that pins exact versions of all dependencies
* `portforward_key` – SSH key file for port forwarding setup
* `pyproject.toml` – configuration file for managing Python projects and dependencies
* `README.md` – Markdown file with a general project description, usage instructions, or other important information
* `run_all_linux.sh` – shell script to run the application on Linux systems
* `run_all_windows.ps1` – PowerShell script to run the application on Windows systems

The suggested project structure is by no means the only correct one and may vary depending on your needs. For orientation and inspiration, take a look at [Cookiecutter](https://www.cookiecutter.io/templates) templates—for example, the [Data Science template](https://github.com/drivendataorg/cookiecutter-data-science).

## Virtual environments

<details>
  <summary>Why are isolated virtual environments needed?</summary>

* **Project cleanliness and independence** — isolation allows each project to maintain its own unique dependencies without affecting other projects.
* **Preventing version conflicts** — different projects may require different versions of the same library, which would otherwise lead to incompatibilities and errors.
* **Easy dependency management** — you can clearly control and update library versions in each project without disrupting others.
* **Improved reproducibility** — a virtual environment helps you reproduce the working environment exactly, making the project easier to port to other machines or revisit later.
* **Security and stability** — isolated environments protect against unexpected changes on the system and keep the project stable even when new versions of packages or dependencies appear on the computer.

</details>

### [venv](https://docs.python.org/3/library/venv.html)

The standard tool in Python for creating virtual environments. It lets you create isolated environments, activate and deactivate them, and install the required packages into each environment.

```bash
# Create a virtual environment:
python -m venv environment_name
# Often called venv or .venv

# Activate the virtual environment
source ./environment_name/bin/activate

# Check which python and pip are active
which python
which pip

# Install packages with pip as usual
pip install requests

# Deactivate the virtual environment
deactivate

# Remove the virtual environment (simply delete the directory)
rm -rf environment_name
```

Demonstration in practice: using *venv* with the “chat generator” example, activating the environment in VS Code. Notice that while the main environment with Python 3.12 is active, VS Code warns that `typing.Dict` is deprecated; switching to Python 3.8 removes this warning.

There are, in fact, many utilities for creating and managing Python virtual environments; let’s look at a few more:

### [pyenv](https://github.com/pyenv/pyenv/blob/master/README.md)

A command-line utility that, in addition to creating virtual environments, also lets you manage multiple Python versions and switch between them.

### [pipenv](https://pipenv.pypa.io/en/latest/)

A combination of *pip* and *virtualenv*. It automates creating and managing virtual environments and handling dependencies, and it can also pin every package version via `Pipfile.lock`.

We will examine **Poetry** in more detail:

### [poetry](https://python-poetry.org/)

A modern Python dependency-management tool that simplifies creating, publishing, and deploying packages. We will use it in today’s project.

```bash
# Initialise a new Poetry project
poetry init

# Add a package to the dependency list
poetry add <package-name>

# Remove a package from the dependency list
poetry remove <package-name>

# Update packages to the latest compatible version
poetry update

# Show installed packages and their versions
poetry show

# Start a shell with the virtual environment activated
poetry shell

# Run a command inside the virtual environment
poetry run <command>

# Install all required dependencies
poetry install
```

The main configuration mechanism in Poetry is the **pyproject.toml** file. It provides a convenient and standardised way to configure a Python project, making dependency management, tool configuration, and reproducibility easier.

What can be configured through *pyproject.toml*:

* Dependencies
* Metadata
* Build tools
* Test tools
* Formatting, linters, and other tools

Practical demo: **pyproject.toml** using the project as an example.

The [Python Packaging User Guide](https://packaging.python.org/en/latest/) contains more details on working with Python packages and on building and publishing your own packages.

When specifying package versions, it is worth mentioning [Semantic Versioning](https://semver.org/) (SemVer). A set of rules regulates how a project’s version number should change depending on the modifications made.

```
Given a version number MAJOR.MINOR.PATCH, increment:
MAJOR when you make incompatible API changes,
MINOR when you add functionality in a backwards-compatible manner, and
PATCH when you make backwards-compatible bug fixes.
```
 



[Regular expressions for versioning in **Poetry**](https://python-poetry.org/docs/dependency-specification/).
Poetry is more concise in this respect than, for example, specifying versions in `requirements.txt`.

* **Poetry:** `package = ^1.2.3`
* **requirements.txt:** `package>=1.2.3,<2.0.0`

## Running

We now have the project and an isolated environment; everything is ready for coding.
In our case, the code is already written, so we can simply run it.

From the console:

```bash
# Start the service that predicts the probability that a conversation partner is a bot
poetry run fastapi dev app/api/main.py --host 0.0.0.0 --port 8000
```

The service accepts HTTP requests:

```bash
# curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"text": "Where is the money Lebowski?",
        "dialog_id": "c6701438-3486-4f55-9b7b-5f06adaa26a0",
        "id": "35131732-7de8-4e7d-a514-355887262d32",
        "participant_index": 0
    }'
```

Starting from VSCode is configured via the **`launch.json`** file.
VSCode also gives you immediate access to the debugger for the running program, but first we will look at debugging from the console.

Practice demonstration: simultaneously launching two programs from VSCode.

## Debugging

> Nowadays, console debugging is used rather rarely because IDEs provide a more convenient UI, but it is still worth knowing.

* [`pdb`](https://docs.python.org/3/library/pdb.html) — the interactive debugger from the Python standard library.
* [`ipdb`](https://pypi.org/project/ipdb/) — the same `pdb`, but improved (syntax highlighting, autocompletion, etc.).
  [Cheatsheet](https://cheatsheetindex.com/pdb-cheat-sheet/)

With a properly configured **`launch.json`**, Python debugging is also available directly in VSCode.

An example could look like this:

```json
{
  "name": "Run Client emulator",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/tools/client_example/main.py",
  "python": "${workspaceFolder}/tools/client_example/venv/bin/python",
  "console": "integratedTerminal"
}
```

Official [guide](https://code.visualstudio.com/docs/python/debugging) for debugging Python programs in VSCode.

## Formatting

Code formatting is not just aesthetics; it is a crucial part of readability and maintainability.
It helps other developers (and future you) quickly understand the code.

A **formatter** is a tool that automatically brings code to a unified style, fixing its appearance.

**Goal:** Improve readability and make the code uniform without changing its behaviour.

What it does:

* Adds or removes spaces, blank lines, and indentation.

* Formats strings, brackets, line length, etc.

* Eliminates stylistic inconsistencies (e.g. quote style, line length).

* [PEP 8](https://peps.python.org/pep-0008/) — the official Python style guide covering formatting and more.

* [`flake8`](https://flake8.pycqa.org/en/latest/index.html) — a popular lightweight tool for static analysis; it combines PEP 8 compliance checks with detection of potential errors.

* [`isort`](https://pypi.org/project/isort/) — orders imports per PEP 8, grouping them into standard-library, third-party, and local imports.

* [`black`](https://black.readthedocs.io/en/stable/index.html) — automatically formats code into a consistent style and intentionally offers almost no configuration.

As noted earlier, most linting and formatting tools are configured in `pyproject.toml`.

<!-- [`ruff`](https://astral.sh/ruff) — a fast, multifunctional linter and formatter for Python code, written in Rust. -->

## Linting

A **linter** is a tool for analysing and checking source code for errors, style violations, and potential issues.

**Goal:** Maintain code quality by detecting errors, inefficiencies, and deviations from coding standards.

What it does:

* Checks adherence to coding style (e.g. PEP 8 for Python).

* Searches for logical errors, unused variables, incorrect imports, etc.

* Can reveal potential bugs (e.g. using a variable before it is defined).

* [`Pylint`](https://www.pylint.org/) — a static code analyser that checks your code for style compliance, helps find errors, and suggests improvements.

* [`Mypy`](https://mypy-lang.org/) — a type checker for Python that verifies code against type annotations, bringing static typing to your project.

### [`Ruff`](https://docs.astral.sh/ruff/)

> “An extremely fast Python linter and code formatter, written in Rust.”
> “Ruff can replace Flake8 (plus dozens of plugins), Black, isort, pydocstyle, pyupgrade, autoflake, and more, while running tens or hundreds of times faster than any individual tool.”

```bash
# Installation
pip install ruff
poetry add ruff

# Run the linter (specify a directory/file to process, if desired)
ruff check

# Run the linter with automatic fixes
ruff check --fix

# Run code formatting
ruff format
```

Ruff is also configured via `pyproject.toml`; see an example in this project.

## Git: Version-Control System

<details>
  <summary>Why do we need version-control systems (and Git in particular)?</summary>

<br>

[Git](https://git-scm.com/) is a version-control system (VCS) that lets you track changes in code, collaborate on a project, and manage different versions.
Git is one of the most popular developer tools thanks to its flexibility, speed, and ubiquity.

* **History of changes:**
  Git stores every version of project files, allowing you to revert to any of them.
  For example, you can roll back to a working state after an error.

* **Collaboration:**
  Several developers can work on the same project without interfering with each other.
  Changes are merged via *merge* operations.

* **Branching:**
  Git allows you to create branches for new features or bug fixes while keeping the main branch stable.

* **Backup:**
  A repository can be stored in the cloud (e.g. on GitHub), protecting you from data loss.

</details>



```bash
# Project initialization
git init

# Clone a remote repository
git clone <repo_url>

# Add files to the repository
git add <file>
git add .

# Create a commit (save changes)
git commit -m "Description of changes"

# View repository status
git status

# Create a branch
git branch <branch_name>

# Switch between branches
git checkout <branch_name>

# Create a branch and switch to it immediately
git checkout -b <branch_name>

# Merge changes from branch_name into the current branch
git merge <branch_name>

# Push changes to the remote repository
git push origin <branch_name>

# Pull changes from the remote repository
git pull origin <branch_name>
```

### Example of using Git in collaborative development

Suppose you are developing a project in a team and several people are simultaneously adding new features or performing refactoring.

A typical workflow looks like this:

```bash
# Switch to the main branch (main or master)
git checkout main

# Update the local branch to the latest version
git pull

# Create a new branch for the new feature (and switch to it right away)
git checkout -b feature/new-feature-name

# Optionally save your branch changes to the remote repository
git add .
git commit -m "some changes"
git push

# After all necessary changes are made in the separate branch,
# they need to be integrated into the main branch.
# Conflicts may arise because the same part of the code could have been
# modified by other developers, and Git cannot merge them automatically. 
```

![Here](assets/git-merge-vis.png)

When working in a feature branch, it makes sense to rebase onto the main branch from time to time so that you do not have to resolve dozens of conflicts later.
If the commit history becomes especially complex, it may be easier to create a new branch from the up-to-date main branch and port your changes there. 🙂

**Collaboration platforms:**

* **GitHub** — the leading Git hosting service.
* **GitLab** — provides advanced CI/CD capabilities.
* **Bitbucket** — integrates tightly with the Atlassian ecosystem.

### Conventional Commits and beyond

When working as a team, unified conventions for branch names, merge requests, and commit messages simplify collaboration and help automate processes.

* **Readable history:** It is easier to understand why certain changes were made and how they affect the project.
* **Consistency:** Uniform branch names and commits improve orientation in the codebase and boost efficiency.
* **Automation:** Conventions can drive scripts or tools that create versions, changelogs, or adjust CI/CD pipelines.

Examples from my practice:

* Branch names:

  * `refactor/alexborisov/UCP-3925-remove-old-feature-extractors`
  * `alexborisov/task/mix_retries/MUSICRECO-547`
* Merge Request title: include the task number to link the MR automatically to the issue tracker.

Read more about Conventional Commits [here](https://www.conventionalcommits.org/en/v1.0.0/).

### [Pre-commit hooks](https://pre-commit.com/)

To maintain code quality in the main branch, various CI/CD pipelines usually run before merging an MR.
Basic checks—such as formatting or PEP 8 compliance—can be enforced at the commit stage so that non-conforming code never even enters a commit.
This is exactly what pre-commit hooks are for.

---

## Command line & shell

A command line is a text interface for interacting with the operating system.
A **shell** is the program that interprets these commands (e.g. Bash, Zsh, PowerShell).

**Why it is important to know the command line:**

* **Task automation:** Write scripts to perform repetitive tasks.
* **Access to system tools:** Use built-in OS utilities.
* **Working on remote servers:** Most servers have no graphical interface.
* **Project management:** Many developer tools (e.g. Git) work via the command line.

[Bash cheat sheet](https://devhints.io/bash)

A brief overview of some Bash commands—there are, in fact, many more useful commands and utilities.

```bash
# List directory contents. If no path is given, use the current directory.
ls path
ls -lah path

# Create a directory
mkdir dir-name
mkdir -p /dir1/dir2

# Navigate the filesystem
cd path
cd ..

# Create an empty file
touch file.txt

# `rm` — removes files and directories
# Remove a file
rm file.txt
# Remove a directory and all its contents (`-r` — recursive)
rm -r my_folder

# Copy a file
cp src dest

# Copy multiple files or a directory (glob patterns supported)
cp -r src-dir dest-dir

# `lsof` (list open files) shows open files and the processes using them
# Find processes using a specific file:
lsof /path/to/file
# Find processes listening on a specific port (e.g. 8080):
lsof -i :8080

# `which` — find the path to an executable
which python

# `history` — show the command history
# Show the last 50 commands
history 50

# `grep` — search for patterns in files or input streams
# Find commands in history (e.g. those containing `git`)
history | grep git
 
find . -name "*.txt"
 
# Reload environment variables from .bashrc
source ~/.bashrc
```



You can save a sequence of commands to a file and run it from the command line as a shell script.

However, if the script becomes large and complex, it may be better to rewrite it in a language that is easier to maintain.

From personal experience: maintaining cron pipelines made up of dozens of shell scripts is not very convenient.

## Remote development

Remote development lets you work with projects on remote servers or in the cloud without pulling the code onto your local machine. It allows you to use powerful server-side computing resources, access data and services that exist only on those systems, and work in a single, consistent environment regardless of local settings. Remote development also simplifies collaboration and helps avoid dependency and OS-compatibility issues.

### SSH

SSH is a cryptographically secure protocol that provides a protected communication channel between a client (your local machine) and a server. In remote development, SSH is the main tool for connecting to the servers that host your projects or computational resources.

Key features of SSH:

* **Encryption:** All data transmitted via SSH is protected by encryption, preventing information leaks.
* **Authentication:** SSH supports two authentication methods:

  * **Password:** confirm your identity with a password.
  * **SSH keys:** a more secure method that uses a public/private key pair.

Check availability/version:

```bash
ssh -V
```

Connect to a remote server:

```bash
ssh username@remote-server-ip
```

where

* **username** — your user name on the remote server.
* **remote-server-ip** — the server’s IP address or domain name.

By default, SSH listens on port 22. If the server uses a different port, add `-p`:

```bash
ssh -p 2222 username@remote-server-ip
```

The more convenient (and recommended!) way to connect is with SSH keys.

<details>
  <summary>Quick reference on SSH keys (see more details <a href="https://habr.com/ru/articles/747080/">here</a>).</summary>

<br>

A secure SSH connection uses a key pair:

* **Private key:** stored only on your local computer; strictly confidential and never transmitted.
* **Public key:** copied to the remote server and added to `~/.ssh/authorized_keys`.

When you connect, SSH checks whether your private key pairs with the public key on the server. If they match, access is granted without a password.
This method is safer than passwords because the private key never leaves your device and is extremely hard to crack.

</details>

```bash
# Generate a key pair
ssh-keygen -t rsa -b 4096

# Copy the public key to the server 
# (actually copies ~/.ssh/id_rsa.pub to ~/.ssh/authorized_keys on the server)
ssh-copy-id username@remote-server-ip

# After the keys are set up, you can connect without a password
ssh username@remote-server-ip
```

Use **scp** (secure copy) to transfer files between local and remote machines.

```bash
# Copy a file from the local machine to the server
scp /path/to/local/file username@remote-server-ip:/path/to/remote/directory

# Copy a file from the server to the local machine
scp username@remote-server-ip:/path/to/remote/file /path/to/local/directory
```

### Port forwarding

Local port forwarding lets you route traffic from your local machine to a remote machine over SSH. This is handy when a service on the remote server runs on a certain port and you want to access it locally.

**Syntax**

```bash
ssh -L <local_port>:<remote_host>:<remote_port> <user>@<server>
```

**Example**

Assume our **turing\_test\_service** runs on the remote server `remote-server` and listens on port 8000:

```bash
ssh -L 9999:localhost:8000 user@remote-server
```

Now you can query the service through `localhost:9999` on your local machine.

Reverse port forwarding works the other way round:

```bash
ssh -R <remote_port>:<local_host>:<local_port> <user>@<server>
```

The commands above also open a remote shell. To forward ports only, add:

* `-N` — do not run a remote command, just establish the tunnel.
* `-f` — run SSH in the background.

```bash
ssh -L 9999:localhost:8000 -N -f user@remote-server
```

### Handling unstable connections

On an unreliable connection you may lose your terminal state and interrupt running processes. Here are a few ways to avoid that.

#### **tmux**

`tmux` lets you create multiple virtual terminals in one window and detach/attach to them at will.

```bash
# Start a new tmux session
tmux new-session -s mysession

# Inside the session, launch a long-running process, e.g. model training
python3 train.py

# Detach without stopping the process: press Ctrl-b then d.
# If the connection drops, the process keeps running inside tmux.

# Reattach later
tmux attach-session -t mysession
```

#### **nohup**

If you don’t need to keep terminal state and only want to guarantee that a long process keeps running after you disconnect, use `nohup` (NO HANG UP).

```bash
nohup python3 long_script.py &
```

* `nohup` runs the command immune to hang-ups.
* `&` sends it to the background.

Output is written to `nohup.out` (or another file if you specify one). View it with:

```bash
tail -f nohup.out
```

### Remote development in VSCode

![Here](assets/vscode_remote.png)

**Remote-SSH** is a VSCode extension that lets you connect to a remote server via SSH and work with files as if they were local—super convenient!

<details>
  <summary>How to set it up</summary>

<br>

1. **Install the extension**
   Open VSCode, go to **Extensions** (or press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>), search for **Remote – SSH**, and install it.

2. **Connect to the server**
   Open the Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>), choose **Remote-SSH: Connect to Host…**, and enter the SSH address, for example `user@remote-server.com`.

3. **Configure SSH**
   On first connection VSCode may guide you through setting up the SSH client, including creating or selecting existing SSH keys.

4. **Work with code**
   Once connected, you can open, edit, and save files on the server directly from VSCode. The editor behaves normally, but all changes happen on the server.

</details>

Demo: configuring our service remotely.

Full setup (almost from scratch) on a remote server:

1. Clone the Git repository.
2. Open the remote project in VSCode.
3. Configure the Python environment.
4. Start the service (from VSCode).
5. Make requests from the local machine with `curl` and catch them in the VSCode debugger.