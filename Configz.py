import os
import sys
import json
import stat
import shutil


def clear():
    os.system('cls')


def on_rm_error(func, path, exc_info):
    # Stolen from https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def install():
    clear()


class Configz:
    def __init__(self):
        with open('settings.json', 'r') as fp:
            settings = json.load(fp)
        self.settings = settings
        self.applications = settings["applications"]

        self.configFolder = settings["scriptSettings"]["configFolder"]

    def menu(self):
        clear()
        response = input("What would you like todo?\n"
                         "Enter the corresponding char to toggle\n"
                         "----------------------------------\n"
                         "[A] Copy configs on this machine to \"ConfigCopies\"\n"
                         "[B] Install configs from \"ConfigCopies\"\n"
                         "[C] Exit\n")

        if response.upper() == "A":
            Configz.copy_step1(self)
        elif response.upper() == "B":
            install()
        elif response.upper() == "C":
            sys.exit()
        else:
            clear()
            Configz.menu(self)

    def copy_step1(self):
        clear()
        print("What application(s) would you like to copy?\n"
              "Enter the corresponding char to toggle\n"
              "Num\t| Yes\t| Application\n"
              "----------------------------------")
        i = 0
        for application in self.applications:
            status = str(self.applications[application]["status"]).lower()
            if status == "enabled":
                status = "[X]"
            elif status == "disabled":
                status = "[ ]"
            else:
                status = "[ ]"
                self.settings["applications"][str(list(self.applications)[i])]["status"] = "disabled"
                with open('settings.json', 'w') as fp:
                    json.dump(self.settings, fp, sort_keys=False, indent=4)
            i += 1
            print("[" + str(i) + "]\t| " + status + "\t| " + application)

        print("----------------------------------\n"
              "[A]\t| Continue\n"
              "[B]\t| Back")

        response = input("")

        if response.upper() == "A":
            Configz.copy_step2(self)
            return
        elif response.upper() == "B":
            Configz.menu(self)
            return

        try:
            if int(response) <= len(self.applications):
                response = int(response) - 1

                if self.applications[list(self.applications)[int(response)]]["status"] == "enabled":
                    self.settings["applications"][str(list(self.applications)[int(response)])]["status"] = "disabled"
                else:
                    self.settings["applications"][str(list(self.applications)[int(response)])]["status"] = "enabled"
                with open('settings.json', 'w') as fp:
                    json.dump(self.settings, fp, sort_keys=False, indent=4)
                Configz.copy_step1(self)
        except ValueError:
            Configz.copy_step1(self)
        else:
            Configz.copy_step1(self)

    def copy_step2(self):
        clear()
        i = 0
        for application in self.applications:
            if self.applications[list(self.applications)[i]]["status"] == "enabled":
                self.folder(r"{}\{}".format(self.configFolder, application), application)

                for rule in self.applications[list(self.applications)[i]]["rules"]:
                    try:
                        for folder in self.applications[list(self.applications)[i]]["rules"][rule]["configFolders"]:
                            self.folder(r"{}\{}\{}".format(self.configFolder, application, folder), application)
                            self.copy_folder(
                                r"{}\{}".format(self.applications[list(self.applications)[i]]["rules"][rule]["dir"],
                                                folder), r"{}\{}\{}".format(self.configFolder, application, folder),
                                application)
                    except KeyError:
                        pass  # no config files/folders
                    try:
                        for file in self.applications[list(self.applications)[i]]["rules"][rule]["configFiles"]:
                            self.copy_files(self.applications[list(self.applications)[i]]["rules"][rule]["dir"], file,
                                            application)
                    except KeyError:
                        pass  # no config files/folders

            i += 1
        print("Finished!")
        self.menu()

    def decode(self, entry: str):  # todo add regex later
        i = 1
        k = 1
        drives = self.settings["machineSettings"][str(self.settings["scriptSettings"]["activeMachine"])]["drives"]
        steamLibs = self.settings["machineSettings"][str(self.settings["scriptSettings"]["activeMachine"])][
            "steamLibraries"]
        for drive in drives:
            entry = entry.replace(str("__drive{}__").format(i), self.settings["machineSettings"][
                str(self.settings["scriptSettings"]["activeMachine"])]["drives"][drive])
            i += 1

        for lib in steamLibs:
            entry = entry.replace(str("__steamLib{}__").format(k), self.settings["machineSettings"][
                str(self.settings["scriptSettings"]["activeMachine"])]["steamLibraries"][lib])
            k += 1

        entry = entry.replace("__username__", os.getlogin())
        return entry

    def copy_files(self, start_dir: str, file, app: str):
        start_dir = self.decode(start_dir)
        end_dir = r"{}\{}".format(self.configFolder, app)
        try:
            shutil.copy2(r"{}\{}".format(start_dir, file), end_dir)
            print("[{}] Copying {}".format(app, file))

        except FileNotFoundError:
            print("*[{}] Couldn't find {}".format(app, file))

    def copy_folder(self, start_dir: str, end_dir: str, app: str):
        start_dir = self.decode(start_dir)

        self.folder(self.configFolder, app)
        self.folder(r"{}\{}".format(self.configFolder, app), start_dir)

        shutil.rmtree(end_dir, onerror=on_rm_error)  # deletes the subfolder's contents
        shutil.copytree(start_dir, end_dir)
        print("[{}] Copying {}".format(app, start_dir))

    def folder(self, location: str, app: str):
        location = self.decode(location)

        if not os.path.exists(location):
            os.makedirs(location)  # creates base folder if one isn't already made
            print("[{}] Creating {}".format(app, location))


Configz().menu()
