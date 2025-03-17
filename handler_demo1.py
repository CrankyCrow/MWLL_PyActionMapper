import dearpygui.dearpygui as dpg
import time

dpg.create_context()

def change_text(sender, app_data):
    dpg.set_value("text_item", f"Mouse Button: {app_data[0]}, Down Time: {app_data[1]} seconds")

def double_click_detected(sender, app_data):
    dpg.set_value("text_item", f"Double-click Detected!")
    time.sleep(1)


with dpg.handler_registry():
    dpg.add_mouse_down_handler(callback=change_text)
    dpg.add_mouse_double_click_handler(callback=double_click_detected)

with dpg.window(width=500, height=300):
    dpg.add_text("Press any mouse button", tag="text_item")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
