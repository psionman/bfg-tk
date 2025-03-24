
"""Signin for Bid for Game."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from psiutils.constants import PAD, DIALOG_STATUS
from psiutils.buttons import ButtonFrame, Button
from psiutils.utilities import window_resize

from constants import APP_TITLE, DEFAULT_GEOMETRY
from config import read_config, save_config
import text

from main_menu import MainMenu

FRAME_TITLE = f'{APP_TITLE} - login'


class LoginFrame():
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()
        self.status = DIALOG_STATUS['undefined']

        # tk variables
        self.username = tk.StringVar()
        self.remember_username = tk.BooleanVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)

        self.username.trace_add('write', self._value_changed)
        self.password.trace_add('write', self._value_changed)

        self.show()

    def show(self):
        root = self.root
        try:
            root.geometry(self.config.geometry[Path(__file__).stem])
        except KeyError:
            root.geometry(DEFAULT_GEOMETRY)
        root.title(FRAME_TITLE)

        root.bind('<Control-x>', self.dismiss)
        root.bind('<Control-o>', self._process)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        label = ttk.Label(frame, text='Username')
        label.grid(row=1, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        entry = ttk.Entry(frame, textvariable=self.username)
        entry.grid(row=1, column=1, sticky=tk.EW)

        check_button = ttk.Checkbutton(
            frame, text='Remember', variable=self.remember_username)
        check_button.grid(row=1, column=3, sticky=tk.W)

        label = ttk.Label(frame, text='Password')
        label.grid(row=2, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        # check_button = ttk.Checkbutton(
        #     frame, text='Remember', variable=self.remember_password)
        # check_button.grid(row=2, column=3, sticky=tk.W)

        self.password_entry = ttk.Entry(
            frame, textvariable=self.password, show=text.BULLET)
        self.password_entry.grid(row=2, column=1, sticky=tk.EW)

        check_button = ttk.Checkbutton(
            frame,
            text='Show password',
            variable=self.show_password,
            command=self._toggle_password)
        check_button.grid(row=3, column=1, sticky=tk.W)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            Button(
                frame,
                text=text.OK,
                command=self._process,
                underline=0,
                dimmable=True),
            Button(
                frame,
                text=text.EXIT,
                command=self.dismiss,
                sticky=tk.E,
                underline=1),
        ]
        frame.enable(False)
        return frame

    def _value_changed(self, *args):
        if self.username.get() and self.password.get():
            self.button_frame.enable()

    def _toggle_password(self, *args) -> None:
        self.password_entry.configure(show=text.BULLET)
        if self.show_password.get():
            self.password_entry.configure(show='')

    def _process(self, *args) -> None:
        self.config.update('remember_username', self.remember_username.get())
        save_config(self.config)
        self.status = DIALOG_STATUS['ok']
        self.dismiss()

    def dismiss(self, *args) -> None:
        self.root.destroy()
