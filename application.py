import telebot
import requests
import json
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

class ConvertionExeption(Exception):
    pass


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботов введите через "пробел" команду в формате:\n<название валюты, которую хотим конвертировать> \
<название валюты в которую хотим перевести> \
<количество конвертируемой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны следующие:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    values3 = quote, base, amount
    if len(values3) != 3:
        raise ConvertionExeption ('Должно быть только 3 параметра')
    if quote == base:
        raise ConvertionExeption('нельзя переводить в одну и ту же валюту')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionExeption(f'Неверно введена валюта: {quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionExeption(f'Неверно введена валюта: {base}')

    try:
        amount = int(amount)
    except ValueError:
        raise ConvertionExeption(f'Количество валюты должно быть целым числом')

    api_key = {
        'apikey': 'мой апи ключ',
    }
    request_1 = requests.get(
        f'https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={int(amount)}',
        headers=api_key)
    resp = json.loads(request_1.content)
    respond = resp['result']
    text = f'{amount} {quote} перевести в {base} будет {respond}'
    bot.send_message(message.chat.id, text)


bot.polling()

