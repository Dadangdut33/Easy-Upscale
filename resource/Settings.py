import os
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pyperclip
from .Mbox import Mbox
from .Public import fJson

# ----------------------------------------------------------------
# SettingUI
class SettingUI:
    # -------------------------------------------------
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.root.title("Settings")
        self.root.geometry("500x250")
        self.root.wm_attributes('-topmost', False) # Keep on top or not
        self.root.wm_withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frames
        self.firstFrame = ttk.LabelFrame(self.root, text="• Image / OCR Setting")
        self.firstFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)
        
        self.firstFrameContent = Frame(self.firstFrame)
        self.firstFrameContent.pack(side=TOP, fill=X, expand=False)
        
        self.firstFrameContent_2 = Frame(self.firstFrame)
        self.firstFrameContent_2.pack(side=TOP, fill=X, expand=False)

        self.secondFrame = ttk.LabelFrame(self.root, text="• Queue Settings")
        self.secondFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.secondFrameContent = Frame(self.secondFrame)
        self.secondFrameContent.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_2 = Frame(self.secondFrame)
        self.secondFrameContent_2.pack(side=TOP, fill=X, expand=False)

        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=False)

        # Var
        self.image_output_checkbutton_var = BooleanVar(self.root, name="image_output_check_default", value=True)

        # Create a checkbutton for image output default or not
        self.image_output_checkbutton = ttk.Checkbutton(self.firstFrameContent, text="Default Output Folder", variable=self.image_output_checkbutton_var, command=self.checkBtnChanged)
        self.image_output_checkbutton.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)

        # Create a textbox for image output folder
        self.image_output_textbox = ttk.Entry(self.firstFrameContent_2)
        self.image_output_textbox.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        self.image_output_textbox.bind("<Key>", lambda event: self.allowedKey(event)) # Disable textbox input

        # Create a button for image output folder
        self.image_output_button = ttk.Button(self.firstFrameContent_2, text="Browse", command=self.folder_Dialog)
        self.image_output_button.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)

        # Create a label for spinbox
        self.spinbox_label = ttk.Label(self.secondFrameContent, text="Max Queue Size : ")
        self.spinbox_label.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)

        # Create a spinbox for queue size
        self.validateDigits = (self.root.register(self.validateSpinBox), '%P')
        self.queue_spinbox_var = IntVar(self.root)
        self.queue_spinbox = Spinbox(self.secondFrameContent, from_=1, to=200, width=20, textvariable=self.queue_spinbox_var)
        self.queue_spinbox.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)
        self.queue_spinbox.configure(validate='key', validatecommand=self.validateDigits)

        # Info about the queue size
        self.queue_info = Label(self.secondFrameContent_2, text="Changes made on max queue size will be effective on next program startup", font=("Segoe UI", 8), foreground="red")
        self.queue_info.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)
        
        # Read default settings using the functions in jsonHandling
        setting_Status, settings = fJson.loadSetting()
        if setting_Status == True:
            # Check settings output folder
            if settings["output_folder"].lower() == "default":
                print("Settings successfully loaded!")
                self.image_output_checkbutton_var.set(True)
                self.image_output_textbox.delete(0, END)
                self.image_output_textbox.insert(0, settings["output_path"])
            else:
                # First check if the folder exists
                if os.path.isdir(settings["output_path"]):
                    print("Settings successfully loaded!")
                    self.image_output_checkbutton_var.set(False)
                    self.image_output_textbox.delete(0, END)
                    self.image_output_textbox.insert(0, settings["output_path"])
                else:
                    print("Output Directory not found in settings! Program will now set the output directory to default!")
                    Mbox("Warning", "Output directory not found! Program will now set the output directory to default!", 2, self.root)
                    status, details = fJson.setDefault()
                    if status:
                        Mbox("Success", details, 0, self.root)
                    else: # Error should not happen but just in case
                        Mbox("Error", details, 2, self.root)

                    status, details = fJson.loadSetting()
                    self.image_output_textbox.delete(0, END)
                    self.image_output_textbox.insert(0, details["output_path"])

            # Spinbox
            self.queue_spinbox_var.set(settings["max_queue"])
        else: # Error should not happen but just in case
            fJson.setDefault()
            fJson.loadSetting()
            print("Error: Cannot load settings")
            Mbox("Error", "Settings faild to load! Program will now try to set the settings to default. Error Details: " + settings, 2, self.root)

        # Create a button for save settings
        self.save_button = ttk.Button(self.bottomFrame, text="Save", command=self.save_Settings)
        self.save_button.pack(side=RIGHT, fill=X, expand=False, padx=5, pady=5)

        # Create a button for copy currently set path
        self.copy_button = ttk.Button(self.bottomFrame, text="Copy Path", command=self.copy_Path)
        self.copy_button.pack(side=RIGHT, fill=X, expand=False, padx=5, pady=5)

        # Create a button for set to currently set setting
        self.currently_stored_button = ttk.Button(self.bottomFrame, text="Set to currently saved settings", command=self.set_Currently_Stored)
        self.currently_stored_button.pack(side=RIGHT, fill=X, expand=False, padx=5, pady=5)

        # Create a button for set settings to default
        self.default_button = ttk.Button(self.bottomFrame, text="Set to Default", command=self.set_Default)
        self.default_button.pack(side=RIGHT, fill=X, expand=False, padx=5, pady=5)

        # Initiation
        self.iniate_Elements()

    # -------------------------------------------------
    # Functions
    def folder_Dialog(self):
        if not self.image_output_checkbutton_var.get() == True:
            self.folder_Get = filedialog.askdirectory()

            if self.folder_Get: # If user chooses a folder
                # Empty the text box first
                self.image_output_textbox.delete(0, END)

                # Then input the new dir
                self.image_output_textbox.insert(0, self.folder_Get.replace('/', '\\'))
    
    # Open settings
    def show(self):
        self.iniate_Elements()
        self.root.wm_deiconify()

    # Close settings
    def on_closing(self):
        self.root.wm_withdraw()

    # Spinbox validation
    def validateSpinBox(self, event):
        return event.isdigit()

    # Initiate all the elements
    def iniate_Elements(self):
        # Initiate all the elements from the settings
        self.queue_spinbox_var.set(fJson.readSetting()["max_queue"])
        self.image_output_textbox.delete(0, END)
        self.image_output_textbox.insert(0, fJson.readSetting()["output_path"].replace(r'\resource\..', '').replace('/', '\\'))
        if self.image_output_checkbutton_var.get() == True: # If default path is checked
            self.image_output_textbox.delete(0, END)
            self.image_output_textbox.insert(0, fJson.getDefaultImgPath().replace(r'\resource\..', '').replace('/', '\\'))
            self.image_output_textbox.config(state=DISABLED)
            self.image_output_button.config(state=DISABLED)
        else:
            self.image_output_textbox.config(state=NORMAL)
            self.image_output_button.config(state=NORMAL)

    # CheckBtn, if checked then make the textbox disabled
    def checkBtnChanged(self):
        if self.image_output_checkbutton_var.get() == True:
            # Reset textbox to default
            self.image_output_textbox.delete(0, END)
            self.image_output_textbox.insert(0, fJson.getDefaultImgPath().replace(r'\resource\..', '').replace('/', '\\'))

            # Change state to disabled
            self.image_output_textbox.config(state=DISABLED)
            self.image_output_button.config(state=DISABLED)
        else:
            self.image_output_textbox.config(state=NORMAL)
            self.image_output_button.config(state=NORMAL)
    
    # Save settings to json file
    def save_Settings(self):
        settings = {}
        if self.image_output_checkbutton_var.get() == True: # If set to default
            settings = {
                "output_folder": "default",
                "output_path": "",
                "max_queue": self.queue_spinbox_var.get()
            }
        else:
            settings = {
                "output_folder": "custom",
                "output_path": self.image_output_textbox.get(),
                "max_queue": self.queue_spinbox_var.get()
            }
    
        # Save settings
        if (settings["output_folder"] == "default"): # Check if output folder is default or not
            status, details = fJson.writeSetting(settings)
            if status:
                print(details)
                Mbox("Success", details, 0, self.root)
                self.iniate_Elements()
            else:
                Mbox("Error", details, 2, self.root)
        else:
            if os.path.isdir(settings["output_path"]): # If not default then check again the dir exist or not
                status, details = fJson.writeSetting(settings)
                if status:
                    print(details)
                    Mbox("Success", details, 0, self.root)
                    self.iniate_Elements()
                else:
                    Mbox("Error", details, 2, self.root)
            else:
                Mbox("Error", "The folder does not exist", 2, self.root)

    # Copy currently selected path to clipboard
    def copy_Path(self):
        pyperclip.copy(self.image_output_textbox.get())
        print("Text copied to clipboard")
        Mbox("Success", "Path has been copied to clipboard", 0, self.root)

    # Set current setting to default
    def set_Default(self):
        # Ask for confirmation
        if Mbox("Confirmation", "Are you sure you want to set the default settings?", 3, self.root):
            status, details = fJson.setDefault()
            if status:
                print(details)
                Mbox("Success", details, 0, self.root)
                self.image_output_checkbutton_var.set(True)
                self.iniate_Elements()
            else:
                print(details)
                Mbox("Error", details, 2, self.root)
    
    # Set current setting to currently stored
    def set_Currently_Stored(self):
        # Ask for confirmation
        if Mbox("Confirmation", "Are you sure you want to reset the currently stored settings?", 3, self.root):            
            settings = fJson.readSetting()
            print(settings)
            Mbox("Success", "Successfully set setting to currently stored", 0, self.root)

            self.iniate_Elements()

    # Allowed keys
    def allowedKey(self, event):
        key = event.keysym
        allowed = False

        if key.lower() in ['left', 'right']: # Arrow left right
            allowed = True
            return
        if (4 == event.state and key == 'a'): # Ctrl + a
            allowed = True
            return
        if (4 == event.state and key == 'c'): # Ctrl + c
            allowed = True
            return
        
        if not allowed:
            return "break"