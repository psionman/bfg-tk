"""User data for BfG."""

import json
from PIL import ImageTk, Image
from io import BytesIO
import base64

from constants import DATA_FILE
from api import response_from_api
from user import User


def image_from_api(image_str: str, scale: float = 1) -> Image:
    if ',' in image_str:
        # Remove 'data:image/jpeg;base64,'
        image_str = image_str.split(',')[1]

    missing_padding = len(image_str) % 4
    if missing_padding:
        image_str += '=' * (4 - missing_padding)

    image_data = base64.b64decode(image_str)
    image = Image.open(BytesIO(image_data))
    image = image.resize(
        (int(image.width * scale), int(image.height * scale)),
        Image.LANCZOS)
    return image


class DataStore():
    def __init__(self, user: User):
        self.user = user
        self.data = {}
        self.static_data = {
            'call_images': {},
        }
        self.raw_data = self.read()
        self.static_data = StaticData(self.raw_data)
        # for key, item in self.raw_data.items():
        #     print(key, type(item))

        # if 'call_images' in self.raw_data:
        #     for key in self.raw_data['call_images']:
        #         self.static_data['call_images'][key] = self.call_image(key)

    def call_image(self, call: str, scale: float = 1) -> ImageTk.PhotoImage:
        assert call in self.raw_data['call_images']
        image = image_from_api(self.raw_data['call_images'][call], scale)
        return ImageTk.PhotoImage(image)

    def card_image(self, card: str, scale: float = 1) -> ImageTk.PhotoImage:
        assert card in self.raw_data['card_images']
        image = image_from_api(self.raw_data['card_images'][card], scale)
        return ImageTk.PhotoImage(image)

    def read(self) -> dict:
        try:
            with open(DATA_FILE, 'r') as f_data:
                store = json.load(f_data)
        except json.JSONDecodeError:
            store = {}
        self.username = '' if 'username' not in store else store['username']
        self.data = store

        return response_from_api('static-data')

    def write(self, store: dict) -> None:
        with open(DATA_FILE, 'w') as f_data:
            json.dump(f_data, store)
        self.data = store


class StaticData():
    def __init__(self, data):
        self.card_images: dict = data['card_images']
        self.call_images: dict = data['call_images']
        self.cursor: str = data['cursor']
        self.calls: list = data['calls']
        self.solo_set_hands: dict = data['solo_set_hands']
        self.duo_set_hands: dict = data['duo_set_hands']
        self.sources: dict = data['sources']
        self.versions: dict = data['versions']


class NewBoard():
    def __init__(self, data):
        self.EW_tricks: int = data['EW_tricks']
        self.NS_tricks: int = data['NS_tricks']
        self.bid_box_extra_names: list = data['bid_box_extra_names']
        self.bid_box_names: list = data['bid_box_names']
        self.bid_history: list = data['bid_history']
        self.board_number: int = data['board_number']
        self.board_pbn: str = data['board_pbn']
        self.contract: str = data['contract']
        self.contract_target: int = data['contract_target']
        self.current_player: str = data['current_player']
        self.dealer: str = data['dealer']
        self.declarer: str = data['declarer']
        self.dummy: None = data['dummy']
        self.hand_cards: list = data['hand_cards']
        self.hand_suit_length: dict = data['hand_suit_length']
        self.identifier: str = data['identifier']
        self.max_suit_length: dict = data['max_suit_length']
        self.passed_out: bool = data['passed_out']
        self.previous_player: None = data['previous_player']
        self.score: int = data['score']
        self.source: int = data['source']
        self.stage: None = data['stage']
        self.suit_order: list = data['suit_order']
        self.test: bool = data['test']
        self.three_passes: bool = data['three_passes']
        self.trick_count: int = data['trick_count']
        self.trick_suit: str = data['trick_suit']
        self.tricks: list = data['tricks']
        self.tricks_leaders: list = data['tricks_leaders']
        self.unplayed_card_names: dict = data['unplayed_card_names']
        self.vulnerable: str = data['vulnerable']


"""
StaticData ->
    card_images: dict
    call_images: dict
    cursor: str
    calls: list
    solo:_set_hands dict
    duo_set_hands: dict
    sources: dict
    versions: dict

NewBoard ->
    EW_tricks: int
    NS_tricks: int
    bid_box_extra_names: list
    bid_box_names: list
    bid_history: list
    board_number: int
    board_pbn: str
    contract: str
    contract_target: int
    current_player: str
    dealer: str
    declarer: str
    dummy: None
    hand_cards: list
    hand_suit_length: dict
    identifier: str
    max_suit_length: dict
    passed_out: bool
    previous_player: None
    score: int
    source: int
    stage: None
    suit_order: list
    test: bool
    three_passes: bool
    trick_count: int
    trick_suit: str
    tricks: list
    tricks_leaders: list
    unplayed_card_names: dict
    vulnerable: str

"""
