import requests
import string
import secrets
from src.config import *


URL = TEMP_MAIL_SERVICE_URL


def randomizer(symbol):
    length = int(secrets.choice(string.digits[4:]))
    return ''.join(secrets.choice(symbol) for i in range(length))


class Creator:
    def __init__(self):
        self._address: str
        self._password: str
        self._token: str

    def create_account(self):
        # getting domain
        response_1 = requests.get(f'{URL}/domains')
        member = response_1.json()['hydra:member'][0]
        assert member['isActive'] is True, 'No domains'
        domain = member['domain']

        # creating user
        address = f'{randomizer(string.ascii_letters).lower()}@{domain}'
        password = randomizer(string.ascii_letters + string.digits)
        data = {
            'address': address,
            'password': password
        }
        response_2 = requests.post(f'{URL}/accounts', json=data)
        assert address == response_2.json()['address'], 'Address not the same'
        self._address = address
        self._password = password

        # getting token
        response_3 = requests.post(f'{URL}/token', json=data)
        self._token = response_3.json()['token']
        # text = f"{self.token}\n{self.address}\n{self.password}"
        # MyWith.write_new_txt('src/EmailCreator_data.txt', text)
        return self._token

    def get_email(self): 
        return self._address

    def get_pass(self): 
        return self._password


class Messages:
    def __init__(self, token):
        self._headers = {'Authorization': f'Bearer {token}'}
        self._email: str
        self._name: str
        self._subject: str
        self._text: str

    def get_messages_id(self):
        data = {'page': 1}
        response = requests.get(f'{URL}/messages', headers=self._headers, params=data)
        message_ids = [dict_['id'] for dict_ in response.json()['hydra:member']]
        return message_ids

    def form_message_info(self, message_id:str):
        try:
            response = requests.get(f'{URL}/messages/{message_id}', headers=self._headers)
            self._email = response.json()['from']['address']
            self._name = response.json()['from']['name']
            self._subject = response.json()['subject']
            self._text = response.json()['text']
        except KeyError:
            list_of_ids = self.get_messages_id()
            if not list_of_ids:
                raise Exception('Sorry, but id is wrong. Actually, there are no messages at all.')
            raise Exception(f'Sorry, there are no message with id "{message_id}". Try: {list_of_ids}')

    def form_last_message_info(self):
        last_message_id = self.get_messages_id()[0]
        self.form_message_info(last_message_id)

    def get_email(self):
        return self._email

    def get_name(self):
        return self._name

    def get_subject(self):
        return self._subject

    def get_text(self):
        return self._text
