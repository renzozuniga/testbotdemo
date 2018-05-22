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
#PAGE_ACCESS_TOKEN = "EAAF22Aabsu4BAHDo3ZBfBnuUZClrVZAHZCfWu1OZCxlDVUZCOZCpkFGPbbZA0QFJc3DzgXyhvX00A1Fd30rZAM7BvFaXm8nuS78riutc5QOvuy4YLQeGSkpcZB9w71LQMgsOEkM0XCihcjUzrpMtEz6kU6oWsJGKhvZBFn2YmgiTLUKFgZDZD"
#VERIFY_TOKEN = "5432167890"
#API_KEY = "e66da512f0d41fb64642d7ddc47ab311"
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
API_KEY = os,environ['API_KEY']

def post_facebook_message(self, fbid, recevied_message):       
	musixmatch = Musixmatch(API_KEY)

	track = recevied_message.split("-")
	if(len(track) == 2):
		result = musixmatch.matcher_track_get(track[0], track[1])
		body = result.get('message').get('body')

		if(body != ''):
			track_id = body.get('track').get('track_id')

			res_lyrics = musixmatch.track_lyrics_get(track_id)
			lyr_body = res_lyrics.get('message').get('body')

			if(lyr_body != ''):
				lyrics = lyr_body.get('lyrics').get('lyrics_body')
				cl_lyrics = lyrics.split("*****")
				lyrics = cl_lyrics[0]

			else:
				lyrics = "Lyrics not found!"

		else:
			lyrics = "Lyrics not found!"

	else:
		lyrics = "Lyrics not found!"

	cursor.execute('INSERT INTO words VALUES (?)', [recevied_message])	
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":lyrics}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	#pprint(status.json())

class TestBotView(generic.View, BaseMessenger):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
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
                    post_facebook_message(self, message['sender']['id'], message['message']['text'])    
        return HttpResponse()
