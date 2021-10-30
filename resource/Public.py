from .JsonHandling import JsonHandler
from time import localtime, strftime
import tkinter as tk

class Globals:
    def __init__(self):
        self.threads_Running = False
        self.is_Terminating = False
        self.running_Batch = False
        self.is_error = False
        self.mode_batch = False
        self.main_Frame = None
        self.status_label = None
        self.status_var = None

    def statusChange(self, newStatus):
        oldText = self.status_var.get()        
        currTime = strftime("%H:%M:%S", localtime())
        oldText += f"\n[{currTime}] {newStatus}"
        nlines = len(oldText.splitlines())

        if nlines == 5: # max line is 4
            oldText = oldText.splitlines()[4]

        self.status_var.set(oldText)

    def set_Status_Ready(self):
        self.status_label.config(text="Ready!", fg="green")

    def set_Status_Running(self):
        self.status_label.config(text="Running...", fg="blue")

    def set_Status_Error(self):
        self.status_label.config(text="Error!", fg="red")

    def set_Status_Terminating(self):
        self.status_label.config(text="Terminating...", fg="red")

fJson = JsonHandler()
global_ = Globals()

options = ["ESPCN", "FSRCNN", "FSRCNN-small", "LapSRN", "None"] # EDSR IS TOO SLOW SO ITS REMOVED

optionsVal = {
    # "EDSR": [2, 3, 4],
    "ESPCN": [2, 3, 4],
    "FSRCNN": [2, 3, 4],
    "FSRCNN-small": [2, 3, 4],
    "LapSRN": [2, 4, 8],
    "None": "None"
}

# ------------------------------
# TextWithVar, taken from: https://stackoverflow.com/questions/21507178/tkinter-text-binding-a-variable-to-widget-text-contents
class TextWithVar(tk.Text):
    '''A text widget that accepts a 'textvariable' option'''
    def __init__(self, parent, *args, **kwargs):
        try:
            self._textvariable = kwargs.pop("textvariable")
        except KeyError:
            self._textvariable = None

        tk.Text.__init__(self, parent, *args, **kwargs)

        # if the variable has data in it, use it to initialize
        # the widget
        if self._textvariable is not None:
            self.insert("1.0", self._textvariable.get())

        # this defines an internal proxy which generates a
        # virtual event whenever text is inserted or deleted
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # if the contents changed, generate an event we can bind to
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate $widget <<Change>> -when tail
                }
                # return the result from the real widget command
                return $result
            }
            ''')

        # this replaces the underlying widget with the proxy
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

        # set up a binding to update the variable whenever
        # the widget changes
        self.bind("<<Change>>", self._on_widget_change)

        # set up a trace to update the text widget when the
        # variable changes
        if self._textvariable is not None:
            self._textvariable.trace("wu", self._on_var_change)

    def _on_var_change(self, *args):
        '''Change the text widget when the associated textvariable changes'''

        # only change the widget if something actually
        # changed, otherwise we'll get into an endless
        # loop
        text_current = self.get("1.0", "end-1c")
        var_current = self._textvariable.get()
        if text_current != var_current:
            self.delete("1.0", "end")
            self.insert("1.0", var_current)

    def _on_widget_change(self, event=None):
        '''Change the variable when the widget changes'''
        if self._textvariable is not None:
            self._textvariable.set(self.get("1.0", "end-1c"))

# ---------------------------------------------------------------
# Tooltip
""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16
"""

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 250     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Make it stay on top
        self.tw.wm_attributes('-topmost', True)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()