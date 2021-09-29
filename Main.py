import os
from tkinter import *
from tkinter import filedialog
from PIL import Image
import tkinter.ttk as ttk
from resource.JsonHandling import JsonHandler
from resource.Upscale import Upscale, getImgName
from resource.Queue import Circular_Q
from resource.Mbox import Mbox
import webbrowser
import subprocess
import pyperclip

# Create a public jsonHandler object
fJson = JsonHandler()

# Public var
dir_path = os.path.dirname(os.path.realpath(__file__))

# Public function
def console():
    print("-" * 80)
    print("Debugging window")
    print("Use The GUI Window to start upscaling")
    print("This window is for debugging purposes")

def startfile(filename):
  try:
    os.startfile(filename)
  except:
    subprocess.Popen(['xdg-open', filename])

def OpenUrl(url):
    webbrowser.open_new(url)

def allowedKey(event):
    key = event.keysym
    if key.lower() in ['left', 'right']: # Arrow left right
        return
    elif (12 == event.state and key == 'a'):
        return
    elif (12 == event.state and key == 'c'): 
        return
    else:
        return "break"

def getImgDimensions(img):
    image = Image.open(img)
    w, h = image.size

    return f"{w} x {h}"

# ----------------------------------------------------------------
# SettingUI
class SettingUI():
    # -------------------------------------------------
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.root.title("Settings")
        self.root.geometry("500x150")
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
        self.image_output_textbox.bind("<Key>", lambda event: allowedKey(event)) # Disable textbox input

        # Create a button for image output folder
        self.image_output_button = ttk.Button(self.firstFrameContent_2, text="Browse", command=self.folder_Dialog)
        self.image_output_button.pack(side=LEFT, fill=X, expand=False, padx=5, pady=5)

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
                    print("Directory not found! Program will set the output directory to default!")
                    Mbox("Warning", "Directory not found! Program will set the output directory to default!", 2)
                    status, details = fJson.setDefault()
                    if status:
                        Mbox("Success", details, 0)
                    else: # Error should not happen but just in case
                        Mbox("Error", details, 2)

                    status, details = fJson.loadSetting()
                    self.image_output_textbox.delete(0, END)
                    self.image_output_textbox.insert(0, details["output_path"])
        else: # Error should not happen but just in case
            print("Error: Cannot load settings")
            Mbox("Error", settings, 2)

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

    # Initiate all the elements
    def iniate_Elements(self):
        self.image_output_textbox.delete(0, END)
        self.image_output_textbox.insert(0, fJson.readSetting()["output_path"].replace(r'\resource\..', '').replace('/', '\\'))
        if self.image_output_checkbutton_var.get() == True:
            self.image_output_textbox.insert(0, fJson.getDefaultSetting().replace(r'\resource\..', '').replace('/', '\\'))
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
            self.image_output_textbox.insert(0, fJson.getDefaultSetting().replace(r'\resource\..', '').replace('/', '\\'))

            # Change state to disabled
            self.image_output_textbox.config(state=DISABLED)
            self.image_output_button.config(state=DISABLED)
        else:
            self.image_output_textbox.config(state=NORMAL)
            self.image_output_button.config(state=NORMAL)
    
    # Save settings to json file
    def save_Settings(self):
        if self.image_output_checkbutton_var.get() == True: # If checkbox is checked
            status, details = fJson.setDefault()
            if status:
                print("Setting has been changed successfully")
                Mbox("Success", "Setting has been changed successfully", 0)
                self.iniate_Elements()
            else:
                Mbox("Error", details, 2)
        else:
            settings = {
                "output_folder": "custom",
                "output_path": self.image_output_textbox.get()
            }
            # Check if the folder exists
            if os.path.isdir(settings["output_path"]):
                status, details = fJson.writeSetting(settings)
                if status:
                    print(details)
                    Mbox("Success", details, 0)
                    self.iniate_Elements()
                else:
                    Mbox("Error", details, 2)
            else:
                Mbox("Error", "The folder does not exist", 2)

    # Copy currently selected path to clipboard
    def copy_Path(self):
        pyperclip.copy(self.image_output_textbox.get())
        print("Text copied to clipboard")
        Mbox("Success", "Path has been copied to clipboard", 0)

    # Set current setting to default
    def set_Default(self):
        # Ask for confirmation
        if Mbox("Confirmation", "Are you sure you want to set the default settings?", 3):
            status, details = fJson.setDefault()
            if status:
                print(details)
                Mbox("Success", details, 0)
                self.image_output_checkbutton_var.set(True)
                self.iniate_Elements()
            else:
                print(details)
                Mbox("Error", details, 2)
    
    # Set current setting to currently stored
    def set_Currently_Stored(self):
        # Ask for confirmation
        if Mbox("Confirmation", "Are you sure you want to reset the currently stored settings?", 3):            
            settings = fJson.readSetting()
            print(settings)
            Mbox("Success", "Successfully set setting to currently stored", 0)

            self.iniate_Elements()

