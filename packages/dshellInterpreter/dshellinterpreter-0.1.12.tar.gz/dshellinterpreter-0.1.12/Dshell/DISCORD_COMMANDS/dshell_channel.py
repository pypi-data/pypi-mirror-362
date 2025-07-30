from asyncio import sleep
from re import search
from typing import Union

from discord import MISSING, PermissionOverwrite, Member, Role, Message

__all__ = [
    'dshell_create_text_channel',
    'dshell_delete_channel',
    'dshell_delete_channels',
    'dshell_create_voice_channel'
]


async def dshell_create_text_channel(ctx: Message,
                                     name,
                                     category=None,
                                     position=MISSING,
                                     slowmode=MISSING,
                                     topic=MISSING, nsfw=MISSING,
                                     permission: dict[Union[Member, Role], PermissionOverwrite] = MISSING,
                                     reason=None):
    """
    Creates a text channel on the server
    """

    channel_category = ctx.channel.guild.get_channel(category)

    created_channel = await ctx.guild.create_text_channel(name,
                                                          category=channel_category,
                                                          position=position,
                                                          slowmode_delay=slowmode,
                                                          topic=topic,
                                                          nsfw=nsfw,
                                                          overwrites=permission,
                                                          reason=reason)

    return created_channel.id

async def dshell_create_voice_channel(ctx: Message,
                                      name,
                                      category=None,
                                      position=MISSING,
                                      bitrate=MISSING,
                                      permission: dict[Union[Member, Role], PermissionOverwrite] = MISSING,
                                      reason=None):
    """
    Creates a voice channel on the server
    """

    channel_category = ctx.channel.guild.get_channel(category)

    created_channel = await ctx.guild.create_voice_channel(name,
                                                           category=channel_category,
                                                           position=position,
                                                           bitrate=bitrate,
                                                           overwrites=permission,
                                                           reason=reason)

    return created_channel.id


async def dshell_delete_channel(ctx: Message, channel=None, reason=None, timeout=0):
    """
    Deletes a channel.
    You can add a waiting time before it is deleted (in seconds)
    """

    channel_to_delete = ctx.channel if channel is None else ctx.channel.guild.get_channel(channel)

    if channel_to_delete is None:
        raise Exception(f"Le channel {channel} n'existe pas !")

    await sleep(timeout)

    await channel_to_delete.delete(reason=reason)

    return channel_to_delete.id


async def dshell_delete_channels(ctx: Message, name=None, regex=None, reason=None):
    """
    Deletes all channels with the same name and/or matching the same regex.
    If neither is set, it will delete all channels with the same name as the one where the command was executed.
    """
    for channel in ctx.channel.guild.channels:

        if name is not None and channel.name == str(name):
            await channel.delete(reason=reason)

        elif regex is not None and search(regex, channel.name):
            await channel.delete(reason=reason)
