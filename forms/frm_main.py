
"""MainFrame for Bid for Game."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from psiutils.constants import PAD, DIALOG_STATUS
from psiutils.buttons import ButtonFrame, Button
from psiutils.utilities import window_resize

from constants import APP_TITLE
from config import read_config
from data import DataStore
import text

from main_menu import MainMenu
from forms.frm_login import LoginFrame

FRAME_TITLE = APP_TITLE


class MainFrame():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config = read_config()
        self.data_store = DataStore()
        self.data_store.read

        # tk variables

        self.show()

        dlg = LoginFrame(self)
        self.root.wait_window(dlg.root)
        if dlg.status != DIALOG_STATUS['ok']:
            self.dismiss()

    def show(self):
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
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
        # frame.columnconfigure(1, weight=1)

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

    def _process(self, *args) -> None:
        ...

    def dismiss(self, *args) -> None:
        self.root.destroy()
