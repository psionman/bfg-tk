"""BiddingBoxFrame for BfG."""
import tkinter as tk
from tkinter import ttk

from psiutils.constants import PAD
from psiutils.buttons import Button
from psiutils.utilities import window_resize
from psiutils.widgets import clickable_widget

from constants import APP_TITLE
from config import read_config
import text

FRAME_TITLE = f'{APP_TITLE} - Bidding box'

DENOMINATIONS = [text.CLUBS, text.DIAMS, text.HEARTS, text.SPADES, 'NT']
BUTTON_STYLES = [
    'black.TButton',
    'red.TButton',
    'red.TButton',
    'black.TButton',
    'black.TButton',
    ]


class BiddingBoxFrame():
    def __init__(self, parent: tk.Frame) -> None:
        self.root = tk.Toplevel(parent.root)
        self.root.overrideredirect(True)
        self.parent = parent
        self.config = read_config()
        self.buttons = {}
        self.call = None

        # tk variables
        self.confirm_bids = tk.BooleanVar(value=self.config.confirm_bids)

        self.show()

        self._initial_goemetry()
        if self.config.confirm_bids:
            self.ok_button.enable()
        else:
            self.ok_button.disable()

    def show(self) -> None:
        root = self.root
        root.bind('<Button-1>', self._click_on_window)
        root.bind('<B1-Motion>', self._drag_window)
        root.bind('<ButtonRelease>', self._drag_drop)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master, style='green.TFrame')

        bidding_box = self._bidding_box(frame)
        bidding_box.grid(row=0, column=0, padx=PAD,  pady=PAD)

        self.button_frame = self._button_frame(frame)
        self.button_frame.grid(row=1, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        return frame

    def _bidding_box(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master, style='green.TFrame')

        for rank in range(1, 8):
            for index, denomination in enumerate(DENOMINATIONS):
                style = BUTTON_STYLES[index]
                call = f'{rank}{denomination}'
                button = ttk.Button(
                    frame, text=call, style=style)
                button.bind('<Button-1>', self._call_made)
                button.grid(row=rank-1, column=index, padx=1, pady=1)
                clickable_widget(button)
                self.buttons[button] = call

        return frame

    def _button_frame(self, master: ttk.Frame) -> tk.Frame:
        frame = ttk.Frame(master, style='green.TFrame')
        frame.columnconfigure(0, weight=1)

        self.ok_button = Button(
                frame,
                text=text.OK,
                command=self._process_call,
                underline=0,
                dimmable=True)
        self.ok_button.grid(row=0, column=0)
        clickable_widget(self.ok_button)

        check_button = ttk.Checkbutton(
            frame, text='Confirm bids',
            variable=self.confirm_bids,
            style='green.TCheckbutton',
            command=self._check_Button,)
        # check_button.configure(bg='green', fg='white')
        check_button.grid(row=1, column=0, pady=PAD)
        clickable_widget(check_button)

        return frame

    def _process_call(self, *args) -> None:
        if self.call:
            self.dismiss()

    def _initial_goemetry(self) -> None:
        self.root.update_idletasks()
        parent = self.parent.root
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x_pos = (parent.winfo_rootx() +
                 int((parent.winfo_width() - self.root.winfo_width()) / 2))
        y_pos = (parent.winfo_rooty() +
                 int((parent.winfo_height() - self.root.winfo_height()) / 2))
        self.root.geometry(f'{width}x{height}+{x_pos}+{y_pos}')

    def _drag_window(self, *args):
        self.root.config(cursor='fleur')
        root = self.root

        x = self.window_x_pos + root.winfo_pointerx() - self.start_x
        y = self.window_y_pos + root.winfo_pointery() - self.start_y
        root.geometry(f'+{x}+{y}')

    def _drag_drop(self, *args):
        self.root.config(cursor='')

    def _click_on_window(self, *args):
        self.window_x_pos = self.root.winfo_rootx()
        self.window_y_pos = self.root.winfo_rooty()

        self.start_x = self.root.winfo_pointerx()
        self.start_y = self.root.winfo_pointery()

    def _call_made(self, event: tk.Event) -> None:
        event.widget.style = 'red.TButton'
        self.call = self.buttons[event.widget]
        self._configure_call_buttons( )
        if not self.confirm_bids.get():
            self.dismiss()

    def _configure_call_buttons(self):
        red_suits = [text.HEARTS, text.DIAMS]
        for button, call in self.buttons.items():
            button.configure(style='black.TButton')
            if call[1] in red_suits:
                button.configure(style='red.TButton')
            if call == self.call:
                widget = button
        widget.configure(style='black_clicked.TButton')
        if self.call[1] in red_suits:
            widget.configure(style='red_clicked.TButton')

    def _check_Button(self, *args) -> None:
        self.ok_button.disable()
        if self.confirm_bids.get():
            self.ok_button.enable()

    def dismiss(self, *args) -> None:
        self.root.destroy()
