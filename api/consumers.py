from channels import Group

def ws_connect(message, user):
	print("User group connected: ", user)
	Group(user).add(message.reply_channel)
	message.reply_channel.send({"accept": True})
	Group(user).send({'text': '{"message":"' + user + ' is connected."}'}, immediately=True)
	if user == 'cam':
		Group('staff').send({'text': '{"message":"cam is connected"}'}, immediately=True)
	if user == 'staff':
		Group('cam').send({'text': '{"message":"staff is connected"}'}, immediately=True)


def ws_disconnect(message, user):
    Group(user).discard(message.reply_channel)
    Group(user).send({'close': True})