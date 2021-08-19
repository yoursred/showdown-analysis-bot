import showdown as sd

# |pm| host|!guest|/invite battle-blah

with open('login.txt') as f:
    username, password = f.read().strip().splitlines()

class SummonedClient(sd.Client):
    async def on_private_message(self, private_message):
        if private_message.content.startswith('/invite'):
            room_id = private_message.content.split(' ')[-1]
            if room_id not in self.rooms:
                await self.join(room_id)
                await self.say(room_id, f'I have been summoned by {private_message.author}')

SummonedClient(name=username, password=password).start()