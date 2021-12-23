import telebot
from config import dict_of_currency, TOKEN
from extensions import ConvertionException, Get_price

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите <имя валюты, цену которой Вы хотите узнать> ' \
           '<имя валюты в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>\n' \
           '/start или /help - подсказка.\n' \
           '/values - вывести список всех доступных валют.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in dict_of_currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        if len(val) != 3:
            raise ConvertionException('Неверное количество параметров.')
        quote, base, amount = val
        if float(amount) <= 0:
            raise ConvertionException('Количество должно быть больше 0.')
        total_base = Get_price.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(total_base * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()