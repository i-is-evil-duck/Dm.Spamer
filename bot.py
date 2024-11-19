import discord
from discord.ext import commands
import asyncio
import random
import json

intents = discord.Intents.all()
intents.messages = True
intents.members = True

with open('tokens.json', 'r') as f:
    tokens_data = json.load(f)

def generate_invite_link(client_id):
    permissions = 8  # This represents the 'administrator' permission, change if necessary
    return f"https://discord.com/oauth2/authorize?client_id={client_id}&scope=bot&permissions={permissions}"

async def run_bot(token, client_id=None):
    bot = commands.Bot(command_prefix="^", intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} - Ready to send DMs!')

    @bot.command()
    async def dm(ctx, count: int, users: str, *, message: str):
        """
        Sends a direct message to multiple users with random delays.
        
        Syntax: ^dm [count] [@user1,@user2,...] [message]
        Example: ^dm 5 @user1,@user2 Hello, how are you?
        """
        try:
            await ctx.message.add_reaction("✅")

            user_mentions = users.split(',')
            users_list = []

            for user_mention in user_mentions:
                user_mention = user_mention.strip()
                user = discord.utils.get(ctx.guild.members, mention=user_mention)
                if user:
                    users_list.append(user)
                else:
                    await ctx.send(f"Couldn't find user: {user_mention}")
                    return

            for user in users_list:
                for _ in range(count):
                    personalized_message = message.replace("{username}", user.name)
                    await user.send(personalized_message)
                    delay = random.randint(1, 10)
                    await asyncio.sleep(delay)

        except Exception as e:
            await ctx.send(f"Failed to send message: {e}")

    await bot.start(token)

async def main():
    tasks = []
    invite_links = []
    
    for bot_data in tokens_data:
        token = bot_data["token"]
        client_id = bot_data.get("client_id")

        if client_id:
            invite_link = generate_invite_link(client_id)
            invite_links.append(invite_link)

        tasks.append(run_bot(token, client_id))

    if invite_links:
        with open("invite.txt", "w") as file:
            for link in invite_links:
                file.write(link + "\n")
            print("Invite links saved to invite.txt")

    await asyncio.gather(*tasks)

asyncio.run(main())
