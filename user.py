"""User class for BfG"""


class User():
    def __init__(self, username: str = '') -> None:
        self.username = username
        self.login_id = ''
        self.logged_in = False
        self.contacts = []
        self.contact_details = []
        self.last_message = ''
        self.boards = []
        self.set_hands = []
        self.use_set_hands = False
        self.display_hand_type = False
        self.set_hand_save_list = []
        self.last_mode = ''
        self.use_solo_comments = False
        self.mode = ''
        self.tester = False
        self.test_card_play = False
        self.test_card_play_allowed = False
        self.pbn_allowed = False
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.id = ''
        self.partner = ''
        self.room_name = ''
        self.seat = ''


def test_user() -> User:
    user = User()
    user.username = 'jeff'
    user.login_id = ''
    user.logged_in = True
    user.contacts = []
    user.contact_details = []
    user.last_message = ''
    user.boards = []
    user.set_hands = []
    user.use_set_hands = False
    user.display_hand_type = False
    user.set_hand_save_list = []
    user.last_mode = ''
    user.use_solo_comments = False
    user.mode = 'solo'
    user.tester = True
    user.test_card_play = True
    user.test_card_play_allowed = True
    user.pbn_allowed = True
    user.first_name = 'Jeff'
    user.last_name = 'Watkins'
    user.email = 'jeffwatkins2000@gmail.com'
    user.id = 'jeff'
    user.partner = ''
    user.room_name = 'jeff'
    user.seat = 'N'
    return user
