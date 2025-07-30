# sqlite_toolkit

Sqlite scaffold with CLI and dashboarding functionalities

# CLI Installation & Usage Best Practices

This project provides a CLI tool called `sqlitekit` for managing your SQLite toolkit from the terminal.

### Professional Installation Methods

| Use Case         | Command to Install         | Where to Run CLI    | Notes                          |
|------------------|---------------------------|---------------------|--------------------------------|
| Development      | `pip install -e .`        | In venv             | Activate venv before use       |
| Personal Global  | `pip install --user .`    | Anywhere            | Ensure ~/.local/bin is in PATH |
| System-wide      | `pip install .`           | Anywhere            | Requires admin rights          |
| Distribution     | Publish to PyPI           | Anywhere            | For users everywhere           |

### Required Dependencies

Some CLI commands require extra Python packages:

- **Alembic**: Required for `db-init` and database migrations.
- **Faker**: Required for all faker/bash data generation scripts (e.g., `sqlitekit bash faker run-items`).

**Install all requirements:**
- Recommended: install everything with:
  ```bash
  pip install -r requirements.txt
  # or for dev:
  pip install -r requirements-dev.txt
  ```
- Or, install missing packages individually:
  ```bash
  pip install alembic faker
  ```

> If you see errors like `ModuleNotFoundError: No module named 'alembic'` or `'faker'`, install the missing package as shown above.

### Uninstalling `sqlitekit`

To remove the CLI, uninstall the `sqlite_toolkit` package with pip. The command is the same regardless of how you installed it, but the location and environment may differ:

- **Local editable/dev install (in your venv):**
  - Activate your virtual environment and run from anywhere inside your project directory:
    ```bash
    source .venv/bin/activate  # if not already active
    pip uninstall sqlite_toolkit
    ```
- **User/global install:**
  - Make sure you are _not_ in a virtual environment. Run from any directory:
    ```bash
    deactivate  # if you are in a venv
    pip uninstall sqlite_toolkit
    ```
- **PyPI install:**
  - Make sure you are _not_ in a virtual environment. Run from any directory:
    ```bash
    deactivate  # if you are in a venv
    pip uninstall sqlite_toolkit
    ```

> **Note:** The pip uninstall command uses the package name `sqlite_toolkit`, not the CLI command `sqlitekit`.

#### 1. Development (Recommended)
Use a virtual environment to keep dependencies isolated:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
After activation, you can run:
```bash
sqlitekit
```

