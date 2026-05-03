# structure:
# tab {} -> section {} -> action [] -> definition (actionmaps.xml category, display name, tooltip/note?)
# leave out joystick controls for now, low prio, still need to figure out a process to map such input

class TabsActionDictMaster:
    tabs = {
        # "player"
        "mech": {
            "Movement": {
                "v_rotatepitch": ["mech", "Torso pitch up/down"],
                # "xi_v_rotatepitch": ["mech", ""],
                "v_rotateyaw": ["mech", "Torso twist left/right"],
                # "xi_v_rotateyaw": ["mech",],
                # "xi_v_movex": ["mech",],
                "v_moveforward": ["mech", "Increase throttle"],
                "v_moveback": ["mech", "Decrease throttle"],
                # "SetThrottleval": ["mech", "Set throttle value"],
                # "xi_v_movey": ["mech",],
                "v_turnleft": ["mech", "Turn left"],
                "v_turnright": ["mech", "Turn right"]
            },
            "Other": {
                "v_crouch": ["mech", "Crouch"],
                "jump_jets": ["mech", "Engage jump jets"],
                "CenterTorso": ["vehicle", "Center Torso to Legs"]          # vehicle category but this seems to only work for mechs
            }
        },
        "tank": {
            "Movement": {
                "v_rotateyaw": ["tank", "Turret twist left/right"],
                # "xi_v_rotateyaw": ["tank",],
                "v_rotatepitch": ["tank", "Turret pitch up/down"],
                # "xi_v_rotatepitch": ["tank",],
                # "xi_v_movex": ["tank",],
                "v_moveforward": ["tank", "Increase throttle"],
                "v_moveback": ["tank", "Decrease throttle"],
                "v_turnleft": ["tank", "Turn left"],
                "v_turnright": ["tank", "Turn right"],
            },
            "Other": {
                "deploy": ["tank", "Deploy"],
            }
        },
        "vtol": {
            "Vertical Movement": {
                "v_moveup": ["vtol", "Increase altitude"],
                "v_movedown": ["vtol", "Decrease altitude"]
            },
            "Pitch": {
                "v_rotatepitch": ["vtol", "Pitch up/down"],
                # "xi_v_rotatepitch": ["vtol",],
                "v_pitchup": ["vtol", "Pitch up"],
                "v_pitchdown": ["vtol", "Pitch down"],
            },
            "Turn": {
                "v_rotateyaw": ["vtol", "Turn left/right"],
                # "xi_v_rotateyaw": ["vtol",],
                "v_turnleft": ["vtol", "Turn left"],
                "v_turnright": ["vtol", "Turn right"],
            },
            "Strafe": {
                # "xi_v_movex": ["vtol",],
                "v_strafeleft": ["vtol", "Strafe left"],
                "v_straferight": ["vtol", "Strafe right"],
            },
            "Throttle": {
                # "SetThrottleval": ["vtol",],
                # "xi_v_movey": ["vtol",],
                "v_moveforward": ["vtol", "Increase throttle"],
                "v_moveback": ["vtol", "Decrease Throttle"],
            },
            "Other": {
                "levelout": ["vtol", "Level out"],
                "ToggleGears": ["vtol", "Toggle landing gear"],
            }
        },
        "aerospace": {
            "Pitch": {
                "v_rotatepitch": ["aerospace", "Pitch up/down"],
                # "xi_v_rotatepitch": ["aerospace",],
                "v_pitchup": ["aerospace", "Pitch up"],
                "v_pitchdown": ["aerospace", "Pitch down"],
            },
            "Turn": {
                "v_rotateyaw": ["aerospace", "Turn left/right"],
                # "xi_v_rotateyaw": ["aerospace",],
                "v_turnleft": ["aerospace", "Turn left"],
                "v_turnright": ["aerospace", "Turn right"],
            },
            "Roll": {
                "v_rotateroll": ["aerospace", "Roll left/right"],
                # "xi_v_rotateroll": ["aerospace",],
                "v_rollleft": ["aerospace", "Roll left"],
                "v_rollright": ["aerospace", "Roll right"],
            },
            "Throttle": {
                # "SetThrottleval": ["aerospace",],
                # "xi_v_movey": ["aerospace",],
                "v_moveup": ["aerospace", "Increase throttle"],
                "v_movedown": ["aerospace", "Decrease throttle"],
            },
            "Other": {
                "levelout": ["aerospace", "Level out"],
                "ToggleGears": ["aerospace", "Toggle landing gear"],
            }
        }
    }

