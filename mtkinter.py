from tkinter import *
from tkinter.ttk import Progressbar, Spinbox, Combobox
from tkinter import filedialog as tkfd
from tkinter import messagebox as tkmb
from tkinter import font as tkfont

tkCheckbutton = Checkbutton

CONFLICTS = ['Button', 'Checkbutton',
             'Entry', 'Frame',
             'Label', 'LabelFrame',
             'Menubutton', 'OptionMenu',
             'PanedWindow', 'Radiobutton',
             'Scale', 'Scrollbar',
             'Spinbox', 'Widget',
             '_flatten', '_join',
             '_splitdict', '_stringify']


class EntryWithPlaceholder:

    def __init__ (self, root, **kw):
        options = {'text': ''}      
        ph_options = {'text': ''}   # default
        for option in kw:
            if option.startswith('ph'):
                value = kw[option]
                option = option[2:]
                ph_options[option] = value
            else:
                options[option] = kw[option]
        self.___options = options
        self.___ph_options = ph_options
        self.___obj = Entry(root, **ph_options)
        self.___obj.bind('<FocusIn>', self.___focus_in)
        self.___obj.bind('<FocusOut>', self.___focus_out)
        self.__dir__ = self.___obj.__dir__
        self.___setup(self.___ph_options)
        self.___user_focus_in_func = lambda *_: None
        self.___user_focus_out_func = lambda *_: None

    def __getattr__ (self, name):
        return getattr(self.___obj, name)

    def ___setup (self, options):
        self.___obj.configure(options)
        if 'text' in options:
            self.___obj.delete(0, 'end')
            self.___obj.insert(0, options['text'])

    def ___focus_in (self, *args):
        if 'text' in self.___ph_options:
            if self.___obj.get() == self.___ph_options['text']:
                self.___setup(self.___options)
        self.___user_focus_in_func(*args)

    def ___focus_out (self, *args):
        if 'text' in self.___options:
            if self.___obj.get() == self.___options['text']:
                self.___setup(self.___ph_options)
        self.___user_focus_out_func(*args)

    def bind (self, event, func):
        if event == '<FocusIn>':
            ___user_focus_in_func = func
        elif event == '<FocusOut>':
            ___user_focus_out_func = func
        else:
            self.___obj.bind(event, func)

    def configure (self, **kw):
        options = {'text': ''}      
        ph_options = {'text': ''}   # default
        for option in kw:
            if option.startswith('ph'):
                value = kw[option]
                option = option[2:]
                ph_options[option] = value
            else:
                options[option] = kw[option]

        self.___options = options
        self.___ph_options = ph_options
        self.___setup(ph_options)


class EntryFileLocation:

    def __init__ (self, root, **kw):
        self.root = root
        options = {}      
        button_options = {'text': 'O'}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]
        self.___obj = Entry(root, **options)
        self.button_overview = Button(root, **button_options)
        self.button_overview.configure(command=self.___click)
        self.__dir__ = self.___obj.__dir__
        self.___user_button_func = lambda *_: None

    def __getattr__ (self, name):
        return getattr(self.___obj, name)

    def ___click (self, *args):
        directory = tkfd.askopenfilename()
        self.___obj.delete(0, 'end')
        self.___obj.insert(0, directory)
        self.___user_button_func(*args)
        self.root.focus_force() # due to unknown reasons
        # window disappear after clicking on overview button
        # it makes window focused again

    def configure (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        if 'command' in button_options:
            self.___user_button_func = button_options.pop('command')
                
        self.___obj.configure(**options)
        self.button_overview.configure(**button_options)

    def pack (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        self.___obj.pack(**options)
        self.button_overview.pack(**button_options)

    def grid (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        self.___obj.grid(**options)
        self.button_overview.grid(**button_options)

    def place (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        button_default_options = {
            'x': options['x'] + options['width'] + 5,
            'y': options['y'],
            'width': 20,
            'height': 20
            }

        button_options = {**button_default_options, **button_options}

        self.___obj.place(**options)
        self.button_overview.place(**button_options)



class EntryDirectory:

    def __init__ (self, root, **kw):
        self.root = root
        options = {}      
        button_options = {'text': 'O'}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]
        self.___obj = Entry(root, **options)
        self.button_overview = Button(root, **button_options)
        self.button_overview.configure(command=self.___click)
        self.__dir__ = self.___obj.__dir__
        self.___user_button_func = lambda *_: None

    def __getattr__ (self, name):
        return getattr(self.___obj, name)

    def ___click (self, *args):
        directory = tkfd.askdirectory()
        self.___obj.delete(0, 'end')
        self.___obj.insert(0, directory)
        self.___user_button_func(*args)
        self.root.focus_force() # due to unknown reasons
        # window disappear after clicking on overview button
        # it makes window focused again

    def configure (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        if 'command' in button_options:
            self.___user_button_func = button_options.pop('command')
                
        self.___obj.configure(**options)
        self.button_overview.configure(**button_options)

    def pack (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        self.___obj.pack(**options)
        self.button_overview.pack(**button_options)

    def grid (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        self.___obj.grid(**options)
        self.button_overview.grid(**button_options)

    def place (self, **kw):
        options = {}      
        button_options = {}   # default
        for option in kw:
            if option.startswith('button'):
                value = kw[option]
                option = option[6:]
                button_options[option] = value
            else:
                options[option] = kw[option]

        button_default_options = {
            'x': options['x'] + options['width'] + 5,
            'y': options['y'],
            'width': 20,
            'height': 20
            }

        button_options = {**button_default_options, **button_options}

        self.___obj.place(**options)
        self.button_overview.place(**button_options)


class Checkbutton:
    def __init__ (self, *args, **kwargs):
        var = IntVar()
        self.___obj = tkCheckbutton(*args, variable=var, **kwargs)
        self.___obj.var = var
        self.___obj.get = self.___obj.var.get
        self.___obj.set = self.___obj.var.set
        self.__dir__ = self.___obj.__dir__

    def __getattr__ (self, name):
        return getattr(self.___obj, name)