#### 2. Personal Global Install
Install the CLI just for your user (no admin needed):
```bash
# in the project folder, outside venv
deactivate
pip install --user .
```
Make sure `~/.local/bin` is in your `PATH` (add this to your `~/.zshrc` or `~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Now you can use `sqlitekit` anywhere.

#### 3. System-wide Install
If you want the CLI for all users (requires admin):
```bash
pip install .
```

#### 4. Distribution
To share with others, publish to PyPI. Then users can run:
```bash
pip install sqlite-toolkit
```

# User using CLI sqlite

This project uses two requirements files:

- **`requirements.txt`**: Core dependencies needed to run the application.
- **`requirements-dev.txt`**: Additional packages needed for development and testing (includes everything in `requirements.txt` plus testing tools like `pytest`).

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI:
   ```bash
   sqlitekit --help
   sqlitekit [COMMAND]
   ```

## CLI Database Initialization & Command Gating

**IMPORTANT:** Before you can use any CLI commands to manage items, item details, or the database, you must initialize the database using the `db-init` command.

- On first run, only the `db-init` command is available:
  ```bash
  sqlitekit --help
  # Output:
  # Commands:
  #   db-init  Initialize the database schema using Alembic migrations.
  ```
- Run `db-init` to set up the database:
  ```bash
  sqlitekit db-init
  # Prompts for a database path if not configured; runs migrations.
  ```
- After initialization, all CLI commands become available:
  ```bash
  sqlitekit --help
  # Commands:
  #   item         ...
  #   item-detail  ...
  #   db           Database management commands
  #   bash         ...
  ```
- If you delete the database file (see below), the CLI will again only show `db-init` until you re-initialize.

## Database Management Commands (`db` group)

After the database is initialized, you can manage it using the `db` command group:

- **Show database path and directory:**
  ```bash
  sqlitekit db dir
  # Shows the full path and containing directory of the database file.
  ```
- **Wipe all data (keep schema):**
  ```bash
  sqlitekit db wipe
  # Deletes all data from all tables, but keeps the schema/tables.
  ```
- **Delete the database file:**
  ```bash
  sqlitekit db delete
  # Removes the database file. After this, only db-init is available again.
  ```

## Commands

### Item commands
- `add` — Add a new entry
- `list` — List all entries
- `edit ENTRY_ID` — Edit an entry
- `delete ENTRY_ID` — Delete an entry

### Item detail commands (grouped under `item-detail`)
- `item-detail add` — Add a new detail to an item
- `item-detail list` — List details (optionally filter by item)
- `item-detail edit DETAIL_ID` — Edit a detail
- `item-detail delete DETAIL_ID` — Delete a detail

Example (item CRUD):
```bash
sqlitekit add
sqlitekit list
sqlitekit edit 1 --name "New Name"
sqlitekit delete 1
```

## Bash Faker CLI Usage

There are 2 faker bash scripts available:
- `bash etl/fake_items.sh <number_of_items>`
- `bash etl/fake_item_details.sh <number_of_details> <item_id>`

You can run bash-based faker scripts for generating fake data via the CLI:

- **Add fake items:**
  ```bash
  sqlitekit bash faker run-items <NUM_ITEMS>
  # Example: sqlitekit bash faker run-items 10
  ```
- **Add fake item details:**
  ```bash
  sqlitekit bash faker run-item-details <NUM_DETAILS> <ITEM_ID>
  # Example: sqlitekit bash faker run-item-details 5 1
  ```

All bash script triggers are grouped under the `bash faker` command group for consistency and extensibility.

## Item Detail CLI Usage

You can manage item details using the `item-detail` command group:

- **Add a detail:**
  ```bash
  sqlitekit item-detail add
  # Prompts for item_id, key, value
  ```
- **List details:**
  ```bash
  sqlitekit item-detail list --item-id 1
  # Lists all details for item 1
  ```
- **Edit a detail:**
  ```bash
  sqlitekit item-detail edit 1 --key color --value blue
  # Edits detail with id=1
  ```
- **Delete a detail:**
  ```bash
  sqlitekit item-detail delete 1
  # Deletes detail with id=1
  ```

# User using dashboard

- [ ] TODO

# Dev using this scaffold

Best practice: You always start by **making a clean _new Git repo_** — _outside_ your IDE or AI tool first. Then you pull it into PyCharm → then let WindSurf work _inside_ that new repo with full context.

**Clone & copy the scaffold**
```
mkdir sqlite_toolkit
cp -r crud_cli_scaffold/* sqlite_toolkit/
cd sqlite_toolkit
rm -rf .git __pycache__ .venv docker-compose.yml
git init
git add .
git commit -m "init: scaffold copied from crud_cli_scaffold"
```
- [ ] maybe make bash script on this.

**Setup virtual environment**
```zsh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

```
`pip install requirements.txt` for runtime, but `-dev.txt` for both dev and runtime.

Add gitignore and other changes for the first commit.

**Push to GitHub**

Create repo → link remote → push:

```zsh
git remote add origin <YOUR_NEW_REPO_URL>
git branch -M main
```
In Fork: stage commits, commit, push.

idk why, but do this too:
```zsh
git merge origin/main --allow-unrelated-histories --no-ff
```
Resolve then merge. Then
```zsh
git add .
git commit
git push main origin
```
---