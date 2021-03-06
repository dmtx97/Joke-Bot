import discord
from discord.ext import commands
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List
import random
import asyncio
import json
from ..user import User

class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        with open("guild_members.json", "r+") as f:
            data = json.loads(f.read())

            if member.discriminator in data:
                pass

            else:
                new_user = User(member.name, member.id, [])
                user_dict = {member.discriminator : new_user.to_dict()}
                data.update(user_dict)
                f.seek(0)
                json.dump(data, f, indent=4, sort_keys=False)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if reaction.message.author.id == bot.user.id and reaction.emoji == '⭐':
            
            message = str(reaction.message.content)
            joke_preview = ""

            with open("guild_members.json", "a+") as f:

                data = json.loads(f)

                if "Joke ID:" in message:
                    date_saved = datetime.today().strftime("%m/%d/%Y")
                    joke_id = message.partition("Joke ID: ")[2]
                    joke_id = int(joke_id)
                    joke_preview += message[0:23] + "..."

                    if len(message) <= 23:
                        joke_preview += message

                    #check if user discriminator is in the json file and if he/she already has the joke saved
                    if user.discriminator in data and joke_id not in data[user.discriminator]["jokes"].values():
                        data[user.discriminator]['jokes'].append({"joke_id" : str(joke_id), "joke_preview" : joke_preview, "date_saved" : str(date_saved) })
                        json.dump(data, f, indent=4, sort_keys=False)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        if reaction.message.author.id == bot.user.id and reaction.emoji == '⭐':
            message = str(reaction.message.content)

            with open("guild_members.json", "a+") as f:
                data = json.loads(f)

                if "Joke ID:" in message:
                    joke_id = message.partition("Joke ID: ")[2]
                    joke_id = int(joke_id)

                    if(user.discriminator in data):
                        for content in data[user.discriminator]["jokes"]:
                            if joke_id in content.values():
                                data[user.discriminator]["jokes"].remove(content)
                                f.seek(0)
                                json.dump(data, f, indent=4, sort_keys = False)

    @commands.command()
    async def listfavs(self, ctx, member = discord.Member):

        embed = discord.Embed(
            title = "{}'s Saved Jokes".format(member.name),
            description = "Below is a preview of the jokes that you have saved.",
            colour = discord.Colour.dark_purple()
        )

        dis = member.discriminator

        with open("guild_members.json", "r+") as f:
            guild_data = json.loads(f.read())
            user_dict = guild_data[dis]

            joke_id = ""
            joke_preview = ""
            date_saved = ""
            for saved_jokes in user_dict['jokes']:
                joke_id += saved_jokes["joke_id"] + '\n'
                joke_preview += saved_jokes["joke_preview"] + '\n'
                date_saved += saved_jokes["date_saved"] + '\n'

            embed.add_field(name = "Joke ID", value = joke_id, inline = True)
            embed.add_field(name = "Joke Preview", value = joke_preview, inline = True)
            embed.add_field(name = "Date Saved", value = date_saved, inline = True)
            embed.set_footer(text = "To view the full joke, use command !telljoke followed with the joke ID separated by a space.")

        await bot.send(embed = embed)

def setup(bot):
    bot.add_cog(Member(bot))