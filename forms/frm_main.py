
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

from main_menu import MainMenu
from forms.frm_login import LoginFrame
from forms.frm_bidding_box import BiddingBoxFrame

FRAME_TITLE = APP_TITLE
SCALE = 0.35
OVERLAP = 25
BACK_OVERLAP = 10

DISPLAY = {
    'none': 0,
    'partner': 1,
    'opps': 2,
    'all': 3,
}


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
        # dlg = BiddingBoxFrame(self)
        # self.root.wait_window(dlg.root)

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
        # frame.rowconfigure(0, weight=1)
        # frame.columnconfigure(1, weight=1)

        # contract_frame =

        display_frame = self._display_frame(frame)
        display_frame.grid(row=0, column=2)

        top_player = self._top_player(frame)
        top_player.grid(row=0, column=1)

        left_player = self._left_player(frame)
        left_player.grid(row=1, column=0)

        # bidding_box = BiddingBoxFrame(self)
        # bidding_box = BiddingBoxFrame(self)
        # bidding_box.grid(row=1, column=1)

        right_player = self._right_player(frame)
        right_player.grid(row=1, column=2)

        bottom_player = self._bottom_player(frame)
        bottom_player.grid(row=2, column=1)

        self.button_frame = self._button_frame(frame)
        self.button_frame.grid(row=0, column=9, rowspan=9,
                               sticky=tk.NS, padx=PAD, pady=PAD)

        return frame

    def _display_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = tk.Frame(
            master, highlightbackground="black", highlightthickness=1,)

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
        self.top_hand.grid(row=2, column=1)

        return frame

    def _right_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        right_hand = self._right_hand_frame(frame)
        right_hand.grid(row=0, column=0)

        return frame

    def _right_hand_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        self.right_hand_backs = ttk.Frame(frame)
        self.right_hand_backs.grid(row=0, column=0)

        self.right_hand_spades = ttk.Frame(frame)
        self.right_hand_spades.grid(row=0, column=0, sticky=tk.W)
        self.right_hand_hearts = ttk.Frame(frame)
        self.right_hand_hearts.grid(row=1, column=0, sticky=tk.W)
        self.right_hand_diams = ttk.Frame(frame)
        self.right_hand_diams.grid(row=2, column=0, sticky=tk.W)
        self.right_hand_clubs = ttk.Frame(frame)
        self.right_hand_clubs.grid(row=3, column=0, sticky=tk.W)

        return frame

    def _left_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        left_hand = self._left_hand_frame(frame)
        left_hand.grid(row=0, column=0)

        return frame

    def _left_hand_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        self.left_hand_backs = ttk.Frame(frame)
        self.left_hand_backs.grid(row=0, column=0)

        self.left_hand_spades = ttk.Frame(frame)
        self.left_hand_spades.grid(row=0, column=0)
        self.left_hand_hearts = ttk.Frame(frame)
        self.left_hand_hearts.grid(row=1, column=0)
        self.left_hand_diams = ttk.Frame(frame)
        self.left_hand_diams.grid(row=2, column=0)
        self.left_hand_clubs = ttk.Frame(frame)
        self.left_hand_clubs.grid(row=3, column=0)

        return frame

    def _bottom_player(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)

        self.bottom_hand = ttk.Frame(frame)
        self.bottom_hand.grid(row=2, column=1)

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
            self._display_hands()

    def _new_board(self, *args) -> NewBoard:
        response = response_from_api('new-board', self.user)
        self.board = NewBoard(response)
        self._display_hands()

    def _display_hands(self, *args) -> None:
        cards = self.board.hand_cards
        self._horizontal_hand(self.top_hand, cards[2], True)
        self._right_hand(cards[3])
        self._horizontal_hand(self.bottom_hand, cards[0])
        self._left_hand(cards[1])

    def _horizontal_hand(self, frame, cards, partner: bool = False) -> None:
        for widget in frame.winfo_children():
            widget.destroy()
        for index in range(len(cards)):
            image = self.data_store.card_image(cards[index], SCALE)
            if self._hide_partner(partner):
                image = self.data_store.card_image('back', SCALE)
            label = ttk.Label(frame, image=image)
            label.image = image
            overlap = (len(cards) - index) * OVERLAP
            label.grid(row=0, column=0,
                       sticky=tk.E, padx=(0, overlap), pady=PAD)

    def _left_hand(self, cards) -> None:
        max_length = self.board.max_suit_length['E']
        frames = {
            'B': self.left_hand_backs,
            'S': self.left_hand_spades,
            'H': self.left_hand_hearts,
            'D': self.left_hand_diams,
            'C': self.left_hand_clubs,
            }
        self._clear_frames_cards(frames)

        if self._hide_opps():
            self._display_backs(self.left_hand_backs, cards)
        else:
            self._display_side_hand(frames, cards, max_length)

    def _right_hand(self, cards, backs: bool = False) -> None:
        max_length = self.board.max_suit_length['W']
        frames = {
            'B': self.right_hand_backs,
            'S': self.right_hand_spades,
            'H': self.right_hand_hearts,
            'D': self.right_hand_diams,
            'C': self.right_hand_clubs,
            }
        self._clear_frames_cards(frames)

        if self._hide_opps():
            self._display_backs(self.right_hand_backs, cards)
        else:
            self._display_side_hand(frames, cards, max_length)

    def _clear_frames_cards(self, frames: list) -> None:
        for frame in frames.values():
            for widget in frame.winfo_children():
                widget.destroy()

    def _hide_opps(self) -> bool:
        return (self.display.get() == DISPLAY['partner']
                or self.display.get() == DISPLAY['none'])

    def _hide_partner(self, partner: bool) -> bool:
        return ((self.display.get() == DISPLAY['opps']
                or self.display.get() == DISPLAY['none'])
                and partner)

    def _display_backs(self, frame: ttk.Frame, cards: list) -> None:
        self._side_hands_forget()
        image = self.data_store.card_image('back', SCALE)
        for index in range(len((cards))):
            label = ttk.Label(frame, image=image)
            label.image = image
            label.grid(row=0, column=0, sticky=tk.E,
                       padx=(0, index*BACK_OVERLAP))

    def _display_side_hand(
            self, frames: list, cards: list, max_length: int) -> None:
        self._side_hands_remember()
        positions = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
        for card in cards:
            suit = card[1]
            frame = frames[suit]
            pos = positions[suit]
            positions[suit] = pos + 1
            image = self.data_store.card_image(card, SCALE)
            label = ttk.Label(frame, image=image)
            label.image = image
            overlap = (max_length - pos - 1) * OVERLAP
            label.grid(row=0, column=0, sticky=tk.E, padx=(0, overlap))

    def _side_hands_remember(self) -> None:
        self.left_hand_spades.grid(row=0, column=0)
        self.left_hand_hearts.grid(row=1, column=0)
        self.left_hand_diams.grid(row=2, column=0)
        self.left_hand_clubs.grid(row=3, column=0)

        self.right_hand_spades.grid(row=0, column=0)
        self.right_hand_hearts.grid(row=1, column=0)
        self.right_hand_diams.grid(row=2, column=0)
        self.right_hand_clubs.grid(row=3, column=0)

    def _side_hands_forget(self) -> None:
        self.left_hand_spades.grid_forget()
        self.left_hand_hearts.grid_forget()
        self.left_hand_diams.grid_forget()
        self.left_hand_clubs.grid_forget()

        self.right_hand_spades.grid_forget()
        self.right_hand_hearts.grid_forget()
        self.right_hand_diams.grid_forget()
        self.right_hand_clubs.grid_forget()

    def dismiss(self, *args) -> None:
        self.root.destroy()
