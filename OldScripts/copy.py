import shutil, stat
import ctypes, sys
import json

import os
user = os.getlogin()


"""
if not ctypes.windll.shell32.IsUserAnAdmin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
"""


# Stolen from https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


try:
    shutil.rmtree(r'ConfigCopies', onerror=on_rm_error)  # ignore_errors=True is because some files may be read-only
    # os.makedirs(r'ConfigCopies')
except FileNotFoundError:
    os.makedirs(r'ConfigCopies')

except PermissionError as e:
    print(e)
    os.remove(str(r"".join(str(e).split("'")[1::2])))


def copyfile(files: list, folders: list, location: str, game: str):
    print("\n=====================================================\n")

    endFolder = r'ConfigCopies\{}'.format(game)

    for subfolder in folders:
        subfolderLocation = r"\{}".format(subfolder)

        try:
            if not os.path.exists(endFolder):
                os.makedirs(endFolder)  # creates base folder for game if one isn't already made

            if not os.path.exists(endFolder + subfolderLocation):
                os.makedirs(endFolder + subfolderLocation)  # creates folder for each subfolder if one isn't already made

            shutil.rmtree(endFolder + subfolderLocation, onerror=on_rm_error)  # deletes the subfolder's contents
            shutil.copytree(r"{}\{}".format(location, subfolder), endFolder + subfolderLocation)
            print("[* {}] Copying {}".format(game, subfolder))

        except (PermissionError, FileNotFoundError) as e:
            print("\n[* {} - ERROR] {}\n".format(game, e))

    for file in files:
        try:
            if not os.path.exists(endFolder):
                os.makedirs(endFolder)

            shutil.copy2(r"{}\{}".format(location, file), endFolder)
            print("[** {}] Copying {}".format(game, file))

        except (PermissionError, FileNotFoundError) as e:
            print("\n[** {} - ERROR] {}\n".format(game, e))


if __name__ == "__main__":
    try:
        with open('settings.json', 'r') as fp:
            settings = json.load(fp)
        drive = settings["drive"]

    except (TypeError, KeyError, json.decoder.JSONDecodeError):
        try:
            with open('settings.json', 'r') as fp:
                settings = json.load(fp)
        except json.decoder.JSONDecodeError:
            settings = {}
        drive = input("Enter the drive your configs are stored on:\nIt should be formatted something like \"C:\\\"\n")
        settings["drive"] = drive
        with open('settings.json', 'w') as fp:
            json.dump(settings, fp, sort_keys=True, indent=2)


    # ========================== Apex ==========================
    location = drive + r"Users\{}\Saved Games\Respawn\Apex".format(user)
    config_folders = [r"local", r"profile"]
    copyfile([], config_folders, location, "Apex")

    location = drive + r"Program Files (x86)\Origin Games\Apex\cfg"
    config_files = ["autoexec.cfg"]
    copyfile(config_files, [], location, "Apex")

    # ========================== Quake Live ==========================
    steamid = (os.listdir(drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live"))[0]

    location = drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live\{}\baseq3".format(steamid)
    config_files = ["autoexec.cfg"]
    copyfile(config_files, [], location, "Quake Live")

    print("\n=====================================================\n")
    k = input("Press Enter to Exit")
