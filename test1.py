import glob
from pathlib import Path
import dearpygui.dearpygui as dpg
from screeninfo import get_monitors
from default_actionmaps_parser import returnDict as actionmapsdict
import pygame, pygame.freetype
from demos.pynput_demo1 import MouseTracker, KeyboardTracker
import time
import os

dpg.create_context()
dpg.create_viewport(title="test1")
dpg.configure_viewport(0, width=920, height=600, max_width=920, decorated=True, resizable=False)

from theme import global_theme, invisible_button_theme

from pyactionmapper.structure import actionmaps
# from pyactionmapper.structure import profile

"""
Ideas for waaaaayyyyyy later:
- Custom command maker: for perhaps being able to add stuff like custom paint selections on buy menu open
"""

class mapper():
    def test_callback(self, param1, param2):
        print(param1, param2)

    def get_monitor_res(self):
        for m in get_monitors():
            if m.is_primary:
                return m.width, m.height

    def __init__(self, selected_profile=None):
        self.FILE_DEFAULTACTIONMAPS = "xml/default_actionmaps.xml"
        xml_dir = Path("{}/xml".format("E:/Documents/ProgrammingStuff/Python/DearPyGUI_Sandbox"))
        self.xml_actionmap = Path(f"{xml_dir}/default_actionmaps.xml")
        self.dtd_actionmap = Path(f"{xml_dir}/actionmaps.dtd")
        self.xml_templates = glob.glob(f"{xml_dir}/actionmaps_*.xml")

        self.actionmap_complete = actionmaps()
        # NOTE: actionmap_complete will only be useful/populated with data after its "load" method has been run
        self.actionmap_complete.load(self.xml_actionmap, self.dtd_actionmap)
        # print(self.actionmap_complete)

        self.IMAGE_KEY_BG = "images/button_type1.png"

        monitor_res = self.get_monitor_res()
        self.PRIMARY_MONITOR_RES_W = monitor_res[0]
        self.PRIMARY_MONITOR_RES_H = monitor_res[1]

        with dpg.item_handler_registry(tag="widget_handler"):
            dpg.add_item_double_clicked_handler(callback=self.test_callback)

        with dpg.font_registry():
            self.default_font = dpg.add_font("fonts/27_RussellSquare.ttf", 12)
            self.header_font = dpg.add_font("fonts/27_RussellSquare.ttf", 14)
        self.setup_display()
        dpg.set_primary_window(window=self.main_window, value=True)
        self.user_input_device_type = ""

    def setup_display(self):
        with dpg.window(label="test1", tag="primary", no_resize=True) as self.main_window:
            # establish menu bar and its child buttons:
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Switch Profile")
                    dpg.add_menu_item(label="New...")
                    dpg.add_menu_item(label="Import...")
                    dpg.add_menu_item(label="Export...")
                    dpg.add_separator()
                    dpg.add_menu_item(label="Exit", callback=self.exit_window)
                dpg.add_menu_item(label="Help")

            self.binds_display = dpg.add_child_window(parent=self.main_window, pos=[0, 16], width=904, resizable_x=False, show=True, always_auto_resize=True)

            self.profile_player_name = dpg.add_text(parent=self.binds_display, default_value="Profile: MechWarrior")

            # establish our tab bar and all child tabs:
            self.main_tab_bar = dpg.add_tab_bar(parent=self.binds_display)
            self.main_tab_player = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_player", label="Player")
            self.main_tab_vehicle = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_vehicle", label="Vehicle")
            self.main_tab_mech = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_mech", label="Mech")
            self.main_tab_tank = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_tank", label="Tank")
            self.main_tab_vtol = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_vtol", label="VTOL")
            self.main_tab_aerospace = dpg.add_tab(parent=self.main_tab_bar, tag="tabbar_tab_aero", label="Aerospace")

            # establish tab contents:
            self.tab_contents_player = self.tab_contents(parent=self.main_tab_player, ctrlcat="player")
            self.tab_contents_vehicle = self.tab_contents(parent=self.main_tab_vehicle, ctrlcat="vehicle")
            self.tab_contents_mech = self.tab_contents(parent=self.main_tab_mech, ctrlcat="mech")
            self.tab_contents_tank = self.tab_contents(parent=self.main_tab_tank, ctrlcat="tank")
            self.tab_contents_vtol = self.tab_contents(parent=self.main_tab_vtol, ctrlcat="vtol")
            self.tab_contents_aerospace = self.tab_contents(parent=self.main_tab_aerospace, ctrlcat="aerospace")


            # self.binds_configure = dpg.add_child_window(parent=self.main_window, pos=[500, 16], width=400, resizable_x=False)
            # self.binds_test_text = dpg.add_text(parent=self.binds_configure, default_value="binds configuration happens here", pos=[0, 0])

            # bind item-specific handlers:


            # configure global font:
            dpg.bind_font(self.default_font)

            # configure individual item fonts:
            dpg.bind_item_font(self.profile_player_name, self.header_font)
            dpg.bind_item_font(self.main_tab_bar, self.header_font)
            dpg.bind_item_font(self.main_tab_player, self.header_font)
            dpg.bind_item_font(self.main_tab_vehicle, self.header_font)
            dpg.bind_item_font(self.main_tab_mech, self.header_font)
            dpg.bind_item_font(self.main_tab_tank, self.header_font)
            dpg.bind_item_font(self.main_tab_vtol, self.header_font)
            dpg.bind_item_font(self.main_tab_aerospace, self.header_font)



        dpg.bind_theme(global_theme)
        # dpg.bind_item_theme(self.binds_test_text_button, invisible_button_theme)
        # dpg.bind_item_theme(self.profile_player_name, invisible_button_theme)

        # dpg.show_style_editor()

    def load_actionmap_as_list(self, cat):
        """
        Loads a list of actions given a tab category (e.g. "mech", "VTOL", "tank")
        :param cat: a category of actions to load ("player", "vehicle", "mech", "tank", "vtol", "aerospace")
        :return: a list of actions and their assigned binds, from the corresponding actionmaps section
        """

        actions_list = self.actionmap_complete.get_section(cat)[0]["action"]
        print(actions_list)
        return actions_list

    def tab_contents(self, parent, ctrlcat):
        """
        Insert a window with a table into the indicated tab, populated with that tab's corresponding actionmap actions.
        :param parent: the tab the completed table will belong to
        :param ctrlcat: the action category ("player", "vehicle", "mech", "tank", "vtol", "aerospace")
        :return: the final window with populated table
        """

        # TODO: Create a class-wide dictionary that holds lists of all sections of actionmaps, which is written to when making any bind change. This is then written to a new XML file.

        # controlcategory_dict = actionmapsdict(self.FILE_DEFAULTACTIONMAPS)[ctrlcat]
        # print(controlcategory_dict)
        controlcategory_list = self.load_actionmap_as_list(ctrlcat)
        controlcategory = dpg.add_child_window(parent=parent)
        with dpg.table(parent=controlcategory, header_row=True, resizable=True):
            column_action = dpg.add_table_column(label="Action")
            column_bind1 = dpg.add_table_column(label="Bind 1")
            column_bind2 = dpg.add_table_column(label="Bind 2")

            for action in controlcategory_list:
                action_name = action["@name"]
                print(action_name)
                with dpg.table_row(tag=f"table_{ctrlcat}_row_{action_name}") as bind_row:
                    action_text = dpg.add_text(f"{action_name}")
                    try:
                        action_bind1 = action["key"][0]["@name"]
                        action_bind2 = action["key"][1]["@name"]
                        if action_bind1 == "null":
                            action_bind1 = "none"
                        if action_bind2 == "null":
                            action_bind2 = "none"
                    except KeyError:
                        # for cases where the actionmaps file only has one bind listed for the action currently being read
                        if type(action["key"]) == dict:
                            action_bind1 = action["key"]["@name"]
                            if action_bind1 == "null":
                                action_bind1 = "none"
                            action_bind2 = "none"
                    bind1_text = dpg.add_selectable(label=f"{action_bind1}",
                                                    tag=f"{ctrlcat}#{action_name}#bind1#{action_bind1}",
                                                    callback=self.pass_selected_actionbind)
                    bind2_text = dpg.add_selectable(label=f"{action_bind2}",
                                                    tag=f"{ctrlcat}#{action_name}#bind2#{action_bind2}",
                                                    callback=self.pass_selected_actionbind)
                    dpg.bind_item_handler_registry(bind1_text, "widget_handler")
                    dpg.bind_item_handler_registry(bind2_text, "widget_handler")

            # for action in controlcategory_dict:
            #     print(controlcategory_dict[action])
            #     with dpg.table_row(tag=f"table_{ctrlcat}_row_{action}") as bind_row:
            #         print(f"bind_row: {dpg.get_item_alias(bind_row)}")         # trying to identify which integers correspond to which UI widgets/elements...
            #         action_text = dpg.add_text(f"{action}")
            #         print(action_text)
            #         action_bind1 = controlcategory_dict[action][0]
            #         bind1_text = dpg.add_selectable(label=f"{action_bind1}", tag=f"{ctrlcat}#{action}#bind1#{action_bind1}", callback=self.pass_selected_actionbind)
            #         dpg.bind_item_handler_registry(bind1_text, "widget_handler")
            #         print(bind1_text)
            #         action_bind2 = controlcategory_dict[action][1]
            #         bind2_text = dpg.add_selectable(label=f"{action_bind2}", tag=f"{ctrlcat}#{action}#bind2#{action_bind2}", callback=self.pass_selected_actionbind)
            #         dpg.bind_item_handler_registry(bind2_text, "widget_handler")
            #         print(bind2_text)

        return controlcategory

    def pass_selected_actionbind(self, bindtag):
        dpg.configure_item(item=bindtag, default_value=False)
        print(bindtag)
        extracted_action_info = bindtag.split("#")
        extracted_action_name = extracted_action_info[1]
        extracted_action_selectedbind = extracted_action_info[3]
        extracted_action_selectedbindnum = extracted_action_info[2].replace("bind", "bind ")
        self.on_keybind_click(extracted_action_name, extracted_action_selectedbind, extracted_action_selectedbindnum)


    def combo_setvalue(self, sender):
        combo_value = dpg.get_value(sender)
        # self.user_input_device_type = combo_value
        # print(self.user_input_device_type)
        selectedInput = self.get_user_device_input_pynput(combo_value)
        if selectedInput != "":
            dpg.configure_item("rebindwindow_promptfield", default_value=selectedInput)
        else:
            print("need input to proceed!")

    def on_keybind_click(self, action, bind, bindnum):
        # print(type(action), type(bind))
        print(action, bind, bindnum)
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
            rebindwindow_prompttext = dpg.add_text(f"Rebind {action} ({bindnum}) to")
            rebindwindow_promptfield = dpg.add_input_text(default_value=f"{bind} (current)", auto_select_all=True, readonly=True, tag="rebindwindow_promptfield")
            # put section on right half of window that gives the user options to choose input method (from dropdown menu; kbd/m/jstk-cntrlr)
            # selecting one of these options will then open a screen prompting the user to press a key or move their mouse/press mouse button
            rebindwindow_inputdevicetype_list = ["mouse axis", "mouse button", "keyboard", "joystick / controller"]
            rebindwindow_inputdevicetype = dpg.add_combo(items=rebindwindow_inputdevicetype_list,
                                                         default_value="Select an input device",
                                                         callback=self.combo_setvalue)

            dpg.add_text("After selecting an input device, you will be prompted to use it", wrap=250)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="confirm")
                dpg.add_button(label="cancel", callback=lambda: dpg.delete_item("rebind_popup"))

            # print(dpg.get_value(rebindwindow_inputdevicetype))
            dpg.bind_item_font(rebindwindow_prompttext, self.header_font)

        # get_user_input = self.get_user_device_input()



    """def get_user_device_input(self):
        # 
        # This function is needed to get user key/mouse/joystick inputs and format their names into terms that Crysis Wars will understand
        # :return:
        # 

        key_name = ""
        mouse_pressed = ""
        mouse_scroll = ""
        mouse_dir = ""

        active_input = "Press a key"

        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()

        # takeover_size_W = self.PRIMARY_MONITOR_RES_W // 2
        # takeover_size_H = self.PRIMARY_MONITOR_RES_H // 2

        takeover_size_W = dpg.get_viewport_width()
        takeover_size_H = dpg.get_viewport_height()

        takeover_pos_X = dpg.get_viewport_pos()[0]
        takeover_pos_Y = dpg.get_viewport_pos()[1]

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (takeover_pos_X, takeover_pos_Y)

        screen = pygame.display.set_mode(size=(takeover_size_W, takeover_size_H), flags=pygame.NOFRAME)
        screen.fill((255, 255, 255, 0))
        a_font = pygame.font.Font("fonts/27_RussellSquare.ttf", 24)
        while True:
            key_press = a_font.render(f"{active_input}", True, (255, 0, 0))
            screen.blit(source=key_press, dest=(takeover_size_W // 2, takeover_size_H // 2))
            print(active_input)
            pygame.display.flip()
            clock.tick(60)
            while key_name == "" and mouse_pressed == "" and mouse_scroll == "" and mouse_dir == "":
                for event in pygame.event.get():
                    mouse1, mouse3, mouse2, mouse4, mouse5 = pygame.mouse.get_pressed(num_buttons=5)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        key_name = pygame.key.name(event.key)
                        # rename keys as necessary
                        if key_name == "\\":
                            key_name = "backslash"
                        if key_name == "'":
                            key_name = "apostrophe"
                        if key_name == ";":
                            key_name = "semicolon"
                        if key_name == ".":
                            key_name = "period"
                        if key_name == ",":
                            key_name = "comma"
                        if key_name == "enter":
                            key_name = "np_enter"
                        if key_name == "return":
                            key_name = "enter"
                        if key_name == "right alt":
                            key_name = "ralt"
                        if key_name == "left alt":
                            key_name = "lalt"
                        if key_name == "right ctrl":
                            key_name = "rctrl"
                        if key_name == "left ctrl":
                            key_name = "lctrl"
                        if key_name == "right shift":
                            key_name = "rshift"
                        if key_name == "left shift":
                            key_name = "lshift"
                        if key_name == "page up":
                            key_name = "pgup"
                        if key_name == "page down":
                            key_name = "pgdn"
                        if key_name == "[1]":
                            key_name = "np_1"
                        if key_name == "[2]":
                            key_name = "np_2"
                        if key_name == "[3]":
                            key_name = "np_3"
                        if key_name == "[4]":
                            key_name = "np_4"
                        if key_name == "[5]":
                            key_name = "np_5"
                        if key_name == "[6]":
                            key_name = "np_6"
                        if key_name == "[7]":
                            key_name = "np_7"
                        if key_name == "[8]":
                            key_name = "np_8"
                        if key_name == "[9]":
                            key_name = "np_9"
                        if key_name == "[0]":
                            key_name = "np_0"
                        if key_name == "[*]":
                            key_name = "np_multiply"
                        if key_name == "[/]":
                            key_name = "np_divide"
                        if key_name == "[+]":
                            key_name = "np_add"
                        if key_name == "[-]":
                            key_name = "np_subtract"
                        if key_name == "[.]":
                            key_name = "np_period"
                        print(key_name)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if mouse1:
                            mouse_pressed = "mouse1"
                            print(mouse_pressed)
                        if mouse2:
                            mouse_pressed = "mouse2"
                            print(mouse_pressed)
                        if mouse3:
                            mouse_pressed = "mouse3"
                            print(mouse_pressed)
                        if mouse4:
                            mouse_pressed = "mouse4"
                            print(mouse_pressed)
                        if mouse5:
                            mouse_pressed = "mouse5"
                            print(mouse_pressed)
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y > 0:
                            mouse_scroll = "mwheel_up"
                            print(mouse_scroll)
                        if event.y < 0:
                            mouse_scroll = "mwheel_down"
                            print(mouse_scroll)
                    if event.type == pygame.MOUSEMOTION:
                        if event.pos[0] != 0 and event.pos[1] == 0:
                            mouse_dir = "maxis_y"
                            print(mouse_dir)
                        if event.pos[1] != 0 and event.pos[0] == 0:
                            mouse_dir = "maxis_x"
                            print(mouse_dir)
            for input_cat in [key_name, mouse_pressed, mouse_scroll, mouse_dir]:
                if input_cat != "":
                    active_input = input_cat
                    print(active_input)

            time.sleep(0.5)
            pygame.quit()
            break

        print(active_input)
        return active_input
"""

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
                mousemoveInput_button = dpg.add_button(label=f"{mousemoveInput}", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(mousemoveInput_button, invisible_button_theme)
                user_input = mousemoveInput

            elif devicetype == "mouse button":
                inputdevice_mousemove_instr_button = dpg.add_button(label="Press a mouse button or scroll", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a mouse button or scroll")[0], dpg.get_viewport_height() // 2 - 25])
                dpg.bind_item_theme(inputdevice_mousemove_instr_button, invisible_button_theme)

                mouseTracker = MouseTracker()
                mouseTracker.start_tracking(waitTime)
                mousebuttonInput = mouseTracker.get_buttonPressed()
                mousebuttonInput_button = dpg.add_button(label=f"{mousebuttonInput}", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(mousebuttonInput_button, invisible_button_theme)
                user_input = mousebuttonInput

            elif devicetype == "keyboard":
                inputdevice_keyboard_instr_button = dpg.add_button(label="Press a keyboard button", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a keyboard button")[0], dpg.get_viewport_height() // 2 - 25])
                dpg.bind_item_theme(inputdevice_keyboard_instr_button, invisible_button_theme)

                keyboardTracker = KeyboardTracker()
                keyboardTracker.start_tracking()
                keyboardkeyInput = keyboardTracker.get_keyPressed()
                keyboardkeyInput_button = dpg.add_button(label=f"{keyboardkeyInput}", width=int(dpg.get_text_size("------------------------------")[0]), pos=[dpg.get_viewport_width()//2 - dpg.get_text_size("------------------------------")[0], dpg.get_viewport_height()//2])
                dpg.bind_item_theme(keyboardkeyInput_button, invisible_button_theme)
                user_input = keyboardkeyInput

            elif devicetype == "joystick / controller":
                inputdevice_keyboard_instr_button = dpg.add_button(label="[WIP] Press a joystick button [WIP]", width=window_rect_size[0], pos=[dpg.get_viewport_width() // 2 - dpg.get_text_size("Press a keyboard button")[0], dpg.get_viewport_height() // 2 - 25])
                dpg.bind_item_theme(inputdevice_keyboard_instr_button, invisible_button_theme)

            time.sleep(waitTime)
            dpg.configure_item("rebind_popup", show=True)
            dpg.delete_item("input_prompt")

        return user_input


    @staticmethod
    def exit_window(_sender, _data):
        dpg.stop_dearpygui()


if __name__ == '__main__':
    mapper = mapper()


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

