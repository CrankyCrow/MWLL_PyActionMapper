import dearpygui.dearpygui as dpg
from config_management import Config
# from main import mapper

# the following three lines MUST be placed BEFORE the import statement that follows them!
dpg.create_context()
# dpg.create_viewport(title="Startup Profile Selection")
# dpg.configure_viewport(0, width=300, height=150, max_width=300, decorated=True, resizable=False)

from theme import global_theme, invisible_button_theme

class ProfileSelect:
    def __init__(self, profiles_list, callback):
        self.on_startup_profile_prompt(profiles_list, callback)
        # dpg.set_primary_window(window=self.profile_popup, value=True)
        self.config = Config()

        # dpg.setup_dearpygui()
        # dpg.show_viewport()
        # # dpg.start_dearpygui()
        # while dpg.is_dearpygui_running():
        #     dpg.render_dearpygui_frame()
        # dpg.destroy_context()

    def on_startup_profile_prompt(self, profiles_list, callback):
        with dpg.value_registry():
            dpg.add_bool_value(tag="tracker_bool_dontaskagain")
            dpg.add_string_value(tag="tracker_str_defaultprofile")

        with dpg.font_registry():
            self.default_font = dpg.add_font("fonts/27_RussellSquare.ttf", 12)
            self.header_font = dpg.add_font("fonts/27_RussellSquare.ttf", 14)

        # configure global font:
        dpg.bind_font(self.default_font)

        with dpg.window(label=f"Startup Profile Selection",
                        tag="startup_profile_popup",
                        autosize=True,
                        width=250,
                        height=150,
                        no_resize=False,
                        modal=True,
                        popup=True,
                        no_close=True) as self.profile_popup:
            dpg.add_text("Select a profile:")
            profile_list = profiles_list
            dpg.add_listbox(items=profile_list, tag="listbox_profiles", source="tracker_str_defaultprofile")
            dpg.add_checkbox(label="Don\'t ask again", tag="checkbox_dontaskagain", source="tracker_bool_dontaskagain")

            dpg.add_button(label="Confirm", tag="startup_profile_popup_confirm",
                           callback=lambda s, d: [
                               self.config.createConfig(defaultprofile=dpg.get_value("tracker_str_defaultprofile"),
                                                        dontaskagain=dpg.get_value("tracker_bool_dontaskagain")),
                               self.exit_window(s, d),
                               callback()
                           ])

        dpg.configure_item("startup_profile_popup", pos=[int(dpg.get_viewport_max_width() // 2) - (dpg.get_item_width("startup_profile_popup") // 2), int(dpg.get_viewport_height() // 2) - (dpg.get_item_height("startup_profile_popup") // 2)])

    @staticmethod
    def exit_window(_sender, _data):
        # dpg.stop_dearpygui()
        dpg.delete_item("startup_profile_popup")



# plist = ["MechWarrior", "[SA] Bird_Thing"]
# if __name__ == '__main__':
#     profile_select = ProfileSelect(plist)



