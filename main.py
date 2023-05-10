import telebot
from conf import TOKEN, keys
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nПосмотреть список всех доступных валют: /currencies'
    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')

        if len(values_) != 3:
            raise APIException('Неверное количество параметров')

        base_currency, conv_currency, amount = values_
        total_conv = CryptoConverter.get_price(base_currency, conv_currency, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base_currency} в {conv_currency} - {total_conv}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)