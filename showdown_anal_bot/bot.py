import showdown as sd

from .command import handle_msg
from .helpers import filter_from_bwlists as f_bw, filter_user_from_bwlists as f_u_bw, log
from . import cfg

# |pm| host|!guest|/invite battle-blah


class SummonedClient(sd.Client):
    def __init__(self, *args, **kwargs):
        self.users_whitelisted = kwargs.get('enable_user_whitelist', False)
        self.users_blacklisted = kwargs.get('enable_usersblacklist', False)
        self.rooms_whitelisted = kwargs.get('enable_format_whitelist', False)
        self.rooms_blacklisted = kwargs.get('enable_format_blacklist', False)
        for k in ['enable_user_whitelist', 'enable_user_blacklist', 'enable_format_whitelist', 'enable_format_blacklist']:
            kwargs.pop(k, None)
        super().__init__(*args, **kwargs)

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


def main(**kwargs):
    with open(kwargs['login']) as f:
        username, password = f.read().strip().splitlines()
    kwargs.pop('login')
    client = SummonedClient(username, password, **kwargs)
    log('Starting bot...')
    client.start()
    log('Bot started')
