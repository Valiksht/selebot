import os
from gigachat import GigaChat
from text_messege import MAX_VALUE

"""Функция для генерации поздравления."""


def genegate(name, event, description):
    text = (
        f'Ты поздравляешь {name} с {event}. '
        f'{name}: {description}. '
        f'Напиши поздравление объемом {MAX_VALUE} символов.'
    )
    with GigaChat(
        credentials=os.getenv('AUTHORIZATION_KEY'),
        ca_bundle_file="russian_trusted_root_ca.cer"
    ) as giga:
        response = giga.chat(text)
        return response.choices[0].message.content


"""Функция для получения баланса."""


def get_balance():
    with GigaChat(
        credentials=os.getenv('AUTHORIZATION_KEY'),
        ca_bundle_file="russian_trusted_root_ca.cer"
    ) as giga:
        balance = giga.get_balance()
        for model in balance.balance:
            if model.usage == 'GigaChat':
                return ('Остаток токенов: ' + str(int(model.value)))
