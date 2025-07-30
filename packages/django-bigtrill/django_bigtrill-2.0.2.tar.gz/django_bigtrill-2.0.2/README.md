## django-bigtrill

**django-bigtrill** is a Django utility to help you migrate from the default Django `User` model to a custom user model in an existing project. It automates the process, making it safer and easier to switch without manual errors.

---

### Features

- Detects and updates references to the default Django `User` model
- Creates a new custom user model in an app with a name you choose
- Updates settings and migrations automatically
- Provides admin integration for the new user model
- Automatically creates backups of files before modification
- Allows you to restore files from backup with a flag
- Supports a dry run mode to preview changes without modifying files

---

### Installation

```bash
pip install django-bigtrill
```

or clone into your project root directory:

```bash
git clone https://github.com/alexander-any7/django-bigtrill
```

---

**Important**: Your `INSTALLED_APPS` must be a list or this will not work.

### Usage

1. **Configure**: Create a file named `bigtrill_settings.py` in the directory where you will run the start command. This file is required and must contain the following variables:

   - `PYTHON`: Your Python command (e.g., `python` or `python3`)
   - `MANAGE_PY_FILE`: Path to your `manage.py`
   - `COPY_MODEL`: Desired name for your custom user model
   - `NEW_AUTH_APP_LABEL`: App label for the new user model
   - `INSTALLED_APPS_SETTINGS_FILE_PATH`: Absolute or relative path to your main `settings.py` or where the `INSTALLED_APPS` is defined. (Relative paths will be converted automatically)
   - `AUTH_USER_MODEL_PATH`: Absolute or relative path to where the `AUTH_USER_MODEL` variable is or will be defined
   - `DEFAULT_DJANGO_USER_MODEL_FILE_PATHS`: List of files referencing the default user model (absolute or relative paths; optional)
   - `BASE_DIR`: Absolute or relative path to your project root. You are advised to run `pwd` and provide the output of the command.
   - `GITIGNORE_PATH`: Path to your `.gitignore` file. This MUST be relative to `BASE_DIR`. The folders in the gitignore will not be searched for references to the default `User` model.

   Example:

   ```python
   # bigtrill_settings.py
   PYTHON = "python"
   MANAGE_PY_FILE = "manage.py"
   COPY_MODEL = "CustomUser"
   NEW_AUTH_APP_LABEL = "accounts"
   INSTALLED_APPS_SETTINGS_FILE_PATH = "<absolute or relative path to your settings.py>"
   AUTH_USER_MODEL_PATH = INSTALLED_APPS_SETTINGS_FILE_PATH
   FILES_TO_SEARCH = []  # absolute or relative paths
   BASE_DIR = "<absolute or relative path to your project root>"
   GITIGNORE_PATH = ".gitignore"  # MUST BE RELATIVE to BASE_DIR

   ```

2. **Run the start script**:

   If installed via pip:

   ```bash
   bigtrill-start
   ```

   or

   ```bash
   python -m bigtrill.start
   ```

   or

   If cloned from git:

   ```bash
   python django-bigtrill/bigtrill/start.py
   ```

   Flags:

   - `--dry_run` : Show which files would be modified without making any changes.
   - `--restore` : Restore files from backup and exit.
   - `--skip_pause` : Skips the pause that allows you to check everything before proceeding to rename the model

   Follow the prompts. The script will:

   - Search for references to the default user model
   - Create a new app and custom user model
   - Update settings and run migrations
   - Update imports and references

3. **Review and test**:
   - Check your code and migrations
   - Test your application thoroughly after using this.

---

### Notes

- **Backup your project and database before running!**
- Do not run on production without testing.
- After migration, update any manual references to the old user model.
- Remove temporary files and update your main settings as needed.

  - Remove temporary files (such as `bigtrill_temp_settings.py`) and move any definitions from them (e.g., `AUTH_USER_MODEL`) to your desired location in your main `settings.py` file to follow Django project conventions.
  - You might also want to remove the `bigtrill_settings.py` file you created.
  - You might also want to remove `bigtrill` from `INSTALLED_APPS`. You can do this by going to the end of the file provided in `INSTALLED_APPS_SETTINGS_FILE_PATH` and there you will see:
    ```python
    # Added by bigtrill.start
    INSTALLED_APPS += [..., 'bigtrill']
    ```
    Simply remove bigtrill from the list. Optionally you can move the first item (the new app label where the new User model resides) to the actual `INSTALLED_APPS` list or definition and remove this comment and the lines below all together.

- **Performance**: Migration performance may vary depending on project size and number of users. For large datasets, consider running during low-traffic periods. Feel free to implement any optimization improvements you deem fit for your specific use case.

---

### TODO

- **Improve logging**: Add detailed logging for each step of the migration process with proper stdout output to help users track progress and debug issues
- **Improve model rename detection**  
  Use a more robust method (e.g., analyzing the generated migration files) to confirm that Django has detected the rename.

---

### License

MIT

---

### Author

Alexander Anyaegbunam (<alexander.any7@gmail.com>)