class MainWindow:
    # -------------------------------------------------
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.settings_window = SettingUI()
        self.image_Pool = Circular_Q(50) # Max image pool is 50
        self.root.title("Ez Upscale")
        self.root.geometry("700x500")
        self.alwaysOnTop = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frames
        # Top Frame
        # 1st frame for image input
        self.firstFrame = Frame(self.root)
        self.firstFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)
        
        self.firstFrameContent = Frame(self.firstFrame)
        self.firstFrameContent.pack(side=TOP, fill=X, expand=False)
        
        self.firstFrameContent_2 = Frame(self.firstFrame)
        self.firstFrameContent_2.pack(side=TOP, fill=X, expand=False)

        # 2nd frame for upscale settings
        self.secondFrame = Frame(self.root)
        self.secondFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.secondFrameContent = Frame(self.secondFrame)
        self.secondFrameContent.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_2 = Frame(self.secondFrame)
        self.secondFrameContent_2.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_3 = Frame(self.secondFrame)
        self.secondFrameContent_3.pack(side=TOP, fill=X, expand=False)

        # Bottom Frame
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=False)

        # ----------------------------------------------------------------
        # Queue Frame / 1st frame
        self.queueFrame = ttk.Frame(self.bottomFrame)
        self.queueFrame.pack(side=TOP, fill=BOTH, expand=True)

        # Create a label for image textbox
        self.image_textbox_label = Label(self.firstFrameContent, text="Image Path:")
        self.image_textbox_label.pack(side=LEFT, padx=5, pady=5)

        # Create a textbox for image path
        self.image_path_textbox = Entry(self.firstFrameContent_2)
        self.image_path_textbox.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        self.image_path_textbox.bind("<Key>", lambda event: allowedKey(event)) # Disable textbox input

        # Create a button for image to browse image
        self.browse_button = Button(self.firstFrameContent_2, text="Browse", command=self.browse_Image)
        self.browse_button.pack(side=LEFT, padx=5, pady=5)

        # Create a button for clear textbox
        self.clear_button = Button(self.firstFrameContent_2, text="Clear", command=self.clear_Textbox)
        self.clear_button.pack(side=LEFT, padx=5, pady=5)

        # ----------------------------------------------------------------
        # Settings Frame / 2nd frame
        # Create a label for image name
        self.image_chosen_label = Label(self.secondFrameContent, text="Image Name: ")
        self.image_chosen_label.pack(side=LEFT, padx=5, pady=5)

        # Create a label for image dimensions
        self.image_dimensions_label = Label(self.secondFrameContent_2, text="Image Dimensions: ")
        self.image_dimensions_label.pack(side=LEFT, padx=5, pady=5)

        # Create a button for image to upscale
        self.upscale_button = Button(self.secondFrameContent_3, text="Upscale", command=self.upscale_Image)
        self.upscale_button.pack(side=LEFT, padx=5, pady=5)

        # Menubar
        self.menubar = Menu(self.root)

        # Menu item
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_checkbutton(label="Always on Top", command=self.always_on_top)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit Application", command=self.on_closing)
        self.menubar.add_cascade(label="Options", menu=self.file_menu)

        self.filemenu2 = Menu(self.menubar, tearoff=0)
        self.filemenu2.add_command(label="Setting", command=self.open_Setting) # Open Setting Window
        self.filemenu2.add_command(label="Output", command=self.open_Output) # Open Setting Window
        self.menubar.add_cascade(label="View", menu=self.filemenu2)

        self.filemenu3 = Menu(self.menubar, tearoff=0)
        self.filemenu3.add_command(label="Tutorial", command=self.tutorial) # Open Tutorial Window
        self.filemenu3.add_command(label="About", command=self.about) # Open About Window
        self.filemenu3.add_separator()
        self.filemenu3.add_command(label="Open GitHub Repo", command=lambda aurl="https://github.com/Dadangdut33/Screen-Translate":OpenUrl(aurl)) # Exit Application
        self.menubar.add_cascade(label="Help", menu=self.filemenu3)

        self.root.config(menu=self.menubar)
        # Initiation
        self.iniate_Elements()

    # -------------------------------------------------
    # Functions
    # Open the settings window
    def open_Settings(self):
        self.settings_window.show()

    # Menubar
    def always_on_top(self):
        if self.alwaysOnTop:
            self.alwaysOnTop = False
            self.root.wm_attributes('-topmost', False)
        else:
            self.alwaysOnTop = True
            self.root.wm_attributes('-topmost', True)

    # Initiation
    def iniate_Elements(self):
        print("Initiating elements")

    # on close
    def on_closing(self):
        if Mbox("Confirmation", "Are you sure you want to exit?", 3):
            self.root.destroy()
            exit()        

    # Open the settings window
    def open_Setting(self):
        self.settings_window.show()

    # Open the output folder
    def open_Output(self):
        settings = fJson.readSetting()
        if settings['output_folder'] == "default":
            print("Default output folder")
            startfile(fJson.getDefaultSetting())
        else:
            print("Custom output folder")
            startfile(settings['output_path'])

    # About
    def about(self):
        Mbox("About", "Ez Upscale\nVersion: 1.0\nAuthor:\n-Fauzan Farhan Antoro\n-Muhammad Hanief Mulfadinar", 0)

    # Tutorial
    def tutorial(self):
        Mbox("Tutorial", "Tutorial", 0)

    # Upscale Image
    def upscale_Image(self):
        pass

    # Browse Image
    def browse_Image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("image files", "*.jpg"), ('image files', '*.png'), ('image files', '*.jpeg'), # Allow images only
        ))
        if self.image_path != "":
            self.image_path_textbox.delete(0, END)
            self.image_path_textbox.insert(0, self.image_path)

            # Update the label
            self.image_chosen_label.config(text="Image Name: " + getImgName(self.image_path))
            self.image_dimensions_label.config(text="Image Dimensions: " + getImgDimensions(self.image_path))


    # Clear Textbox
    def clear_Textbox(self):
        self.image_path_textbox.delete(0, END)
        # Update the label
        self.image_chosen_label.config(text="Image Name: ")
        self.image_dimensions_label.config(text="Image Dimensions: ")

if __name__ == "__main__":
    # setting = SettingUI()
    # setting.root.mainloop()
    main = MainWindow()
    main.root.mainloop()