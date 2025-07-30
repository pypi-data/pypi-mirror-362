import argparse
import os
import subprocess
import sys
from textwrap import dedent

custom_model = """\nfrom django.contrib.auth.models import AbstractUser, Group, Permission


class {n}(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # or any unique name
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # or any unique name
        blank=True,
        help_text="Specific permissions for this user.",
    )
"""

rename_custom_model = """\nfrom django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    pass

"""

admin_content = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
"""


def validate_path(path, var_name):
    if not path:
        raise ValueError(f"{var_name} must be set. Provided: '{path}'")
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{var_name} does not exist: '{path}'")


class BigTrill:
    def __init__(self, full=True):
        if not os.path.exists("bigtrill_settings.py"):
            raise FileNotFoundError(
                "bigtrill_settings.py not found. Please create this file with the necessary settings."
            )

        sys.path.append(os.getcwd())
        import bigtrill_settings as settings

        # Validate paths and set class variables
        validate_path(settings.BASE_DIR, "BASE_DIR")
        self.base_dir = settings.BASE_DIR
        self.temp_settings = "bigtrill_temp_settings.py"
        if full:
            self._validate_and_set_settings(settings)

    def _validate_and_set_settings(self, settings):
        """Validate settings and set class variables."""
        validate_path(
            settings.INSTALLED_APPS_SETTINGS_FILE_PATH, "INSTALLED_APPS_SETTINGS_FILE_PATH"
        )
        validate_path(settings.MANAGE_PY_FILE, "MANAGE_PY_FILE")

        self.installed_apps = settings.INSTALLED_APPS_SETTINGS_FILE_PATH
        self.manage_py = settings.MANAGE_PY_FILE
        self.python = settings.PYTHON
        self.label = settings.NEW_AUTH_APP_LABEL
        self.copy_model = settings.COPY_MODEL
        self.gitignore_path = settings.GITIGNORE_PATH
        self.paths_to_search = settings.FILES_TO_SEARCH

        # Validate FILES_TO_SEARCH paths if provided
        if self.paths_to_search:
            for path in self.paths_to_search:
                validate_path(path, "FILES_TO_SEARCH")

    def _get_excluded_dirs(self):
        """Get directories to exclude from search based on .gitignore."""
        exclude_dirs = set()
        if os.path.exists(self.gitignore_path):
            with open(self.gitignore_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("!"):
                        # Only handle directory ignores for now
                        if line.endswith("/"):
                            exclude_dirs.add(os.path.normpath(os.path.join(self.base_dir, line)))
                        elif os.path.isdir(os.path.join(self.base_dir, line)):
                            exclude_dirs.add(os.path.normpath(os.path.join(self.base_dir, line)))

        exclude_dirs.add(os.path.normpath(os.path.join(self.base_dir, self.label)))
        exclude_dirs.add(os.path.normpath(os.path.join(self.base_dir, "bigtrill")))
        return exclude_dirs

    def _find_python_files(self):
        """Find all Python files in the project directory, excluding specified directories."""
        if self.paths_to_search:
            return

        exclude_dirs = self._get_excluded_dirs()
        self.paths_to_search = []

        for root, dirs, files in os.walk(self.base_dir):
            # Remove excluded directories from search
            dirs[:] = [
                d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_dirs
            ]
            for file in files:
                if file.endswith(".py"):
                    self.paths_to_search.append(os.path.join(root, file))

    def _find_user_model_references(self):
        """Search for references to the default User model in Python files."""
        found = []
        for path in self.paths_to_search:
            with open(path, "r") as f:
                content = f.read()
            if "from django.contrib.auth.models" in content:
                found.append(path)
        return found

    def _create_backups(self, files):
        """Create backups of files that will be modified."""
        print(
            f"\nCreating backups of the files that will be edited in a directory named 'bigtrill_backup' in {self.base_dir}"
        )
        backup_dir = os.path.join(self.base_dir, "bigtrill_backup")
        os.makedirs(backup_dir, exist_ok=True)
        for file in files:
            # Convert file path to backup filename by replacing separators with descriptive text
            backup_filename = file.replace("/", "_SH_").replace("\\", "_BH_")
            backup_path = os.path.join(backup_dir, backup_filename)

            # Copy the file to backup
            with open(file, "r") as source:
                content = source.read()
            with open(backup_path, "w") as backup:
                backup.write(content)
            print(f"Backed up {file} to {backup_path}")

    def _restore_and_cleanup(self):
        backup_dir = os.path.join(self.base_dir, "bigtrill_backup")
        if not os.path.exists(backup_dir):
            print("No backups found to restore.")
            return

        for backup_path in os.listdir(backup_dir):
            full_backup_path = os.path.join(backup_dir, backup_path)
            original_path = backup_path.replace("_SH_", "/").replace("_BH_", "\\")
            print(f"Restoring {original_path} from {full_backup_path}")
            with open(full_backup_path, "r") as backup:
                content = backup.read()
            with open(original_path, "w") as original:
                original.write(content)

        if os.path.exists(self.temp_settings):
            os.remove(self.temp_settings)
            print(f"Removed temporary settings file: {self.temp_settings}")

        try:
            import shutil

            import bigtrill_settings as settings
            if settings.NEW_AUTH_APP_LABEL:
                shutil.rmtree(settings.NEW_AUTH_APP_LABEL, ignore_errors=True)
        except Exception:
            pass

        print("All backups restored successfully and files cleaned up.")
        print(
            "You may want to delete the 'bigtrill_backup' folder and 'bigtrill_settings.py' files if you no longer need them."
        )

    def _setup_custom_user_app(self):
        """Create and configure the custom user app."""
        # Start the app
        subprocess.run([self.python, self.manage_py, "startapp", self.label])

        # Edit the models.py file to add the custom user model
        with open(f"{self.label}/models.py", mode="a") as f:
            f.write(custom_model.format(n=self.copy_model))

        # Add the new app to INSTALLED_APPS
        with open(self.installed_apps, "a") as f:
            f.write("\n\n# Added by bigtrill.start\n")
            f.write(f"INSTALLED_APPS += ['{self.label}', 'bigtrill']\n")

    def _replace_user_imports(self, files):
        """Replace imports of the default User model with the custom one."""
        for file in files:
            with open(file, "r") as f:
                lines = f.readlines()

            new_lines = []
            inserted = False
            for line in lines:
                if "django.contrib.auth.models" in line:
                    code_part = line.split("#")[0]
                    if "import" in code_part and "User" in code_part:
                        new_lines.append(line)
                        # Insert the custom import on the next line
                        new_lines.append(
                            f"from {self.label}.models import {self.copy_model} as User\n"
                        )
                        inserted = True
                        continue
                new_lines.append(line)

            if inserted:
                with open(file, "w") as f:
                    f.writelines(new_lines)

    def _setup_temp_settings(self):
        """Create and configure temporary settings file."""
        with open(self.temp_settings, "w") as f:
            pass

        # Import the temp settings into the main settings
        with open(self.installed_apps, "a") as f:
            f.write(f"from {self.temp_settings.split('.')[0]} import * # noqa isort:skip\n")

        with open(self.temp_settings, "a") as f:
            f.write(f"AUTH_USER_MODEL = '{self.label}.{self.copy_model}'\n")

    def _rename_model_to_user(self, files):
        """Rename the custom model from copy_model to User."""
        # Rename the model in models.py
        with open(f"{self.label}/models.py", "r") as f:
            content = f.read()
            content = content.replace(self.copy_model, "User")

        with open(f"{self.label}/models.py", "w") as f:
            f.write(content)

        # Update imports in found files
        for file in files:
            with open(file, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                if f"from {self.label}.models import {self.copy_model} as User" in line:
                    print(
                        f"Fixing import in {file}: {line.strip()} -> from {self.label}.models import User"
                    )
                    line = line.replace(
                        f"from {self.label}.models import {self.copy_model} as User",
                        f"from {self.label}.models import User",
                    )
                new_lines.append(line)

            if new_lines:
                with open(file, "w") as f:
                    f.writelines(new_lines)

    def _run_migrations(self, migration_message):
        """Run makemigrations and migrate commands."""
        output = subprocess.run(
            [self.python, self.manage_py, "makemigrations", self.label],
            text=True,
            capture_output=True,
            input="y\n",
        )

        if migration_message.lower() not in output.stdout.lower():
            print(
                dedent(
                    f"""
                Warning: It looks like the migrations did not detect {migration_message}.
                This may indicate the models.py file was edited mid process or the process did not edit the file correctly.
                Please check the output below. We will stop here to avoid running migrate as something is likely wrong.
                You may need to manually perform the changes.
                """
                )
            )
            print("Output from makemigrations:")
            print(output.stdout)
            print(output.stderr)
            return False

        if not os.path.exists(f"{self.label}/migrations/0002_rename_{self.copy_model.lower()}_user.py"):
            print(
                dedent(
                    f"""
                Error: Migration file for renaming model '{self.label}.{self.copy_model}' to 'User' was not created.
                Please check the output below. We will stop here to avoid running migrate as something is likely wrong.
                You may need to manually perform the changes.
                """
                )
            )
            print("Output from makemigrations:")
            print(output.stdout)
            print(output.stderr)
            # return False

        subprocess.run(
            [self.python, self.manage_py, "migrate", self.label], text=True, input="y\n"
        )
        return True

    def _setup_admin(self):
        """Configure admin.py for the custom user model."""
        with open(f"{self.label}/admin.py", "w") as f:
            f.write(admin_content)

    def _simplify_user_model(self):
        """Simplify the custom user model after migration."""
        with open(f"{self.label}/models.py", "w") as f:
            f.write(rename_custom_model)

    def _print_success_message(self):
        """Print final instructions and success message."""
        print(
            f"\nSuccessfully switched to the new custom user model '{self.label}.User'. You may want to perform the following cleanup steps:"
        )
        print(
            f" - Remove any manual references to the old user model and point to the new model '{self.label}.User'"
        )
        print(
            f" - Remove the temporary settings file '{self.temp_settings}' and the import from {self.installed_apps} and add AUTH_USER_MODEL = '{self.label}.User' directly to your main settings.py"
        )
        print(" - Check your migrations to ensure everything is correct")
        print(
            "\nPlease TEST YOUR APPLICATION thoroughly to ensure everything is working correctly with the new user model."
        )
        print(dedent("""
                Please Note that the default user table still exists in the database and will not be deleted.
                You can manually delete it if you are sure everything works and you no longer need it.
                """))

        print("To restore files from backup, run this script with the --restore flag.")

    def main(self, skip_pause=True, dry_run=False):
        """Main method to execute the user model migration process."""
        if not dry_run:
            input(
                dedent("""
                This script will attempt to switch your Django project to use a new custom user model.
                Please ensure you have a backup of your project and database before proceeding.
                We will backup the files that will be edited in a directory named 'bigtrill_backup' in your project root directory, but you should also backup your project and database manually.
                Press Enter to continue, or Ctrl+C to abort.
                PLEASE DO NOT RUN THIS ON A PRODUCTION SYSTEM WITHOUT TESTING FIRST.
                """))

        # Find and process files with User model references
        self._find_python_files()
        found_files = self._find_user_model_references()

        print(
            "Search complete. Found references to the default User model in the following files:"
        )
        for f in found_files:
            print(f" - {f}")

        if dry_run:
            print("\nDry run mode: No changes will be made.")
            return

        # Create backups
        if found_files:
            self._create_backups(found_files)
        self._create_backups([self.installed_apps])

        print("\nStarting the process to switch to a new custom user model...")

        # Setup custom user app
        self._setup_custom_user_app()

        # Run initial migrations
        subprocess.run([self.python, self.manage_py, "makemigrations"])
        subprocess.run([self.python, self.manage_py, "migrate"])

        # Copy users
        subprocess.run([self.python, self.manage_py, "trillcopy", self.label])

        # Replace User model imports
        self._replace_user_imports(found_files)

        # Setup temporary settings
        self._setup_temp_settings()

        print(
            dedent(
                """
            We have successfully switched to using the new custom user model.
            We will now attempt to rename the model to 'User' in the models.py file, and then make migrations and migrate.
            """
            )
        )

        if not skip_pause:
            input(
                dedent(
                    f"""
                Please check if everything is correct,
                then press Enter to continue to rename model '{self.label}.{self.copy_model} to {self.label}.User'.
                (You can add the --skip_pause flag to skip this pause next time)
                """
                )
            )

        # Rename model and update imports
        self._rename_model_to_user(found_files)

        # Clear temp settings for rename migration
        with open(self.temp_settings, "w") as f:
            f.write("")

        # Run rename migrations
        if not self._run_migrations("rename model"):
            return

        # Update AUTH_USER_MODEL in temp settings
        with open(self.temp_settings, "w") as f:
            f.write(f"AUTH_USER_MODEL = '{self.label}.User'\n")

        # Setup admin and simplify model
        self._setup_admin()
        self._simplify_user_model()

        # Run final migrations
        subprocess.run(
            [self.python, self.manage_py, "makemigrations", self.label], text=True, input="y\n"
        )
        subprocess.run([self.python, self.manage_py, "migrate", self.label])

        self._print_success_message()


def main():
    parser = argparse.ArgumentParser(description="Custom user model setup script.")
    parser.add_argument(
        "--skip_pause",
        action="store_true",
        default=False,
        help="Skip the pause that allows you to check everything before proceeding to rename the model. "
        "By default, the script will pause for verification.",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        default=False,
        help="Show which files would be modified without making any changes.",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        default=False,
        help="Restore files from backup and exit.",
    )
    args = parser.parse_args()

    if args.restore:
        bigtrill = BigTrill(full=False)
        bigtrill._restore_and_cleanup()
    else:
        bigtrill = BigTrill()
        bigtrill.main(skip_pause=args.skip_pause, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
