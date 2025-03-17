import glob
from os.path import dirname,expanduser
from pathlib import Path
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk

import collections

from structure import actionmaps
from structure import profile

def donothing():
    pass
# from util import VerticalScrolledFrame
class mapper():
    _file=Path(__file__)
    _module=dirname(_file.absolute())
    print(_module)
    src_dir=dirname(_module)
    print(src_dir)
    app_name="action mapper"
    

    # At some point should upgrade this to point to either the real mwll dir OR the mwll-code dir
    xml_dir=Path("{}/xml".format(src_dir))
    xml_actionmap=Path(f"{xml_dir}/default_actionmaps.xml")
    dtd_actionmap=Path(f"{xml_dir}/actionmaps.dtd")
    xml_templates=glob.glob(f"{xml_dir}/actionmaps_*.xml")

    def __init__(self,selected_profile=None):
        self.main_window=None
        # alpha has different directory i think, but old action mapper didnt have obvious handling for that.
        # because of that, making this a per-instance var so we can update it.
        self.user_dir_suffix="My Games/Crysis Wars/Profiles"

        # Get user directory
        # new win
        self.user_dir=expanduser("~/Documents")
        # old win
        self.user_dir=expanduser("~/My Documents")
        self.profiles_dir=Path(f"{self.user_dir}/{self.user_dir_suffix}")
        self.user_dir=Path(self.user_dir)
        self.profiles=self.get_profiles()
        if not len(self.profiles):
            print(f"No user profiles found, will use example data")
            self.profiles=[ profile(mapper.xml_dir,test_mode=True) ]
            self.profiles[0].xml_actionmaps=Path(f"{mapper.xml_dir}/example_user.xml")
            selected_profile=None
        if selected_profile is None:
            self.selected_profile=self.profiles[0]
        else:
            self.selected_profile=None
            for _p in self.profiles:
                if _p.name == selected_profile:
                    self.selected_profile=_p
                    break
            if self.selected_profile is None:
                raise ValueError(f"Bad profile specified, no {selected_profile} in {self.profiles_dir}")
        
        self.load_default()

        # todo: support other command line flags where we might not setup display
        self.setup_display()
        self.switch_profile(self.selected_profile)
        # main_window is defined inside setup_display, there is clearly an incorrect ordre of operations here.
        self.main_window.mainloop()

    def load_default(self):
        self.default_map=actionmaps()
        self.default_map.load(mapper.xml_actionmap,mapper.dtd_actionmap)
        #print("Sections:{}".format(self.default_map.sections()))
    def get_profiles(self):
        # should return a list of profiles, profiles are a minimal class to hold name, and dir, and backup_dir etc....
        return [ profile(dirname(a_map)) for a_map in glob.glob(f"{self.profiles_dir}/*/actionmaps.xml") ]
    def switch_profile(self,a_profile):
        #TODO: update the loaded values. This highlights current strucutre is bad becuase this is a chore. 
        #   configure should be changed such that filling the entries is its own function
        # load user map
        # update display map...?
        self.selected_profile=a_profile
        self.selected_profile.load_actionmaps(mapper.dtd_actionmap)
        self.profile_name.set(f"Profile name = {self.selected_profile.name}")
        self.u_map=self.selected_profile.actionmaps
        if not self.u_map.xml_valid:
            print(f"Warning: XML NOT valid!, take care when modifiying XML!, will give this our best try")
        user_missing=[]
        for s_idx,section_name in enumerate(self.tab_names):
            (section,map_s_idx)=self.default_map.get_section(section_name)
            if section is None:
                print(f"Found no xml section {section_name}")
                continue
            (u_section,u_map_s_idx)=self.u_map.get_section(section_name)
            if u_section is None:
                print(f"missing user section {section_name}")
                section=u_section
                self.selected_profile.modified=True
            u_vers=u_section["version"]
            d_vers=section["version"]
            if u_vers != d_vers :
                u_section["version"]=d_vers
                self.selected_profile.modified=True
            # update section labels text ?
            #self.section_labels[s_idx]
            for a_idx,action in enumerate(section["action"]):
                # get the user action
                (a,a_idx)=self.u_map.get_action(u_section,action["name"],True)
                if a is None:
                    user_missing.append((section_name,action["name"]))
                    #raise Exception(f"section {section_name} no user action {action} user section {u_section}")
                    a=action
                try:
                    ky_dct=a["key"]
                except Exception as e:
                    print(f"Invalid action! {a}. Substituting default data!")
                    a=action
                    ky_dct=a["key"]
                print(f"section_name: {section_name}")
                print(f"action_keys: {self.action_keys}")
                print(f"action[\"name\"]: {action['name']}")
                try:
                    a_keys=self.action_keys[section_name][action["name"]]
                except KeyError as e:
                    print(self.action_keys.keys())
                    raise e
                print(f"a_keys (l127): {a_keys}")
                # bandaid when only one key is defined. This should be fixed during load instead of here.
                if type(ky_dct) is not list:
                    ky_dct=[ky_dct,None]
                    self.selected_profile.modified=True
                for col,key in enumerate(a_keys):
                    try:
                        k_name=ky_dct[col]["name"]
                    except Exception as e:
                        k_name="null"
                    if k_name == "null":
                        k_name=""
                    if k_name != a_keys[col].get():
                        # TODO: Some how add feedback that the user key is not default, and potentially offer a set-default button?
                        # print(f"User key {action['name']}{col+1} is not default")
                        pass
                    a_keys[col].set(k_name)
        if len(user_missing):
            print("These actions were not defined by the user, and will be updated with the default values:")
            for missing in user_missing:
                print(missing)
   
    def setup_display(self):
        # generate main display
        self.tab_names=self.default_map.section_names()
        # not sold on calling this method configure... but that is what the user would be doing.
        self.main_window = tk.Tk()
        self.main_window.title(mapper.app_name)
        
        self.menubar = Menu(self.main_window)
        self.profile_menu = Menu(self.menubar, tearoff=0)
        #self.profile_menu.add_command(label="New", command=donothing)
        self.profile_menu.add_command(label="Restore Backup", command=self.restore_backup)
        self.profile_menu.add_command(label="Save", command=self.selected_profile.save_actionmaps())
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Exit", command=self.main_window.quit)
        self.menubar.add_cascade(label="File", menu=self.profile_menu)
        #'''
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        #'''
        self.main_window.config(menu=self.menubar)
        
        self.profile_name=tk.IntVar()
        self.profile_name.set(f"Profile name = {self.selected_profile.name}")
        self.profile_label=ttk.Label(self.main_window,textvariable=self.profile_name)# text=self.selected_profile.name)
        self.profile_label.pack(expand=1, fill="both")

        ### generate the section tabs from default xml
        self.tab_control = ttk.Notebook(self.main_window)
        self.tab_control.pack(expand=1, fill="both")
        self.section_tabs=[None] * len(self.tab_names)
        self.section_labels=[None] * len(self.tab_names)
        self.action_labels=collections.OrderedDict()
        self.action_keys=collections.OrderedDict()
        # note: we use default actionmaps to handle ordering, so we use the section names from there.
        for s_idx,section_name in enumerate(self.tab_names):
            self.section_tabs[s_idx] = ttk.Frame(self.tab_control)
            # gui_tabs[s_idx] = VerticalScrolledFrame(tabControl)
            self.tab_control.add(self.section_tabs[s_idx], text=section_name)
            #s_label.pack()
            row_n=0
            (section,map_s_idx)=self.default_map.get_section(section_name)
            if section is None:
                print(f"Found no xml section {section_name}")
                continue
            map_vers=section["version"]
            self.section_labels[s_idx]=ttk.Label(self.section_tabs[s_idx], text=f"{section_name} vers={map_vers}")
            self.section_labels[s_idx].grid(column=0, row=row_n, padx=30, pady=30)
            row_n=row_n+1
            col_st=0
            self.action_labels[section_name]=collections.OrderedDict()
            self.action_keys[section_name]=collections.OrderedDict()
            # note: we use default actionmaps to handle ordering, so we use the default section to set the action order, 
            # also we update user info from there (when user does not have a given action listed).
            for a_idx,action in enumerate(section["action"]):
                try:
                    self.action_labels[section_name][action["name"]]=ttk.Label(self.section_tabs[s_idx], text=action["display_name"])
                except KeyError as e:
                    self.action_labels[section_name][action["name"]]=ttk.Label(self.section_tabs[s_idx], text=action["name"])
                self.action_labels[section_name][action["name"]].grid(column=col_st, row=row_n, padx=0, pady=0)
                #a_label.pack()
                ky_dct=action["key"]
                if type(ky_dct) is not list:
                    k=collections.OrderedDict()
                    k["name"]="null"
                    ky_dct=[ky_dct,k]
                a_keys=[]
                for col,key in enumerate(ky_dct):
                    k_name=key["name"]
                    if k_name == "null":
                        k_name=""
                    tvar=tk.StringVar()
                    tvar.set(k_name)
                    a_keys.append(tvar)
                    # Text entry is NOT the correct thing. It would probably be better to use a button which after clicking waited for user entered key.
                    e = tk.Entry(self.section_tabs[s_idx],textvariable=tvar)
                    e.grid(row=row_n,column=col+col_st+1)
                    #e.pack()
                    print(f"a_keys for {k_name} (l228): {a_keys}")
                self.action_keys[section_name][action["name"]]=a_keys
                row_n=row_n+1
                # prevent row count from getting too long. 
                # This is to prevent a need for scrolling in the interface becuase that was hard to implement.
                if row_n > len(section["action"])/2 or row_n > 25:
                    col_st=col_st+3
                    row_n=1
        
    def validate(self):
        # validate a loaded action map(WAIT.... no no no, that should be part of the actionap loading...)
        pass
    def compare(self,map1,map2=None):
        # with two actionmaps create comparrison data structure,...
        # display either through printout, OR through some kinda cool tree visualization.
        if map2 is None:
            map2=map1
            map1=self.default_map
        pass
    def restore_backup(self,):
        pass

if __name__ == '__main__':
    mapper=mapper()
    