import dearpygui.dearpygui as dpg

# Global variables.
global mainWidth, mainHeight
mainWidth = 1200
mainHeigth = 800


def getPrevText(sender, data):
    print('Previous...')


def getNextText(sender, data):
    print('Next...')


def getDate():
    return 'Mar 26 2019 12:34PM'


# Window object settings.
dpg.window.set_main_window_title('App')
dpg.window.set_main_window_pos(100, 50)
dpg.window.set_theme("Gold")

with dpg.window('main'):

    with managed_columns("Columns", 2):

        with child("Left Group", autosize_x=True, autosize_y=True):
            add_text(getDate())
            add_spacing(count=10)

        with child("Right Group", autosize_x=True, autosize_y=True):
            add_text(getDate())
            add_spacing(count=10)

start_dearpygui(primary_window='main')

