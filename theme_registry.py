import dearpygui.dearpygui as dpg

CLEARBG = (0, 0, 0, 0)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 15, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 20, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 0, category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200), category=dpg.mvThemeCat_Core)

        widgets = [dpg.mvInputText, dpg.mvButton, dpg.mvRadioButton, dpg.mvTabBar, dpg.mvTab, dpg.mvImage, dpg.mvMenuBar,
                   dpg.mvViewportMenuBar, dpg.mvMenu, dpg.mvMenuItem, dpg.mvChildWindow, dpg.mvGroup,
                   dpg.mvDragFloatMulti, dpg.mvSliderFloat, dpg.mvSliderInt, dpg.mvFilterSet, dpg.mvDragFloat,
                   dpg.mvDragInt, dpg.mvInputFloat, dpg.mvInputInt, dpg.mvColorEdit, dpg.mvClipper, dpg.mvColorPicker,
                   dpg.mvTooltip, dpg.mvCollapsingHeader, dpg.mvSeparator, dpg.mvCheckbox, dpg.mvListbox, dpg.mvText,
                   dpg.mvCombo, dpg.mvPlot, dpg.mvSimplePlot, dpg.mvDrawlist, dpg.mvWindowAppItem, dpg.mvSelectable,
                   dpg.mvTreeNode, dpg.mvProgressBar, dpg.mvSpacer, dpg.mvImageButton, dpg.mvTimePicker, dpg.mvDatePicker,
                   dpg.mvColorButton, dpg.mvFileDialog, dpg.mvTabButton, dpg.mvDrawNode, dpg.mvNodeEditor, dpg.mvNode,
                   dpg.mvNodeAttribute, dpg.mvTable, dpg.mvTableColumn, dpg.mvTableRow]
        # define Disabled theme:
        for w in widgets:
            with dpg.theme_component(w, enabled_state=False):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [int(0.50 * 255), int(0.50 * 255), int(0.50 * 255), 255])
                dpg.add_theme_color(dpg.mvThemeCol_Button, (45, 45, 48))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (45, 45, 48))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (45, 45, 48))

with dpg.theme() as savebutton_enabled_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (25, 100, 25))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (45, 75, 48))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (45, 75, 48))

with dpg.theme() as error_popup_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 40, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (236, 51, 29))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 40, 0))

with dpg.theme(default_theme=True) as invisible_button_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, CLEARBG, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, CLEARBG, category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, CLEARBG, category=dpg.mvThemeCat_Core)


