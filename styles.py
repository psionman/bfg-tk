"""Styles definitions for BfG"""
from tkinter import ttk


def load_styles() -> None:
    # BiddingBox
    style = ttk.Style()
    style.configure(
        'black.TButton',
        foreground='black',
        background='white',
        font=('Helvetica', 15, 'bold'),
        width=3.5,
        )
    style.map(
        "black.TButton",
        foreground=[('pressed', 'white'), ('active', 'black')],
        background=[('pressed',  'black'), ('active', '#999999')]
        )

    style = ttk.Style()
    style.configure(
        'black_clicked.TButton',
        foreground='white',
        background='black',
        font=('Helvetica', 15, 'bold'),
        width=3.5,
        )
    style.map(
        "black_clicked.TButton",
        foreground=[('pressed', 'white'), ('active', 'black')],
        background=[('pressed',  'black'), ('active', '#999999')]
        )

    style.configure(
        'red.TButton',
        foreground='red',
        background='white',
        font=('Helvetica', 15, 'bold'),
        width=3.5,
        )
    style.map(
        "red.TButton",
        foreground=[('pressed', 'white'), ('active', 'red')],
        background=[('pressed',  'red'), ('active', '#999999')]
        )

    style = ttk.Style()
    style.configure(
        'red_clicked.TButton',
        foreground='white',
        background='red',
        font=('Helvetica', 15, 'bold'),
        width=3.5,
    )
    style.map(
        "red_clicked.TButton",
        foreground=[('pressed', 'white'), ('active', 'red')],
        background=[('pressed',  'red'), ('active', '#999999')]
        )

    style.configure(
        'green.TCheckbutton',
        foreground='white',
        background='green',
        )
    style.map(
        "green.TCheckbutton",
        foreground=[('pressed', 'white'), ('active', 'green')],
        background=[('pressed',  'black'), ('active', 'white')]
        )
