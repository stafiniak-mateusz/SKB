from django.shortcuts import render
import requests
import telegram
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from ipware.ip import get_ip
from django.conf import settings

URL=settings.TELEGRAM_BOT_URL
bot_token=settings.TELEGRAM_BOT_TOKEN
chat_id='placeholder'

class JsonEncoder(DjangoJSONEncoder):
    def default(self,obj):
        if isinstance(obj,dict):
            return str(obj)
        return super().default(obj)

def bot(request, msg, token=bot_token):
    bot=telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id,text=msg)

def home(request):
    bot(request, "Test")
# Create your views here.
