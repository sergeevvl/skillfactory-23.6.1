import requests
import json
from conf import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base_currency: str, conv_currency: str, amount: str):
        if base_currency == conv_currency:
            raise APIException(f'Невозможно перевести одинаковые валюты')

        try:
            base_currency_t = keys[base_currency]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base_currency}')

        try:
            conv_currency_t = keys[conv_currency]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {conv_currency}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_currency_t}&tsyms={conv_currency_t}')
        total_conv = json.loads(r.content)[keys[conv_currency]] * float(amount)

        return total_conv

