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

        self.config_folder = settings["script_settings"]["config_folder"]
        self.avaliable_configs = os.listdir(self.config_folder)

    def menu(self):
        response = input("What would you like todo?\n"
                         "Enter the corresponding char to toggle\n"
                         "----------------------------------\n"
                         "[A] Copy configs on this machine to \"ConfigCopies\"\n"
                         "[B] Install configs from \"ConfigCopies\"\n"
                         "[C] Exit\n")

        if response.upper() == "A":
            Configz.copy_step1(self)
        elif response.upper() == "B":
            Configz.install_step1(self)
        elif response.upper() == "C":
            sys.exit()
        else:
            clear()
            Configz.menu(self)

    def copy_step1(self):
        clear()
        print("What application(s) would you like to copy?\n"
              "Enter the corresponding char to toggle\n"
              "Num\t| State\t| Application\n"
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
            clear()
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
                self.verify(r"{}\{}".format(self.config_folder, application), application)

                for rule in self.applications[list(self.applications)[i]]["rules"]:
                    try:
                        for folder in self.applications[list(self.applications)[i]]["rules"][rule]["config_folders"]:
                            self.verify(r"{}\{}\{}".format(self.config_folder, application, folder), application)
                            self.copy_folder(
                                r"{}\{}".format(self.applications[list(self.applications)[i]]["rules"][rule]["dir"],
                                                folder), r"{}\{}\{}".format(self.config_folder, application, folder),
                                application)
                    except KeyError:
                        pass  # no config folder(s)
                    try:
                        for file in self.applications[list(self.applications)[i]]["rules"][rule]["config_files"]:
                            self.copy_files(self.applications[list(self.applications)[i]]["rules"][rule]["dir"], r"{}\{}".format(self.config_folder, application), file,
                                            application)
                    except KeyError:
                        pass  # no config file(s)

            i += 1
        print("Finished!")
        self.menu()

    def install_step1(self):
        clear()
        print("What application(s) would you like to install?\n"
              "Enter the corresponding char to toggle\n"
              "Num\t| State\t| Application\n"
              "----------------------------------")
        i = 0

        for application in self.applications:
            if application in self.avaliable_configs:
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
            else:
                status = "[BAD]"  # if script doesn't find game in ConfigCopies folder

            i += 1
            print("[" + str(i) + "]\t| " + status + "\t| " + application)

        print("----------------------------------\n"
              "[A]\t| Continue\n"
              "[B]\t| Back")

        response = input("")

        if response.upper() == "A":
            Configz.install_step2(self)
            return
        elif response.upper() == "B":
            clear()
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
                Configz.install_step1(self)
        except ValueError:
            Configz.install_step1(self)
        else:
            Configz.install_step1(self)

    def install_step2(self):
        clear()
        i = 0
        for application in self.applications:
            if application in self.avaliable_configs:
                if self.applications[list(self.applications)[i]]["status"] == "enabled":
                    for rule in self.applications[list(self.applications)[i]]["rules"]:
                        if os.path.exists(self.decode(str(self.applications[list(self.applications)[i]]["rules"][rule]["dir"]))):
                            try:
                                for folder in self.applications[list(self.applications)[i]]["rules"][rule]["config_folders"]:
                                    self.verify(r"{}\{}".format(self.applications[list(self.applications)[i]]["rules"][rule]["test_dir"], folder), application)
                                    self.copy_folder(
                                        r"{}\{}\{}".format(self.config_folder, application, folder),
                                        r"{}\{}".format(self.applications[list(self.applications)[i]]["rules"][rule]["test_dir"], folder), application)
                            except KeyError:
                                pass  # no config folder(s)
                            try:
                                for file in self.applications[list(self.applications)[i]]["rules"][rule]["config_files"]:
                                    self.copy_files(
                                        r"{}\{}".format(self.config_folder, application),
                                        self.applications[list(self.applications)[i]]["rules"][rule]["test_dir"],
                                        file, application)
                            except KeyError:
                                pass  # no config file(s)
                        else:
                            print("[ERROR] Couldn't find {} installed at {}".format(application, self.applications[list(self.applications)[i]]["rules"][rule]["dir"]))

                i += 1
        print("Finished!")

    def decode(self, entry: str):  # todo add regex later
        i = 1
        k = 1
        drives = self.settings["machine_settings"][str(self.settings["script_settings"]["active_machine"])]["drives"]
        steamLibs = self.settings["machine_settings"][str(self.settings["script_settings"]["active_machine"])][
            "steam_libraries"]
        for drive in drives:
            entry = entry.replace(str("__drive_{}__").format(i), self.settings["machine_settings"][
                str(self.settings["script_settings"]["active_machine"])]["drives"][drive])
            i += 1

        for lib in steamLibs:
            entry = entry.replace(str("__steam_lib_{}__").format(k), self.settings["machine_settings"][
                str(self.settings["script_settings"]["active_machine"])]["steam_libraries"][lib])
            k += 1

        entry = entry.replace("__username__", os.getlogin())
        return entry

    def copy_files(self, start_dir: str, end_dir: str, file, app: str):
        start_dir = self.decode(start_dir)
        end_dir = self.decode(end_dir)
        self.verify(start_dir, app)
        self.verify(end_dir, app)

        try:
            shutil.copy2(r"{}\{}".format(start_dir, file), end_dir)
            print("[{}] Copying file {}".format(app, file))

        except FileNotFoundError as e:
            print("*[{}] Couldn't find file {} ({})".format(app, file, e))

    def copy_folder(self, start_dir: str, end_dir: str, app: str):
        start_dir = self.decode(start_dir)
        end_dir = self.decode(end_dir)

        self.verify(start_dir, app)
        self.verify(end_dir, app)
        self.verify(self.config_folder, app)
        self.verify(r"{}\{}".format(self.config_folder, app), start_dir)

        shutil.rmtree(end_dir, onerror=on_rm_error)  # deletes the subfolder's contents
        shutil.copytree(start_dir, end_dir)
        print("[{}] Copying folder {}".format(app, start_dir))

    def verify(self, location: str, app: str):
        location = self.decode(location)

        if not os.path.exists(location):
            os.makedirs(location)  # creates base folder if one isn't already made
            print("[{}] Creating folder {}".format(app, location))


Configz().menu()
