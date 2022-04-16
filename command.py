"""
This thing parses and handles commands
"""
import showdown

from commands import cmds
from cfg import command_prefix


def split_command(
        cmd: str, fs: list, fallback: dict = None, token_parser: callable = None
) -> tuple[str, dict]:
    if fallback is None:
        fallback = dict()
    final = fallback
    s = cmd.split(' ')

    args = ' '.join(s[1:]).split(', ')

    if token_parser is None:
        args = [
            int(token) if token.isnumeric() else
            token.split(';') if ';' in token
            else token
            for token in args
        ]
    else:
        args = [
            token_parser(token, n, len(args))
            for n, token in enumerate(args)
        ]

    fks, fts = [[*f.keys()] for f in fs], [[*f.values()] for f in fs]

    found = False

    for ft, fk in zip(fts, fks):
        if found:
            break
        match args:
            case ft:
                found = True
                final = {k: v for k, v in zip(fk, args)}
                break

    return s[0], final


async def handle_msg(msg: showdown.ChatMessage, ctx: showdown.Client):
    pre = msg.content
    if pre.startswith(command_prefix):
        pre = pre[1:]
    else:
        return

    cmd = pre.split(' ')[0]

    if cmd not in cmds:
        await ctx.say(msg.room_id, f'Command not found: {cmd}')
        return

    cmd, args = split_command(pre, cmds[cmd]['format'], cmds[cmd].get('fallback'), cmds[cmd].get('token_parser'))

    await cmds[cmd]['function'](args, ctx, msg)
