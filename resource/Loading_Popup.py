from tkinter import *
import tkinter.ttk as ttk
import threading
from .Public import global_

# Ex:  run_func_with_loading_popup(lambda: task('joe'), 'joe_mama') 
def run_func_with_loading_popup(func, msg, window_title = None, bounce_speed = 8, pb_length = None):
    func_return_l = []
    class Main_Frame(object):
        def __init__(self, top, window_title, bounce_speed, pb_length):
            print("Loading frame opened. Please wait...")
            self.func = func
            # save root reference
            self.root = top

            # Remove the default title bar
            self.root.overrideredirect(1)

            # Placement
            self.root.eval('tk::PlaceWindow . center')

            # set title bar
            self.root.title(window_title)

            # Load bar configuration
            self.bounce_speed = bounce_speed
            self.pb_length = pb_length

            # The text label
            self.msg_lbl = Label(top, text=msg)
            self.msg_lbl.pack(padx = 10, pady = 5)

            # the progress bar will be referenced in the "bar handling" and "work" threads
            self.load_bar = ttk.Progressbar(top)
            self.load_bar.pack(padx = 10, pady = (0,10))

            # The cancel button
            self.cancel_btn = Button(top, text='Cancel', command=self.cancel)
            self.cancel_btn.pack(padx = 10, pady = 5)

            self.bar_init()

        def bar_init(self):
            self.start_bar_thread = threading.Thread(target=self.start_bar, args=())
            self.start_bar_thread.daemon = True
            self.start_bar_thread.start()
        
        def cancel(self):
            if global_.is_Terminating: # if the program is terminating, then do not cancel
                return
            print(">> Canceling process")
            self.msg_lbl.config(text="Terminating process, please wait until it finishes...")
            global_.threads_Running = False
            global_.is_Terminating = True
            global_.running_Batch = False
            global_.set_Status_Terminating()
            global_.statusChange("Terminating process, please wait until it finishes...")
            
        def start_bar(self):
            # load bar configuration
            self.load_bar.config(mode='indeterminate', maximum=100, value=0, length = self.pb_length)

            # Speed 
            self.load_bar.start(self.bounce_speed)            

            # start the work thread
            self.work_thread = threading.Thread(target=self.work_task, args=())
            self.work_thread.daemon = True
            self.work_thread.start()

            # wait for the work thread to finish
            self.work_thread.join()

            # Quit the loading frame
            global_.threads_Running = False
            self.root.quit()
            self.root.wm_withdraw()

        def work_task(self):
            func_return_l.append(func())

    # create root window
    root = Tk()
    global_.threads_Running = True

    # call Main_Frame class with reference to root as top
    Main_Frame(root, window_title, bounce_speed, pb_length)
    root.mainloop()
    if len(func_return_l) > 0:
        return func_return_l[0]
    else:
        return None