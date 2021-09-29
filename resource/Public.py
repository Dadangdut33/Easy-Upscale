from .JsonHandling import JsonHandler

fJson = JsonHandler()

options = ["ESPCN", "FSRCNN", "FSRCNN-small", "LapSRN", "EDSR"]

optionsVal = {
    "EDSR": [2, 3, 4],
    "ESPCN": [2, 3, 4],
    "FSRCNN": [2, 3, 4],
    "FSRCNN-small": [2, 3, 4],
    "LapSRN": [2, 4, 8]
}