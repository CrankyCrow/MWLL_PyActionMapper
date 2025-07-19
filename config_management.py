import time

from structure.structure import profile as profilereader
import configparser
import os

class Config:
    def __init__(self):
        # get the root path to all profiles:
        homedir = os.path.expanduser("~/")
        profiles_root = os.path.join(homedir, "Documents/My Games/Crysis Wars/Profiles")
        # print(profiles_root)
        profiles_paths_list = [f.path for f in os.scandir(profiles_root) if f.is_dir()]
        # print(profiles_paths_list)
        # make a list of all profiles in the root profiles directory:
        self.profiles_list = []
        for profile_path in profiles_paths_list:
            if os.path.exists(os.path.join(profile_path, "profile.xml")):
                profile_obj = profilereader(profile_path)
                self.profiles_list.append(profile_obj)
        # print(self.profiles_list)

    def get_profiles_list(self):
        return self.profiles_list

    def createConfig(self, defaultprofile, dontaskagain):
        config = configparser.ConfigParser()
        # add sections and key-value pairs:
        config["config"] = {"setting_dontaskagain": str(dontaskagain),
                            "setting_defaultprofile": defaultprofile}

        for profile in self.profiles_list:
            config[f"{profile.name}"] = {"profile_path": profile.profile_dir, "profile_backups_dir": profile.backup_dir}

        print(config)

        with open("config.ini", "w") as configfile:
            config.write(configfile)

    @staticmethod
    def readConfig():
        config = configparser.ConfigParser()

        config.read("config.ini")

        config_values = []

        for s in config.sections():
            if s != "config":
                profile_dict = {"config_profile_name": s,
                                "config_profile_path": config.get(s, "profile_path"),
                                "config_profile_backups_dir": config.get(s, "profile_backups_dir")}
                config_values.append(profile_dict)
            else:
                config_settings_dict = {"config_setting_dontaskagain": config.getboolean(s, "setting_dontaskagain"),
                                        "config_setting_defaultprofile": config.get(s, "setting_defaultprofile")}
                config_values.append(config_settings_dict)

        # print("config values:", config_values)
        return config_values

# conf = Config()
# conf.createConfig()
# print(conf.readConfig())


