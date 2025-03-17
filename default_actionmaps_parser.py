import xml.etree.ElementTree as ET

"""
This is a tentative solution and is only meant for loading *in*
actionmapper actions and their respective binds.
"""
def returnDict(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    actionmaps = root.findall("actionmap")

    actionmaps_exceptions = ["STOVL", "debug", "multiplayer", "singleplayer"]

    actionmaps_dict = {}

    for actionmap in actionmaps:
        actionmap_name = actionmap.attrib.get("name")
        if actionmap_name not in actionmaps_exceptions:
            # print(f"=={actionmap_name}==")
            action_dict = {}
            for action in actionmap:
                action_name = action.attrib.get("name")
                # print(f"-{action_name}")
                binds_list = []
                for key in action:
                    key_name = key.attrib.get("name")
                    # print(f"...{key_name}")
                    binds_list.append(key_name)
                if len(binds_list) == 1:
                    binds_list.append('null')
                action_dict[action_name] = binds_list
            actionmaps_dict[actionmap_name] = action_dict

    # print(actionmaps_dict)


    return actionmaps_dict



# print(returnDict("xml/default_actionmaps.xml"))

