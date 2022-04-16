import asyncio as aio

from command import handle_msg
from cfg import fake_username


class FakeContext:
    @staticmethod
    async def say(author, message):
        print(message)


class FakeMessage:
    class FakeAuthor:
        name = fake_username
    author = FakeAuthor
    room_id = 'gen8ou'

    def __init__(self, c):
        self.content = c


while True:
    msg = FakeMessage('.' + input('>> '))
    aio.run(handle_msg(msg, FakeContext))
