"""
Commands are stored here or something, idk
"""
import showdown
# from showdown import ChatMessage

from .helpers import format_from_roomid
from .team_extractor import get_team_from_replays, team2str

anal_format = [
    {'user': str, 'required_pokes': str | list, 'depth': int, 'format': str},
    {'user': str, 'required_pokes': str | list, 'depth': int},
    {'user': str, 'depth': int, 'required_pokes': str | list},
    {'user': str, 'depth': int},
    {'user': str, 'required_pokes': str | list},
    {'user': str},
]


async def anal_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage, private=False):
    # args: dict = anal_default.update(args)

    user = str(args['user'])

    pokes = args.get('required_pokes', [])
    pokes = [str(pokes)] if isinstance(pokes, int) else [pokes] if isinstance(pokes, str) and pokes != '' else []

    depth = int(args.get('depth', 5))

    format_ = str(args.get('format', format_from_roomid(msg.room_id) if isinstance(msg, showdown.ChatMessage) else ''))

    team, th, b = get_team_from_replays(user, format_, required_pokes=pokes, c=depth)

    paste = team2str(team).strip()

    if paste:
        for line in paste.splitlines():
            if private:
                await ctx.private_message(msg.author.name, line)
            else:
                await ctx.say(msg.room_id, line)
    else:
        if private:
            await ctx.private_message(
                msg.author.name,
                f'No team found for player {user} in this format, perhaps the archives are incomplete?'
            )
        else:
            await ctx.say(
                msg.room_id,
                f'No team found for player {user} in this format, perhaps the archives are incomplete?'
            )


banish_format = []


async def banish_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    await ctx.say(msg.room_id, 'My people need me')
    ctx.rooms[msg.room_id].logs.clear()
    await ctx.leave(msg.room_id)


help_format = [

]


async def help_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    pass


cmds = {
    'anal': {
        'format': anal_format,
        'function': anal_cmd,
    },

    'pnal': {
        'format': anal_format,
        'function': lambda a, c, m: anal_cmd(a, c, m, private=True),
    },

    'banish': {
        'format': banish_format,
        'function': banish_cmd
    },

    'help': {
        'format': help_format,
        'function': help_cmd
    }
}
