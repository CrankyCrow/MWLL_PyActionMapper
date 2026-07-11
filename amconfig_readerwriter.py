import configparser

class ActionmapperCFGReader:
    def __init__(self, file):
        self.FILE_CFG = file
        self.cfg_contents = ""

    def read_cfg(self):
        parser = configparser.ConfigParser()
        with open(self.FILE_CFG) as stream:
            # read config file starting from after "[top]\n" in the parser's interpretation
            parser.read_string("[top]\n" + stream.read())
            # populate the cfg_contents var with all items in the "top" section
            self.cfg_contents = parser.items("top")

    def get_cfgcontents(self):
        # reformat cfg contents to a dictionary for ease of use/access:
        new_cfg_contents = {}
        for a in self.cfg_contents:
            action_name = ""
            action_val = False
            for i in a:
                try:
                    i = bool(int(i))
                    action_val = i
                except ValueError:
                    action_name = i
            new_cfg_contents[action_name] = action_val

        return new_cfg_contents


class ActionmapperCFGWriter:
    def __init__(self, file):
        self.FILE_CFG = file

    def write_cfg(self,
                  val_list=None):
        if val_list is None:
            val_list = [0, 0, 0, 0, 0]
        config = configparser.ConfigParser()

        #define structure of actionmapper.cfg file
        config['DEFAULT'] = {'v_invertAeroPitchControl': str(val_list[0]),
                             'v_invertAeroYawControl': str(val_list[1]),
                             'v_invertAeroRollControl': str(val_list[2]),
                             'v_invertVTOLPitchControl': str(val_list[3]),
                             'v_invertVTOLYawControl': str(val_list[4]),
                             'v_invertVTOLRollControl': '0',
                             'v_tankAutoBoost': '0'}

        # process inputs to re-write the cfg conditionally:
        text = '\n'.join(['='.join(entry) for entry in config.items('DEFAULT')])

        with open(self.FILE_CFG, 'w') as config_file:
            config_file.write(text)

