import time
import glob
from pathlib import Path
import dearpygui.dearpygui as dpg
import lxml.etree as xmlementtree
from screeninfo import get_monitors
from ast import literal_eval as EvalStr
import xmltodict
import os
import platform
import ctypes
from ctypes import wintypes

from input.pynput_trackers import MouseTracker, KeyboardTracker
import config_management
from structure.tabs_actiondict_master import TabsActionDictMaster as actiondict_master

# the following three lines MUST be placed BEFORE the import statement that follows them!
dpg.create_context()
dpg.create_viewport(title="pyActionmapper")
dpg.configure_viewport(0, width=920, height=600, max_width=920, max_height=600, decorated=True, resizable=False)

from theme_registry import global_theme, invisible_button_theme, error_popup_theme
from gui_elements import *

from structure.structure import actionmaps
from profile_select import ProfileSelect

class PyMapper:
    def __init__(self):
        with dpg.value_registry():
            dpg.add_string_value(tag="tracker_str_selectedprofile", default_value="MechWarrior")
            dpg.add_string_value(tag="tracker_str_selectedprofile_actionmaps", default_value="")

        monitor_res = self.get_monitor_res()
        self.PRIMARY_MONITOR_RES_W = monitor_res[0]
        self.PRIMARY_MONITOR_RES_H = monitor_res[1]

        self.VERSION = "0.0.5a"

        # establish vars for config management
        ## get the root path to all profiles:
        homedir = ""
        systemType = platform.system()
        # print(systemType)
        if systemType == "Windows":
            homedir = str(self.SpecialFolder(5))
        elif systemType == "Linux":
            homedir = os.path.expanduser("~/")
        cwdir = "\\My Games\\Crysis Wars"
        print("homedir:", homedir)
        self.profiles_root = homedir + cwdir + "\\Profiles"
        print(self.profiles_root)
        profilefolder_missing = False
        try:
            self.config = config_management.Config(profiles_root=self.profiles_root)
        except FileNotFoundError:
            profilefolder_missing = True
        print("profile folder missing?", profilefolder_missing)
        self.config_setting_dontaskagain = False
        self.config_profiles_names_list = []

        self.profile_player_actionmap_path = ""

        # get the root path to MWLL client dir (to access actionmapper.cfg)
        # self.client_root = os.path.join(homedir, "/My Games/Crysis Wars/MWLL/Client")
        self.client_root = homedir + cwdir + "\\MWLL\\Client"
        self.client_actionmapperconfig = "actionmapper.cfg"
        print(self.checkActionmapper_cfg())

        self.xml_dir = Path(f"{os.getcwd()}/xml")
        self.TEMPFILE_NAME = ".amtemp"
        self.TEMPFILE_PATH = Path(f"{self.xml_dir}/{self.TEMPFILE_NAME}.xml")
        self.xml_default_actionmap = Path(f"{self.xml_dir}/default_actionmaps.xml")  # default actionmaps
        self.dtd_actionmap = Path(f"{self.xml_dir}/actionmaps.dtd")
        self.dtd_game_gen_actionmap = Path(f"{self.xml_dir}/game_gen_actionmaps.dtd")
        self.xml_templates = glob.glob(f"{self.xml_dir}/actionmaps_*.xml")

        self.actionmap_active = actionmaps()
        self.actionmap_saved = actionmaps()
        # NOTE: the above two variables will only be useful/populated with data after their respective "load" methods have been run
        self.actionmap_active.load(self.xml_default_actionmap, self.dtd_actionmap)          # this is the currently active actionmap, by default loaded with the default actionmaps
        self.actionmap_saved.load(self.xml_default_actionmap, self.dtd_actionmap)
        print(type(self.actionmap_active))
        # create list object to hold initially-loaded actionmaps:
        self.actionmap_master_OG_list = EvalStr(
            self.actionmap_saved.__str__().removeprefix("actionmaps(").removesuffix(")"))
        # print("Original AM:", self.actionmap_master_OG_list)
        # create list object to hold what will be the modified actionmaps:
        self.actionmap_master_new_list = EvalStr(
            self.actionmap_active.__str__().removeprefix("actionmaps(").removesuffix(")"))
        print(type(self.actionmap_master_new_list))
        # create link to dictionary file that maps tab contents' layouts:
        self.actiondict_master = actiondict_master
        # immediately create a temporary file that will serve as the actionmap to write to and read from when changes are made:
        self.write_actionmaps_to_xml(self.actionmap_master_new_list, istemp=True)

        # establish list of special case actions that are linked to another action:
        ## special case actions should not be displayed for editing, as modifying them may cause undesirable behavior in-game
        ## each entry is structured to include data that acts as a pointer for what to compare with:
        ### tab name -> action name -> pointer to linked action, containing: linked action name, linked action tab name, and linked action tab section
        self.ACTIONS_MIRROREDBINDS = {
            "player": {
                "hud_hide_multiplayer_scoreboard": {"linkedAction": "hud_show_multiplayer_scoreboard", "linkedActionTab": "player", "linkedActionSection": "Main HUD Elements"},
            },
            "vehicles": {
                "Toggle_CBill_Menu": {"linkedAction": "Toggle_CBill_Menu", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},
                "Confirm_CBill_Menu": {"linkedAction": "Confirm_CBill_Menu", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},
                "Choose_CBill_Player": {"linkedAction": "Choose_CBill_Player", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},
                "Choose_CBill_Amount": {"linkedAction": "Choose_CBill_Amount", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},
                "Next_CBill_Option": {"linkedAction": "Next_CBill_Option", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},
                "Prev_CBill_Option": {"linkedAction": "Prev_CBill_Option", "linkedActionTab": "player", "linkedActionSection": "C-Bill Sharing"},

                "Stop_Fire_Current_Group": {"linkedAction": "Fire_Current_Group", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group1": {"linkedAction": "Fire_Group1", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group2": {"linkedAction": "Fire_Group2", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group3": {"linkedAction": "Fire_Group3", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group4": {"linkedAction": "Fire_Group4", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group5": {"linkedAction": "Fire_Group5", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
                "Stop_Fire_Group6": {"linkedAction": "Fire_Group6", "linkedActionTab": "vehicles", "linkedActionSection": "Weapon Management"},
            }
        }

        # control exceptions that can be permitted to be inverted (this will be written to actionmapper.cfg as cvars)
        self.EXCEPTIONS_INVERTCONTROLS = {"maxis_x", "maxis_y"} # come up with a better solution.... that is dependent on control type (e.g. ASF pitch, VTOL yaw) rather than input type

        # center the viewport in the user's primary monitor
        dpg.configure_viewport(0, x_pos=(self.PRIMARY_MONITOR_RES_W // 2) - (dpg.get_viewport_max_width() // 2),
                               y_pos=(self.PRIMARY_MONITOR_RES_H // 2) - (dpg.get_viewport_height() // 2))

        # self.setup_display()

        dpg.set_exit_callback(callback=self.delete_tempfile)

        # check that the [user home]/Profiles folder exists and/or is populated
        if profilefolder_missing or (len(os.listdir(self.profiles_root)) == 0):
            error_msg = f"No profiles found in Documents\\My Games\\Crysis Wars\\Profiles!\n\nYou must create a new profile in Crysis Wars before using this application.\n"
            self.on_error_popup(error_title="No profiles found, exiting!", error_msg=error_msg, showbutton=True, callback=self.exit_window)

        # assuming profiles' root folder exists, detect whether a config.ini file exists in the Profiles dir
        # if config file doesn't exist, prompt the user to generate one via the profile selection screen, before they can use the rest of the software
        if not profilefolder_missing:
            configPath = os.path.join(self.profiles_root, "actionmapper_config.ini")
            if not os.path.exists(configPath):
                print("No actionmapper_config.ini found! Prompting user for initial profile selection...")
                self.config.createConfig(defaultprofile=None, dontaskagain=False)         # generate placeholder config
                self.prompt_profileselect_default()
            else:
                print("actionmapper_config.ini found...")
                self.get_configdata()
                print(" checking if user asked to be prompted again...")
                print(" config dontaskagain:", self.config_setting_dontaskagain)
                if self.config_setting_dontaskagain:
                    print(" user did NOT want to be asked again...")
                    self.prompt_profileselect_default()         # Initialize the dialogue, so it may be opened later
                    dpg.hide_item("profile_popup")
                else:
                    print(" user did want to be asked again...")
                    self.prompt_profileselect_default()

        dpg.set_primary_window(window=self.main_window, value=True)

    def SpecialFolder(self, id):
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, id, None, 0, buf)
        return Path(buf.value)

    def checkActionmapper_cfg(self):
        print("Client dir:", self.client_root)
        print("Client dir found?", os.path.exists(self.client_root))
        fileCheck = os.path.exists(self.client_root + os.sep + self.client_actionmapperconfig)
        if fileCheck:
            return "actionmapper.cfg detected"
        else:
            return "no actionmapper.cfg found in Client directory"

    def load_actionmaps(self, actionmap_xml):
        # redefine which actionmap file is loaded, as both active and save state instances
        try:
            print(f"trying to validate {actionmap_xml} with {self.dtd_actionmap.name}...")
            dpg.set_value("tracker_str_selectedprofile_actionmaps", value=actionmap_xml)
            self.actionmap_active.load(actionmap_xml, self.dtd_actionmap)  # this is the currently active actionmap
            self.actionmap_saved.load(actionmap_xml, self.dtd_actionmap)
        except xmlementtree.DTDParseError:
            print(f"trying to validate {actionmap_xml} with {self.dtd_game_gen_actionmap.name}...")
            self.actionmap_active.load(actionmap_xml,
                                       self.dtd_game_gen_actionmap)
            self.actionmap_saved.load(actionmap_xml, self.dtd_game_gen_actionmap)

        # create list object to hold initially-loaded actionmaps:
        self.actionmap_master_OG_list = EvalStr(
            self.actionmap_saved.__str__().removeprefix("actionmaps(").removesuffix(")"))
        # print("Original AM:", self.actionmap_master_OG_list)
        # create list object to hold what will be the modified actionmaps:
        self.actionmap_master_new_list = EvalStr(
            self.actionmap_active.__str__().removeprefix("actionmaps(").removesuffix(")"))
        # immediately create a temporary file that will serve as the actionmap to write to and read from when changes are made:
        self.write_actionmaps_to_xml(self.actionmap_master_new_list, istemp=True)
        # refresh display
        dpg.delete_item("primary")
        self.setup_display()
        dpg.set_primary_window("primary", True)

    def prompt_profileselect_default(self):
        """
        Opens the Profile Select window by calling profile_select.py.
        """
        self.get_configdata()
        print("profiles list from config.ini:", self.config_profiles_names_list)
        ProfileSelect(profiles_list=self.config_profiles_names_list, callback=self.get_configdata, profiles_root=self.profiles_root, dont_ask_again=self.config_setting_dontaskagain)

    def add_profile_name_to_profilenameslist(self, sctn):
        if "config_profile_name" in sctn:
            profile_name = sctn["config_profile_name"]
            if (profile_name != "" or profile_name != "None") and (profile_name not in self.config_profiles_names_list):
                self.config_profiles_names_list.append(profile_name)

    def get_configdata(self):
        """
        Reads the contents of actionmapper_config.ini \n
        Sets value of `self.config_setting_dontaskagain` and updates the profile names list
        """
        print("reading config data...")
        config = config_management.Config(profiles_root=self.profiles_root)
        config_data = config.readConfig()
        # print(config_data)
        # generate list of profiles:
        for section in config_data:
            print("config section:", section)
            if "config_setting_dontaskagain" in section:
                self.config_setting_dontaskagain = section["config_setting_dontaskagain"]
                print("config dontaskagain:", self.config_setting_dontaskagain)
            if "config_setting_defaultprofile" in section:
                dpg.set_value("tracker_str_selectedprofile", section["config_setting_defaultprofile"])
                print("default profile name:", section["config_setting_defaultprofile"])
            if ("config_profile_name" in section) and (section["config_profile_name"] == dpg.get_value("tracker_str_selectedprofile")) and ("config_profile_path" in section):
                self.profile_player_actionmap_path = Path(os.path.join(section['config_profile_path'], 'actionmaps.xml'))
                print("Selected profile's actionmaps path:", self.profile_player_actionmap_path)
                if os.path.exists(self.profile_player_actionmap_path):
                    try:
                        print("selected profile\'s actionmaps.xml file found, attempting validation...")
                        self.load_actionmaps(self.profile_player_actionmap_path)
                    except Exception as e:
                        print(e)
                        # self.on_error_popup(e)

            self.add_profile_name_to_profilenameslist(section)

    def get_monitor_res(self):
        for m in get_monitors():
            if m.is_primary:
                return m.width, m.height

    def on_error_popup(self, error_title, error_msg, showbutton=False, callback=None):
        with dpg.window(label=f"{error_title}",
                        tag="error_popup",
                        autosize=True,
                        width=400,
                        height=150,
                        no_resize=False,
                        modal=True,
                        popup=True,
                        no_close=True):
            dpg.add_text(error_msg, wrap=400)
            dpg.add_spacer(width=dpg.get_item_width("error_popup"), height=5)
            dpg.add_button(label="Okay", tag="error_popup_button_okay", show=showbutton, callback=callback)

        dpg.configure_item("error_popup", pos=[
            int(dpg.get_viewport_max_width() // 2) - (dpg.get_item_width("error_popup") // 2),
            int(dpg.get_viewport_height() // 2) - (dpg.get_item_height("error_popup") // 2)
        ])

        dpg.bind_item_theme(item="error_popup", theme=error_popup_theme)

    def setup_display(self, default_tab=None):
        # dpg.set_frame_callback(5, callback=self.startup_check_config)
        with dpg.window(label="pyActionmapper", tag="primary", no_resize=True) as self.main_window:
            # establish menu bar and its child buttons:
            with dpg.menu_bar(tag="primary_menubar", parent="primary"):
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Switch Profile", callback=self.on_switchprofile_prompt)            # open a different profile's actionmaps
                    # dpg.add_menu_item(label="Reset to default", callback=self.on_resetdefault_prompt)         # reset current actionmap to default version
                    # dpg.add_menu_item(label="Reset changes")          # reset current actionmap to last saved version of current actionmap
                    # dpg.add_menu_item(label="New")                                          # create a new actionmap
                    dpg.add_menu_item(label="Open", callback=self.on_open_prompt)           # browse to and open an existing actionmap
                    dpg.add_menu_item(label="Save As", callback=self.on_save_prompt)           # save actionmap to a file
                    dpg.add_separator()
                    dpg.add_menu_item(label="Exit", callback=self.exit_window)
                # with dpg.menu(label="Tools"):
                #     dpg.add_menu_item(label="Generate Keymap Diagram")          # implement later, see @TO-DO#QOL_IDEA_3
                with dpg.menu(label="Help"):
                    # dpg.add_menu_item(label="Usage guide (opens in browser)", callback=None)            # implement later
                    # dpg.add_separator()
                    dpg.add_menu_item(label="About", callback=self.on_about_dialogbox)

            dpg.add_child_window(tag="binds_display", parent=self.main_window, pos=[0, 16], width=904, resizable_x=False, show=True, always_auto_resize=True)

            with dpg.group(tag="profile_info_display", parent="binds_display", horizontal=False):
                with dpg.group(tag="profile_info_player_name_group", parent="profile_info_display", horizontal=True):
                    dpg.add_text("Profile:", tag="profile_info_player_name_prompt", parent="profile_info_player_name_group")
                    dpg.add_text("", tag="profile_info_player_name", parent="profile_info_player_name_group", source="tracker_str_selectedprofile", indent=60)
                with dpg.group(tag="profile_info_player_actionmaps_path_group", parent="profile_info_display", horizontal=True):
                    dpg.add_text("Current Actionmaps:", tag="profile_info_player_actionmaps_path_prompt", parent="profile_info_player_actionmaps_path_group")
                    dpg.add_text("", tag="profile_info_player_actionmaps_path", source="tracker_str_selectedprofile_actionmaps", parent="profile_info_player_actionmaps_path_group")

            dpg.add_separator(parent="binds_display")

            # establish our tab bar and all child tabs:
            dpg.add_tab_bar(tag="tabbar_main", parent="binds_display")
            dpg.add_tab(tag="tabbar_tab_player", parent="tabbar_main", label="Player")
            dpg.add_tab(tag="tabbar_tab_ba", parent="tabbar_main", label="Battle Armor")
            dpg.add_tab(tag="tabbar_tab_vehicles", parent="tabbar_main", label="All Vehicles")
            dpg.add_tab(tag="tabbar_tab_mech", parent="tabbar_main", label="Mech")
            dpg.add_tab(tag="tabbar_tab_tank", parent="tabbar_main", label="Tank")
            dpg.add_tab(tag="tabbar_tab_vtol", parent="tabbar_main", label="VTOL")
            dpg.add_tab(tag="tabbar_tab_aerospace", parent="tabbar_main", label="Aerospace")

            # establish tab contents:
            self.populate_tab(parent="tabbar_tab_player", tabname="player")
            self.populate_tab(parent="tabbar_tab_ba", tabname="ba")
            self.populate_tab(parent="tabbar_tab_vehicles", tabname="vehicles")
            self.populate_tab(parent="tabbar_tab_mech", tabname="mech")
            self.populate_tab(parent="tabbar_tab_tank", tabname="tank")
            self.populate_tab(parent="tabbar_tab_vtol", tabname="vtol")
            self.populate_tab(parent="tabbar_tab_aerospace", tabname="aerospace")

            # configure global font:
            dpg.bind_font(default_font)

            # configure individual item fonts:
            # dpg.bind_item_font("profile_info_player_name_prompt", header_font)
            # dpg.bind_item_font("profile_info_player_name", header_font)
            dpg.bind_item_font("tabbar_main", header_font)
            dpg.bind_item_font("tabbar_tab_player", header_font)
            # dpg.bind_item_font("tabbar_tab_interface", header_font)
            dpg.bind_item_font("tabbar_tab_ba", header_font)
            dpg.bind_item_font("tabbar_tab_vehicles", header_font)
            dpg.bind_item_font("tabbar_tab_mech", header_font)
            dpg.bind_item_font("tabbar_tab_tank", header_font)
            dpg.bind_item_font("tabbar_tab_vtol", header_font)
            dpg.bind_item_font("tabbar_tab_aerospace", header_font)

            dpg.bind_theme(global_theme)

            # bring the user back to the tab they were working in:
            if default_tab is not None:
                print(f"restoring tab: {default_tab}")
                dpg.set_value(item="tabbar_main", value=f"tabbar_tab_{default_tab.lower()}")

    def load_actionmap_as_list(self, cat):
        """
        Loads a list of actions given a tab category (e.g. "mech", "VTOL", "tank")
        :param cat: a category of actions to load ("player", "vehicle", "mech", "tank", "vtol", "aerospace")
        :return: a list of actions and their assigned binds, from the corresponding actionmaps section
        """

        actions_list = self.actionmap_active.get_section(cat)[0]["action"]
        # print(actions_list)
        return actions_list

    def tab_action_format_checker(self, actionval):
        """
        Checks that the given line/action in the actiondict_master follows the format [category, description, [list of binds]]
        :param actionval: the value of the checked action in the actiondict_master
        :return: True or False - whether the given action's value follows the aforementioned format
        """
        check_pass = False
        print("actionval:", actionval)
        if type(actionval[0]) == str and type(actionval[1]) == str and type(actionval[2]) == list and len(actionval[2]) == 2:
            check_pass = True

        return check_pass

    def update_tabs(self, tabname):
        selectedTab = self.actiondict_master.tabs[tabname]
        # print("selectedTab:", selectedTab)
        for section in selectedTab:
            # print(section)
            for action in selectedTab[section]:
                # print(action, f"\n  {selectedTab[section][action]}")
                action_category = selectedTab[section][action][0]
                controlcategory_list = self.load_actionmap_as_list(action_category)
                # print("controlcategory_list:", controlcategory_list)
                # print(self.actionmap_active.get_action(action_category, action))
                # print("controlcategory_list:", controlcategory_list)
                for actionmap_action in controlcategory_list:
                    if str(actionmap_action["@name"]) == action:
                        if len(selectedTab[section][action]) == 2:
                            print("actionmap_action:", actionmap_action)
                            # print(selectedTab[section][action])
                            # for exceedingly rare cases where the current action has no bind slots at all:
                            if "key" not in actionmap_action:
                                print(f"encountered action with no binds: {actionmap_action}")
                                # force add two empty bind slots:
                                selectedTab[section][action].append([{'@name': "null"}, {'@name': "null"}])
                                actionmap_action["key"] = selectedTab[section][action][2]
                                # print("modified actionmap_action:", actionmap_action)
                                # print("modified controlcategory_list:", controlcategory_list)
                                print("added two empty bind slots")
                            # for cases where loaded actionmap xml has only one bind slot for the current action:
                            elif len(actionmap_action["key"]) == 1:
                                print(f"encountered action with missing bind slot: {actionmap_action}")
                                # force add empty second bind slot, as part of a new list of bind slots:
                                selectedTab[section][action].append([actionmap_action["key"], {'@name': "null"}])
                                print("added one empty second bind slot:", selectedTab[section][action])
                            else:
                                selectedTab[section][action].append(actionmap_action["key"])

                        elif self.tab_action_format_checker(selectedTab[section][action]):
                            selectedTab[section][action][2] = actionmap_action["key"]

                    else:
                        pass

                # mirror any special case actions' binds to their corresponding actions
                if tabname in self.ACTIONS_MIRROREDBINDS.keys():
                    print(f"tabname {tabname} found in ACTIONS_MIRROREDBINDS")
                    if action in self.ACTIONS_MIRROREDBINDS[tabname].keys():
                        linked_action = self.ACTIONS_MIRROREDBINDS[tabname][action]["linkedAction"]  # get name of linked action to copy bind slots
                        linked_action_section = self.ACTIONS_MIRROREDBINDS[tabname][action]["linkedActionSection"]  # get tab section of linked action
                        linked_action_tab = self.ACTIONS_MIRROREDBINDS[tabname][action]["linkedActionTab"]   # get tab of linked action
                        print(f"ENCOUNTERED ACTION {action} ({section}), WHICH IS LINKED TO {linked_action} ({linked_action_tab}, {linked_action_section}):")
                        print(" pre-mirror:", selectedTab[section][action])
                        selectedTab[section][action][2] = self.actiondict_master.tabs[linked_action_tab][linked_action_section][linked_action][2]
                        print(f"    SPECIAL CASE ACTION {action} RE-BOUND AS FOLLOWS: {selectedTab[section][action]}")
                        bindindx = -1
                        for b in self.actiondict_master.tabs[linked_action_tab][linked_action_section][linked_action][2]:
                            bindindx += 1
                            self.update_master_new_list_bind(category=action_category, action=action,
                                                             bindnum=bindindx,
                                                             newbind=b['@name'])
        print("selectedTab (after tab update):", selectedTab)
        return selectedTab

    def populate_tab(self, parent, tabname):
        """
        Controls visual display of tabs' contents
        :param parent: parent object (tab object)
        :param tabname: name of tab in actiondict_master to populate
        :return: None
        """

        selectedTab = self.update_tabs(tabname)

        hidden_sections = [
            "C-Bill Sharing h",
            "Main HUD Elements h",
            "Weapon Management h"
        ]

        controlcategory = dpg.add_child_window(parent=parent)
        with dpg.table(parent=controlcategory, header_row=True, resizable=True, tag=f"table_{tabname}", borders_innerH=True):

            dpg.add_table_column(label=" Action", no_clip=True, tag=f"table_{tabname}_columnheader_action")
            dpg.add_table_column(label="Bind 1", no_clip=True, tag=f"table_{tabname}_columnheader_bind1")
            dpg.add_table_column(label="Bind 2", no_clip=True, tag=f"table_{tabname}_columnheader_bind2")
            # print("item width:", dpg.get_item_configuration(parent))
            for actiontype in selectedTab:
                print(actiontype)
                if actiontype in hidden_sections:
                    pass
                else:
                    with dpg.table_row(tag=f"table_{tabname}_row_{actiontype}"):
                        with dpg.child_window(no_scrollbar=True, menubar=False, border=False, auto_resize_y=True, auto_resize_x=True, width=dpg.get_viewport_width()):
                            dpg.add_text(f"{actiontype}", tag=f"table_{tabname}_row_{actiontype}_text")
                for action in selectedTab[actiontype]:
                    tab_hasMirroredBinds = False
                    if tabname in self.ACTIONS_MIRROREDBINDS:
                        tab_hasMirroredBinds = True
                    if tab_hasMirroredBinds and action in self.ACTIONS_MIRROREDBINDS[tabname] and actiontype in hidden_sections:
                        print(f"FOUND SPECIAL CASE ACTION - {action} - SKIPPING DISPLAY")
                        pass
                    else:
                        with dpg.table_row(tag=f"table_{tabname}_row_{action}"):
                            currentAction = selectedTab[actiontype][action]
                            currentAction_binds = currentAction[2]
                            # print("currentAction_binds (generating row):", currentAction_binds)
                            dpg.add_text(f"   {currentAction[1]}")
                            try:
                                action_bind1 = currentAction_binds[0]["@name"]
                                action_bind2 = currentAction_binds[1]["@name"]
                                if action_bind1 == "null":
                                    action_bind1 = "none"
                                if action_bind2 == "null":
                                    action_bind2 = "none"
                            except KeyError:
                                # for cases where the actionmaps file only has one bind listed for the action currently being read
                                print(f"encountered action {action} with missing bind slot!")
                                if type(currentAction_binds) == dict:
                                    print("action binds are a dictionary! expected list of 2 dictionaries!")
                                    action_bind1 = currentAction_binds["@name"]
                                    # print(action_bind1)
                                    if action_bind1 == "null":
                                        action_bind1 = "none"
                                    action_bind2 = "none"
                            bind1_text = dpg.add_selectable(label=f"{action_bind1}",
                                                            tag=f"{tabname}#{currentAction[0]}#{action}#bind1#{action_bind1}",
                                                            callback=self.pass_selected_actionbind)
                            bind2_text = dpg.add_selectable(label=f"{action_bind2}",
                                                            tag=f"{tabname}#{currentAction[0]}#{action}#bind2#{action_bind2}",
                                                            callback=self.pass_selected_actionbind)
                            dpg.bind_item_handler_registry(bind1_text, "widget_handler")
                            dpg.bind_item_handler_registry(bind2_text, "widget_handler")


    def pass_selected_actionbind(self, bindtag):
        dpg.configure_item(item=bindtag, default_value=False)
        print(bindtag)
        extracted_action_info = bindtag.split("#")
        extracted_action_tab = extracted_action_info[0]
        extracted_action_category = extracted_action_info[1]
        extracted_action_name = extracted_action_info[2]
        extracted_action_selectedbind = extracted_action_info[4]
        extracted_action_selectedbindnum = extracted_action_info[3].replace("bind", "bind ")
        self.on_keybind_click(extracted_action_tab, extracted_action_category, extracted_action_name, extracted_action_selectedbindnum, extracted_action_selectedbind)

    def combo_setvalue(self, sender):
        combo_value = dpg.get_value(sender)
        # self.user_input_device_type = combo_value
        # print(self.user_input_device_type)
        selectedInput = self.get_user_device_input_pynput(combo_value)
        if selectedInput != "":
            dpg.configure_item("rebindwindow_promptfield", default_value=selectedInput)
            # if selectedInput in self.EXCEPTIONS_INVERTCONTROLS:
            #     dpg.configure_item("rebindwindow_invert_checkbox", show=True)
            # else:
            #     dpg.configure_item("rebindwindow_invert_checkbox", show=False)
        else:
            print("need input to proceed!")

    def on_keybind_click(self, tab, category, action, bindnum, bind):
        """
        Defines what happens when a user clicks on a keybind in the generated list of binds.
        A prompt will open, instructing the user to select a form of input.
        :param category: the name of the control category in the master actionmaps
        :param action: the name of the action in the list of actionmaps
        :param bind: the currently bound key name (as used in the actionmaps file)
        :param bindnum: the bind name and number (1 or 2), used mostly for display purposes
        :return:
        """
        # print(type(action), type(bind))
        print(category, action, bindnum, bind)
        with dpg.window(label=f"Rebind {action}",
                        no_title_bar=True,
                        autosize=True,
                        tag="rebind_popup",
                        width=250,
                        height=150,
                        no_resize=False,
                        pos=[int(dpg.get_viewport_max_width()//2) - 125, int(dpg.get_viewport_height()//2) - 75],
                        modal=True,
                        popup=True) as self.rebindwindow:
            rebindwindow_prompttext = dpg.add_text(f"Rebind {action} ({bindnum}) to", wrap=250)
            rebindwindow_promptfield = dpg.add_input_text(default_value=f"{bind} (current)", auto_select_all=True, readonly=True, tag="rebindwindow_promptfield")
            # put section on right half of window that gives the user options to choose input method (from dropdown menu; kbd/m/jstk-cntrlr)
            # selecting one of these options will then open a screen prompting the user to press a key or move their mouse/press mouse button
            rebindwindow_inputdevicetype_list = ["mouse axis", "mouse button / wheel", "keyboard"] #, "joystick / controller"]
            rebindwindow_inputdevicetype = dpg.add_combo(items=rebindwindow_inputdevicetype_list,
                                                         default_value="Select an input device",
                                                         callback=self.combo_setvalue)
            # dpg.add_checkbox(label="invert", tag="rebindwindow_invert_checkbox", show=False)
            dpg.add_text("After selecting an input device, you will be prompted to use it", wrap=250)
            dpg.add_separator()
            bind_slot = int(bindnum.removeprefix("bind ")) - 1
            with dpg.group(horizontal=True):
                print(category, action, bindnum, bind)
                dpg.add_button(label="confirm", callback=lambda: [self.on_keybind_prompt_confirm(tab=tab, category=category, action=action, bindnum=bind_slot, newbind=dpg.get_value("rebindwindow_promptfield")), dpg.delete_item("rebind_popup")])
                dpg.add_button(label="cancel", callback=lambda: dpg.delete_item("rebind_popup"))

                # if bind in self.EXCEPTIONS_INVERTCONTROLS:
                #     dpg.configure_item("rebindwindow_invert_checkbox", show=True)
                dpg.add_spacer(width=65)
                dpg.add_button(label="clear bind", callback=lambda: dpg.configure_item("rebindwindow_promptfield", default_value="none"))

            # print(dpg.get_value(rebindwindow_inputdevicetype))
            dpg.bind_item_font(rebindwindow_prompttext, header_font)

    def get_user_device_input_pynput(self, devicetype):
        # print(devicetype)
        dpg.configure_item("rebind_popup", show=False)
        user_input = ""
        waitTime = 1
        with dpg.window(
                no_title_bar=True,
                tag="input_prompt",
                show=True,
                width=dpg.get_viewport_width(),
                height=dpg.get_viewport_height(),
                no_resize=True,
                no_move=True,
                pos=[-1, 0]
        ) as inputprompt:
            window_rect_size = dpg.get_item_rect_size("rebind_popup")
            if devicetype == "mouse axis":
                # dpg.add_text("Move mouse or press a mouse button", wrap=250, label="inputdevice_mouse_instr")
                # text_rect_size = dpg.get_item_rect_size("inputdevice_mouse_instr")
                # dpg.configure_item("inputdevice_mouse_instr", pos=[int(window_rect_size[0] // 2) - text_rect_size[0], int(window_rect_size[1] // 2) - text_rect_size[1]])
                inputdevice_mousemove_instr_button = dpg.add_button(label="Move your mouse horizontally or vertically", width=window_rect_size[0], pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("Move your mouse horizontally or vertically")[0], dpg.get_viewport_height()//2 - 25])
                dpg.bind_item_theme(inputdevice_mousemove_instr_button, invisible_button_theme)

                mouseTracker = MouseTracker()
                mouseTracker.start_tracking(waitTime)
                mousemoveInput = mouseTracker.get_larger_moveAxis()
                mousemoveInput_button = dpg.add_button(label=f"{mousemoveInput} detected", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(mousemoveInput_button, invisible_button_theme)
                user_input = mousemoveInput

            elif devicetype == "mouse button / wheel":
                inputdevice_mousemove_instr_button = dpg.add_button(label="Press a mouse button or scroll", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a mouse button or scroll")[0], dpg.get_viewport_height() // 2 - 25])
                dpg.bind_item_theme(inputdevice_mousemove_instr_button, invisible_button_theme)

                mouseTracker = MouseTracker()
                mouseTracker.start_tracking(waitTime)
                mousebuttonInput = mouseTracker.get_buttonPressed()
                mousebuttonInput_button = dpg.add_button(label=f"{mousebuttonInput} detected", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(mousebuttonInput_button, invisible_button_theme)
                user_input = mousebuttonInput

            elif devicetype == "keyboard":
                inputdevice_keyboard_instr_button = dpg.add_button(label="Press a keyboard button", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a keyboard button")[0], dpg.get_viewport_height() // 2 - 25])
                dpg.bind_item_theme(inputdevice_keyboard_instr_button, invisible_button_theme)

                keyboardTracker = KeyboardTracker()
                keyboardTracker.start_tracking()
                keyboardkeyInput = keyboardTracker.get_keyPressed()
                keyboardkeyInput_button = dpg.add_button(label=f"{keyboardkeyInput} detected", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(keyboardkeyInput_button, invisible_button_theme)
                user_input = keyboardkeyInput

            # elif devicetype == "joystick / controller":
            #     inputdevice_keyboard_instr_button = dpg.add_button(label="[WIP] Press a joystick button [WIP]", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a keyboard button")[0], dpg.get_viewport_height() // 2 - 25])
            #     dpg.bind_item_theme(inputdevice_keyboard_instr_button, invisible_button_theme)

            time.sleep(waitTime)
            dpg.configure_item("rebind_popup", show=True)
            dpg.delete_item("input_prompt")

        return user_input

    def update_master_new_list_bind(self, category, action, bindnum, newbind):
        """

        :param category: the name of the section where the action-to-be-modified is located
        :param action: the name of the action being modified
        :param bindnum: the index number (0 or 1) of the bind slot to modify
        :param newbind: the name of the key to set in the bind slot
        :return:
        """
        # print("pre-update actionmap_master_new_list (given category):", self.actionmap_master_new_list[0][1]['actionmap'][9])
        newbind = str(newbind).removesuffix(" (current)")
        # print(self.actionmap_active.get_section(category))
        category_chosen = self.actionmap_active.get_section(category)[0]  # remember that get_section returns a tuple, with the important value being index 0
        # print("category chosen:", category_chosen)
        # get the index of the actionmaps section being updated:
        # print("self.actionmap_master_new_list:", self.actionmap_master_new_list)
        category_chosen_index = self.actionmap_master_new_list[0][1]['actionmap'].index(category_chosen)
        # print("player section index:", category_chosen_index)
        action_chosen = self.actionmap_active.get_action(category, action)[0]  # ditto for get_action, re: returned tuple having important stuff in index 0
        # print("chosen action:", action_chosen)
        ## get the index of the action being modified:
        action_chosen_index = category_chosen['action'].index(action_chosen)
        # print("action index:", action_chosen_index)
        # print("newbind:", newbind)
        # print("bindnum:", bindnum)
        if newbind == "none":
            newbind = "null"
        # print(action_chosen['key'])
        if type(action_chosen['key']) is dict:
            action_chosen['key'] = [{'@name': 'null'}, {'@name': 'null'}]
        ## update chosen keybind of said action:
        action_chosen['key'][bindnum]['@name'] = newbind
        # print("updated action chosen:", action_chosen)
        ## add this action back into its corresponding section, using the index acquired earlier:
        category_chosen['action'][action_chosen_index] = action_chosen
        # print("updated category chosen:", category_chosen)
        ## update the master actionmap data with the updated section:
        self.actionmap_master_new_list[0][1]['actionmap'][category_chosen_index] = category_chosen
        # print("updated master actionmaps:", self.actionmap_master_new_list)

    def on_keybind_prompt_confirm(self, tab, category, action, bindnum, newbind):
        """
        Updates a given action's bind slot with the user's chosen key.
        This change is immediately made in the new actionmaps's temp file (".amtemp.xml")
        Example: update_bind("givemecbills", 1, "rctrl") will set the "givemecbills" command's bind slot 1 to "rctrl"
        :param tab: the name of the GUI tab
        :param category: the name of the section where the action-to-be-modified is located
        :param action: the name of the action being modified
        :param bindnum: the index number (0 or 1) of the bind slot to modify
        :param newbind: the name of the key to set in the bind slot
        :return:
        """
        print("running on_keybind_prompt_confirm with these inputs:", tab, category, action, bindnum, newbind)
        self.update_master_new_list_bind(category=category, action=action, bindnum=bindnum, newbind=newbind)

        # refresh GUI:
        ## write to temp file:
        self.write_actionmaps_to_xml(self.actionmap_master_new_list, istemp=True)
        ## reload from temp file (make it the active actionmaps):
        # self.actionmap_active.load(self.TEMPFILE_PATH, self.dtd_actionmap)
        # print(self.actionmap_active.get_action(category, action))
        self.load_actionmaps(self.TEMPFILE_PATH)
        dpg.set_viewport_title("pyActionmapper *")
        ## delete existing interface at its root, and reload it with new one:
        dpg.delete_item("primary")
        print(f"restoring tab: {tab}")
        self.setup_display(default_tab=tab)
        dpg.set_primary_window(window=self.main_window, value=True)

    def write_actionmaps_to_xml(self, actionmaplist, istemp=False, outputpath=None, writedata=None, onsavegood=None):
        """
        Write actionmaps to an xml file using xmltodict.unparse
        """
        # note: the source data MUST be a dictionary
        # thus, prepare source to be turned into a dictionary:
        master_dict = {
            actionmaplist[0][0]: actionmaplist[0][1]
        }
        output_data = xmltodict.unparse(master_dict, pretty=True)
        # print(output_data)
        if istemp:
            with open(self.TEMPFILE_PATH, "w") as xmlfile:
                xmlfile.write(output_data)
                print("successfully saved temp file")
        else:
            with open(outputpath, "w") as xmlfile:
                xmlfile.write(output_data)
                if writedata["file_path_name"] == outputpath:
                    print("save successful")
                    time.sleep(0.1)
                    onsavegood()
                    self.load_actionmaps(outputpath)

    def on_save_good(self):
        """
        Popup window to alert user to a succesful xml file save.
        """
        with dpg.mutex():
            viewport_width = dpg.get_viewport_client_width()
            viewport_height = dpg.get_viewport_client_height()

            with dpg.window(tag="save_good_popup",
                            autosize=True,
                            width=250,
                            height=50,
                            no_resize=False,
                            modal=True,
                            popup=True,
                            no_close=True) as self.save_notif_good:
                dpg.add_text("File saved successfully")

        dpg.split_frame()
        popup_width = dpg.get_item_width("save_good_popup")
        popup_height = dpg.get_item_height("save_good_popup")
        print(popup_width, popup_height)
        dpg.set_item_pos("save_good_popup", [(viewport_width // 2) - (popup_width // 2), (viewport_height // 2) - (popup_height // 2)])
        print("file saved successfully")
        dpg.set_viewport_title("pyActionmapper")
        time.sleep(2)
        dpg.delete_item("save_good_popup")

    def delete_tempfile(self):
        Path.unlink(self.TEMPFILE_PATH, missing_ok=True)

    def on_switchprofile_prompt(self):
        dpg.show_item("profile_popup")

    def on_open_prompt(self):
        with dpg.file_dialog(label="Open Actionmap",
                             width=600,
                             height=300,
                             modal=True,
                             default_path=(str(self.profile_player_actionmap_path).removesuffix("actionmaps.xml")),
                             callback=lambda s, a: [print(s, a), self.load_actionmaps(actionmap_xml=a["file_path_name"])]
                             ):
            dpg.add_file_extension(".xml", color=(255, 255, 255, 255))

    def on_save_prompt(self):
        with dpg.file_dialog(label="Save Actionmap",
                             width=600,
                             height=300,
                             modal=True,
                             default_path=(str(self.profile_player_actionmap_path).removesuffix("actionmaps.xml")),
                             callback=lambda s, a: [self.write_actionmaps_to_xml(self.actionmap_master_new_list,
                                                                                 outputpath=a["file_path_name"],
                                                                                 writedata=a,
                                                                                 onsavegood=self.on_save_good),
                                                    print(s, a)]):
            dpg.add_file_extension(".xml", color=(255, 255, 255, 255))

    def on_about_dialogbox(self):
        """
        Create dialog box with pyActionmapper's description and other info.
        """
        # mutex + split_frame necessary to perform popup's positioning after it's been created, rather than during its creation
        # what happens under mutex is in one frame
        with dpg.mutex():
            viewport_width = dpg.get_viewport_client_width()
            viewport_height = dpg.get_viewport_client_height()

            with dpg.window(label=f"About pyActionmapper",
                            tag="about_popup",
                            autosize=True,
                            width=400,
                            height=150,
                            no_resize=False,
                            modal=True,
                            popup=True,
                            no_close=True) as self.about_popup:
                dpg.add_text(f"pyActionmapper is a Python-based keybind editor designed for MechWarrior: Living Legends", wrap=400)
                dpg.add_text(f"Version: {self.VERSION}")
                dpg.add_separator(tag="about_popup_separator")
                with dpg.group(tag="about_popup_buttongroup", horizontal=True):
                    dpg.add_button(tag="about_popup_button_close", label="Close", callback=lambda: dpg.delete_item("about_popup"))


        # what happens after split_frame is called will take place in the frame immediately after mutex's commands
        dpg.split_frame()
        popup_width = dpg.get_item_width(self.about_popup)
        popup_height = dpg.get_item_height(self.about_popup)
        print(popup_width, popup_height)
        dpg.set_item_pos(self.about_popup, [(viewport_width // 2) - (popup_width // 2), (viewport_height // 2) - (popup_height // 2)])
        print(dpg.get_item_pos("about_popup_separator"))
        popup_button_close_width = dpg.get_item_rect_size("about_popup_button_close")[0]
        dpg.set_item_pos("about_popup_button_close", [(popup_width // 2) - (popup_button_close_width // 2), (popup_height - 15)])

    def on_resetdefault_prompt(self):
        # create prompt asking if the user is sure they wish to proceed:
        with dpg.window(label=f"Confirm selection",
                        no_title_bar=True,
                        autosize=True,
                        tag="reset_popup",
                        width=250,
                        height=150,
                        no_resize=False,
                        pos=[int(dpg.get_viewport_max_width() // 2) - 125, int(dpg.get_viewport_height() // 2) - 75],
                        modal=True,
                        popup=True) as self.resetpopup:
            dpg.add_text("All changes will be lost.\nThis is not reversible.")
            dpg.add_spacer(height=25)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Proceed", callback=lambda: [self.on_reset_confirm(), dpg.delete_item("reset_popup")])
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("reset_popup"))

    def on_reset_confirm(self):
        print("Original AM (just before reset):", self.actionmap_master_OG_list)
        print("performing reset...")
        self.delete_tempfile()
        dpg.delete_item("primary")
        # perform reset:
        ## load back in the original actionmap xml, then reset the GUI initialized with that data
        self.actionmap_active.load(self.xml_default_actionmap, self.dtd_actionmap)
        print("Original AM givemecbills:", self.actionmap_saved.get_action("player", "givemecbills"))
        self.actionmap_master_new_list = self.actionmap_master_OG_list
        print("Original AM (just after reset):", self.actionmap_master_new_list)
        self.write_actionmaps_to_xml(self.actionmap_master_new_list, istemp=True)
        # dpg.delete_item("primary")
        self.setup_display()
        dpg.set_primary_window(window=self.main_window, value=True)
        dpg.set_viewport_title("pyActionmapper")

    @staticmethod
    def exit_window(_sender, _data):
        dpg.stop_dearpygui()

if __name__ == '__main__':
    PyMapper()

dpg.show_viewport()
dpg.setup_dearpygui()
dpg.start_dearpygui()
dpg.destroy_context()

