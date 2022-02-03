import showdown as sd

from command import handle_msg
from team_extractor import team2str, get_team_from_replays
from helpers import filter_from_bwlists as f_bw, filter_user_from_bwlists as f_u_bw
import cfg

# |pm| host|!guest|/invite battle-blah

with open('login.txt') as f:
    username, password = f.read().strip().splitlines()


class SummonedClient(sd.Client):
    async def on_private_message(self, private_message):
        if private_message.content.startswith('/invite'):
            room_id = private_message.content.split(' ')[-1]
            if f_u_bw(private_message.author, cfg.user_bl, cfg.user_wl):
                if f_bw('-'.join(room_id.split('-')[:-1]), cfg.format_bl, cfg.format_wl):
                    if room_id not in self.rooms:
                        await self.join(room_id)
                        await self.say(room_id, f'I have been summoned by {private_message.author}')
        else:
            await handle_msg(private_message, self)

    async def on_chat_message(self, chat_message):
        await handle_msg(chat_message, self)


SummonedClient(name=username, password=password).start()
