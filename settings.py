import json
import logging
import os


class Settings:
    """
    A settings object containing all the settings with the given id set in the settings file.
    """
    def __init__(self, settingsfile, printerid):
        self.filename = settingsfile
        self.printerid = printerid
        self.settings = None

        if not os.path.exists(self.filename):
            raise FileNotFoundError("The settingsfile {0} could not be found.".format(self.filename))

        logging.info("Initializing settings...")
        self.read_config_file()

    def read_config_file(self):
        with open(self.filename, "r") as file:
            settingsfile = json.loads(file.read())["printer"]
            for setting in settingsfile:
                if setting['id'] == str(self.printerid):
                    self.settings = setting
                    logging.info("Settings have been loaded.")
                    return

            raise IndexError("The setting with index {0} could not be found.".format(self.printerid))

    def get(self, setting):
        try:
            return self.settings[setting]
        except ValueError:
            logging.error("Value not found, returning None")
            return None
