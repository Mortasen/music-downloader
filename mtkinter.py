from tkinter import *
from tkinter.ttk import Progressbar, Spinbox, Combobox
from tkinter import filedialog as tkfd
from tkinter import messagebox as tkmb
from tkinter import font as tkfont

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


class EntryFileLocation:

    def __init__ (self, root, **options):
        self.___obj = Entry(root, **options)
        self.___obj.bind('<Button-1>', self.___click)
        self.__dir__ = self.___obj.__dir__
        self.___user_button1_func = lambda *_: None

    def __getattr__ (self, name):
        return getattr(self.___obj, name)

    def ___click (self, *args):
        file_path = tkfd.askopenfilename()
        self.___obj.delete(0, 'end')
        self.___obj.insert(0, file_path)
        self.___user_button1_func(*args)

    def bind (self, event, func):
        if event == '<Button-1>':
            ___user_button1_func = func
        else:
            self.___obj.bind(event, func)



class EntryDirectory:

    def __init__ (self, root, **options):
        self.___obj = Entry(root, **options)
        self.___obj.bind('<Button-1>', self.___click)
        self.__dir__ = self.___obj.__dir__
        self.___user_button1_func = lambda *_: None

    def __getattr__ (self, name):
        return getattr(self.___obj, name)

    def ___click (self, *args):
        directory = tkfd.askdirectory()
        self.___obj.delete(0, 'end')
        self.___obj.insert(0, directory)
        self.___user_button1_func(*args)

    def bind (self, event, func):
        if event == '<Button-1>':
            ___user_button1_func = func
        else:
            self.___obj.bind(event, func)
