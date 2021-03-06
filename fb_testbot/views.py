import json, requests, random, re
import sqlite3
import os 

from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from musixmatch import Musixmatch

from fbmessenger import BaseMessenger
from fbmessenger import quick_replies

from fb_testbot.models import UsersBot
from fb_testbot.models import Conversations
from fb_testbot.models import FavoriteSongs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# initialize the connection to the database
connection = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'), check_same_thread=False)
cursor = connection.cursor()

# create the tables needed by the program
create_table_request_list = [
    'CREATE TABLE words(word TEXT)',
]
for create_table_request in create_table_request_list:
    try:
        cursor.execute(create_table_request)
    except:
        pass

# Create your views here.
PAGE_ACCESS_TOKEN = "EAAF22Aabsu4BAHDo3ZBfBnuUZClrVZAHZCfWu1OZCxlDVUZCOZCpkFGPbbZA0QFJc3DzgXyhvX00A1Fd30rZAM7BvFaXm8nuS78riutc5QOvuy4YLQeGSkpcZB9w71LQMgsOEkM0XCihcjUzrpMtEz6kU6oWsJGKhvZBFn2YmgiTLUKFgZDZD"


def after_send(payload, response):
	""":type event: fbmq.Payload"""
	pprint("complete")

def post_facebook_message(fbid, recevied_message):       
	musixmatch = Musixmatch('e66da512f0d41fb64642d7ddc47ab311')

	track = recevied_message  #name of the song
	answer = ""
	result = musixmatch.matcher_track_get(track, "")
	body = result.get('message').get('body')

	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	
	objUsr = UsersBot()
	objUsr.user_id = user_details['id']
	objUsr.first_name = user_details['first_name']
	objUsr.last_name = user_details['last_name']

	users_bot = UsersBot.objects.all()
	
	if objUsr in users_bot:
		objUsr.save()

	if(body != ''):
		track_id = body.get('track').get('track_id')

		res_lyrics = musixmatch.track_lyrics_get(track_id)
		lyr_body = res_lyrics.get('message').get('body')

		if(lyr_body != ''):
			
			

			lyrics = lyr_body.get('lyrics').get('lyrics_body')
			cl_lyrics = lyrics.split("*****")
			answer = cl_lyrics[0]

		else:
			answer = "Lyrics not found!"

	else:
		answer = "Lyrics not found!"

	objConv = Conversations()
	objConv.user_id = user_details['id']
	objConv.message_in = recevied_message
	objConv.message_out = answer
	objConv.save()

	#cursor.execute('INSERT INTO words VALUES (?)', [recevied_message])	
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":answer}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	#pprint(status.json())

class TestBotView(generic.View, BaseMessenger):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '5432167890':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message) 
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
        return HttpResponse()
