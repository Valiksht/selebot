import os
from dotenv import load_dotenv

from gigachat import GigaChat

from text_messege import MAX_VALUE

load_dotenv()

setreficate = 'russian_trusted_root_ca.cer'

ca_file_path = os.path.join(os.path.dirname(__file__), setreficate)

"""Функция для генерации поздравления."""


def genegate(name, event, description):
    text = (
        f'Ты поздравляешь {name} с {event}. '
        f'{name}: {description}. '
        f'Напиши поздравление объемом {MAX_VALUE} символов.'
    )
    with GigaChat(
        credentials=os.getenv('AUTHORIZATION_KEY'),
        ca_bundle_file=ca_file_path
    ) as giga:
        response = giga.chat(text)
        return response.choices[0].message.content


"""Функция для получения баланса."""


def get_balance():
    with GigaChat(
        credentials=os.getenv('AUTHORIZATION_KEY'),
        ca_bundle_file=ca_file_path
    ) as giga:
        balance = giga.get_balance()
        for model in balance.balance:
            if model.usage == 'GigaChat':
                return (int(model.value))
