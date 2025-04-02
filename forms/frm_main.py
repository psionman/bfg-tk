
"""MainFrame for Bid for Game."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from psiutils.constants import PAD, DIALOG_STATUS
from psiutils.buttons import ButtonFrame, Button
from psiutils.utilities import window_resize

from constants import APP_TITLE
from config import read_config
from data import DataStore, NewBoard
import text
from user import test_user
from api import response_from_api
import hand_display as hd

from main_menu import MainMenu
from forms.frm_login import LoginFrame
from forms.frm_bidding_box import BiddingBoxFrame

FRAME_TITLE = APP_TITLE
DUMMY_SCALE = 0.01
SPACER_HEIGHT = 330
CALL_SCALE = 0.7

DISPLAY = {
    'none': 0,
    'partner': 1,
    'opps': 2,
    'all': 3,
}

SEATS = 'NESW'


class MainFrame():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.config = read_config()
        self.user = test_user()
        self.data_store = DataStore(self.user)
        self.board = None

        # tk variables
        self.display = tk.IntVar(value=DISPLAY['none'])

        self.show()

        self._new_board()

        # TODO edit LoginFrame to reactivate
        # dlg = LoginFrame(self)
        # self.root.wait_window(dlg.root)
        # if dlg.status != DIALOG_STATUS['ok']:
        #     self.dismiss()

        # TODO edit BiddingBoxFrame to reactivate
        dlg = BiddingBoxFrame(self)
        self.root.wait_window(dlg.root)

    def show(self):
        root = self.root
        root.geometry(self.config.geometry[Path(__file__).stem])
        root.title(FRAME_TITLE)

        root.bind('<Control-x>', self.dismiss)
        # root.bind('<Control-o>', self._process)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        main_menu = MainMenu(self)
        main_menu.create()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

        contract_frame = self._contract_frame(frame)
        contract_frame.grid(row=0, column=0)

        display_frame = self._display_selection_frame(frame)
        display_frame.grid(row=0, column=2)

        top_player = self._top_player(frame)
        top_player.grid(row=0, column=1)

        left_player = self._left_player(frame)
        left_player.grid(row=1, column=0)

        # Spacer to separate N & S
        image = self.data_store.card_image('back', DUMMY_SCALE)
        label = tk.Label(frame, image=image, height=SPACER_HEIGHT)
        label.grid(row=1, column=1, sticky=tk.E, padx=PAD, pady=PAD)

        right_player = self._right_player(frame)
        right_player.grid(row=1, column=2)

        bottom_player = self._bottom_player(frame)
        bottom_player.grid(row=2, column=1)

        self.button_frame = self._button_frame(frame)
        self.button_frame.grid(row=0, column=9, rowspan=9,
                               sticky=tk.NS, padx=PAD, pady=PAD)

        return frame

    def _contract_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = tk.Frame(
            master, highlightbackground='black', highlightthickness=1,)

        self.contract_frame = ttk.Frame(frame)
        self.contract_frame.grid(row=1, column=0)
        return frame

    def _display_selection_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = tk.Frame(
            master, highlightbackground='black', highlightthickness=1,)

        button = ttk.Radiobutton(
            frame,
            text='Show all',
            variable=self.display,
            value=DISPLAY['all'],
            command=self._show_button,
        )
        button.grid(row=0, column=0, sticky=tk.W)

        button = ttk.Radiobutton(
            frame,
            text='Show partner',
            variable=self.display,
            value=DISPLAY['partner'],
            command=self._show_button,
        )
        button.grid(row=0, column=1, sticky=tk.W)

        button = ttk.Radiobutton(
            frame,
            text='Show opps',
            variable=self.display,
            value=DISPLAY['opps'],
            command=self._show_button,
        )
        button.grid(row=1, column=0, sticky=tk.W)

        button = ttk.Radiobutton(
            frame,
            text='Show none',
            variable=self.display,
            value=DISPLAY['none'],
            command=self._show_button,
        )
        button.grid(row=1, column=1, sticky=tk.W)

        return frame

    def _top_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        self.top_hand = ttk.Frame(frame)
        self.top_hand.grid(row=2, column=0)

        index = SEATS.index(self.user.seat)
        index = (index + 2) % 4
        label = ttk.Label(
            frame,
            # text=f'{SEATS[index]} ({self.user.first_name})',
            text=f'{SEATS[index]}',
            style='name.TLabel')
        label.grid(row=1, column=0)

        return frame

    def _right_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        right_hand = hd.right_hand_frame(self, frame)
        right_hand.grid(row=0, column=0)

        index = SEATS.index(self.user.seat)
        index = (index + 3) % 4
        label = ttk.Label(
            frame,
            text=f'{SEATS[index]}',
            style='name.TLabel')
        label.grid(row=0, column=1)

        return frame

    def _left_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        left_hand = hd.left_hand_frame(self, frame)
        left_hand.grid(row=0, column=2)

        index = SEATS.index(self.user.seat)
        index = (index + 1) % 4
        label = ttk.Label(
            frame,
            text=f'{SEATS[index]}',
            style='name.TLabel')
        label.grid(row=0, column=1)

        return frame

    def _bottom_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        self.bottom_hand = ttk.Frame(frame)
        self.bottom_hand.grid(row=0, column=0)
        label = ttk.Label(
            frame,
            text=f'{self.user.seat} ({self.user.first_name})',
            style='name.TLabel')
        label.grid(row=1, column=0)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.VERTICAL)
        frame.buttons = [
            Button(
                frame,
                text=text.NEW_BOARD,
                command=self._new_board,
                underline=0,
                dimmable=False),
            Button(
                frame,
                text=text.EXIT,
                command=self.dismiss,
                sticky=tk.S,
                underline=1),
        ]
        frame.enable(False)
        return frame

    def _show_button(self, *args):
        if self.board:
            hd.display_hands(self)

    def _new_board(self, *args) -> NewBoard:
        response = response_from_api('new-board', self.user)
        self.board = NewBoard(response)
        hd.display_hands(self)
        self._display_bids()

    def _display_bids(self, *args) -> None:
        frame = self.contract_frame
        for widget in frame.winfo_children():
            widget.destroy()

        dealer = f'Dealer: {self.board.dealer}'
        label = ttk.Label(frame, text=dealer)
        label.grid(row=0, column=0, columnspan=4,
                   sticky=tk.W, padx=PAD, pady=PAD)

        blank = self.data_store.card_image('back', DUMMY_SCALE)
        for index, seat in enumerate(SEATS):
            label = ttk.Label(frame, text=seat, style='seat.TLabel')
            label.grid(row=1, column=index, padx=PAD)
            padding = tk.Label(frame, image=blank, height=1, width=20)
            padding.grid(row=2, column=index)

        ic(self.board.bid_history)
        row = 3
        dealer = SEATS.index(self.board.dealer)
        col = index + dealer
        for index, call in enumerate(self.board.bid_history):
            image = self.data_store.call_image(call, CALL_SCALE)
            label = ttk.Label(frame, image=image)
            label.image = image

            dealer = SEATS.index(self.board.dealer)
            col = index + dealer
            label.grid(row=row, column=col,
                       sticky=tk.E, padx=PAD, pady=(0, PAD))

    def _hide_opps(self) -> bool:
        return (self.display.get() == DISPLAY['partner']
                or self.display.get() == DISPLAY['none'])

    def _hide_partner(self, partner: bool) -> bool:
        return ((self.display.get() == DISPLAY['opps']
                or self.display.get() == DISPLAY['none'])
                and partner)

    def dismiss(self, *args) -> None:
        self.root.destroy()
