"""
NOTE: This uses an old version of DPG that seems incompatible with the current 2.0.0 version
"""


from time import sleep

import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


def show_info(title, message, selection_callback):
    # guarantee these commands happen in the same frame

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    with dpg.window(label=title, no_open_over_existing_popup=False, modal=True, no_close=True, tag="modal") as modal_id:
        dpg.add_text(message)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=lambda: show_info_two())
            dpg.add_button(label="Cancel", width=75, user_data=(modal_id, False), callback=selection_callback)

    # guarantee these commands happen in another frame
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])


def show_info_two():
    """
    You have to delete the other modal window and after you delete it you have to sleep for 0.1 second otherwise it doesnt work
    """
    # dpg.hide_item("modal")
    # dpg.delete_item("modal")
    # sleep(0.1)

    with dpg.window(label="Lade...", no_open_over_existing_popup=False, modal=True, tag="loading",
                    width=400, height=400, no_background=True, no_resize=True,
                    no_move=False, pos=[int((dpg.get_viewport_width() // 2 - 400 // 2)),
                                        int((dpg.get_viewport_height() / 2 - 400 / 2))]):
        dpg.add_loading_indicator(speed=1, radius=10, show=True, pos=[150, 150])


def on_selection(sender, unused, user_data):
    if user_data[1]:
        print("User selected 'Ok'")
    else:
        print("User selected 'Cancel'")

    # delete window
    dpg.delete_item(user_data[0])


with dpg.window(label="Example"):
    dpg.add_button(label="Open Messagebox",
                   callback=lambda: show_info("Message Box", "Do you wish to proceed?", on_selection))
    dpg.add_button(label="2nd",
                   callback=lambda: show_info_two())

# main loop
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()

