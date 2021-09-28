import json
import os
from .Mbox import Mbox
dir_path = os.path.dirname(os.path.realpath(__file__))
jsons_path = os.path.join(dir_path, '../settings/')
setting_dir_path = os.path.join(dir_path, '../settings/Setting.json')
default_img_path = os.path.join(dir_path, '../output/')

# Default Setting
default_Setting = {
    "output_folder": "default", # If default, then output is default_img_path, output path not written in Setting.json
    "output_path": "", 
}

class JsonHandler:
    settingsCache = None

    # -------------------------------------------------
    # Create dir if not exists
    def createDirIfGone(self):
        # Will create the dir if not exists
        if not os.path.exists(setting_dir_path):
            try:
                os.makedirs(setting_dir_path)
            except Exception as e:
                print("Error: " + str(e))
                Mbox("Error: ", str(e), 2)

    # -------------------------------------------------
    # Settings
    def writeSetting(self, data):
        is_Success = False
        status = ""
        try:
            self.createDirIfGone()
            with open(setting_dir_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                status = "Setting has been changed successfully"
                is_Success = True
        except Exception as e:
            status = str(e)
            print("Error: " + str(e))
            Mbox("Error: ", str(e), 2)
        finally:
            self.settingsCache = data
            return is_Success, status

    def setDefault(self):
        is_Success = False
        status = ""
        try:
            self.createDirIfGone()
            with open(setting_dir_path, 'w', encoding='utf-8') as f:
                json.dump(default_Setting, f, ensure_ascii=False, indent=4)
                status = "Successfully set setting to default"
                is_Success = True
        except Exception as e:
            status = str(e)
            print("Error: " + str(e))
            Mbox("Error: ", str(e), 2)
        finally:
            self.settingsCache = default_Setting
            return is_Success, status

    def loadSetting(self):
        is_Success = False
        data = ""
        try:
            self.createDirIfGone()
            with open(setting_dir_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                is_Success = True
        except FileNotFoundError as e:
            data = ["Setting file is not found", "Setting.json could not be loaded please do not move or delete the setting file.\n\nProgram will now automatically create and set the setting to default value"]
            # Handle exceptions in main
        except Exception as e:
            data = [str(e)]
            print("Error: " + str(e))
            Mbox("Error: ", str(e), 2)
        finally:
            self.settingsCache = data
            return is_Success, data

    def readSetting(self):
        return self.settingsCache

    def getDefaultSetting(self):
        return default_img_path