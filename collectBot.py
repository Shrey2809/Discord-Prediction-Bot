import discord
from discord.ext import commands
import logging
import aiohttp
import csv
import random
import pandas as pd

extensions = (
    "cogs.meta", 
    )


class CollectReactions(commands.AutoShardedBot):

    def __init__(self, config):

        self.emojiList = {
            "<:BD:1036742528139006012>"    :  "BD",
            "<:BDS:1036742529175003176>"   :  "BDS",
            "<:CAG:1036742530601058314>"   :  "CAG",
            "<:DW:1036742531897114714>"    :  "DW",
            "<:FAZE:1036742533021184050>"  :  "FAZE",
            "<:FURY:1036742534241722580>"  :  "FURY",
            "<:HEROIC:1036752991820202025>":  "HEROIC",
            "<:LIQUID:1036742536242397225>" :  "LIQUID",
            "<:MNM:1036742537920118794>"   :  "MNM", 
            "<:MRG:1036750082906783784>"   :  "MRG",
            "<:SBXG:1036742540860346368>"  :  "SBXG",
            "<:SQ:1036742542731001907>"    :  "SQ",
            "<:SSG:1036742544387752027>"   :  "SSG",
            "<:TSM:1036750106667524217>"   :  "TSM",
            "<:W7M:1036742546971430993>"   :  "W7M",
            "<:WOLVES:1036742548405882920>":  "WOL"
        }


        prefixes = ["+", "poll:", "Poll:", "POLL:"]
        self.fname = "SixSwedenMajor2022\\Day1.csv"
        self.channelID = 840243454537891851
        self.messageIDs = [1010617598033023006]
        self.first_game = 5
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

        self.superSet   = set()
        self.teamUsersA = []
        self.teamUsersB = []
        self.outputList = []
        
        for extension in extensions:
            self.load_extension(extension)


    def find_title(self, message):
        # this is the index of the first character of the title  
        first = message.find('{') + 1
        # index of the last character of the title
        last = message.find('}')
        if first == 0 or last == -1:
            return "Not using the command correctly"
        return message[first:last]


    async def on_ready(self):
        client = discord.Client()
        self.http_session = aiohttp.ClientSession()
        print("Reaction Collection Bot Online")
        print("------------------------------")

        
    async def on_message(self, message):
        if message.content.startswith("+end") or message.content.startswith("+exit") or message.content.startswith("+e"):
            e = discord.Embed(title="Bot's going offline", description="Offline now!", colour=0x006AA8)
            await message.channel.send(embed=e)
            exit()

        if message.content.startswith("+cr"):
            task  = message.content[4:]
            i     = int(task)
            print (self.messageIDs[i-1])
            messageID = self.messageIDs[i-1]
            print("Game " + str(i))
            msg = await message.channel.fetch_message(messageID)
            j=0
            
            for reaction in msg.reactions:
                reactionStr = str(reaction)
                
                if j == 0:
                    if reactionStr in self.emojiList.keys():
                        teamAName = self.emojiList[reactionStr]
                    else:
                        teamAName = "A"
                elif j == 1:
                    if reactionStr in self.emojiList.keys():
                        teamBName = self.emojiList[reactionStr]
                    else:
                        teamBName = "B"

                users = set()
                async for user in reaction.users():
                    users.add(user.name)

                if j == 0:
                    teamAList = list(users)
                    teamCount = len(teamAList)
                elif j == 1:
                    teamBList = list(users)
                    teamCount = len(teamBList)

                teamCount = teamCount - 1
                print (reactionStr + ' has count: ' + str(teamCount))
                j+=1


            df = pd.read_csv(self.fname)
            self.superSet = df.columns
            for column in df.columns:
                if not column == "----":
                    if column in teamBList and column in teamAList:
                        self.outputList.append("N/A")
                    elif column in teamBList:
                        self.outputList.append(teamBName)
                    elif column in teamAList:
                        self.outputList.append(teamAName)
                    else:
                        self.outputList.append("N/A")

            await message.channel.send("Game is now closed")

            self.outputList.append("MATCH " + str(i))

            with open(self.fname, 'a', encoding='UTF8', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(self.outputList)
                self.outputList.clear()

            df = pd.read_csv(self.fname)
            for user in teamAList:
                if user not in df.columns:
                    print (user + " Not in overall list - voted for team " + teamAName)

            for user in teamBList:
                if user not in df.columns:
                    print (user + " Not in overall list - voted for team " + teamBName)  

        if message.content.startswith("+build"):
            for messageID in self.messageIDs:
                msg = await message.channel.fetch_message(messageID)
                for r in msg.reactions:
                    users = set()
                    async for user in r.users():
                        users.add(user.name)
                    self.superSet = set.union(self.superSet, users)
            setOfUsers = list(self.superSet)
            setOfUsers.append('----')
            with open(self.fname, 'w', encoding='UTF8', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(setOfUsers)

            e = discord.Embed(title="List built!", description="List built", colour=0x006AA8)
            await message.channel.send(embed=e)

    def run(self):
        super().run(self.config["discord_token"], reconnect=True)
            








