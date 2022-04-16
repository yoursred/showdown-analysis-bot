import gzip

import showdown as sd

import cfg
from cfg import battle_log_location
from helpers import format_from_roomid, log


class ReplayClient(sd.Client):
    def __init__(self, name='', password='', *, loop=None, max_room_logs=5000,
                 server_id='showdown', server_host=None, strict_exceptions=False, to_stalk=None, game_modes=None,
                 min_elo=1000, max_battles=None):
        super(ReplayClient, self).__init__(name=name, password=password, loop=loop, max_room_logs=max_room_logs,
                                           server_id=server_id, server_host=server_host,
                                           strict_exceptions=strict_exceptions)
        self.to_stalk = to_stalk
        self.game_modes = game_modes
        self.min_elo = min_elo
        self.max_battles = max_battles

    async def on_query_response(self, response_type, data):
        if self.max_battles is not None and len(self.rooms) >= self.max_battles:
            log(f'Max battles reached, not receiving any more queries')
            return
        if response_type == 'roomlist':
            for battle_id in set(data['rooms']) - set(self.rooms):
                log(f'Joining {battle_id}')
                await self.join(battle_id)
                log(f'Joined {battle_id}')
                if self.max_battles is not None and len(self.rooms) >= self.max_battles:
                    log(f'Max battles reached, not joining any more battles')
                    break
        elif response_type == 'userdetails':
            for room in data['rooms']:
                if room not in self.rooms and (self.game_modes is None or format_from_roomid(room) in self.game_modes):
                    log(f'Joining {room} to stalk {data["id"]}')
                    await self.join(room)
                    log(f'Joined {room} to stalk {data["id"]}')
                    if self.max_battles is not None and len(self.rooms) >= self.max_battles:
                        log(f'Max battles reached, not joining any more battles')
                        break

    async def on_receive(self, room_id, inp_type, params):
        if inp_type == 'win':
            p = battle_log_location + '/' + room_id + '.gz'
            with open(p, 'wb') as f:
                f.write(gzip.compress(bytes('\n'.join(self.rooms[room_id].logs), 'utf-8')))
                log(f'{room_id} finished, saved to {p}')
            log(f'Now leaving {room_id}')

    @sd.Client.on_interval(interval=5)
    async def stalk(self):
        if self.game_modes is None:
            log(f'Max battles reached, not sending any more queries')
            return
        if self.to_stalk is not None:
            for user in self.to_stalk:
                log(f'Querying user {user}')
                await self.send_message('/cmd userdetails ' + user)
        elif self.game_modes is not None:
            for mode in self.game_modes:
                log(f'Querying mode {mode}')
                await self.query_battles(battle_format=mode, lifespan=3)
        else:
            log(f'Querying all battles')
            await self.query_battles()


stalk_config = cfg.stalk_config
to_stalk = stalk_config['to_stalk']
game_modes = stalk_config['game_modes']
min_elo = stalk_config['min_elo']  # TODO: implement
max_battles = stalk_config['max_battles']

log(f'Starting stalk client')

ReplayClient(
    '', '', to_stalk=to_stalk, game_modes=game_modes, min_elo=min_elo, max_battles=max_battles
).start(autologin=False)
