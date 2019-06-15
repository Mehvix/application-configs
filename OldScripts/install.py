import shutil

import os
user = os.getlogin()


# TODO add launch options
# • https://steamidfinder.com/lookup/mehvix/
# • C:\Program Files (x86)\Steam\userdata\167477970

drive = "C:\\"


# Locations
age_location = drive + r"Program Files (x86)\Steam\steamapps\common\Age2HD\Profiles"
tf2_location = drive + r"Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg"
steamid = (os.listdir(drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live"))[0]
ql_location = drive + r"Program Files (x86)\Steam\steamapps\common\Quake Live\{}\baseq3".format(steamid)
apex1_location = drive + r"Users\{}\Saved Games\Respawn\Apex".format(user)
apex2_location = drive + r"Program Files (x86)\Origin Games\Apex\cfg"


def install(files: list, folders: list, location: str, game: str):
    print("\n=====================================================\n")

    # endFolder = r'ConfigCopies\{}'.format(game)
    endFolder = location

    for subfolder in folders:
        # subfolderLocation = r"\{}".format(subfolder)
        subfolderLocation = r'ConfigCopies\{}\{}'.format(game, subfolder)

        try:
            if not os.path.exists(r"{}\{}".format(endFolder, subfolder)):
                os.makedirs(r"{}\{}".format(endFolder, subfolder))  # creates folder for each subfolder if one isn't already made

            shutil.rmtree(r"{}\{}".format(endFolder, subfolder))  # deletes the subfolder's contents
            shutil.copytree(subfolderLocation, r"{}\{}".format(endFolder, subfolder))
            print("[* {}] Copying {}".format(game, subfolder))

        except (PermissionError, FileNotFoundError) as e:
            print("\n[* {} - ERROR] {}\n".format(game, e))

    for file in files:
        try:
            shutil.copy2(r'ConfigCopies\{}\{}'.format(game, file), endFolder)
            print("[** {}] Copying {}".format(game, file))

        except (PermissionError, FileNotFoundError) as e:
            print("\n[** {} - ERROR] {}\n".format(game, e))


print("\n=====================================================\n")

k = input("Press Enter to Exit")
