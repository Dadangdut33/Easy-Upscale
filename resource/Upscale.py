import cv2
import os
import time
from datetime import timedelta
from .Mbox import Mbox
from .Public import global_, fJson
dir_path = os.path.dirname(os.path.realpath(__file__))

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

def getImgName_With_Ext(imgPath):
    """
    Get the name of the image with the extension
    """
    return os.path.basename(imgPath)

def get_time_hh_mm_ss(sec):
    """
    Get the time in hh:mm:ss format
    """
    # create timedelta and convert it into string
    td_str = str(timedelta(seconds=sec))

    # split string into individual component
    x = td_str.split(':')
    timeGet = f"{x[0]}:{x[1]}:{x[2]}"
    return timeGet

class Upscale:
    """
    Contains the methods/functions to upscale, error ui will be thrown from here. Results send back are boolean either success (True) or failure (False).
    """
    # -------------------------------------------------
    # Create dir if not exists
    def createDirIfGone(self, dir_Output):
        # Will create the dir if not exists
        if not os.path.exists(dir_Output):
            try:
                os.makedirs(dir_Output)
            except Exception as e:
                print("Error: " + str(e))
                Mbox("Error: ", str(e), 2, global_.main_Frame)

    def cancel(self):
        """
        Cancel the current process
        """
        self.is_Success = None # Signaling that it got canceled
        global_.statusChange(f"Upscaling process of {self.imgName_With_Ext} canceled")

    # -------------------------------------------------
    # Upscale
    def up_type(self, up_Type, img_Path, scale, noise_Removal, dir_Output):
        """Upscale the image using ESPCN models, available scale are 2 3 4"""
        # Check directory first
        self.createDirIfGone(dir_Output)

        # Set status
        global_.set_Status_Running()
        self.imgName_With_Ext = getImgName_With_Ext(img_Path)
        global_.statusChange(f"Processing {self.imgName_With_Ext}")
        
        # Set var
        self.is_Success = False
        startTime = time.time()
        try:
            print("="*50 + f"\n{up_Type} Upscaling.\nScale\t\t: {scale}\nRemove noise\t: {noise_Removal}")
            model = ""
            modelset = up_Type.lower()
            # Models checking
            # -------------------------------------------------
            # ESPCN
            if modelset == "espcn":
                scale = int(scale)
                scales = {2: "ESPCN_x2", 3: "ESPCN_x3", 4: "ESPCN_x4"}
                if scale not in scales:
                    raise InvalidScale("Invalid scale! Available scale for ESPCN are either 2, 3, or 4")
                model = scales[scale]
            # --------------------------------------------------
            # EDSR
            elif modelset == "edsr":
                scale = int(scale)
                scales = {2: "EDSR_x2", 3: "EDSR_x3", 4: "EDSR_x4"}
                if scale not in scales:
                    raise InvalidScale("Invalid scale! Available scale for EDSR are either 2, 3, or 4")
                model = scales[scale]
            # --------------------------------------------------
            # LapSRN
            elif modelset == "lapsrn":
                scale = int(scale)
                scales = {2: "LapSRN_x2", 4: "LapSRN_x4", 8: "LapSRN_x8"}
                if scale not in scales:
                    raise InvalidScale("Invalid scale! Available scale for LapSRN are either 2, 4, or 8")
                model = scales[scale]
            # --------------------------------------------------
            # FSRCNN
            elif modelset == "fsrcnn":
                scale = int(scale)
                scales = {2: "FSRCNN_x2", 3: "FSRCNN_x3", 4: "FSRCNN_x4"}
                if scale not in scales:
                    raise InvalidScale("Invalid scale! Available scale for FSRCNN are either 2, 3, or 4")
                model = scales[scale]
            # ---------------------------------------------------
            # FSRCNN-small
            elif modelset == "fsrcnn-small":
                scale = int(scale)
                scales = {2: "FSRCNN-small_x2", 3: "FSRCNN-small_x3", 4: "FSRCNN-small_x4"}
                if scale not in scales:
                    raise InvalidScale("Invalid scale! Available scale for FSRCNN-small are either 2, 3, or 4")
                model = scales[scale]
            # ---------------------------------------------------
            # None
            elif modelset == "none":
                model = ""
            # ---------------------------------------------------
            # Invalid
            else:
                Mbox("Error", "Invalid upscale type!\nAvailable upscale type are:\nESPCN\nEDSR\nLapSRN\nFSRCNN\nFSRCNN-small", 2, global_.main_Frame)
                return self.is_Success

            # For fsrcnn-small
            if "small" in modelset:
                modelset = "fsrcnn"

            # ---------------------------------------------------
            # Check if upscaling or not
            if model != "":
                # Check threads
                if global_.threads_Running == False:
                    self.cancel()
                    return self.is_Success
                # Run the upscale
                # Super resolution
                sr = cv2.dnn_superres.DnnSuperResImpl_create()

                # Model
                pathToModel = os.path.join(dir_path + "/../models/" + model + ".pb")
                sr.readModel(pathToModel) # Load the model
                sr.setModel(modelset, scale) # set the model by passing the value and the upsampling ratio

                print(">> Loading model from: " + pathToModel)
                global_.statusChange("Loading model from: " + pathToModel)

                # Upscale
                imgGet = cv2.imread(img_Path) # read the image
                
                print('>> Upscaling the image.... Please wait....')
                global_.statusChange('Upscaling the image.... Please wait....')
                upscaled = sr.upsample(imgGet) # upscale the input image
                # Check threads
                if global_.threads_Running == False:
                    self.cancel()
                    return self.is_Success

                print('Upscaling complete!')
                global_.statusChange('Upscaling complete!')
                upscaled_Time = time.time()
                
                print(f'Upscaling took {get_time_hh_mm_ss(upscaled_Time - startTime)} seconds')
                global_.statusChange(f'Upscaling took {get_time_hh_mm_ss(upscaled_Time - startTime)} seconds')

            # Check if noise is removed or not
            if noise_Removal: 
                if model != "": # If upscaling and removing noise
                    print('>> Removing noise.... Please wait....')
                    global_.statusChange('Removing noise.... Please wait....')
                    denoised = cv2.fastNlMeansDenoisingColored(upscaled, None, 10, 10, 7, 21) # denoise the image
                    # Check threads
                    if global_.threads_Running == False:
                        self.cancel()
                        return self.is_Success
                    # ---------------------------------

                    print('Noise removal complete!')
                    global_.statusChange('Noise removal complete!')
                    
                    print(f'Denoising took {get_time_hh_mm_ss(time.time() - upscaled_Time)} seconds')
                    global_.statusChange(f'Denoising took {get_time_hh_mm_ss(time.time() - upscaled_Time)} seconds')
                else: # If only removing noise
                    print('>> Removing noise.... Please wait....')
                    global_.statusChange('Removing noise.... Please wait....')
                    imgGet = cv2.imread(img_Path) # read the image
                    denoised = cv2.fastNlMeansDenoisingColored(imgGet, None, 10, 10, 7, 21)
                    # Check threads
                    if global_.threads_Running == False:
                        self.cancel()
                        return self.is_Success
                    # ---------------------------------
                    
                    print('Noise removal complete!')
                    global_.statusChange('Noise removal complete!')
                    
                    print(f'Denoising took {get_time_hh_mm_ss(time.time() - startTime)} seconds')
                    global_.statusChange(f'Denoising took {get_time_hh_mm_ss(time.time() - startTime)} seconds')
                
                # Check threads
                if global_.threads_Running == False:
                    self.cancel()
                    return self.is_Success
                # ---------------------------------

                # Saving the image after removing noise is done
                if fJson.readSetting()['output_folder'].lower() == "default":
                    outputDir = fJson.getDefaultImgPath() + "/" + getImgName(img_Path) + " " + model  + " denoised.png"
                else:
                    outputDir = fJson.readSetting()['output_path'] + "/" + getImgName(img_Path) + " " + " denoised.png"

                cv2.imwrite(outputDir, denoised)
                print(">> Image saved to: " + outputDir)
                global_.statusChange("Image saved to: " + outputDir)
            # ---------------------------------
            # If not removing noise
            else:
                # Check threads
                if global_.threads_Running == False:
                    self.cancel()
                    return self.is_Success

                # Saving the image after upscaling process is done
                if fJson.readSetting()['output_folder'].lower() == "default":
                    outputDir = fJson.getDefaultImgPath() + "/" + getImgName(img_Path) + " " + model + ".png"
                else:
                    outputDir = fJson.readSetting()['output_path'] + "/" + getImgName(img_Path) + " " + model + ".png"

                cv2.imwrite(outputDir, upscaled)
                print(">> Image saved to: " + outputDir)
                global_.statusChange("Image saved to: " + outputDir)

            # Set status to success
            self.is_Success = True
        # ---------------------------------
        # Error exception
        except InvalidScale as e:
            global_.running_Batch = False
            global_.is_Terminating = False
            global_.is_error = True
            global_.set_Status_Error()
            # Print the error message
            print(str(e))
            Mbox("Error: Invalid scale", "Invalid scale! Scale must be either 2, 3 or 4", 2, global_.main_Frame)
            global_.statusChange("Error: Invalid scale")
        except cv2.error as e:
            global_.running_Batch = False
            global_.is_Terminating = False
            global_.is_error = True
            global_.set_Status_Error()
            if "Can't open" in str(e):
                # Print error to console
                print("Error: ")
                print("Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!")

                # Error popup
                Mbox("Error: Model not found", "Model not found! Please verify that the model exist in 'models' folder. " + 
                "If model is lost, you need to download it again!\n\nError details: " + str(e), 2, global_.main_Frame)
                global_.statusChange("Error: Model not found")
            elif "Insufficient memory" in str(e):
                # Print error to console
                print("Error: ")
                print("Insufficient memory! This usually happen because the image resolution is too big! This error happened because it literally takes that many memories to start upscaling")
                print(">> Tips: Try to use other models")

                # Error popup
                Mbox("Error: Insufficient memory", "Insufficient memory!\nThis usually happen because the image resolution is too big! This error happened because it literally takes that many memories to start upscaling\n*Tips: Try to use other models\n\nError details: " + str(e), 2, global_.main_Frame)
                global_.statusChange("Error: Insufficient memory")
            else: 
                # Print error to console
                print("Error: ")
                print(str(e))

                # Error popup
                Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2, global_.main_Frame)
                global_.statusChange("Error")
        except Exception as e:
            global_.running_Batch = False
            global_.is_Terminating = False
            global_.is_error = True
            global_.set_Status_Error()
            # Print error to console
            print(str(e))

            # Error popup
            Mbox("Error", "Error occured while processing the image.\n\nDetails: " + str(e), 2, global_.main_Frame)
            global_.statusChange("Error")
        # ---------------------------------
        # Finally
        finally:
            print(f">> Total time taken: {get_time_hh_mm_ss(time.time() - startTime)}")
            global_.statusChange(f"Total time taken: {get_time_hh_mm_ss(time.time() - startTime)}")
            global_.set_Status_Ready()
            return self.is_Success