import telebot
import json
import random
import requests
import pickle


SKB_ENDPOINT = "http://127.0.0.1:8000/api/news/"


bot = telebot.TeleBot(
    "1362539074:AAHalCYo18mnfIyqy7tmUu-XclQo3Up-K_s", parse_mode="HTML")


def send_notification():
    return "HueHue"


def send_random_news():
    url = f"{SKB_ENDPOINT}?limit=20"
    r = requests.get(url)
    responseAsJson = json.loads(r.content)
    results = responseAsJson["results"]
    randomArticle = random.randint(0, 19)

    reply = f'<b>Cześć, widziałeś już to?</b>\n\n'
    reply += f'<b>News:</b> {results[randomArticle]["title"]}\n'
    reply += f'<b>Czytaj Więcej:</b> {results[randomArticle]["href"]}\n\n'

    return reply


for chat_id in pickle.load(open("subscription_set.p", "rb")):
    print(chat_id)
    bot.send_message(chat_id, send_random_news())
