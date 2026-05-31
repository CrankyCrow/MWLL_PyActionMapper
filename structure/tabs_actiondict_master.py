# structure:
# tab (internal tab name, use single words only) {} -> section {} -> action [] -> definition (actionmaps.xml category, display name, tooltip/note?)
# leave out joystick controls for now, low prio, still need to figure out a process to map such input

class TabsActionDictMaster:
    tabs = {
        "player": {
            "Spectating": {
                "toggleIntCvar hud_spec_minimumMode": ["player", "Toggle minimum HUD"],  # Spectator-exclusive minimum mode
                # "specmovez": ["player", ""],                                     # joystick-exclusive up/down spec movement
                "specmoveup": ["player", "Move up"],
                "specmovedown": ["player", "Move down"],
                "next_spectator_target": ["default", "View next player"],
                "prev_spectator_target": ["default", "View previous player"],
                "cycle_spectator_mode": ["default", "Cycle spectator mode"],
            },
            "General Movement\n(Spectator / Battle Armor)": {  # shared between spectator and BA
                "sprint": ["player", "Sprint"],
                "moveforward": ["player", "Move forward"],
                "moveback": ["player", "Move backward"],
                "moveleft": ["player", "Move left"],
                "moveright": ["player", "Move right"],
                "rotateyaw": ["player", "Look left/right"],
                "rotatepitch": ["player", "Look up/down"]
            },
            "Main HUD Elements": {
                "hud_show_multiplayer_scoreboard": ["default", "Show scoreboard"],
                "hud_buy_weapons": ["default", "Toggle buy menu"],
                "hud_show_pda_map": ["default", "Toggle map interface"],
                "objectives": ["default", "Toggle map objective icons"],
            },
            "Main HUD Elements h": {
                "hud_hide_multiplayer_scoreboard": ["default", "Hide scoreboard"],
            },
            "Targeting and Radar": {
                "toggle_radar_mode": ["default", "Toggle active/passive radar"],
                "track_reticle": ["default", "Target under reticle"],
                "track_enemy_surface": ["default", "Target nearest/next enemy (surface)"],
                "track_previous_enemy_surface": ["default", "Target previous enemy (surface)"],
                "track_previous_enemy_air": ["default", "Target previous enemy (air)"],
                "track_friendly_surface": ["default", "Target nearest/next friendly (surface)"],
                "track_friendly_air": ["default", "Target nearest/next friendly (air)"],
                "track_previous_friendly_surface": ["default", "Target previous friendly (surface)"],
                "track_previous_friendly_air": ["default", "Target previous friendly (air)"]
            },
            "Legacy Targeting": {
                "track_nearest_enemy": ["default", "Target nearest enemy"],
                "track_next_enemy": ["default", "Target next enemy"],
                "track_previous_enemy": ["default", "Target previous enemy"],
                "track_nearest_friendly": ["default", "Target nearest friendly"],
                "track_next_friendly": ["default", "Target next friendly"],
                "track_previous_friendly": ["default", "Target previous friendly"]
            },
            "Communication": {
                "hud_openchat": ["default", "Open global chat"],
                "hud_openteamchat": ["default", "Open team chat"],  # only available when spawned in
                "radio_group_0": ["multiplayer", "Toggle radio menu - Comms"],  # only available when spawned in
                "radio_group_1": ["multiplayer", "Toggle radio menu - Intel"],  # only available when spawned in
                "radio_group_2": ["multiplayer", "Toggle radio menu - Tactic"],  # only available when spawned in
                "radio_group_3": ["multiplayer", "Toggle radio menu - Strategy"],  # only available when spawned in
                "hud_select1": ["default", "(Radio menu) Select option 1"],  # only available when spawned in
                "hud_select2": ["default", "(Radio menu) Select option 2"],  # only available when spawned in
                "hud_select3": ["default", "(Radio menu) Select option 3"],  # only available when spawned in
                "hud_select4": ["default", "(Radio menu) Select option 4"],  # only available when spawned in
                "hud_select5": ["default", "(Radio menu) Select option 5"]  # only available when spawned in
            },
            "C-Bill Sharing": {
                "Toggle_CBill_Menu": ["player", "Toggle C-Bill donation menu"],
                "Confirm_CBill_Menu": ["player", "Confirm donation"],
                "Choose_CBill_Player": ["player", "Choose player"],
                "Choose_CBill_Amount": ["player", "Choose amount"],
                "Next_CBill_Option": ["player", "Next menu option"],
                "Prev_CBill_Option": ["player", "Previous menu option"]
            },
            "Equipment": {
                "hud_night_vision": ["default", "Toggle night vision"],
                "zoom": ["default", "Cycle zoom levels"],
            },
            "Other Interfacing": {
                "use": ["default", "Use/Enter asset/Eject"],
                "givemecbills": ["vehicle", "Get C-Bills (from server)"]
            },

        },
        "ba": {
            "Weapon Management": {
                "nextitem": ["player", "Select next weapon"],  # BA select next weapon
                "previtem": ["player", "Select previous weapon"],  # BA select previous weapon
                "drop": ["player", "Drop currently selected weapon"],  # BA drop currently selected weapon
                "medium": ["player", "Select main weapon"],  # BA select main weapon action
                "explosive": ["player", "Select SRMs"],  # BA select SRMs action
                # "handgrenade": ["player", ""],    # BA change grenade action (currently unused)
                # "grenade": ["player", ""]     # BA throw grenade action (currently unused)
            },
            "Other": {
                "crouch": ["player", "Crouch"],
                "jump": ["player", "Jump/hop"],
                "jump_jets": ["player", "Engage jump jets"],
                "leanleft": ["player", "Lean left"],
                "leanright": ["player", "Lean right"]
            },
        },
        "vehicles": {
            "C-Bill Sharing h": {                                                                 # this section to not be shown in UI
                "Toggle_CBill_Menu": ["vehicle", "Toggle C-Bill donation menu"],
                "Confirm_CBill_Menu": ["vehicle", "Confirm donation"],
                "Choose_CBill_Player": ["vehicle", "Choose player"],
                "Choose_CBill_Amount": ["vehicle", "Choose amount"],
                "Next_CBill_Option": ["vehicle", "Next menu option"],
                "Prev_CBill_Option": ["vehicle", "Previous menu option"]
            },
            "Power and Heat Management": {
                "Toggle_Powerup_Shutdown": ["vehicle", "Power up/shut down"],
                "Toggle_Auto_Shutdown": ["vehicle", "Toggle auto shutdown override"],
                "Flush_Coolant": ["vehicle", "Flush coolant"],
            },
            "Aiming": {
                "toggle_free_reticle": ["vehicle", "Toggle free/locked reticle"],
                "center_free_reticle": ["vehicle", "Center reticle"],
                "toggleIntCvar cl_free_reticle_independent": ["vehicle", "Toggle independent reticle"],
            },
            "Weapon Management": {
                "firemode": ["vehicle", "Toggle groupfire/chainfire"],
                "Toggle_Weapon": ["vehicle", "Toggle weapon grouping"],
                "Next_Weapon": ["vehicle", "Select next weapon"],
                "Previous_Weapon": ["vehicle", "Select previous weapon"],
                "Next_Weapon_Group": ["vehicle", "Select next weapon grouping"],
                "Previous_Weapon_Group": ["vehicle", "Select previous weapon grouping"],
                # "CurrentWeaponFiremodeChange": ["vehicle", ""],                 # seemingly unused, needs research
                "Fire_Current_Group": ["vehicle", "Fire currently selected weapon group"],
                # "XI_Fire_Current_Group": ["vehicle", ""],
                "Fire_Group1": ["vehicle", "Fire weapon group 1"],
                # "XI_Fire_Group1": ["vehicle", ""],
                "Fire_Group2": ["vehicle", "Fire weapon group 2"],
                # "XI_Fire_Group2": ["vehicle", ""],
                "Fire_Group3": ["vehicle", "Fire weapon group 3"],
                # "XI_Fire_Group3": ["vehicle", ""],
                "Fire_Group4": ["vehicle", "Fire weapon group 4"],
                # "XI_Fire_Group4": ["vehicle", ""],
                "Fire_Group5": ["vehicle", "Fire weapon group 5"],
                # "XI_Fire_Group5": ["vehicle", ""],
                "Fire_Group6": ["vehicle", "Fire weapon group 6"],
                # "XI_Fire_Group6": ["vehicle", ""],
                "Dump_Ammo": ["vehicle", "Dump current weapon ammo ton"],
                "Force_Reload": ["vehicle", "Force weapon reload"],
                "buyammo": ["default", "Autobuy ammo"]
            },
            "Weapon Management h": {
                "Stop_Fire_Current_Group": ["vehicle", "Stop firing currently selected weapon group"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Current_Group
                # "XI_Stop_Fire_Current_Group": ["vehicle", ""],
                "Stop_Fire_Group1": ["vehicle", "Stop firing weapon group 1"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group1
                # "XI_Stop_Fire_Group1": ["vehicle", ""],
                "Stop_Fire_Group2": ["vehicle", "Stop firing weapon group 2"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group2
                # "XI_Stop_Fire_Group2": ["vehicle", ""],
                "Stop_Fire_Group3": ["vehicle", "Stop firing weapon group 3"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group3
                # "XI_Stop_Fire_Group3": ["vehicle", ""],
                "Stop_Fire_Group4": ["vehicle", "Stop firing weapon group 4"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group4
                # "XI_Stop_Fire_Group4": ["vehicle", ""],
                "Stop_Fire_Group5": ["vehicle", "Stop firing weapon group 5"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group5
                # "XI_Stop_Fire_Group5": ["vehicle", ""],
                "Stop_Fire_Group6": ["vehicle", "Stop firing weapon group 6"],                      # not needed visually, but for stability, modify this to mirror binds for Fire_Group6
                # "XI_Stop_Fire_Group6": ["vehicle", ""],
            },
            "Equipment": {
                "v_lights": ["vehicle", "Toggle vehicle lights"],           # not to be confused with the unused lights action in the player section
                "v_boost": ["vehicle", "Engage MASC/boost/afterburner"]
            },
            "Throttle": {
                "Toggle_Ramping_Throttle": ["vehicle", "Toggle ramping/instant throttle"],
                "v_brake": ["vehicle", "Throttle hard stop (Brake)"],
            },
            "Extended Throttle Control": {
                "SetThrottle0": ["vehicle", "Set throttle 0%"],
                "SetThrottle1": ["vehicle", "Set throttle 10%"],
                "SetThrottle2": ["vehicle", "Set throttle 20%"],
                "SetThrottle3": ["vehicle", "Set throttle 30%"],
                "SetThrottle4": ["vehicle", "Set throttle 40%"],
                "SetThrottle5": ["vehicle", "Set throttle 50%"],
                "SetThrottle6": ["vehicle", "Set throttle 60%"],
                "SetThrottle7": ["vehicle", "Set throttle 70%"],
                "SetThrottle8": ["vehicle", "Set throttle 80%"],
                "SetThrottle9": ["vehicle", "Set throttle 90%"],
                "SetThrottle10": ["vehicle", "Set throttle 100%"],
                "SetThrottleReverse": ["vehicle", "Set throttle reverse"]
            },
            "Misc. HUD": {
                "next_vehicle_info": ["vehicle", "Vehicle info - next panel"],
                "previous_vehicle_info": ["vehicle", "Vehicle info - previous panel"]
            },
            "Other Interfacing": {
                "sell": ["vehicle", "Sell vehicle"],
                "v_changeseat": ["vehicle", "Cycle available passenger seats"],
                # "v_changeseat1": ["vehicle", "Change seat to "],                # seemingly unused, included here just in case
                # "v_changeseat2": ["vehicle", "Change seat to "],                # seemingly unused, included here just in case
                # "v_changeseat3": ["vehicle", "Change seat to "],                # seemingly unused, included here just in case
                # "v_changeseat4": ["vehicle", "Change seat to "],                # seemingly unused, included here just in case
                # "v_changeseat5": ["vehicle", "Change seat to "],                # seemingly unused, included here just in case
            }
        },
        "mech": {
            "Torso": {
                "v_rotatepitch": ["mech", "Torso pitch up/down"],
                # "xi_v_rotatepitch": ["mech", ""],
                "v_rotateyaw": ["mech", "Torso twist left/right"],
                # "xi_v_rotateyaw": ["mech",],
            },
            "Movement": {
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
            "Turret": {
                "v_rotatepitch": ["tank", "Turret pitch up/down"],
                # "xi_v_rotatepitch": ["tank",],
                "v_rotateyaw": ["tank", "Turret swivel left/right"],
                # "xi_v_rotateyaw": ["tank",],
            },
            "Movement": {
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

