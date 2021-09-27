import cv2
import os
import matplotlib.pyplot as plt
from Loading_Popup import run_func_with_loading_popup
from tkinter import *
from Mbox import Mbox
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_Output = dir_path + "/../output/"

class Error(Exception):
    """
    Base class for other exceptions
    """
    pass

class InvalidScale(Error):
    """
    Custom exceptions for invalid scale, invalid scale shouldn't happen because of the UI but just in case
    """
    pass

def getImgName(imgPath):
    """
    Get the name of the image without the extension
    """
    return os.path.splitext(os.path.basename(imgPath))[0]

class Upscale:
    """
    Contains all the methods/functions to upscale, error ui will be thrown from here. Results send back are either success or failure.
    """
    def ESPCN(self, img, scale, noise_removal):
        """Upscale the image using ESPCN models, available scale are 2 3 4"""
        status = False
        try:
            # Super resolution
            sr = cv2.dnn_superres.DnnSuperResImpl_create()

            # Dictionary of available scales
            scales = {2: "ESPCN_x2", 3: "ESPCN_x3", 4: "ESPCN_x4"}

            #  Throw error if scale is invalid
            if scale not in scales: 
                raise InvalidScale("Invalid scales! Scale must be 2, 3 or 4")

            # Model
            pathToModel = os.path.join(dir_path + "/../models/" + scales[scale] + ".pb")
            sr.readModel(pathToModel) # Load the model
            sr.setModel("espcn", scale) # set the model by passing the value and the upsampling ratio

            print("Loading model from: " + pathToModel)

            # Upscale
            imgGet = cv2.imread(img) # read the images
            print('Upscaling the image.... Please wait....')
        
            upscaled = sr.upsample(imgGet) # upscale the input image
            print('Upscaling complete!')

            if noise_removal:
                # Noise removal
                print('Removing noise.... Please wait....')
                denoised = cv2.fastNlMeansDenoisingColored(upscaled, None, 10, 10, 7, 21) # denoise the image
                print('Noise removal complete!')

                # Save the image
                cv2.imwrite(dir_path + "/../output/" + getImgName(img) + " " + scales[scale] + "denoised .png", denoised)
                print("Image saved to: " + dir_path + "/../output/" + getImgName(img) + " " + scales[scale] + "denoised .png")
            else:
                # Save the image
                cv2.imwrite(dir_path + "/../output/" + getImgName(img) + " " + scales[scale] + ".png", upscaled)
                print("Image saved to: " + dir_path + "/../output/" + getImgName(img) + " " + scales[scale] + ".png")

            # Set status to success
            status = True
        except InvalidScale as e:
            print(str(e))
            Mbox("Error: Invalid scale", "Invalid scale! Scale must be either 2, 3 or 4", 2)
        except cv2.error as e:
            if "Can't open" in str(e):
                print("Error: ")
                print("Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!")
                Mbox("Error: Model not found", "Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!\n\nError details: " + str(e), 2)
            else: 
                print("Error: ")
                print(str(e))
                Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        except Exception as e:
            print(str(e))
            Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        finally:
            return status
        
if __name__ == "__main__":
    upscale = Upscale()
    bounc_speed = 4
    pb_length = 200
    window_title = "Loading..."
    msg = 'Loading, please wait...'

    x = run_func_with_loading_popup(lambda: upscale.ESPCN(dir_path + "/../img/sample_img/sample2.png", 4, True), msg, window_title, bounc_speed, pb_length)

    print(x)
    os._exit(1)