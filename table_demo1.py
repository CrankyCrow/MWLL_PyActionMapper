import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tutorial"):
    with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp, borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):

        # use add_table_column to add columns to the table,
        # table columns use child slot 0
        dpg.add_table_column(label="Header 1")
        dpg.add_table_column(label="Header 2")
        dpg.add_table_column(label="Header 3")

        # add_table_next_column will jump to the next row
        # once it reaches the end of the columns
        # table next column use slot 1
        for i in range(0, 4):
            with dpg.table_row():
                for j in range(0, 3):
                    dpg.add_text(f"Row{i} Column{j}")
                    dpg.add_button(label=f"Row{i} Column{j} a")
                    dpg.add_button(label=f"Row{i} Column{j} b")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()