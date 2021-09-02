import discord, os, json, datetime, random, string, cryptocompare, time, asyncio
from shell import MainShell
from platform import system
from math import *
from prettify import *

# TODO LIST

class MyClient(discord.Client):
    async def on_ready(self):
        print('[.] Logged on as ' + str(self.user))
        print("[!] BOT READY TO USE")
        self.seasonChannel = client.get_channel(882602976303263764)

    def startup(self):
        self.prefix = "."
        self.currency = "$"
        self.databasePath = os.path.join(os.getcwd(), "database.json")
        self.autosaveInterval = 1800
        self.seasonLenght = 14*24*60*60 # 14 days (2 weeks)
        self.database = self.loadDB()
        self.shell = MainShell(self.prefix, self.currency, self.databasePath, self.autosaveInterval, self.seasonLenght)

    def loadDB(self):
        if not os.path.exists(self.databasePath):
            print("[!] Database not found, creating a new one...")
            database = {"user":{}, "market":{"usedIDs":[]}, "heists":{}, "seasonStart":round(time.time()), "races":{}}
            f = open(self.databasePath, 'w')
            f.write(json.dumps(database, sort_keys=True, indent=4))
            f.close()
        else:
            f = open(self.databasePath, 'r')
            database = json.loads(f.read())
            f.close()
        print("[.] Database was successfully loaded")
        return database

    def saveDB(self):
        f = open(self.databasePath, 'w')
        f.write(json.dumps(self.database, sort_keys=True, indent=4))
        f.close()

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith(self.prefix):
            #print("START: ", self.database["seasonStart"])
            #print("LENGHT:", self.seasonLenght)
            if time.time()-self.database["seasonStart"] >= self.seasonLenght:
                print("[!] New season is here!")
                embed = discord.Embed(title="🏆 Season Placements 🏆", description="Here are the TOP 5 players of this season:", color=0xFFFB00)
                embed.set_thumbnail(url="https://cdn.wallpapersafari.com/84/62/jo31gr.jpg")
                unsorted = []
                for user in self.database["user"]:
                    unsorted.append(self.database["user"][user])
                    unsorted[-1]["id"] = int(user)
                sort = sorted(unsorted, key = lambda i: i["balance"])
                leaderBoard = []
                for x in range(len(sort)):
                    i = len(sort)-(x+1)
                    leaderBoard.append(sort[i])
                richTable = ""
                for i in range(len(leaderBoard)):
                    if i < 5:
                        if i == 0:
                            prefix = "🥇"
                        elif i == 1:
                            prefix = "🥈"
                        elif i == 2:
                            prefix = "🥉"
                        elif i == 3:
                            prefix = "🏅"
                        elif i == 4:
                            prefix = "🎖️"
                        richTable += prefix+ " **"+ leaderBoard[i]["name"] + "** - " + nice_price(leaderBoard[i]["balance"], True, 1) + " " + self.currency+"\n"
                embed.description += "\n\n"+richTable[:-1]
                database = {"user":{}, "market":{"usedIDs":[]}, "heists":{}, "seasonStart":round(time.time()), "races":{}}
                f = open(self.databasePath, 'w')
                f.write(json.dumps(database, sort_keys=True, indent=4))
                f.close()
                await self.seasonChannel.send(embed=embed)
            command = message.content.lower().replace("-", "")[len(self.prefix):].split(" ")
            resp = await self.shell.process(command, message, self.database, client)
            if resp != None:
                self.database = resp

if __name__ == "__main__":
    client = MyClient()
    client.startup()
    token = "NzM1NDk1MTEyMjM4NTYzMzI4.XxhFMw.Wr4VmwFAHsFpArhKetC2wnKf34c"
    if token == "":
        if str(system()).lower() == "windows":
            path = "C:\\Program Files\\DarkDealer\\token.tk"
        else:
            path = "/Library/DarkDealer/token.tk"
        f = open(path, 'r')
        token = f.read()
        f.close()
    try:
        client.run(token, bot=True)
    except Exception as e:
        print("Error:", str(e))
    client.saveDB()