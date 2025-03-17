import dearpygui.dearpygui as dpg

dpg.create_context()

texture_data = []
for i in range(0, 100 * 100):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=True):
    dpg.add_static_texture(width=100, height=100, default_value=texture_data, tag="texture_tag")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
