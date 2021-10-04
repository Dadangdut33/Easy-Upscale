from .JsonHandling import JsonHandler

class Flags:
    def __init__(self):
        self.threads_Running = False
        self.is_Terminating = False
        self.running_Batch = False
        self.is_error = False
        self.mode_batch = False

fJson = JsonHandler()
flag = Flags()

options = ["ESPCN", "FSRCNN", "FSRCNN-small", "LapSRN", "None"] # EDSR IS TOO SLOW SO ITS REMOVED

optionsVal = {
    # "EDSR": [2, 3, 4],
    "ESPCN": [2, 3, 4],
    "FSRCNN": [2, 3, 4],
    "FSRCNN-small": [2, 3, 4],
    "LapSRN": [2, 4, 8],
    "None": None
}