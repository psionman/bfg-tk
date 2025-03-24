"""ConfigFrame for Bid for Game."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

from psiutils.buttons import ButtonFrame, Button
from psiutils.constants import PAD
from psiutils.utilities import window_resize

from constants import APP_TITLE
from config import read_config, save_config
import text


class ConfigFrame():
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.config = read_config()

        # tk variables
        self.xxx = tk.StringVar(value='')

        self.xxx.trace_add('write', self._check_value_changed)

        self.show()

    def show(self) -> None:
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.transient(self.parent.root)
        root.title(f'{APP_TITLE} - {text.CONFIG}')

        root.bind('<Control-x>', self.dismiss)
        root.bind('<Control-s>', self._save_config)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(1, weight=1)
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
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            Button(
                frame,
                text=text.SAVE,
                command=self._save_config,
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

    def _value_changed(self) -> bool:
        return (
            self.xxx.get() != self.config.xxx or
            ...
        )

    def _check_value_changed(self, *args) -> None:
        enable = bool(self._value_changed())
        self.button_frame.enable(enable)

    def _save_config(self, *args) -> None:
        # To generate assignments from tk-vars run script: assignment-invert
        self.config.update('xxx', self.xxx.get())
        save_config(self.config)
        self.dismiss()

    def dismiss(self, *args) -> None:
        self.root.destroy()
