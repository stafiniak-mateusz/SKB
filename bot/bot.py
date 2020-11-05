from telebot import types
import telebot
import requests
import json
import csv
import pickle

SKB_ENDPOINT = "http://127.0.0.1:8000/api/news/"
PAGINATION_NEXT = " "
SUBSCRIPTION_SET = set()


def given_source_get_three_latest(source):
    global PAGINATION_NEXT
    url = f"{SKB_ENDPOINT}?limit=3&source={source}"
    try:
        r = requests.get(url)
        responseAsJson = json.loads(r.content)
        results = responseAsJson["results"]
        count = responseAsJson["count"]
        PAGINATION_NEXT = responseAsJson["next"]
        reply = f"<b>Total {source}'s News: {count}</b>\n\n"
        for r in results:
            reply += f'<b>News:</b> {r["title"]}\n'
            reply += f'<b>Czytaj Więcej:</b> {r["href"]}\n\n'
        return reply
    except TypeError:
        return "Nice Try..."


def three_latest_api_call(title=None):
    global PAGINATION_NEXT
    url = f"{SKB_ENDPOINT}?limit=3"
    if title:
        if ('&' in title):
            return "Nie baw się xD"
        url += f"&title={title}"
    print(url)
    try:
        r = requests.get(url)
        responseAsJson = json.loads(r.content)
        results = responseAsJson["results"]
        count = responseAsJson["count"]
        PAGINATION_NEXT = responseAsJson["next"]
        reply = f'<b>Total News: {count}</b>\n\n'
        for r in results:
            reply += f'<b>News:</b> {r["title"]}\n'
            reply += f'<b>Czytaj Więcej:</b> {r["href"]}\n\n'
        return reply
    except TypeError:
        return "Nice Try..."


def more_news_api_call():
    global PAGINATION_NEXT
    if(PAGINATION_NEXT):
        r = requests.get(PAGINATION_NEXT)
        responseAsJson = json.loads(r.content)
        results = responseAsJson["results"]
        count = responseAsJson["count"]
        PAGINATION_NEXT = responseAsJson["next"]
        reply = f'<b>Total News: {count}</b>\n\n'
        for r in results:
            reply += f'<b>News:</b> {r["title"]}\n'
            reply += f'<b>Czytaj Więcej:</b> {r["href"]}\n\n'
        return reply
    else:
        return "No more news for given query. Type /3latest or run new /search to refresh."


bot = telebot.TeleBot(
    "1362539074:AAHalCYo18mnfIyqy7tmUu-XclQo3Up-K_s", parse_mode="HTML")


@bot.message_handler(commands=['source'])
def source(message):

    markup = types.ReplyKeyboardMarkup()
    itembtnNiebezpiecznik = types.KeyboardButton('Niebezpiecznik')
    itembtnSekurak = types.KeyboardButton('Sekurak')
    itembtnOrange = types.KeyboardButton('Orange')
    itembtnCERT = types.KeyboardButton('CERT')

    markup.row(itembtnNiebezpiecznik, itembtnSekurak)
    markup.row(itembtnOrange, itembtnCERT)
    bot.send_message(message.chat.id, "Select Source...", reply_markup=markup)
    bot.register_next_step_handler(message, process_source_choice)


def process_source_choice(message):
    if (message.text not in ['Niebezpiecznik', 'Sekurak', 'Orange', 'CERT']):
        bot.send_message(
            message.chat.id, "Nie po to robiłem te kafelki, żebyś pan teraz ich NIE klikał")
    else:
        bot.send_message(
            message.chat.id, given_source_get_three_latest(message.text))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "<b>/3latest</b> - Get Three Latest News\n<b>/search <i>query</i></b> - Search for given query\n<b>/more</b> - Get Another Three News\n<b>/subscribe</b> - Subscribe to receive news regularly\n<b>/unsubscribe</b> - Unsubscribe in order not to receive news regularly\n<b>/source</b> - Select source of articles!")


@bot.message_handler(commands=['3latest'])
def get_three_latest(message):
    bot.reply_to(message, three_latest_api_call())


@bot.message_handler(commands=['more'])
def get_more(message):
    bot.reply_to(message, more_news_api_call())


@bot.message_handler(commands=['search'])
def search_news(message):
    try:
        title = message.text.split('/search ')[1]
    except:
        bot.reply_to(message, "Podaj haslo do przeszukania :D")
        return
    bot.reply_to(message, three_latest_api_call(title))


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    SUBSCRIPTION_SET = pickle.load(open("subscription_set.p", "rb"))
    SUBSCRIPTION_SET.add(message.chat.id)
    print(SUBSCRIPTION_SET)
    pickle.dump(SUBSCRIPTION_SET, open("subscription_set.p", "wb"))
    bot.reply_to(message, "Your subscription is now active!")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    SUBSCRIPTION_SET = pickle.load(open("subscription_set.p", "rb"))
    SUBSCRIPTION_SET.remove(message.chat.id)
    print(SUBSCRIPTION_SET)
    pickle.dump(SUBSCRIPTION_SET, open("subscription_set.p", "wb"))
    bot.reply_to(message, "Your subscription is now inactive!")


bot.polling()
