import xmltodict
import ast
from pathlib import Path
from pyactionmapper.structure import actionmaps

categories = ["player", "vehicle", "mech", "tank", "vtol", "aerospace"]
# master_dict = {}
# test_list_player = [{'name': 'givemecbills', 'onPress': '1', 'consoleCmd': '1', 'key': [{'name': 'home'}, {'name': 'null'}]}, {'name': 'Toggle_CBill_Menu', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'rshift'}, {'name': 'null'}]}, {'name': 'Confirm_CBill_Menu', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'enter'}, {'name': 'null'}]}, {'name': 'Choose_CBill_Player', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'left'}, {'name': 'null'}]}, {'name': 'Choose_CBill_Amount', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'right'}, {'name': 'null'}]}, {'name': 'Prev_CBill_Option', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'up'}, {'name': 'null'}]}, {'name': 'Next_CBill_Option', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'down'}, {'name': 'null'}]}, {'name': 'jump', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'lalt'}, {'name': 'space'}]}, {'name': 'crouch', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'lctrl'}, {'name': 'xi_thumbl'}]}, {'name': 'sprint', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'lshift'}, {'name': 'xi_shoulderl'}]}, {'name': 'special', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 't'}, {'name': 'xi_thumbr'}]}, {'name': 'moveleft', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'a'}, {'name': 'null'}]}, {'name': 'moveright', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'd'}, {'name': 'null'}]}, {'name': 'moveforward', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'w'}, {'name': 'null'}]}, {'name': 'moveback', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 's'}, {'name': 'null'}]}, {'name': 'specmoveup', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'space'}, {'name': 'null'}]}, {'name': 'specmovedown', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1', 'key': [{'name': 'lctrl'}, {'name': 'null'}]}, {'name': 'toggleIntCvar hud_spec_minimumMode', 'onPress': '1', 'consoleCmd': '1', 'key': [{'name': 'rshift'}, {'name': 'null'}]}, {'name': 'specmovez', 'key': {'name': 'joyaxis_z'}}, {'name': 'leanleft', 'onPress': '1', 'onRelease': '1', 'onHold': '1', 'key': [{'name': 'x'}, {'name': 'null'}]}, {'name': 'leanright', 'onPress': '1', 'onRelease': '1', 'onHold': '1', 'key': [{'name': 'c'}, {'name': 'null'}]}, {'name': 'rotateyaw', 'key': [{'name': 'maxis_x'}, {'name': 'null'}]}, {'name': 'rotatepitch', 'key': [{'name': 'maxis_y'}, {'name': 'null'}]}, {'name': 'nextitem', 'onPress': '1', 'key': [{'name': 'mwheel_up'}, {'name': 'xi_dpad_right'}]}, {'name': 'previtem', 'onPress': '1', 'key': [{'name': 'mwheel_down'}, {'name': 'xi_dpad_left'}]}, {'name': 'explosive', 'onPress': '1', 'key': [{'name': '3'}, {'name': 'mouse5'}]}, {'name': 'handgrenade', 'onPress': '1', 'key': [{'name': 'mouse3'}, {'name': 'null'}]}, {'name': 'xi_handgrenade', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'xi_y'}, {'name': 'null'}]}, {'name': 'xi_grenade', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'xi_y'}, {'name': 'null'}]}, {'name': 'zoom_out', 'onPress': '1', 'key': [{'name': 'mwheel_down'}, {'name': 'null'}]}, {'name': 'drop', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'j'}, {'name': 'null'}]}, {'name': 'small', 'onPress': '1', 'key': [{'name': '1'}, {'name': 'null'}]}, {'name': 'medium', 'onPress': '1', 'key': [{'name': '2'}, {'name': 'mouse4'}]}, {'name': 'utility', 'onPress': '1', 'key': [{'name': '5'}, {'name': 'null'}]}, {'name': 'grenade', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'mouse2'}, {'name': 'null'}]}, {'name': 'zoom_in', 'onPress': '1', 'key': [{'name': 'mwheel_up'}, {'name': 'null'}]}, {'name': 'lights', 'onPress': '1', 'key': [{'name': 'l'}, {'name': 'null'}]}, {'name': 'xi_movex', 'key': [{'name': 'xi_thumblx'}, {'name': 'null'}]}, {'name': 'xi_movey', 'key': [{'name': 'xi_thumbly'}, {'name': 'null'}]}, {'name': 'xi_rotateyaw', 'key': [{'name': 'xi_thumbrx'}, {'name': 'null'}]}, {'name': 'xi_rotatepitch', 'key': [{'name': 'xi_thumbry'}, {'name': 'null'}]}, {'name': 'hud_weapon_mod', 'onPress': '1', 'key': [{'name': 'c'}, {'name': 'null'}]}, {'name': 'jump_jets', 'onPress': '1', 'onRelease': '1', 'key': [{'name': 'space'}, {'name': 'xi_a'}]}]

