from discord import MISSING, Message


__all__ = [
    "dshell_ban_member",
    "dshell_unban_member",
    "dshell_kick_member",
    "dshell_rename_member"
]

async def dshell_ban_member(ctx: Message, member: int, reason: str = MISSING):
    """
    Bans a member from the server.
    """
    banned_member = ctx.channel.guild.get_member(member)

    if not banned_member:
        return 1 # Member not found in the server

    await ctx.channel.guild.ban(banned_member, reason=reason)

    return banned_member.id

async def dshell_unban_member(ctx: Message, user: int, reason: str = MISSING):
    """
    Unbans a user from the server.
    """
    banned_users = ctx.channel.guild.bans()
    user_to_unban = None

    async for ban_entry in banned_users:
        if ban_entry.user.id == user:
            user_to_unban = ban_entry.user
            break

    if not user_to_unban:
        return 1  # User not found in the banned list

    await ctx.channel.guild.unban(user_to_unban, reason=reason)

    return user_to_unban.id

async def dshell_kick_member(ctx: Message, member: int, reason: str = MISSING):
    """
    Kicks a member from the server.
    """
    kicked_member = ctx.channel.guild.get_member(member)

    if not kicked_member:
        return 1  # Member not found in the server

    await ctx.channel.guild.kick(kicked_member, reason=reason)

    return kicked_member.id

async def dshell_rename_member(ctx: Message, new_name, member=None):
    """
    Renames a member in the server.
    """
    renamed_member = ctx.channel.guild.get_member(member)

    if not renamed_member:
        return 1  # Member not found in the server

    await renamed_member.edit(nick=new_name)

    return renamed_member.id