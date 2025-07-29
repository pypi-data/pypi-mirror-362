import argparse
import os
import subprocess
import sys

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


def main(pause_to_check=True):
    if not os.path.exists("bigtrill_settings.py"):
        raise FileNotFoundError(
            "bigtrill_settings.py not found. Please create this file with the necessary settings."
        )

    sys.path.append(os.getcwd())
    import bigtrill_settings as settings

    validate_path(settings.INSTALLED_APPS_SETTINGS_FILE_PATH, "INSTALLED_APPS_SETTINGS_FILE_PATH")
    validate_path(settings.BASE_DIR, "BASE_DIR")
    validate_path(settings.MANAGE_PY_FILE, "MANAGE_PY_FILE")

    input("""
This script will attempt to switch your Django project to use a new custom user model.
Please ensure you have a backup of your project and database before proceeding.
Press Enter to continue, or Ctrl+C to abort.\n PLEASE DO NOT RUN THIS ON A PRODUCTION SYSTEM WITHOUT TESTING FIRST.\n
""")

    paths_to_search = settings.FILES_TO_SEARCH
    if paths_to_search:
        for path in paths_to_search:
            validate_path(path, "FILES_TO_SEARCH")

    python = settings.PYTHON
    manage_py = settings.MANAGE_PY_FILE
    label = settings.NEW_AUTH_APP_LABEL
    installed_apps = settings.INSTALLED_APPS_SETTINGS_FILE_PATH
    base_dir = settings.BASE_DIR
    copy_model = settings.COPY_MODEL
    temp_settings = "bigtrill_temp_settings.py"

    # search for references to the default user model
    if not paths_to_search:

        gitignore_path = settings.GITIGNORE_PATH
        exclude_dirs = set()
        if os.path.exists(gitignore_path):
            with open(gitignore_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("!"):
                        # Only handle directory ignores for now
                        if line.endswith("/"):
                            exclude_dirs.add(os.path.normpath(os.path.join(base_dir, line)))
                        elif os.path.isdir(os.path.join(base_dir, line)):
                            exclude_dirs.add(os.path.normpath(os.path.join(base_dir, line)))

        exclude_dirs.add(os.path.normpath(os.path.join(base_dir, label)))
        exclude_dirs.add(os.path.normpath(os.path.join(base_dir, "bigtrill")))
        paths_to_search = []
        for root, dirs, files in os.walk(base_dir):
            # Remove excluded directories from search
            dirs[:] = [
                d for d in dirs if os.path.normpath(os.path.join(root, d)) not in exclude_dirs
            ]
            for file in files:
                if file.endswith(".py"):
                    paths_to_search.append(os.path.join(root, file))

    found = []
    for path in paths_to_search:
        with open(path, "r") as f:
            content = f.read()
        if "from django.contrib.auth.models" in content:
            found.append(path)

    print("Search complete. Found references to the default User model in the following files:")
    for f in found:
        print(f" - {f}")

    paths_to_search = None  # free memory

    # Example: List files in the current directory
    # start the app
    subprocess.run([python, manage_py, "startapp", settings.NEW_AUTH_APP_LABEL], text=True)

    # edit the models.py file to add the custom user model
    with open(f"{settings.NEW_AUTH_APP_LABEL}/models.py", mode="a") as f:
        f.write(custom_model.format(n=copy_model))

    # edit the settings.py file to add the new app
    with open(installed_apps, "a") as f:
        f.write("\n\n# Added by bigtrill.start\n")
        f.write(f"INSTALLED_APPS += ['{label}', 'bigtrill']\n")

    # make and run migrations
    subprocess.run([python, manage_py, "makemigrations"])
    subprocess.run([python, manage_py, "migrate"])

    # copy users
    subprocess.run([python, manage_py, "trillcopy", label], text=True)

    for file in found:
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
                    new_lines.append(f"from {label}.models import {copy_model} as User\n")
                    inserted = True
                    continue
            new_lines.append(line)

        if inserted:
            with open(file, "w") as f:
                f.writelines(new_lines)

    # create a temp_settings file to avoid loading the full django settings
    with open(temp_settings, "w") as f:
        pass

    # import the temp settings into the main settings
    with open(installed_apps, "a") as f:
        f.write(f"from {temp_settings.split('.')[0]} import * # noqa isort:skip\n")

    with open(temp_settings, "a") as f:
        f.write(f"AUTH_USER_MODEL = '{label}.{copy_model}'\n")

    print("""
We have successfully switched to using the new custom user model.
We will now attempt to rename the model to 'User' in the models.py file, and then make migrations and migrate.""")

    if pause_to_check:
        input(f"""
Please check if everything is correct,
then press Enter to continue to rename model '{label}.{copy_model} to {label}.User'.
(You can remove the --pause_to_check flag to skip this pause next time)\n""")

    # rename the model from {copy_model} to User
    with open(f"{label}/models.py", "r") as f:
        content = f.read()
        content = content.replace(copy_model, "User")

    with open(f"{label}/models.py", "w") as f:
        f.write(content)

    # now we edit the files we found to change the import to import User from the new app
    for file in found:
        with open(file, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if f"from {label}.models import {copy_model} as User" in line:
                print(
                    f"Fixing import in {file}: {line.strip()} -> from {label}.models import User"
                )
                line = line.replace(
                    f"from {label}.models import {copy_model} as User",
                    f"from {label}.models import User",
                )
            new_lines.append(line)

        if new_lines:
            with open(file, "w") as f:
                f.writelines(new_lines)

    # remove the AUTH_USER_MODEL line from the temp settings file, so we can migrate
    with open(temp_settings, "w") as f:
        f.write("")

    # makemigrations
    output = subprocess.run(
        f"echo y | {python} {manage_py} makemigrations {label}",
        capture_output=True,
        shell=True,
        text=True,
    )
    if "rename model" not in output.stdout.lower():
        print("""
Warning: It looks like the migrations did not detect a rename of the model. \
This may indicate the models.py file was edited mid process or the process did not edit the file correctly. \
Please check the output below. We will stop here to avoid running migrate as something is likely wrong.
You may need to manually perform the rename.""")
        print("Output from makemigrations:")
        print(output.stdout)
        print(output.stderr)
        return  # stop here to avoid running migrate if something is wrong

    # run migrate again to apply the rename
    subprocess.run([python, manage_py, "migrate", label], text=True, input="y\n")

    # Point the AUTH_USER_MODEL to the renamed model
    with open(temp_settings, "w") as f:
        f.write(f"AUTH_USER_MODEL = '{label}.User'\n")

    # add the content of admin.py
    with open(f"{label}/admin.py", "w") as f:
        f.write(admin_content)

    # overwrite the models.py file with a simple User model definition removing the custom fields
    with open(f"{label}/models.py", "w") as f:
        f.write(rename_custom_model)

    subprocess.run(
        f"echo y | {python} {manage_py} makemigrations {label}",
        capture_output=True,
        shell=True,
        text=True,
    )
    subprocess.run([python, manage_py, "migrate", label], text=True, input="y\n")

    print(
        f"\nSuccessfully switched to the new custom user model '{label}.User'. You may want to perform the following cleanup steps:"  # noqa
    )
    print(
        f" - Remove any manual references to the old user model in and point to the new model '{label}.User'"
    )
    print(
        f" - Remove the temporary settings file '{temp_settings}' and the import from {installed_apps} and add AUTH_USER_MODEL = '{label}.User' directly to your main settings.py"  # noqa
    )
    print(" - Check your migrations to ensure everything is correct")
    print(
        "\nPlease TEST YOUR APPLICATION thoroughly to ensure everything is working correctly with the new user model."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom user model setup script.")
    parser.add_argument(
        "--pause_to_check",
        action="store_true",
        default=True,
        help="This will pause the script switching to the new user model, so you can check everything is correct before proceeding. You can remove this flag to skip the pause and run straight through.",  # noqa
    )
    args = parser.parse_args()
    main(pause_to_check=args.pause_to_check)