xml_dir=Path("{}/xml".format("E:\Documents\ProgrammingStuff\Python\DearPyGUI_Sandbox"))
xml_actionmap=Path(f"{xml_dir}/default_actionmaps.xml")
dtd_actionmap=Path(f"{xml_dir}/actionmaps.dtd")

actionmaps = actionmaps()
actionmaps.load(xml_actionmap, dtd_actionmap)
# start deconstructing the actionmaps object into something that can be modified
actionmaps_master_list = ast.literal_eval(actionmaps.__str__().removeprefix("actionmaps(").removesuffix(")"))
print(actionmaps_master_list)

test_list_player = actionmaps.get_section(categories[0])[0]            # remember that get_section returns a tuple, with the important value being index 0
print(test_list_player)
# get the index of the actionmaps section being updated:
section_index_player = actionmaps_master_list[0][1]['actionmap'].index(test_list_player)
print("player section index:", section_index_player)

# update a keybind for something in the "player" category:
## get an action:
action_name = "givemecbills"
## get a new key to bind to:
new_bind = "rctrl"
test_action_player_givemecbills = actionmaps.get_action(categories[0], action_name)[0]        # ditto for get_action, re: returned tuple having important stuff in index 0
print(test_action_player_givemecbills)
## get the index of the action being modified:
action_index = test_list_player['action'].index(test_action_player_givemecbills)
print("givemecbills action index:", action_index)
## update chosen keybind of said action:
test_action_player_givemecbills['key'][1]['@name'] = new_bind
print(test_action_player_givemecbills)
## add this action back into its corresponding section, using the index acquired earlier:
test_list_player['action'][action_index] = test_action_player_givemecbills
print(test_list_player)
## update the master actionmap data with the updated section:
actionmaps_master_list[0][1]['actionmap'][section_index_player] = test_list_player
print(actionmaps_master_list)

# write to an xml file using xmltodict.unparse:
## note: the source data MUST be a dictionary
## thus, prepare source to be turned into a dictionary:
master_dict = {
    actionmaps_master_list[0][0]: actionmaps_master_list[0][1]
}
output_data = xmltodict.unparse(master_dict, pretty=True)
print(output_data)
with open("actionmaps_test0.xml", "w") as xmlfile:
    xmlfile.write(output_data)

actionmaps.load("actionmaps_test0.xml", dtd_actionmap)

