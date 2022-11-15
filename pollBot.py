import discord
from discord.ext import commands
import logging
import aiohttp
import csv
import random


extensions = (
    "cogs.meta", 
    )

class PollBot(commands.AutoShardedBot):
    def __init__(self, config):
        prefixes = ["+", "poll:", "Poll:", "POLL:"]
        self.emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]

        self.maxGames = 16
        self.emojiList = {
            "Black Dragons"       : "<:BD:1036742528139006012>",
            "BDS"                 : "<:BDS:1036742529175003176>",
            "CAG"                 : "<:CAG:1036742530601058314>", 
            "Dire Wolves"         : "<:DW:1036742531897114714>",
            "Faze"                : "<:FAZE:1036742533021184050>",
            "Fury"                : "<:FURY:1036742534241722580>",
            "Heroic"              : "<:HEROIC:1036752991820202025>",
            "Team Liquid"         : "<:LIQUID:1036742536242397225>",
            "MNM"                 : "<:MNM:1036742537920118794>",
            "Mirage"              : "<:MRG:1036750082906783784>",
            "Sandbox Gaming"      : "<:SBXG:1036742540860346368>",
            "Soniqs"              : "<:SQ:1036742542731001907>",
            "Spacestation Gaming" : "<:SSG:1036742544387752027>",
            "TSM FTX"             : "<:TSM:1036750106667524217>",
            "W7M"                 : "<:W7M:1036742546971430993>",
            "Wolves"              : "<:WOLVES:1036742548405882920>"
        }


        self.team1 = []
        self.team2 = []
        super().__init__(
            command_prefix = prefixes,
            status = discord.Status.online,
            activity = discord.Game(name = "+help"))
        self.config = config
        self.shard_count = self.config["shards"]["count"]
        shard_ids_list = []
        shard_ids = []
        
        # create list of shard ids
        for i in range(self.config["shards"]["first_shard_id"], self.config["shards"]["last_shard_id"]+1):
            shard_ids_list.append(i)
        self.shard_ids = tuple(shard_ids_list)

        self.remove_command("help")
        self.messages = []
        
        for extension in extensions:
            self.load_extension(extension)

    # parses the title, which should be in between curly brackets ('{ title }')
    def find_title(self, message):
        # this is the index of the first character of the title
        first = message.find('{') + 1
        # index of the last character of the title
        last = message.find('}')
        if first == 0 or last == -1:
            return "Not using the command correctly"
        return message[first:last]

    def output_poll(self, title):
        fileName = "matches//" + title + ".csv"
        file     = open(fileName, "r")
        i = 1
        for row in file:
            r = row.split(',')
            self.team1.append(r[0])
            self.team2.append(r[1].strip())
        print(self.team1)
        print(self.team2)
        file.close()


    

    async def on_ready(self):
        self.http_session = aiohttp.ClientSession()
        print("Poll Bot Online")
        print("---------------")


    async def on_message(self, message):
        if message.content.startswith("+poll"):
            messageContent = message.clean_content
            if messageContent.find("{") == -1:
                await message.add_reaction(self.emojiLetters[0])
                await message.add_reaction(self.emojiLetters[1])
            else:
                title = self.find_title(messageContent)
                
                if title[0:3] == "Day" or title[0:3] == "day" :
                    self.output_poll(title)
                    j = 1
                    while j <= self.maxGames:
                        pollMessage = ""
                        options = []
                        i = 0;
                        options.append(self.team1[j-1])
                        options.append(self.team2[j-1])
                        teamA = self.team1[j-1]
                        teamB = self.team2[j-1]

                        print ("TEAM A: "+teamA)
                        print ("TEAM B: "+teamB)
                        for choice in options:
                            if not options[i] == "":
                                if len(options) > 21:
                                    await message.channel.send("Please make sure you are using the command correctly and have less than 21 options.")
                                    return
                                elif not i == len(options):
                                    if i %2 == 0:
                                        pollMessage = pollMessage + "\n\n" + self.emojiList[teamA] + " " + choice
                                    else :
                                        pollMessage = pollMessage + "\n\n" + self.emojiList[teamB] + " " + choice
                            i += 1

                        boxTitle = "**" + "Game " + str(j) + ": " + self.team1[j-1] + " vs " + self.team2[j-1] + "**"
                        '''
                        White Blue : 0x3D7390
                        Dark Blue  : 0x03202F
                        Mid Blue   : 0x066177
                        '''
                        if (j%3 == 1):
                            color = 0x3D7390 # game 1 
                        elif (j%3 == 2): 
                            color = 0x066177 # game 2
                        elif (j%3 == 0):
                            color = 0x03202F # game 3
                        e = discord.Embed(title=boxTitle, description=pollMessage, colour=color)
                        pollMessage = await message.channel.send(embed=e)
                        self.messages.append(pollMessage)


                        i = 0

                        final_options = []  # There is a better way to do this for sure, but it also works that way
                        j += 1

                        for choice in options:
                            if not i == len(options) and not options[i] == "":
                                if i % 2 == 0:
                                    final_options.append(choice)
                                    await pollMessage.add_reaction(self.emojiList[teamA])
                                else:
                                    final_options.append(choice)
                                    await pollMessage.add_reaction(self.emojiList[teamB])
                                i += 1
                    e = discord.Embed(title = "Matches generated!\nYou can now vote!", colour = 0xFFD700)
                    await message.channel.send(embed=e)
                    print ("[")
                    for msg in self.messages:
                        print (msg.id)
                        print (',')
                    print ("]")
                        



        if message.content.startswith("+end") or message.content.startswith("+exit"):
            await message.channel.send("Bot's going offline!")
            exit()


    def run(self):
        super().run(self.config["discord_token"], reconnect=True)
