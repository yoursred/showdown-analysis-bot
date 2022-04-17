import asyncio as aio

from .command import handle_msg


class FakeContext:
    @staticmethod
    async def say(author, message):
        print(message)


class FakeMessage:
    def __init__(self, c, name):
        class FakeAuthor:
            def __init__(self):
                self.name = name

        self.author = FakeAuthor()
        self.room_id = 'gen8ou'
        self.content = c


def main(**kwargs):
    while True:
        msg = FakeMessage('.' + input('>> '), kwargs['fake_username'])
        aio.run(handle_msg(msg, FakeContext))
