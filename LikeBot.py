###################################################################
# A Program to Determine who has the most Likes in a GroupMe Chat #
# Concieved by James Lubowsky                                     #
# Inspired by a love for GroupMe                                  #
###################################################################

import json
import requests
import os
import unicodedata

user_dictionary = {}
last_message_id = None
message_list = None

#group_id = YOUR_GROUP_ID
#token = YOUR_TOKEN_ID

request_url = "https://api.groupme.com/v3/groups/" + group_id + "/messages?token=" + token 
r = requests.get(request_url)

'''else:
	fh = open("data.txt", "r")
	last_message_id = str(fh.readline())
	user_dictionary = json.loads(fh.readline())
	fh.close()
	post_params = { 'before_id' : last_message_id}
	r = requests.get(request_url, params=post_params)
'''

count = 0
last_message_id = None
if len(r.content) == 0:
	num = 1
else:
	message_list = json.loads(r.content)
	count = 0
	while len(message_list['response']['messages']) > 0:

		for message in message_list['response']['messages']:
			if message['sender_id'] not in user_dictionary:
				user_dictionary[message['sender_id']] = [message['name'], len(message['favorited_by']), 1]
			else:
				user_dictionary[message['sender_id']] = [message['name'], user_dictionary[message['sender_id']][1] + len(message['favorited_by']), user_dictionary[message['sender_id']][2] + 1]

			last_message_id = message['id']

		last_message_id = message_list['response']['messages'][-1]['id']
		post_params = { 'before_id' : last_message_id, 'limit': 100}
		r = requests.get(request_url, params=post_params)
		count = count + 1
		print count
		if len(r.content) == 0:
			break
		message_list =  json.loads(r.content)

print count
max_index = 0
max_value = 0
name = None
total = 0
print user_dictionary

best_ratio_name = None
ratio = 0
messages = 0
total_likes = 0

for key, value in user_dictionary.iteritems():

	if int(value[1]) > max_value:
		max_value = int(value[1])
		max_index = key 
		name = value[0]
		total = value[2]

	if float(float(value[1])/float(value[2])) > ratio:
		ratio = float(float(value[1])/float(value[2]))
		total_likes = value[1]
		messages = value[2]
		best_ratio_name = value[0]

text =  (name).encode('utf-8') + " has the most likes at " + str(max_value)+" with an average of " + str(float(max_value/total)) + " likes per message.\n"
text = text + best_ratio_name.encode('utf-8') + " has the best like/message ratio at " + str(ratio) + " with a total of " + str(messages) + " messages and " + str(total_likes) + " likes."

'''
fh = open("data.txt", "w")
fh.write(last_message_id)
fh.write("\n")
fh.write(json.dumps(user_dictionary))
fh.close()


with open("data.txt") as f:
	last_message_id, user_dictionary = f.read().splitlines()
	print last_message_id
	print user_dictionary
	print user_dictionary[0]
'''

#bot_id = YOUR_BOT_ID

post_params = {'bot_id' : bot_id, 'text' : text}
r = requests.post("https://api.groupme.com/v3/bots/post", params=post_params)