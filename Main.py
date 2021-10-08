import os
from resource.Loading_Popup import run_func_with_loading_popup
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
from resource.Public import fJson, options, optionsVal, flag

# ----------------------------------------------------------------
# Locals
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
    except FileNotFoundError:
        Mbox("File not found", "File not found! Please check your output directory in settings!", "error")
    except:
        subprocess.Popen(['xdg-open', filename])

def OpenUrl(url):
    webbrowser.open_new(url)

def getImgDetails(img):
    image = Image.open(img)
    w, h = image.size
    type = imghdr.what(img)

    return f"{w} x {h} [{type}]"

def getImg_W_H(img):
    image = Image.open(img)
    w, h = image.size
    return w, h

def getImgType_Only(img):
    type = imghdr.what(img)
    return type

class MainWindow:
    # -------------------------------------------------
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.settings_window = SettingUI()
        self.upscale = Upscale()
        self.bounc_speed = 4
        self.pb_length = 250
        self.window_title = "Loading..."

        # Load settings
        settings = fJson.readSetting() # Settings are loaded first at SettingUI so now only need to read the settings
        self.upscale_Queue = Circular_Q(settings['max_queue'])
        self.root.title("Ez Upscale")
        self.root.geometry("900x600")
        self.alwaysOnTop = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_Closing)

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
        self.thirdFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)

        self.thirdFrameContent = Frame(self.thirdFrame)
        self.thirdFrameContent.pack(side=TOP, fill=X, expand=False)

        self.thirdFrameContent_2 = Frame(self.thirdFrame)
        self.thirdFrameContent_2.pack(side=TOP, fill=X, expand=False)

        self.thirdFrameContent_3 = Frame(self.thirdFrame) # For treeview
        self.thirdFrameContent_3.pack(side=TOP, fill=BOTH, expand=True)

        self.thirdFrameContent_3_x = Frame(self.thirdFrame)
        self.thirdFrameContent_3_x.pack(side=TOP, fill=X, expand=False)

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
        self.remove_Noise_Var = BooleanVar()
        self.remove_noise_checkbox = Checkbutton(self.secondFrameContent_3, text="Remove Noise", variable=self.remove_Noise_Var)
        self.remove_noise_checkbox.pack(side=LEFT, padx=5, pady=5)

        # Create a button for image to upscale
        self.add_to_queue_button = Button(self.secondFrameContent_4, text="Add to queue", command=self.add_To_Queue)
        self.add_to_queue_button.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        # ----------------------------------------------------------------
        # Queue Frame / 3rd frame
        # Create a label for queue
        self.queue_label = Label(self.thirdFrameContent, text="Total Item in Queue : ")
        self.queue_label.pack(side=LEFT, padx=5, pady=5)

        # Create a button for upscale all
        self.upscale_all_button = Button(self.thirdFrameContent_2, text="Upscale all", command=self.upscale_All)
        self.upscale_all_button.pack(side=LEFT, padx=5, pady=5)

        # Create a button for upscale top queue
        self.upscale_top_button = Button(self.thirdFrameContent_2, text="Upscale top", command=self.upscale_Head)
        self.upscale_top_button.pack(side=LEFT, padx=5, pady=5)

        # Create a button for remove top queue
        self.remove_top_button = Button(self.thirdFrameContent_2, text="Remove top", command=self.remove_Head)
        self.remove_top_button.pack(side=LEFT, fill=X, padx=5, pady=5)

        # Create a button for clear queue
        self.clear_queue_button = Button(self.thirdFrameContent_2, text="Clear queue", command=self.clear_Queue)
        self.clear_queue_button.pack(side=LEFT, fill=X, padx=5, pady=5)
        
        # Create a treeview for queue
        self.scrollbarY = Scrollbar(self.thirdFrameContent_3, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarX = Scrollbar(self.thirdFrameContent_3_x, orient=HORIZONTAL)
        self.scrollbarX.pack(side=TOP, fill=X)

        self.queue_Table = ttk.Treeview(self.thirdFrameContent_3, columns=("Model", "Scale", "Remove Noise", "Image Info", "Image Name"))
        self.queue_Table['columns'] = ("Image Name", "Image Info", "Upscale Model", "Scale", "Remove Noise")
        self.queue_Table.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

        self.queue_Table.heading("#0", text="", anchor=CENTER)
        self.queue_Table.heading("#1", text="Model", anchor=CENTER)
        self.queue_Table.heading("#2", text="Scale", anchor=CENTER)
        self.queue_Table.heading("#3", text="Remove Noise", anchor=CENTER)
        self.queue_Table.heading("#4", text="Image Info", anchor=CENTER)
        self.queue_Table.heading("#5", text=" Image Name", anchor="w")

        self.queue_Table.column("#0", width=20, stretch=False)
        self.queue_Table.column("#1", width=90, stretch=False, anchor=CENTER)
        self.queue_Table.column("#2", width=40, stretch=False, anchor=CENTER)
        self.queue_Table.column("#3", width=90, stretch=False, anchor=CENTER)
        self.queue_Table.column("#4", width=120, stretch=False, anchor=CENTER)
        self.queue_Table.column("#5", width=1000, stretch=False, anchor="w")

        self.scrollbarX.config(command=self.queue_Table.xview)
        self.scrollbarY.config(command=self.queue_Table.yview)
        self.queue_Table.config(yscrollcommand=self.scrollbarY.set, xscrollcommand=self.scrollbarX.set)
        self.queue_Table.bind('<Button-1>', self.handle_click)

        # Menubar
        self.menubar = Menu(self.root)

        # Menu item
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_checkbutton(label="Always on Top", command=self.always_On_Top)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit Application", command=self.on_Closing)
        self.menubar.add_cascade(label="Options", menu=self.file_menu)

        self.filemenu2 = Menu(self.menubar, tearoff=0)
        self.filemenu2.add_command(label="Setting", command=self.open_Setting) # Open Setting Window
        self.filemenu2.add_command(label="Output", command=self.open_Output) # Open Setting Window
        self.menubar.add_cascade(label="View", menu=self.filemenu2)

        self.filemenu3 = Menu(self.menubar, tearoff=0)
        self.filemenu3.add_command(label="Tutorial", command=self.tutorial) # Open Tutorial Window
        self.filemenu3.add_command(label="About", command=self.about) # Open About Window
        self.filemenu3.add_separator()
        self.filemenu3.add_command(label="Open GitHub Repo", command=lambda aurl="https://github.com/Dadangdut33/sda-3a-06-easy_upscale":OpenUrl(aurl)) # Exit Application
        self.menubar.add_cascade(label="Help", menu=self.filemenu3)

        self.root.config(menu=self.menubar)
        # Initiation
        self.iniate_Settings_Elements()
        self.fill_Treeview()

    # -------------------------------------------------
    # Functions
    # Open the settings window
    def open_Settings(self):
        self.settings_window.show()

    # Menubar
    def always_On_Top(self):
        if self.alwaysOnTop:
            self.alwaysOnTop = False
            self.root.wm_attributes('-topmost', False)
        else:
            self.alwaysOnTop = True
            self.root.wm_attributes('-topmost', True)

    # Initiation
    def iniate_Settings_Elements(self):
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
    def on_Closing(self):
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
        print("Opened output folder")
        settings = fJson.readSetting()
        if settings['output_folder'] == "default":
            startfile(fJson.getDefaultImgPath())
            print("Path: " + fJson.getDefaultImgPath())
        else:
            startfile(settings['output_path'])
            print("Path: " + settings['output_path'])

    # About
    def about(self):
        Mbox("About", "Ez Upscale.\nDibuat untuk memenuhi tugas mata kuliah Struktur Data\n\nVersion: 1.0-tg\nKelompok 10 - Kelas 3A\nAuthor:\n-Fauzan Farhan Antoro\n-Muhammad Hanief Mulfadinar\n", 0)

    # Tutorial
    def tutorial(self):
        Mbox("Tutorial", "1. Search for image\n2. Choose upscale settings option\n3. (Optional) Set image output in settings\n4. Start Upscaling", 0)

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
            self.iniate_Settings_Elements()

    # Clear Textbox
    def clear_Textbox(self):
        self.image_path_textbox.delete(0, END)
        # Update the label
        self.image_chosen_label.config(text="Image Name  : ")
        self.image_dimensions_type_label.config(text="Image Details : ")

        # Initiate elements
        self.iniate_Settings_Elements()

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

    # Queue table
    def fill_Treeview(self):
        self.queue_label.config(text="Total Item in Queue : " + str(self.upscale_Queue.get_Size()))

        # Delete the item in table first
        for i in self.queue_Table.get_children():
                self.queue_Table.delete(i)

        queue_Get = self.upscale_Queue.get_Queue()
        count = 0
        for queue in queue_Get:
            # Check if data is none or not, if none then skip
            if queue is None:
                continue
            
            parentID = count
            self.queue_Table.insert(parent='', index='end', text='', iid=count, values=(queue[3], queue[4], queue[5], queue[2], queue[1]))

            count += 1
            # Child
            self.queue_Table.insert(parent=parentID, index='end', text='', iid=count, values=("", "", "", "Path:", queue[0]))

            count += 1

    # Add to queue
    def add_To_Queue(self):
        if flag.is_Terminating:
            return
        # Double checking
        # Check if the image is inputted
        if self.image_path_textbox.get() == "":
            Mbox("Error", "Please input the image", 0)
            return
        # Check if the model is inputted
        if self.model_choosing_combobox.get() == "":
            Mbox("Error", "Please input the model", 0)
            return
        # Check if the scale is inputted
        if self.scaling_options_combobox.get() == "":
            Mbox("Error", "Please input the scale", 0)
            return

        # Check if the image is exist or not
        if not os.path.isfile(self.image_path_textbox.get()):
            Mbox("Error", "Image not found", 0)
            return

        # Check if not upscaling then user must enable the remove noise button
        if self.model_choosing_combobox.get() == "None" and self.remove_Noise_Var.get() == False:
            Mbox("Invalid options", "You need to atleast check one of the options available!", 0)
            return
        
        # Check img resolution, if more than 1920px then show warning
        w, h = getImg_W_H(self.image_path_textbox.get())
        if w > 1920 or h > 1080:
            # Ask for confirmation to continue if image inpujtted is already hd
            if not Mbox("Warning", "The image resolution seems to be at HD already, do you still want to continue?\n\n" + 
                    "*Please note that you might not be able to upscale it any further as it would need more memory resource to process the image", 3):
                return

        # Get the data
        image_path = self.image_path_textbox.get()
        model_name = self.model_choosing_combobox.get()
        scale = self.scaling_options_combobox.get()
        remove_noise = self.remove_Noise_Var.get()
        
        # Add to queue
        self.upscale_Queue.enqueue([image_path, getImgName(image_path), getImgDetails(image_path), model_name, scale, remove_noise])
        # Update the label

        # Log the queue to console
        self.upscale_Queue.display()

        # Load the queue to table
        self.fill_Treeview()

    # Treeviewa behavior
    def handle_click(self, event):
        if self.queue_Table.identify_region(event.x, event.y) == "separator":
            return "break"

    # Upscale all
    def upscale_All(self):
        if flag.is_Terminating:
            return
        
        flag.running_Batch = True
        flag.mode_batch = True
        count = 0
        while flag.running_Batch: # Looping the queue
            self.upscale_Head(True) # Loop the upscale process
            count += 1
            # Check size of queue, if empty then stop
            if self.upscale_Queue.get_Size() == 0:
                flag.running_Batch = False
                flag.mode_batch = False
                break
        if not flag.is_error: # If there is no error then show success message
            print(">> Batch Upscale process completed, Successfully processes " + str(count) + " images")
            Mbox("Batch Upscale process completed", "Successfully processes " + str(count) + " images", 0)
        else: # If there is error then show error message
            flag.is_error = False
            flag.mode_batch = False
            Mbox("Error", "Upscaling process is canceled because of an error", 1)


    # Upscale top
    def upscale_Head(self, running_Batch = False):
        print(flag.is_Terminating)
        if flag.is_Terminating:
            return

        status, headData = self.upscale_Queue.get_Head()
        if status:
            # Get the data of the head
            img_Path = headData[0]
            up_Type = headData[3]
            scale = headData[4]
            remove_Noise = headData[5]
            # Get output path
            if fJson.readSetting()['output_folder'].lower() == "default":
                dir_Output = fJson.getDefaultImgPath()
            else:
                dir_Output = fJson.readSetting()['output_path']

            # Msg for loading popup
            if up_Type != "None":
                noiseRemoved = ' and removing noise' if remove_Noise else ''
                msg = f'Upscaling {getImgName(img_Path)}.{getImgType_Only(img_Path)}{noiseRemoved}\nusing {up_Type}_x{scale}, please wait...'
            else:
                msg = f'Removing noise for {getImgName(img_Path)}.{getImgType_Only(img_Path)}, please wait...'

            # Upscale the image
            upscale_status = run_func_with_loading_popup(
                lambda: self.upscale.up_type(up_Type, img_Path, scale, remove_Noise, dir_Output), msg, self.window_title, self.bounc_speed, self.pb_length
            )

            # If success
            if upscale_status == True:
                status, dequeued_Data = self.upscale_Queue.dequeue()
                if status:
                    self.fill_Treeview()
                    if not running_Batch:
                        print(">> Image successfully processed")
                        Mbox("Success", f"Successfully processed {dequeued_Data[1]}.{getImgType_Only(dequeued_Data[0])}", 0)
            # Canceled by user
            elif upscale_status == None:
                flag.is_Terminating = False
                print(">> Process canceled by user")
                Mbox("Canceled", "Upscaling process canceled by user", 1)
                self.fill_Treeview()

            # Error
            if flag.is_error == True and not flag.mode_batch:
                flag.is_error = False
                print(">> Error")
                Mbox("Error", "Upscaling process is canceled because of an error", 1)
                self.fill_Treeview()

            # Failed is already handled in the upscale class
            # --------------------------------
        # Failed to get queue data
        else:
            self.fill_Treeview()
            Mbox("Error", "Failed to upscale image.\nReason: " + headData, 2)

    # Remove top
    def remove_Head(self):
        if flag.is_Terminating:
            return

        status, data = self.upscale_Queue.dequeue()
        if status:
            self.fill_Treeview()
            Mbox("Success", f"{data[1]}.{getImgType_Only(data[0])} has been removed from queue", 0)
        else:
            self.fill_Treeview()
            Mbox("Error", "Failed to remove the top queue.\nReason: " + data, 2)

    # Remove all
    def clear_Queue(self):
        if flag.is_Terminating:
            return

        status = self.upscale_Queue.clear()
        if status:
            self.fill_Treeview()
            Mbox("Success", "Queue has been cleared successfully", 0)
            self.upscale_Queue.display()

if __name__ == "__main__":
    console()
    main = MainWindow()
    main.root.mainloop()