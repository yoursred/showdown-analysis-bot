import gzip
import pathlib

import showdown as sd

from .helpers import format_from_roomid, log


def make_replay_client(kwargs):
    query_interval = kwargs.pop('query_interval')
    battle_log_location = kwargs.pop('battle_log_location')

    class ReplayClient(sd.Client):
        def __init__(self, name='', password='', *, loop=None, max_room_logs=5000,
                     server_id='showdown', server_host=None, strict_exceptions=False, to_stalk=None, game_modes=None,
                     min_elo=1000, max_battles=None):
            super(ReplayClient, self).__init__(name=name, password=password, loop=loop, max_room_logs=max_room_logs,
                                               server_id=server_id, server_host=server_host,
                                               strict_exceptions=strict_exceptions)
            self.to_stalk = kwargs['to_stalk']
            if self.to_stalk == ['-']:
                self.to_stalk = None
            self.game_modes = kwargs['game_modes']
            if self.game_modes == ['-']:
                self.game_modes = None
            self.min_elo = kwargs['min_elo']
            self.max_battles = kwargs['max_battle_count']

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

        @sd.Client.on_interval(interval=query_interval)
        async def send_queries(self):
            if self.max_battles is not None and len(self.rooms) >= self.max_battles:
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
                log(f'Querying all formats')
                await self.query_battles()

    return ReplayClient


def main(**kwargs):
    # TODO: fix max battle count not working
    ReplayClient = make_replay_client(kwargs)
    log(f'Starting stalk client')
    ReplayClient(
        '', ''
    ).start(autologin=False)
