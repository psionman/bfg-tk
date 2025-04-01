"""Handle api access for BfG."""
import requests
import json
from datetime import datetime

from constants import BASE_URI
from user import User

URIS = {
    'static-data': f'{BASE_URI}static-data/',
    'new-board': f'{BASE_URI}new-board/',
}


def response_from_api(url: str, user: User | None = None) -> dict:
    if not user:
        params = {}
    else:
        params = _get_params(user)
    uri = f'{URIS[url]}{json.dumps(params)}'
    response = requests.get(uri)
    if response.status_code != 200:
        print(f'*** API error; status: {response.status_code}')
        return
    return response.json()


def _get_params(user: User) -> dict:
    params = {
        'room_name': user.room_name,
        'seat': user.seat,
        'username': user.username,
        'set_hands': user.set_hands,
        'use_set_hands': user.use_set_hands,
        'display_hand_type': user.display_hand_type,
        'mode': user.mode,
        'tester': user.tester,
        'timestamp': datetime.now().strftime('%Y%b%d'),
        'partner_username': user.partner,
        'browser': False,
    }
    return params