# testing xmltodict.unparse():
# xmldata = {'ActionMaps': {'visible': {'map': ['default', 'player', 'vehicle', 'mech', 'tank', 'vtol', 'aerospace']},
#                           'actionmap': [{'@name': 'player', '@version': '20', 'action': [
#                               {'@name': 'givemecbills', '@onPress': '1', '@consoleCmd': '1',
#                                'key': [{'@name': 'home'}, {'@name': 'rctrl'}]},
#                               {'name': 'Toggle_CBill_Menu', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'rshift'}, {'name': 'null'}]},
#                               {'name': 'Confirm_CBill_Menu', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'enter'}, {'name': 'null'}]},
#                               {'name': 'Choose_CBill_Player', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'left'}, {'name': 'null'}]},
#                               {'name': 'Choose_CBill_Amount', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'right'}, {'name': 'null'}]},
#                               {'name': 'Prev_CBill_Option', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'up'}, {'name': 'null'}]},
#                               {'name': 'Next_CBill_Option', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'down'}, {'name': 'null'}]},
#                               {'name': 'jump', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'lalt'}, {'name': 'space'}]},
#                               {'name': 'crouch', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'lctrl'}, {'name': 'xi_thumbl'}]},
#                               {'name': 'sprint', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'lshift'}, {'name': 'xi_shoulderl'}]},
#                               {'name': 'special', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 't'}, {'name': 'xi_thumbr'}]},
#                               {'name': 'moveleft', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'a'}, {'name': 'null'}]},
#                               {'name': 'moveright', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'd'}, {'name': 'null'}]},
#                               {'name': 'moveforward', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'w'}, {'name': 'null'}]},
#                               {'name': 'moveback', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 's'}, {'name': 'null'}]},
#                               {'name': 'specmoveup', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'space'}, {'name': 'null'}]},
#                               {'name': 'specmovedown', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                'key': [{'name': 'lctrl'}, {'name': 'null'}]},
#                               {'name': 'toggleIntCvar hud_spec_minimumMode', 'onPress': '1', 'consoleCmd': '1',
#                                'key': [{'name': 'rshift'}, {'name': 'null'}]},
#                               {'name': 'specmovez', 'key': {'name': 'joyaxis_z'}},
#                               {'name': 'leanleft', 'onPress': '1', 'onRelease': '1', 'onHold': '1',
#                                'key': [{'name': 'x'}, {'name': 'null'}]},
#                               {'name': 'leanright', 'onPress': '1', 'onRelease': '1', 'onHold': '1',
#                                'key': [{'name': 'c'}, {'name': 'null'}]},
#                               {'name': 'rotateyaw', 'key': [{'name': 'maxis_x'}, {'name': 'null'}]},
#                               {'name': 'rotatepitch', 'key': [{'name': 'maxis_y'}, {'name': 'null'}]},
#                               {'name': 'nextitem', 'onPress': '1',
#                                'key': [{'name': 'mwheel_up'}, {'name': 'xi_dpad_right'}]},
#                               {'name': 'previtem', 'onPress': '1',
#                                'key': [{'name': 'mwheel_down'}, {'name': 'xi_dpad_left'}]},
#                               {'name': 'explosive', 'onPress': '1', 'key': [{'name': '3'}, {'name': 'mouse5'}]},
#                               {'name': 'handgrenade', 'onPress': '1', 'key': [{'name': 'mouse3'}, {'name': 'null'}]},
#                               {'name': 'xi_handgrenade', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'xi_y'}, {'name': 'null'}]},
#                               {'name': 'xi_grenade', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'xi_y'}, {'name': 'null'}]},
#                               {'name': 'zoom_out', 'onPress': '1', 'key': [{'name': 'mwheel_down'}, {'name': 'null'}]},
#                               {'name': 'drop', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'j'}, {'name': 'null'}]},
#                               {'name': 'small', 'onPress': '1', 'key': [{'name': '1'}, {'name': 'null'}]},
#                               {'name': 'medium', 'onPress': '1', 'key': [{'name': '2'}, {'name': 'mouse4'}]},
#                               {'name': 'utility', 'onPress': '1', 'key': [{'name': '5'}, {'name': 'null'}]},
#                               {'name': 'grenade', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'mouse2'}, {'name': 'null'}]},
#                               {'name': 'zoom_in', 'onPress': '1', 'key': [{'name': 'mwheel_up'}, {'name': 'null'}]},
#                               {'name': 'lights', 'onPress': '1', 'key': [{'name': 'l'}, {'name': 'null'}]},
#                               {'name': 'xi_movex', 'key': [{'name': 'xi_thumblx'}, {'name': 'null'}]},
#                               {'name': 'xi_movey', 'key': [{'name': 'xi_thumbly'}, {'name': 'null'}]},
#                               {'name': 'xi_rotateyaw', 'key': [{'name': 'xi_thumbrx'}, {'name': 'null'}]},
#                               {'name': 'xi_rotatepitch', 'key': [{'name': 'xi_thumbry'}, {'name': 'null'}]},
#                               {'name': 'hud_weapon_mod', 'onPress': '1', 'key': [{'name': 'c'}, {'name': 'null'}]},
#                               {'name': 'jump_jets', 'onPress': '1', 'onRelease': '1',
#                                'key': [{'name': 'space'}, {'name': 'xi_a'}]}]}, {'name': 'vehicle', 'version': '20',
#                                                                                  'action': [{
#                                                                                                 'name': 'CurrentWeaponFiremodeChange',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                          {'name': 'null'},
#                                                                                          {'name': 'null'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Current_Group',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'xi_triggerr_btn'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Toggle_Ramping_Throttle',
#                                                                                                 'onPress': '1',
#                                                                                                 'key': [{'name': 'k'}, {
#                                                                                                     'name': 'null'}]}, {
#                                                                                                 'name': 'Toggle_Auto_Shutdown',
#                                                                                                 'onPress': '1',
#                                                                                                 'key': [{'name': 'h'}, {
#                                                                                                     'name': 'null'}]}, {
#                                                                                                 'name': 'Stop_Fire_Current_Group',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'null'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'EnableThrottleval',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                                 {'name': 'np_divide'},
#                                                                                                 {'name': 'null'}]}, {
#                                                                                                 'name': 'SetThrottleReverse',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                              {'name': 'np_subtract'},
#                                                                                              {'name': 'null'}]}, {
#                                                                                                 'name': 'Next_Weapon_Group',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                              {'name': 'right'}, {
#                                                                                                  'name': 'xi_dpad_right'}]},
#                                                                                             {'name': 'Dump_Ammo',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'delete'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Force_Reload',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'end'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'XI_Stop_Fire_Group6',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': {
#                                                                                                     'name': 'joybut_6'}},
#                                                                                             {'name': 'Stop_Fire_Group6',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '6'}, {
#                                                                                                  'name': 'mouse6'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Group5',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'joybut_5'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {'name': 'Stop_Fire_Group5',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '5'}, {
#                                                                                                  'name': 'mouse5'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Group4',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'joybut_4'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {'name': 'Stop_Fire_Group4',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '4'}, {
#                                                                                                  'name': 'mouse4'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Group3',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'joybut_3'},
#                                                                                                         {
#                                                                                                             'name': 'xi_shoulderr'}]},
#                                                                                             {
#                                                                                                 'name': 'Toggle_Powerup_Shutdown',
#                                                                                                 'onPress': '1',
#                                                                                                 'key': [{'name': 'p'}, {
#                                                                                                     'name': 'null'}]},
#                                                                                             {'name': 'Stop_Fire_Group3',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '3'}, {
#                                                                                                  'name': 'mouse3'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Group2',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'joybut_2'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {'name': 'Stop_Fire_Group2',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '2'}, {
#                                                                                                  'name': 'mouse2'}]}, {
#                                                                                                 'name': 'XI_Stop_Fire_Group1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{
#                                                                                                             'name': 'joybut_1'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'XI_Fire_Current_Group',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                                 {
#                                                                                                     'name': 'xi_triggerr_btn'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'Stop_Fire_Group1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': '1'}, {
#                                                                                                  'name': 'mouse1'}]}, {
#                                                                                                 'name': 'Fire_Current_Group',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                              {'name': 'null'},
#                                                                                              {'name': 'null'}]}, {
#                                                                                                 'name': 'Previous_Weapon_Group',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                              {'name': 'left'},
#                                                                                              {'name': 'xi_dpad_left'}]},
#                                                                                             {
#                                                                                                 'name': 'Confirm_CBill_Menu',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'enter'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {'name': 'givemecbills',
#                                                                                              'onPress': '1',
#                                                                                              'consoleCmd': '1',
#                                                                                              'key': [{'name': 'home'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Toggle_CBill_Menu',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'rshift'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Choose_CBill_Player',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'left'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Choose_CBill_Amount',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'right'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Prev_CBill_Option',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [{'name': 'up'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'Next_CBill_Option',
#                                                                                                 'onPress': '1',
#                                                                                                 'onRelease': '1',
#                                                                                                 'key': [
#                                                                                                     {'name': 'down'},
#                                                                                                     {'name': 'null'}]},
#                                                                                             {'name': 'firemode',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'backspace'}, {
#                                                                                                     'name': 'xi_dpad_up'}]},
#                                                                                             {'name': 'binoculars',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'b'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'zoom_out',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'mwheel_down'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'zoom_in',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'mwheel_up'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'v_horn',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'h'}, {
#                                                                                                  'name': 'xi_thumbr'}]},
#                                                                                             {'name': 'v_brake',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'x'}, {
#                                                                                                  'name': 'xi_thumbl'}]},
#                                                                                             {'name': 'v_boost',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'retriggerable': '1',
#                                                                                              'key': [{'name': 'lshift'},
#                                                                                                      {
#                                                                                                          'name': 'xi_shoulderl'}]},
#                                                                                             {'name': 'sell',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'j'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat1',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'f3'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat2',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '='},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat3',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '-'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat4',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '0'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat5',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '9'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeview',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'f4'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_lights',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'l'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'previous_vehicle_info',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                                 {'name': 'pgup'},
#                                                                                                 {'name': 'null'}]}, {
#                                                                                                 'name': 'next_vehicle_info',
#                                                                                                 'onPress': '1', 'key': [
#                                                                                              {'name': 'pgdn'},
#                                                                                              {'name': 'null'}]},
#                                                                                             {'name': 'v_viewup',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'pgup'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_viewdown',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'pgdn'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'v_changeseat',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'null'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Next_Weapon',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'down'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Previous_Weapon',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'up'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Toggle_Weapon',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'rctrl'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Fire_Group1',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '1'}, {
#                                                                                                  'name': 'mouse1'}]},
#                                                                                             {'name': 'XI_Fire_Group1',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_1'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'Fire_Group2',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '2'}, {
#                                                                                                  'name': 'mouse2'}]},
#                                                                                             {'name': 'XI_Fire_Group2',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_2'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'Fire_Group3',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '3'}, {
#                                                                                                  'name': 'mouse3'}]},
#                                                                                             {'name': 'XI_Fire_Group3',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_3'}, {
#                                                                                                     'name': 'xi_shoulderr'}]},
#                                                                                             {'name': 'Fire_Group4',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '4'}, {
#                                                                                                  'name': 'mouse4'}]},
#                                                                                             {'name': 'XI_Fire_Group4',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_4'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'Fire_Group5',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '5'}, {
#                                                                                                  'name': 'mouse5'}]},
#                                                                                             {'name': 'XI_Fire_Group5',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_5'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'Fire_Group6',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': '6'}, {
#                                                                                                  'name': 'mouse6'}]},
#                                                                                             {'name': 'XI_Fire_Group6',
#                                                                                              'onPress': '1', 'key': [
#                                                                                                 {'name': 'joybut_6'},
#                                                                                                 {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle0',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_0'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle1',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_1'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle2',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_2'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle3',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_3'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle4',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_4'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle5',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_5'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle6',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_6'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle7',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_7'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle8',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_8'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle9',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_9'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottle10',
#                                                                                              'onPress': '1',
#                                                                                              'key': [{'name': 'np_add'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'SetThrottleval',
#                                                                                              'key': [{'name': 'null'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'CenterTorso',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'null'},
#                                                                                                      {'name': 'null'}]},
#                                                                                             {'name': 'Flush_Coolant',
#                                                                                              'onPress': '1',
#                                                                                              'onRelease': '1',
#                                                                                              'key': [{'name': 'c'},
#                                                                                                      {'name': 'xi_y'}]},
#                                                                                             {
#                                                                                                 'name': 'toggleIntCvar cl_free_reticle_independent',
#                                                                                                 'onPress': '1',
#                                                                                                 'consoleCmd': '1',
#                                                                                                 'key': [{'name': 'f1'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'center_free_reticle',
#                                                                                                 'onPress': '1',
#                                                                                                 'key': [{'name': 'f1'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]},
#                                                                                             {
#                                                                                                 'name': 'toggle_free_reticle',
#                                                                                                 'onPress': '1',
#                                                                                                 'key': [{'name': 'f2'},
#                                                                                                         {
#                                                                                                             'name': 'null'}]}]},
#                                         {'name': 'mech', 'version': '21', 'action': [{'name': 'xi_v_rotatepitch',
#                                                                                       'key': [{'name': 'xi_thumbry'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movex',
#                                                                                       'key': [{'name': 'xi_thumblx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movey',
#                                                                                       'key': [{'name': 'xi_thumbly'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_rotateyaw',
#                                                                                       'key': [{'name': 'xi_thumbrx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotateyaw',
#                                                                                       'key': [{'name': 'maxis_x'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotatepitch',
#                                                                                       'key': [{'name': 'maxis_y'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveforward',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'w'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveback',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 's'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'a'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnright',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'd'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_crouch',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'lctrl'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'jump_jets',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'space'},
#                                                                                               {'name': 'xi_a'}]}]},
#                                         {'name': 'tank', 'version': '20', 'action': [{'name': 'xi_v_rotatepitch',
#                                                                                       'key': [{'name': 'xi_thumbry'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'deploy', 'onPress': '1',
#                                                                                       'key': [{'name': 'lctrl'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movex',
#                                                                                       'key': [{'name': 'xi_thumblx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movey',
#                                                                                       'key': [{'name': 'xi_thumbly'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_rotateyaw',
#                                                                                       'key': [{'name': 'xi_thumbrx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotateyaw',
#                                                                                       'key': [{'name': 'maxis_x'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotatepitch',
#                                                                                       'key': [{'name': 'maxis_y'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveforward',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'w'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveback',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 's'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'a'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnright',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'd'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_movex',
#                                                                                       'key': {'name': 'null'}},
#                                                                                      {'name': 'v_strafeleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_straferight',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]}]},
#                                         {'name': 'vtol', 'version': '21', 'action': [{'name': 'xi_v_rotatepitch',
#                                                                                       'key': [{'name': 'xi_thumbly'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_rotateroll',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_rotateyaw',
#                                                                                       'key': [{'name': 'xi_thumbrx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movex',
#                                                                                       'key': [{'name': 'xi_thumblx'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'xi_v_movey',
#                                                                                       'key': [{'name': 'xi_thumbry'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotatepitch',
#                                                                                       'key': [{'name': 'maxis_y'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rotateyaw',
#                                                                                       'key': [{'name': 'maxis_x'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveforward',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'w'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveback',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 's'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_moveup',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'space'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_movedown',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'lctrl'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_strafeleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'a'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_straferight',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'retriggerable': '1',
#                                                                                       'key': [{'name': 'd'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_pitchup',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_pitchdown',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rollleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_rollright',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnleft',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'onHold': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'v_turnright',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'onHold': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'SetThrottleval',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'levelout',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'lalt'},
#                                                                                               {'name': 'null'}]},
#                                                                                      {'name': 'ToggleGears',
#                                                                                       'onPress': '1', 'onRelease': '1',
#                                                                                       'key': [{'name': 'null'},
#                                                                                               {'name': 'null'}]}]},
#                                         {'name': 'aerospace', 'version': '20', 'action': [
#                                             {'name': 'v_rotatepitch', 'key': [{'name': 'maxis_y'}, {'name': 'null'}]},
#                                             {'name': 'xi_v_rotatepitch', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_pitchup', 'onPress': '1', 'onRelease': '1',
#                                              'key': [{'name': 'space'}, {'name': 'null'}]},
#                                             {'name': 'v_pitchdown', 'onPress': '1', 'onRelease': '1',
#                                              'key': [{'name': 'lctrl'}, {'name': 'null'}]},
#                                             {'name': 'v_rotateyaw', 'key': [{'name': 'maxis_x'}, {'name': 'null'}]},
#                                             {'name': 'xi_v_rotateyaw', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_turnleft', 'onPress': '1', 'onRelease': '1', 'onHold': '1',
#                                              'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_turnright', 'onPress': '1', 'onRelease': '1', 'onHold': '1',
#                                              'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_rotateroll', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'xi_v_rotateroll', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_rollleft', 'onPress': '1', 'onRelease': '1',
#                                              'key': [{'name': 'a'}, {'name': 'null'}]},
#                                             {'name': 'v_rollright', 'onPress': '1', 'onRelease': '1',
#                                              'key': [{'name': 'd'}, {'name': 'null'}]},
#                                             {'name': 'SetThrottleval', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'xi_v_movey', 'key': [{'name': 'null'}, {'name': 'null'}]},
#                                             {'name': 'v_moveup', 'onPress': '1', 'onRelease': '1', 'retriggerable': '1',
#                                              'key': [{'name': 'w'}, {'name': 'null'}]},
#                                             {'name': 'v_movedown', 'onPress': '1', 'onRelease': '1',
#                                              'retriggerable': '1', 'key': [{'name': 's'}, {'name': 'null'}]},
#                                             {'name': 'ToggleGears', 'onPress': '1',
#                                              'key': [{'name': 'g'}, {'name': 'null'}]},
#                                             {'name': 'levelout', 'onPress': '1', 'onRelease': '1',
#                                              'key': [{'name': 'lalt'}, {'name': 'null'}]}]}]}}
# print(xmltodict.unparse(xmldata, pretty=True))


# def update_master(category, actionslist):
#     master_dict[category] = actionslist
#     return master_dict
#
# print(master_dict)
# update_master(categories[0], test_list_player)
# print(master_dict)

