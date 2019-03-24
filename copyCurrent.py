import re
import shutil

import os
user = os.getlogin()


# TODO add launch options
# • https://steamidfinder.com/lookup/mehvix/
# • C:\Program Files (x86)\Steam\userdata\167477970

drive = "C:\\"


def copy(files: list, folders: list, location: str, game: str):
    print("\n=====================================================\n")

    endFolder = r'ConfigCopies\{}'.format(game)

    for subfolder in folders:
        subfolderLocation = r"\{}".format(subfolder)

        try:
            if not os.path.exists(endFolder):
                os.makedirs(endFolder)  # creates base folder for game if one isn't already made

            if not os.path.exists(endFolder + subfolderLocation):
                os.makedirs(endFolder + subfolderLocation)  # creates folder for each subfolder if one isn't already made

            shutil.rmtree(endFolder + subfolderLocation)  # deletes the subfolder's contents
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


# Age of Empires II
location = drive + r"Program Files (x86)\Steam\steamapps\common\Age2HD\Profiles"
configFiles = ["player0.hki"]  # Maybe Steam workshop files / mods?
copy(configFiles, [], location, "Age2HD")


# TF2
location = drive + r"Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg"
configFiles = ["autoexec.cfg", "server_blacklist.txt", "config.cfg", "settings.cfg","custom.cfg", "gfx.cfg", "network.cfg", "binds.cfg",
               "demoman.cfg", "engineer.cfg", "heavyweapons.cfg", "medic.cfg", "sniper.cfg", "spy.cfg", "pyro.cfg", "scout.cfg", "soldier.cfg"]
configFolders = [r"tweaks"]
copy(configFiles, configFolders, location, "Team Fortress 2")


# Apex
# Todo: Get nvidia settings file
location = drive + r"Users\{}\Saved Games\Respawn\Apex".format(user)
configFolders = [r"local", r"profile"]  # Maybe Steam workshop files / mods?
copy([], configFolders, location, "Apex")


# Quake Live
steamid = (os.listdir(drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live"))[0]

location = drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live\{}\baseq3".format(steamid)
configFiles = ["autoexec.cfg"]  # Maybe Steam workshop files / mods?
copy(configFiles, [], location, "Quake Live")


print("\n=====================================================\n")
k = input("Press Enter to Exit")
