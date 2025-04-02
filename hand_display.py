""" Display hand functionality for BfG."""

import tkinter as tk
from tkinter import ttk

from psiutils.constants import PAD

CARD_SCALE = 0.35
OVERLAP = 25
BACK_OVERLAP = 10


def right_hand_frame(parent: ttk.Frame, master: tk.Frame) -> ttk.Frame:
    frame = ttk.Frame(master)
    parent.right_hand_backs = ttk.Frame(frame)
    parent.right_hand_backs.grid(row=0, column=0)

    parent.right_hand_spades = ttk.Frame(frame)
    parent.right_hand_spades.grid(row=0, column=0, sticky=tk.W)
    parent.right_hand_hearts = ttk.Frame(frame)
    parent.right_hand_hearts.grid(row=1, column=0, sticky=tk.W)
    parent.right_hand_diams = ttk.Frame(frame)
    parent.right_hand_diams.grid(row=2, column=0, sticky=tk.W)
    parent.right_hand_clubs = ttk.Frame(frame)
    parent.right_hand_clubs.grid(row=3, column=0, sticky=tk.W)

    return frame


def left_hand_frame(parent: ttk.Frame, master: tk.Frame) -> ttk.Frame:
    frame = ttk.Frame(master)
    parent.left_hand_backs = ttk.Frame(frame)
    parent.left_hand_backs.grid(row=0, column=0)

    parent.left_hand_spades = ttk.Frame(frame)
    parent.left_hand_spades.grid(row=0, column=0)
    parent.left_hand_hearts = ttk.Frame(frame)
    parent.left_hand_hearts.grid(row=1, column=0)
    parent.left_hand_diams = ttk.Frame(frame)
    parent.left_hand_diams.grid(row=2, column=0)
    parent.left_hand_clubs = ttk.Frame(frame)
    parent.left_hand_clubs.grid(row=3, column=0)

    return frame


def display_hands(parent: ttk.Frame) -> None:
    cards = parent.board.hand_cards
    _horizontal_hand(parent, parent.top_hand, cards[2], True)
    _right_hand(parent, cards[3])
    _horizontal_hand(parent, parent.bottom_hand, cards[0])
    _left_hand(parent, cards[1])


def _horizontal_hand(parent, frame, cards, partner: bool = False) -> None:
    for widget in frame.winfo_children():
        widget.destroy()
    for index in range(len(cards)):
        image = parent.data_store.card_image(cards[index], CARD_SCALE)
        if parent._hide_partner(partner):
            image = parent.data_store.card_image('back', CARD_SCALE)
        label = ttk.Label(frame, image=image)
        label.image = image
        overlap = (len(cards) - index) * OVERLAP
        label.grid(row=0, column=0,
                   sticky=tk.E, padx=(0, overlap), pady=PAD)


def _right_hand(parent: ttk.Frame, cards) -> None:
    max_length = parent.board.max_suit_length['W']
    frames = {
        'B': parent.right_hand_backs,
        'S': parent.right_hand_spades,
        'H': parent.right_hand_hearts,
        'D': parent.right_hand_diams,
        'C': parent.right_hand_clubs,
        }
    _clear_frames_cards(frames)

    if parent._hide_opps():
        _display_backs(parent, parent.right_hand_backs, cards)
    else:
        _display_side_hand(parent, frames, cards, max_length)


def _left_hand(parent: ttk.Frame, cards: list) -> None:
    max_length = parent.board.max_suit_length['E']
    frames = {
        'B': parent.left_hand_backs,
        'S': parent.left_hand_spades,
        'H': parent.left_hand_hearts,
        'D': parent.left_hand_diams,
        'C': parent.left_hand_clubs,
        }
    _clear_frames_cards(frames)

    if parent._hide_opps():
        _display_backs(parent, parent.left_hand_backs, cards)
    else:
        _display_side_hand(parent, frames, cards, max_length)


def _clear_frames_cards(frames: list) -> None:
    for frame in frames.values():
        for widget in frame.winfo_children():
            widget.destroy()


def _display_backs(parent: ttk.Frame, frame: ttk.Frame, cards: list) -> None:
    _side_hands_forget(parent)
    image = parent.data_store.card_image('back', CARD_SCALE)
    for index in range(len((cards))):
        label = ttk.Label(frame, image=image)
        label.image = image
        label.grid(row=0, column=0, sticky=tk.E,
                   padx=(0, index*BACK_OVERLAP))


def _display_side_hand(
        parent: ttk.Frame, frames: list, cards: list, max_length: int) -> None:
    _side_hands_remember(parent)
    positions = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
    for card in cards:
        suit = card[1]
        frame = frames[suit]
        pos = positions[suit]
        positions[suit] = pos + 1
        image = parent.data_store.card_image(card, CARD_SCALE)
        label = ttk.Label(frame, image=image)
        label.image = image
        overlap = (max_length - pos - 1) * OVERLAP
        label.grid(row=0, column=0, sticky=tk.E, padx=(0, overlap))


def _side_hands_remember(parent: ttk.Frame) -> None:
    parent.left_hand_spades.grid(row=0, column=0)
    parent.left_hand_hearts.grid(row=1, column=0)
    parent.left_hand_diams.grid(row=2, column=0)
    parent.left_hand_clubs.grid(row=3, column=0)

    parent.right_hand_spades.grid(row=0, column=0)
    parent.right_hand_hearts.grid(row=1, column=0)
    parent.right_hand_diams.grid(row=2, column=0)
    parent.right_hand_clubs.grid(row=3, column=0)


def _side_hands_forget(parent: ttk.Frame) -> None:
    parent.left_hand_spades.grid_forget()
    parent.left_hand_hearts.grid_forget()
    parent.left_hand_diams.grid_forget()
    parent.left_hand_clubs.grid_forget()

    parent.right_hand_spades.grid_forget()
    parent.right_hand_hearts.grid_forget()
    parent.right_hand_diams.grid_forget()
    parent.right_hand_clubs.grid_forget()
