"""
Commands are stored here or something, idk
"""
from random import choice

import showdown
# from showdown import ChatMessage
from .parser import generate_syntax_strings
from .helpers import format_from_roomid, did_you_mean
from .team_extractor import get_team_from_replays, team2str, get_likely_back
from .messages import bully_messages

anal_format = [
    {'args': {'user': str}, 'optional': {
        'args': {'required_pokes': str | list},
        'optional': {
            'args': {'depth': int},
            'optional': {
                'args': {'format': str}
               }
            },
        }
    },
    {'args': {'user': str}, 'optional': {
        'args': {'depth': int},
        'optional': {
            'args': {'required_pokes': str | list}
           }
        }
    }
]


async def anal_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage, private=False):
    # args: dict = anal_default.update(args)

    user = str(args['user'])

    pokes = args.get('required_pokes', [])
    pokes = [str(pokes)] if isinstance(pokes, int) else [pokes] if isinstance(pokes, str) and pokes != '' else []

    depth = int(args.get('depth', 5))

    format_ = str(args.get('format', format_from_roomid(msg.room_id) if isinstance(msg, showdown.ChatMessage) else ''))

    team, th, ltm, b = get_team_from_replays(user, format_, required_pokes=pokes, c=depth)

    paste = team2str(team, th, ltm).strip()

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


banish_format = [
    {'args': {}}
]  # banish


async def banish_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    await ctx.say(msg.room_id, 'My people need me')
    ctx.rooms[msg.room_id].logs.clear()
    await ctx.leave(msg.room_id)


cross_back_format = [
    {'args': {'pokes': str | list}}
]


async def cross_back_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    print(args)
    pokes = args.get('pokes', [])
    # pokes = [str(pokes)] if isinstance(pokes, int) else [pokes] if isinstance(pokes, str) and pokes != '' else []

    likely_back = get_likely_back(pokes)
    await ctx.say(msg.room_id, f'{likely_back}')


bully_format = [
    {'args': {'user': str}, 'optional': {
        'args': {'harshness': int}
    }}
]


async def bully_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    if args.get('user', '') == '':
        await ctx.say(msg.room_id, 'You must specify a user to bully')
        return
    else:
        user = args.get('user')
        message = choice(bully_messages)
        if '{}' in message:
            message = message.format(user)
        await ctx.say(msg.room_id, message)


cmds = {
    'anal': {
        'format': anal_format,
        'function': anal_cmd,
        'description': 'Wallhaxes a team from a user\'s replays, optionally specifying required mons and battle count.'
    },

    'pnal': {
        'format': anal_format,
        'function': lambda a, c, m: anal_cmd(a, c, m, private=True),
        'description': 'Same as anal, but sends the results to the user privately.'
    },

    'banish': {
        'format': banish_format,
        'function': banish_cmd,
        'description': 'Banish the bot from the room'
    },

    'crossback': {
        'format': cross_back_format,
        'function': cross_back_cmd,
        'description': 'Get a likely back for a team, need to have ran `anal` first'
    },
    'bully': {
        'format': bully_format,
        'function': bully_cmd,
        'description': 'Bully a user, optionally specifying a harshness'
    }
}

help_format = [
    {'optional': {'args': {'command': str}}}
]
# Syntax: help <command> || help
# Description: Get help for a command


async def help_cmd(args: dict, ctx: showdown.Client, msg: showdown.ChatMessage):
    # This function is defined after cmds because it needs to access the cmds dict
    command = args.get('command', '')
    if command in cmds:
        await ctx.say(msg.room_id, f'Syntax: {cmds[command]["syntax"]}')
        await ctx.say(msg.room_id, f'Description: {cmds[command]["description"]}')
    elif command == '':
        await ctx.say(msg.room_id, f'Available commands: {", ".join(cmds.keys())}')
    else:
        possible = did_you_mean(command, cmds.keys())
        if possible is not None:
            await ctx.say(msg.room_id, f'Command not found: {command}, did you mean {possible}?')
        else:
            await ctx.say(msg.room_id, f'Command not found')

cmds['help'] = {
    'format': help_format,
    'function': help_cmd,
    'description': 'Get help for a command'
}

# Generate the syntax string for each command
for cmd in cmds:
    cmds[cmd]['syntax'] = generate_syntax_strings(cmds[cmd]['format'], cmd)
