"""User data for BfG."""

import requests
import json
from PIL import ImageTk, Image
from io import BytesIO
import base64

from constants import DATA_FILE, BASE_URI, STATIC_DATA


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
    def __init__(self):
        self.data = {}
        self.static_data = {
            'call_images': {},
        }
        self.raw_data = self.read()

        if 'call_images' in self.raw_data:
            for key in self.raw_data['call_images']:
                self.static_data['call_images'][key] = self.call_image(key)

    def call_image(self, call: str, scale: float = 1) -> ImageTk.PhotoImage:
        assert call in self.raw_data['call_images']
        image = image_from_api(self.raw_data['call_images'][call], scale)
        return ImageTk.PhotoImage(image)

    def read(self) -> dict:
        try:
            with open(DATA_FILE, 'r') as f_data:
                store = json.load(f_data)
        except json.JSONDecodeError:
            store = {}
        self.username = '' if 'username' not in store else store['username']
        self.data = store

        PARAMS = json.dumps({
            'username': 'jeff'
            })

        URI = f'{BASE_URI}{STATIC_DATA}{PARAMS}'

        response = requests.get(URI)
        if response.status_code != 200:
            print(f'*** API error; status: {response.status_code}')
            return
        return response.json()

    def write(self, store: dict) -> None:
        with open(DATA_FILE, 'w') as f_data:
            json.dump(f_data, store)
        self.data = store
