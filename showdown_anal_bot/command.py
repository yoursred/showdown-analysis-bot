import showdown

from .parser import split_command
from .commands import cmds
from .helpers import did_you_mean
from .cfg import command_prefix


async def handle_msg(msg: showdown.ChatMessage, ctx: showdown.Client):
    pre = msg.content
    if pre.startswith(command_prefix):
        pre = pre[1:]
    else:
        return

    cmd = pre.split(' ')[0]

    if cmd not in cmds:
        possible = did_you_mean(cmd, cmds)
        if possible is not None:
            await ctx.say(msg.room_id, f'Command not found: {cmd}, did you mean {possible}?')
        else:
            await ctx.say(msg.room_id, f'Command not found: {cmd}')
        return

    cmd, args, matched = split_command(
        pre, cmds[cmd]['format'], cmds[cmd].get('fallback'), cmds[cmd].get('token_parser')
    )
    if matched:
        await cmds[cmd]['function'](args, ctx, msg)
    else:
        await ctx.say(msg.room_id, f'Syntax error! Correct syntax: {cmds[cmd]["syntax"]}')
