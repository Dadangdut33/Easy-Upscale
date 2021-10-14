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