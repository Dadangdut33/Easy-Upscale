import cv2
import os
import time
from datetime import timedelta
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

def get_time_hh_mm_ss(sec):
    # create timedelta and convert it into string
    td_str = str(timedelta(seconds=sec))

    # split string into individual component
    x = td_str.split(':')
    timeGet = f"{x[0]}:{x[1]}:{x[2]}"
    return timeGet

class Upscale:
    """
    Contains all the methods/functions to upscale, error ui will be thrown from here. Results send back are boolean either success (True) or failure (False).
    """
    def ESPCN(self, img, scale, noise_removal): # Fast
        """Upscale the image using ESPCN models, available scale are 2 3 4"""
        is_Success = False
        print("="*50 + f"\nESPCN Upscaling.\nScale\t\t: {scale}\nRemove noise\t: {noise_removal}")
        startTime = time.time()
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

            print(">> Loading model from: " + pathToModel)

            # Upscale
            imgGet = cv2.imread(img) # read the images
            print('>> Upscaling the image.... Please wait....')
        
            upscaled = sr.upsample(imgGet) # upscale the input image
            print('Upscaling complete!')
            upscaled_Time = time.time()
            print(f'Upscaling took {get_time_hh_mm_ss(upscaled_Time - startTime)} seconds')

            if noise_removal:
                # Noise removal
                print('>> Removing noise.... Please wait....')
                denoised = cv2.fastNlMeansDenoisingColored(upscaled, None, 10, 10, 7, 21) # denoise the image
                print('Noise removal complete!')
                print(f'Denoising took {get_time_hh_mm_ss(time.time() - upscaled_Time)} seconds')

                # Save the image
                outputDir = f"{dir_path}/../output/{getImgName(img)} {scales[scale]} denoised.png"
                cv2.imwrite(outputDir, denoised)
                print(">> Image saved to: " + outputDir)
            else:
                # Save the image
                outputDir = f"{dir_path}/../output/{getImgName(img)} {scales[scale]}.png"
                cv2.imwrite(outputDir, upscaled)
                print(">> Image saved to: " + outputDir)

            # Set status to success
            is_Success = True
        except InvalidScale as e:
            print(str(e))
            Mbox("Error: Invalid scale", "Invalid scale! Scale must be either 2, 3 or 4", 2)
        except cv2.error as e:
            if "Can't open" in str(e):
                # Print error to console
                print("Error: ")
                print("Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!")

                # Error popup
                Mbox("Error: Model not found", "Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!\n\nError details: " + str(e), 2)
            else: 
                # Print error to console
                print("Error: ")
                print(str(e))

                # Error popup
                Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        except Exception as e:
            # Print error to console
            print(str(e))

            # Error popup
            Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        finally:
            print(f">> Total time taken: {get_time_hh_mm_ss(time.time() - startTime)}")
            return is_Success

    def EDSR(self, img, scale, noise_removal): # Very slow, like really slow
        """Upscale the image using EDSR models, available scale are 2 3 4"""
        is_Success = False
        print("="*50 + f"\nEDSR Upscaling.\nScale\t\t: {scale}\nRemove noise\t: {noise_removal}")
        startTime = time.time()
        try:
            # Super resolution
            sr = cv2.dnn_superres.DnnSuperResImpl_create()

            # Dictionary of available scales
            scales = {2: "EDSR_x2", 3: "EDSR_x3", 4: "EDSR_x4"}

            #  Throw error if scale is invalid
            if scale not in scales: 
                raise InvalidScale("Invalid scales! Scale must be 2, 3 or 4")

            # Model
            pathToModel = os.path.join(dir_path + "/../models/" + scales[scale] + ".pb")
            sr.readModel(pathToModel) # Load the model
            sr.setModel("edsr", scale) # set the model by passing the value and the upsampling ratio

            print(">> Loading model from: " + pathToModel)

            # Upscale
            imgGet = cv2.imread(img) # read the images
            print('>> Upscaling the image.... Please wait....')
        
            upscaled = sr.upsample(imgGet) # upscale the input image
            print('Upscaling complete!')
            upscaled_Time = time.time()
            print(f'Upscaling took {get_time_hh_mm_ss(upscaled_Time - startTime)} seconds')
            
            if noise_removal:
                # Noise removal
                print('>> Removing noise.... Please wait....')
                denoised = cv2.fastNlMeansDenoisingColored(upscaled, None, 10, 10, 7, 21) # denoise the image
                print('Noise removal complete!')
                print(f'Denoising took {get_time_hh_mm_ss(time.time() - upscaled_Time)} seconds')

                # Save the image
                outputDir = f"{dir_path}/../output/{getImgName(img)} {scales[scale]} denoised.png"
                cv2.imwrite(outputDir, denoised)
                print(">> Image saved to: " + outputDir)
            else:
                # Save the image
                outputDir = f"{dir_path}/../output/{getImgName(img)} {scales[scale]}.png"
                cv2.imwrite(outputDir, upscaled)
                print(">> Image saved to: " + outputDir)

            # Set status to success
            is_Success = True
        except InvalidScale as e:
            print(str(e))
            Mbox("Error: Invalid scale", "Invalid scale! Scale must be either 2, 3 or 4", 2)
        except cv2.error as e:
            if "Can't open" in str(e):
                # Print error to console
                print("Error: ")
                print("Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!")

                # Error popup
                Mbox("Error: Model not found", "Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!\n\nError details: " + str(e), 2)
            else: 
                # Print error to console
                print("Error: ")
                print(str(e))

                # Error popup
                Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        except Exception as e:
            # Print error to console
            print(str(e))

            # Error popup
            Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2)
        finally:
            print(f">> Total time taken: {get_time_hh_mm_ss(time.time() - startTime)}")
            return is_Success
    

    
        
if __name__ == "__main__":
    upscale = Upscale()
    bounc_speed = 4
    pb_length = 250
    window_title = "Loading..."
    img = dir_path + "/../img/sample_img/sample1.png"
    # msg = 'Upscaling ' +  getImgName(img) + ', please wait...'
    scale = 4
    noise_removal = True
    noiseRemoved = 'and removing noise' if noise_removal else ''
    msg = f'Upscaling {getImgName(img)} to {scale}x {noiseRemoved}, please wait'


    x = run_func_with_loading_popup(lambda: upscale.ESPCN(dir_path + "/../img/sample_img/sample1.png", 2, False), msg, window_title, bounc_speed, pb_length)

    print(x)

    # y = run_func_with_loading_popup(lambda: upscale.ESPCN(dir_path + "/../img/sample_img/sample1.png", 3, True), msg, window_title, bounc_speed, pb_length)

    # print(y)
    os._exit(1)