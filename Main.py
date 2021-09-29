import os
from tkinter import *
from tkinter import filedialog
from PIL import Image
import tkinter.ttk as ttk
import webbrowser
import subprocess
import imghdr

# Resource imports
from resource.Upscale import Upscale, getImgName
from resource.Queue import Circular_Q
from resource.Mbox import Mbox
from resource.Settings import SettingUI
from resource.Public import fJson, options, optionsVal

# Public var
dir_path = os.path.dirname(os.path.realpath(__file__))

# Public function
def console():
    print("=" * 70)
    print("|\t\t\t   W E L C O M E\t\t\t     |")
    print("=" * 70)
    print("|\t\t\t  Debugging window\t\t\t     |")
    print("|\t\tUse The GUI Window to start upscaling\t\t     |")
    print("|\t\tThis window is for debugging purposes\t\t     |")
    print("=" * 70)

def startfile(filename):
  try:
    os.startfile(filename)
  except:
    subprocess.Popen(['xdg-open', filename])

def OpenUrl(url):
    webbrowser.open_new(url)

def getImgDetails(img):
    image = Image.open(img)
    w, h = image.size
    type = imghdr.what(img)

    return f"{w} x {h} [{type}]"

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
        self.firstFrame = ttk.LabelFrame(self.root, text="• Input Image")
        self.firstFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)
                
        self.firstFrameContent = Frame(self.firstFrame)
        self.firstFrameContent.pack(side=TOP, fill=X, expand=False)

        # 2nd frame for upscale settings
        self.secondFrame = ttk.LabelFrame(self.root, text="• Upscale Settings")
        self.secondFrame.pack(side=TOP, fill=X, expand=False, padx=5, pady=5)

        self.secondFrameContent = Frame(self.secondFrame)
        self.secondFrameContent.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_2 = Frame(self.secondFrame)
        self.secondFrameContent_2.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_3 = Frame(self.secondFrame)
        self.secondFrameContent_3.pack(side=TOP, fill=X, expand=False)

        self.secondFrameContent_4 = Frame(self.secondFrame)
        self.secondFrameContent_4.pack(side=TOP, fill=X, expand=False)

        # 3rd frame for the queue and the button
        self.thirdFrame = ttk.LabelFrame(self.root, text="• Queue")
        self.thirdFrame.pack(side=TOP, fill=X, expand=False)

        # ----------------------------------------------------------------
        # Browse image
        # Create a textbox for image path
        self.image_path_textbox = Entry(self.firstFrameContent)
        self.image_path_textbox.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        self.image_path_textbox.bind("<Key>", lambda event: self.allowedKey(event)) # Disable textbox input

        # Create a button for image to browse image
        self.browse_button = Button(self.firstFrameContent, text="Browse", command=self.browse_Image)
        self.browse_button.pack(side=LEFT, padx=5, pady=5)

        # Create a button for clear textbox
        self.clear_button = Button(self.firstFrameContent, text="Clear", command=self.clear_Textbox)
        self.clear_button.pack(side=LEFT, padx=5, pady=5)

        # ----------------------------------------------------------------
        # Settings Frame / 2nd frame
        # Create a label for image name
        self.image_chosen_label = Label(self.secondFrameContent, text="Image Name  : ")
        self.image_chosen_label.pack(side=LEFT, padx=5, pady=5)

        # Create a label for image dimensions
        self.image_dimensions_type_label = Label(self.secondFrameContent_2, text="Image Details : ")
        self.image_dimensions_type_label.pack(side=LEFT, padx=5, pady=5)

        # Create a label for model choosing
        self.model_choosing_label = Label(self.secondFrameContent_3, text="Model  : ")
        self.model_choosing_label.pack(side=LEFT, padx=5, pady=5)

        # Create a combobox for model choosing
        self.model_choosing_combobox = ttk.Combobox(self.secondFrameContent_3, state="readonly", values=options, background="white")
        self.model_choosing_combobox.pack(side=LEFT, padx=5, pady=5)
        self.model_choosing_combobox.current(0)
        self.model_choosing_combobox.bind("<<ComboboxSelected>>", self.change_Model)

        # Create a label for scaling options
        self.scaling_options_label = Label(self.secondFrameContent_3, text="Scale     :  ")
        self.scaling_options_label.pack(side=LEFT, padx=5, pady=5)

        # Create a combobox for scaling options
        self.scaling_options_combobox = ttk.Combobox(self.secondFrameContent_3, state="readonly", values=optionsVal[options[0]], background="white")
        self.scaling_options_combobox.pack(side=LEFT, padx=5, pady=5)
        self.scaling_options_combobox.current(0)

        # Create a checkbox for remove noise or not
        self.remove_noise_var = BooleanVar()
        self.remove_noise_checkbox = Checkbutton(self.secondFrameContent_3, text="Remove Noise", variable=self.remove_noise_var)
        self.remove_noise_checkbox.pack(side=LEFT, padx=5, pady=5)

        # Create a button for image to upscale
        self.add_to_queue_button = Button(self.secondFrameContent_4, text="Add to queue", command=self.upscale_Image)
        self.add_to_queue_button.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)

        # ----------------------------------------------------------------
        # Queue Frame / 3rd frame
        self.queueFrame = ttk.Frame(self.thirdFrame)
        self.queueFrame.pack(side=TOP, fill=BOTH, expand=True)

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
        # If image is inputted then make the upscale options enabled, else disable it
        if self.image_path_textbox.get() != "":
            self.model_choosing_combobox["state"] = "readonly"
            self.scaling_options_combobox["state"] = "readonly"
            self.remove_noise_checkbox["state"] = "normal"
            self.add_to_queue_button["state"] = "normal"
        else:
            self.model_choosing_combobox["state"] = "disabled"
            self.scaling_options_combobox["state"] = "disabled"
            self.remove_noise_checkbox["state"] = "disabled"
            self.add_to_queue_button["state"] = "disabled"

    # on close
    def on_closing(self):
        if Mbox("Confirmation", "Are you sure you want to exit?", 3):
            self.root.destroy()
            exit()        

    # Allowed keys
    def allowedKey(self, event):
        key = event.keysym
        if key.lower() in ['left', 'right']: # Arrow left right
            return
        elif (12 == event.state and key == 'a'):
            return
        elif (12 == event.state and key == 'c'): 
            return
        else:
            return "break"

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

    # Browse Image
    def browse_Image(self):
        self.image_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
            ("image files", "*.jpg"), ('image files', '*.png'), ('image files', '*.jpeg'), # Allow images only
        ))
        if self.image_path != "":
            self.image_path_textbox.delete(0, END)
            self.image_path_textbox.insert(0, self.image_path)

            # Update the label
            self.image_chosen_label.config(text="Image Name  : " + getImgName(self.image_path))
            self.image_dimensions_type_label.config(text="Image Details : " + getImgDetails(self.image_path))

            # Initiate elements
            self.iniate_Elements()

    # Clear Textbox
    def clear_Textbox(self):
        self.image_path_textbox.delete(0, END)
        # Update the label
        self.image_chosen_label.config(text="Image Name  : ")
        self.image_dimensions_type_label.config(text="Image Details : ")

        # Initiate elements
        self.iniate_Elements()

    # Changing model
    def change_Model(self, event):
        self.model_name = self.model_choosing_combobox.get()
        self.oldScale_Get = self.scaling_options_combobox.get()
        self.newScale = optionsVal[self.model_name]
        self.scaling_options_combobox['values'] = self.newScale
        # Search for the old scale, exist or not, if not exist then set select to 0
        try:
            indexGet = self.newScale.index(int(self.oldScale_Get))
            self.scaling_options_combobox.current(indexGet)
        except Exception as e:
            self.scaling_options_combobox.current(0)

    # Upscale Image
    def upscale_Image(self):
        pass

if __name__ == "__main__":
    console()
    main = MainWindow()
    main.root.mainloop()