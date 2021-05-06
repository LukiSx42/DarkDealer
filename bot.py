import discord, os, json, datetime, random, string, cryptocompare
from time import time
from platform import system
from math import *

# TODO LIST
# Redo growing plants database thing so bot = faster (big project)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as ' + str(self.user))

    def nice_number(self, num):
        final = ""
        indx = 0
        for char in str(num)[::-1]:
            indx += 1
            if indx % 3 != 0:
                final += char
            else:
                final += char+" "
        final = final[::-1]
        if final.startswith(" "):
            final = final[1:]
        return final

    def startup(self):
        self.prefix = "."
        self.currency = "$"
        self.databasePath = os.path.join(os.getcwd(), "database.json")
        self.autosaveInterval = 1800
        self.lastSave = time()
        self.database = self.loadDB()
        self.fullName = {"pot":":potted_plant: Flower Pot", "led":":bulb: LED Lamp", "hid":":bulb: HID Lamp", "dryer":":control_knobs: Electric Dryer", "ruderalis":":seedling: Ruderalis seeds", "indica":":seedling: Indica seeds", "microscope":":microscope: Microscope", "meth":":cloud: Crystal Meth Powder", "cocaine":":cloud: Cocaine Powder", "heroin":":cloud: Heroin Powder", "amp":":cloud: Amphetamine Powder", "mixer":":sake: Mixer", "wash":":soap: Washing Powder", "soda":":fog: Baking Soda", "sugar":":ice_cube: Sugar", "amf":":cloud: Amfetamin", "grape":":grapes: Grape Sugar", "gun":":gun: Gun", "a11":":hammer_pick: A11", "a10":":hammer_pick: A10", "a9":":hammer_pick: A9", ":pick: 3090rig":":pick: 3090rig", "3080rig":":pick: 3080rig", "3070rig":":pick: 3070rig", "2080rig":":pick: 2080rig", "2070rig":":pick: 2070rig", "filter":":dash: Air Filter", "basket":":basket: Wooden Basket"}
        self.drugName = {"wetweed":":shamrock: Wet Weed", "weed":":herb: Weed", "meth":":cloud: Crystal Meth", "cocaine":":cloud: Cocaine", "heroin":":cloud: Herion", "amp":":cloud: Amphetamine", "sugar":":ice_cube: Sugar", "amf":":cloud: Amfetamin", "mdma":":pill: Ecstasy", "saucer":":mushroom: Flying Saucer Mushroom", "knobby":":mushroom: Knobby Tops", "bohemica":":mushroom: The Bohemian Psilocybe"}
        self.description = {"pot":"A flower pot, used to grow weed. (id => `pot`)", "led":"Cheap and not power efficient lamp. (750W) (id => `led`)", "hid":"High quality and power efficient lamp. (500W) (id => `hid`)", "dryer":"A better way to dry weed, gives you 20% more weed. (id => `dryer`)", "ruderalis":"Avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", "indica":"Grat seeds, slow growth, 30g per plant. (id => `indica`)", "microscope":"Used to analyze drugs. (id => `microscope`)", "meth":"1g powder ==> 4g crystal meth (id => `meth`)", "cocaine":"1g powder ==> 3g cocaine (id => `cocaine`)", "heroin":"1g powder ==> 4g herion (id => `heroin`)", "amp":"1g powder ==> 5g amphetamine (id => `amp`/`amphetamine`)", "mixer":"Needed to mix drugs. (id => `mixer`)", "sugar":"Used to mix drugs with. (id => `sugar`)", "wash":"Used to mix drugs with. (id => `wash`)", "soda":"Used to mix drugs with. (id => `soda`)", "amf":"1g amfetamin ==> 5g mdma (id => `amf`)", "grape":"Needed to produce MDMA (id => `grape`)", "gun":"You can rob with this thing (id => `gun`)", "a11":"You can mine bitcoin with this. (id => `a11`)", "a10":"You can mine bitcoin with this. (id => `a10`)", "a9":"You can mine bitcoin with this. (id => `a9`)", "3090rig":"You can mine ethereum with this. (id => `3090rig`)", "3080rig":"You can mine ethereum with this. (id => `3080rig`)", "3070rig":"You can mine ethereum with this. (id => `3070rig`)", "2080rig":"You can mine ethereum with this. (id => `2080rig`)", "2070rig":"You can mine ethereum with this. (id => `2070rig`)", "filter":"This boosts your weed growth. (id => `filter`)", "basket":"A better way to collect shrooms. (id => `basket`)"}
        self.drugDescription = {"wetweed":"You need to dry wet weed to turn it into sellable weed", "weed":"The green stuff", "meth":"White powder with good effects", "cocaine":"The most expensive drug", "heroin":"The more serious drug", "amp":"So you wanna be fast?", "mdma":"Relaxing pills", "saucer":"The most rare magic mushroom out there. (id => `saucer`)", "knobby":"Expensive and rare shroom. (id => `knobby`)", "bohemica":"The most common magic mushroom (id => `bohemica`)"}
        self.drugLvls = {"1":["weed", "amp"], "10":["meth", "saucer", "knobby", "bohemica"], "25":["cocaine", "heroin", "mdma"]}
        self.prices = {"pot":30, "led":150, "hid":1000, "dryer":2500, "ruderalis":12, "indica":20, "microscope":2000, "meth":15, "cocaine":30, "heroin":10, "amp":7, "lab1":15000, "lab2":50000, "lab3":250000, "mixer":5000, "soda":7, "wash":2, "sugar":5, "amf":25, "gun":1000, "a11":20000, "a10":15000, "a9":10000, "3090rig":20000, "3080rig":12000, "3070rig":10000, "2080rig":7500, "2070rig":5000, "filter":3000, "basket":500}
        self.miners = {"asic":{"a11":20000, "a10":15000, "a9":10000}, "gpu":{"3090rig":20000, "3080rig":12000, "3070rig":10000, "2080rig":7500, "2070rig":5000}}
        self.hashRate = {"a11":5000, "a10":3500, "a9":1500, "3090rig":10000, "3080rig":7500, "3070rig":6000, "2080rig":5000, "2070rig":3500}
        self.producmentTime = {"meth":540, "cocaine":1200, "herion":660, "amp":600, "mdma":600}
        self.produceReward = {"meth":4, "cocaine":3, "herion":4, "amp":5, "mdma":5}
        self.substances = {"soda":10, "wash":0, "sugar":5}
        self.notProduceable = ["weed", "wetweed", "saucer", "knobby", "bohemica"]
        self.shrooms = {"saucer":1, "knobby":7, "bohemica":25}
        self.buildings = {
            "house":[
                {"type":"Small appartment", "name":"Starter appartment", "size":2, "electricity":0.4, "price":30000, "id":"smallappartment"},
                {"type":"Medium appartment", "name":"Friends place", "size":5, "electricity":0.35, "price":80000, "id":"mediumappartment"},
                {"type":"Large appartment", "name":"A more luxurious appartment", "size":10, "electricity":0.35, "price":150000, "id":"largeappartment"},
                {"type":"Small house", "name":"Grandma's small house", "size":25, "electricity":0.4, "price":200000, "id":"smallhouse"},
                {"type":"Medium house", "name":"Avarge house", "size":35, "electricity":0.35, "price":300000, "id":"mediumhouse"},
                {"type":"Large house", "name":"Nice and big house", "size":65, "electricity":0.3, "price":500000, "id":"largehouse"},
                {"type":"Medium mansion", "name":"A fucking mansion!", "size":80, "electricity":0.35, "price":1000000, "id":"mediummansion"},
                {"type":"Large mansion", "name":"Now this is just flex...", "size":110, "electricity":0.3, "price":2500000, "id":"largemansion"}],
            "warehouse":[
                {"type":"Mini warehouse", "name":"Friend's garage", "size":20, "electricity":0.2, "price":20000, "id":"miniwarehouse"},
                {"type":"Small warehouse", "name":"Abadoned warehouse", "size":100, "electricity":0.2, "price":100000, "id":"smallwarehouse"},
                {"type":"Medium warehouse", "name":"A regular warehouse", "size":500, "electricity":0.15, "price":750000, "id":"mediumwarehouse"},
                {"type":"Large warehouse", "name":"A nice big place to grow stuff", "size":1250, "electricity":0.15, "price":1500000, "id":"largewarehouse"},
                {"type":"Mega warehouse", "name":"Now this is a warehouse!", "size":5000, "electricity":0.15, "price":4000000, "id":"megawarehouse"},
                {"type":"Sebko warehouse", "name":"This is a warehouse owned only by sebko himself!", "size":25000, "electricity":0.20, "price":10000000, "id":"sebkowarehouse"}],
            "lab":[
                {"type":"Small lab", "name":"Friend's kitchen", "size":5, "electricity":0.35, "price":15000, "id":"smalllab"},
                {"type":"Medium lab", "name":"Normal chemical lab", "size":15, "electricity":0.3, "price":50000, "id":"mediumlab"},
                {"type":"Large lab", "name":"Modern lab", "size":40, "electricity":0.3, "price":125000, "id":"largelab"},
                {"type":"XL lab", "name":"Large modern lab", "size":100, "electricity":0.25, "price":250000, "id":"xllab"},
                {"type":"XXL lab", "name":"This is science!", "size":250, "electricity":0.25, "price":500000, "id":"xlllab"},
                {"type":"Mega lab", "name":"This is ULTRA science!", "size":500, "electricity":0.25, "price":1000000, "id":"megalab"},
                {"type":"Ultimate lab", "name":"This is ULTIMATE science!", "size":1000, "electricity":0.20, "price":5000000, "id":"ultimatelab"}]}
        self.starterHouse = self.buildings["house"][0]
        self.buildingDB = {}
        for buildingType in self.buildings:
            for building in self.buildings[buildingType]:
                building["btype"] = buildingType
                self.buildingDB[building["id"]] = building
        self.sellPrice = {"weed":8, "amp":10, "meth":12, "heroin":15, "cocaine":45, "mdma":15, "saucer":150, "knobby":30, "bohemica":15}
        self.cooldowns = {"dealRefresh":300, "labBoost":120, "ruderalis":600, "indica":900, "police":300, "heist":600, "msg":2, "woods":300, "saucer":2400, "knobby":1800, "bohemica":1200, "gang":3600}
        self.cryptoName = {"BTC":"Bitcoin", "ETH":"Ethereum", "LTC":"Litecoin", "DOGE":"Dogecoin"}
        self.cryptos = ["BTC", "ETH", "LTC", "DOGE"]
        self.electricityMultiplayer = 1.5
        self.jobs = {"windowcleaner":(120, 500), "youtuber":(60, 400), "programmer":(600, 5000), "mafian":(1800, 25000)}
        self.VIP = ["151721375210536961", "682644855713038384", "264127862498525186", "670545442307702794", "794223995691991052"]
        self.tips = [
            (":potted_plant: Growing Weed Tip", "Warehouses are better than a reagular house, you can list all warehouses with `"+self.prefix+"shop buildigs warehouse` and buy any warehouse with `"+self.prefix+"buy WAREHOUSE`"),
            (":potted_plant: Drying Weed Tip", "You can buy a `dryer` to get 20%+ weed when you dry it."),
            (":potted_plant: Growing Weed Tip", "You can buy a `filter` (air filter) to make your weed grow faster."),
            (":lab_coat: Lab Tip", "You can buy a `lab1`/`lab2`/`lab3` upgrade for your lab to boost your production."),
            (":money: Mining Crypto Tip", "You can buy crypto miners from `mine` shop, then install them in your house with `"+self.prefix+"mine add MINER`"),
            (":electric_plug: Electricity Tip", "You can sell your `LED` lamps and buy `HID` which will not only save you a lot of money, buy also boost your weed growth"),
            (":mushroom: Magic Mushrooms Tip", "You can go to the woods and collect magic mushroom with `.woods`")]
        print("BOT IS READY")

    def loadDB(self):
        if not os.path.exists(self.databasePath):
            print("Database not found, creating a new one...")
            database = {"user":{}, "market":{"usedIDs":[]}, "heists":{}}
            f = open(self.databasePath, 'w')
            f.write(json.dumps(database, sort_keys=True, indent=4))
            f.close()
        else:
            f = open(self.databasePath, 'r')
            database = json.loads(f.read())
            f.close()
        return database

    def saveDB(self):
        f = open(self.databasePath, 'w')
        f.write(json.dumps(self.database, sort_keys=True, indent=4))
        f.close()
    
    def mixQuality(self, q):
        if q <= 50:
            return "horible"
        elif q <= 60:
            return "bad"
        elif q <= 70:
            return "ok"
        elif q <= 80:
            return "good"
        elif q <= 90:
            return "very good"
        else:
            return "excelent"

    def newDeals(self, user, new=False, drug=None, amount=5):
        drugs = self.drugLvls["1"]
        if not new:
            if self.database["user"][user]["lvl"] >= 10:
                for d in self.drugLvls["10"]:
                    drugs.append(d)
            if self.database["user"][user]["lvl"] >= 25:
                for d in self.drugLvls["25"]:
                    drugs.append(d)
        if drug != None:
            if drug in drugs:
                drugs = [drug]
            else:
                return None
        deals = []
        for _ in range(amount):
            deal = {"drug":random.choice(drugs), "quality":random.randint(50, 100)}
            deals.append(deal)
        return deals

    def marketID(self):
        id = "&"+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))
        while id in self.database["market"]["usedIDs"]:
            id = "&"+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))+random.choice(list(string.ascii_lowercase))
        self.database["market"]["usedIDs"].append(id)
        return id

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith(self.prefix):
            t = time()
            if str(message.author.id) not in self.database["user"]:
                await message.channel.send("Hey "+message.author.name+", I see that you are new aroud here. If you want to learn some tips and tricks check this out `"+self.prefix+"help tutorial`")
                self.database["user"][str(message.author.id)] = {"name":message.author.name, "balance":1000, "house":self.starterHouse, "warehouse":None, "lab":None, "upgrades":{"lab":0}, "inventory":{"items":{}, "drugs":{"pure":{}, "mixes":[]}}, "lvl":1, "job":None, "lastJob":0, "growing":[], "producing":[], "electricity":0, "lastBill":round(time()), "deals":self.newDeals(str(message.author.id), True), "dealRefresh":round(time()), "police":{"prison":False, "expire":round(time())}, "crypto":{}, "lastHeist":0, "mining":[], "lastMsg":round(time()), "woodsTime":0, "gang":None, "prestige":1}
            if self.database["user"][str(message.author.id)]["lastMsg"]+self.cooldowns["msg"] > time() and str(message.author.id) not in self.VIP:
                t = self.database["user"][str(message.author.id)]["lastMsg"]+self.cooldowns["msg"]-time()
                await message.channel.send(message.author.mention+" Woah, slow down, you need to wait **"+str(round(t))+" seconds** to send another command")
                return
            if self.database["user"][str(message.author.id)]["lastBill"]+86400 < time():
                self.database["user"][str(message.author.id)]["balance"] -= self.database["user"][str(message.author.id)]["electricity"]*self.electricityMultiplayer
                self.database["user"][str(message.author.id)]["electricity"] = 0
                self.database["user"][str(message.author.id)]["lastBill"] = round(time())
            if self.database["user"][str(message.author.id)]["police"]["prison"]:
                if self.database["user"][str(message.author.id)]["police"]["expire"] < time():
                    await message.channel.send(message.author.mention+" You ware just released from prison, be careful next time...")
                    self.database["user"][str(message.author.id)]["police"]["prison"] = False
                else:
                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][str(message.author.id)]["police"]["expire"]-time()))).split(":")
                    for i in range(len(remaining)):
                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                            remaining[i] = remaining[i][1:]
                    embed = discord.Embed(title="Prison", description="**"+message.author.name+" you ware caught!**\n\n**Released in:** "+str(remaining[0])+" hours "+str(remaining[1])+" minutes "+str(remaining[2])+" seconds", color=discord.Color.blue())
                    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Patch_of_the_New_York_City_Police_Department.svg/1200px-Patch_of_the_New_York_City_Police_Department.svg.png")
                    await message.channel.send(embed=embed)
                    return
            if self.lastSave+self.autosaveInterval < time():
                self.saveDB()
                self.lastSave = time()
            command = message.content.lower().replace("-", "")[len(self.prefix):].split(" ")
            if command[0] == "ping":
                await message.channel.send("Pong!")
            elif command[0] == "help":
                if len(command) != 2:
                    embed = discord.Embed(title="Dark Dealer Help Menu", description="Here is a simple help menu", color=discord.Color.light_gray())
                    embed.add_field(name=":video_game: Basic game info", value="`"+self.prefix+"help info`", inline=True)
                    embed.add_field(name=":gear: List of commands", value="`"+self.prefix+"help commands`", inline=True)
                else:
                    if command[1] == "info":
                        embed = discord.Embed(title="Dark Dealer Info", description="Some informations about the game", color=discord.Color.light_gray())
                        embed.add_field(name=":satellite: Basic Info", value="This is a drug dealing game, you start by selling marijuana (weed) and amphetamine (speed), weed sells at 8 $ per gram and amp sells at 10 $ per gram.", inline=False)
                        embed.add_field(name=":electric_plug: Power", value="Yes, there is electricity in this game (you need to pay your bills). Some equipment (lamps, labs...) have a electricity consumption (in watts), you pay the bill automaticly each 24hours IRL. And yes you can go into negatives, so be careful how much money you have and what you can and cant afford...")
                        embed.add_field(name=":police_officer: Police", value="Cops can fine you and they can put you in prison, they can catch you if you use `.rob` or `.qicksell` if you don't want to get caught just awoid these 2 commands.", inline=False)
                        embed.add_field(name=":herb: Growing Weed", value="So the first step in making money, growing the green stuff. You can grow weed anywhere, but not in your lab. Each house/appartment/warehouse has a different size (capacity) of the amount of plants you can grow there, biger house => more plants => more money. Firstly you need a regular flower pot, its easy to get, but you need to buy it from the online weed shop, then you need to get a lamp (better lamp => less power cusumtion + faster weed growth) and you need to get the actual seeds (from the weed shop too), finaly you need to start growing them (this will take 1day and 6hours with the cheapest lighting). Be careful where you live and where you grow your weed, you attract more police attention and can be swatted anytime.", inline=False)
                        embed.add_field(name=":mag_right: Producing Powder Drugs", value="To produce powder drugs, firstly you need a lab starting from 15k. Then you need some powder to produce the drug from. Lastly you need to produce the drug this takes 2 IRL days without any upgrades. You can list all upgrades with the command `"+self.prefix+"upgrades <BUILDING>` then buy them with the command `"+self.prefix+"upgrade <BUILDING> <UPGRADE_LVL>`", inline=False)
                        embed.add_field(name=":dollar: Selling Drugs", value="So, selling the good stuff isn't that hard as it seems, BUT the police might be interested in participating in the deal aswell so be careful who and how you sell it to... There are 3 ways of selling drugs:\n 1. Qucksell - qucksell is the easiest and fastest method of selling drugs, but you dont make as much money here and also police are interested in investigating quicksells.\n 2. Market - On the market there are 2 ways of selling stuff: 1. Market making - you will create an player only or NPC only or both offer, it will take time before an NPC or an another player buys it (pricing will make a big difference here) 2. Market taking - You will see that some NPC's or other players are willing to buy a certain drug at certain price, you can easly fill the order and quckly finish the trade, but you will pay a 'Market taker fee' this is 5% of your profit, but there is NO police attetion when using the market.\n 3. Gang - Lastly selling to a gang is realy profitalbe sometimes, but realy risky...", inline=False)
                    elif command[1] == "tutorial":
                        embed = discord.Embed(title="Dark Dealer Tutorial", color=discord.Color.light_gray())
                        embed.add_field(name=":shopping_cart: First steps (buying)", value="First you need to buy: **pots** (`pot`), **lamps** (`led`), **seeds** (`indica`/`ruderalis`). You can buy stuff with the command `"+self.prefix+"buy ITEM`.", inline=False)
                        embed.add_field(name=":potted_plant: Growing stuff (planting weed)", value="You now can plant weed in you house using the command `"+self.prefix+"grow grow SEEDS house AMOUNT`. Example command ("+self.prefix+"grow grow indica house 2)\nYou can view your growing info with the command `"+self.prefix+"grow info`.", inline=False)
                        embed.add_field(name=":scissors: Collecting (harvesting weed)", value="When your weeds has grown, you now can harvest it with the command `"+self.prefix+"grow harvest`. Now you have **Wet Weed** which you can't sell yet, you need to dry it first with the command `"+self.prefix+"grow dry`", inline=False)
                        embed.add_field(name=":money_mouth: Making $$$ (selling)", value="Last thing you need to do is sell your weed, you can view your **drug inventory** with the command `"+self.prefix+"drugs`, now you need to **create some deals** using command `"+self.prefix+"newdeals weed`, now do `.deals` to **list** all of the **new deals**. Finaly **pick the best deal** (most $ per gram) and finish it with the command `"+self.prefix+"deals DEAL_NUMBER GRAMS`", inline=False)
                    elif command[1] in ["commands", "cmds"]:
                        embed = discord.Embed(title="Dark Dealer Commands", description="`balance`, `shops`, `shop`, `buy`, `jobs`, `job`, `work`, `inventory`, `drugs`, `buildings`, `grow`, `bills`, `levelup`, `lab`, `heist`, `levelup`, `bet`, `calcmix`, `mix`, `crypto`, `calccrypto`, `give`, `gift`, `startheist`, `joinheist`, `mine`", color=discord.Color.light_gray())
                        embed.set_footer(text="Use "+self.prefix+" before each command!")
                await message.channel.send(embed=embed)
            elif command[0] in ["tip", "tips"]:
                embed = discord.Embed(title="Dark Dealer Tips", description="Here is a random tip for the game:", color=discord.Color.dark_gray())
                tip = random.choice(self.tips)
                embed.add_field(name=tip[0], value=tip[1], inline=False)
                await message.channel.send(embed=embed)
            elif command[0] in ["balance", "bal", "money"]:
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 2 and len(message.mentions) >= 1:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                if user in self.database["user"]:
                    bal = self.nice_number(self.database["user"][user]["balance"])
                    if "." in bal:
                        bal = self.nice_number(int(bal.split(".")[0].replace(" ", "")))
                        self.database["user"][user]["balance"] = round(self.database["user"][user]["balance"])
                else:
                    bal = 0
                embed = discord.Embed(title=name+"'s balance", description="Balance: "+self.currency+" "+str(bal), color=discord.Color.green())
                await message.channel.send(embed=embed)
            elif command[0] in ["info", "profile"]:
                user = str(message.author.id)
                name = message.author.name
                avatar = message.author.avatar_url
                if len(command) == 2 and len(message.mentions) >= 1:
                    if str(message.mentions[0].id) in self.database["user"]:
                        user = str(message.mentions[0].id)
                        name = message.mentions[0].name
                        avatar = message.mentions[0].avatar_url
                embed = discord.Embed(color=discord.Color.blue())
                embed.set_author(name=name+"'s profile", icon_url=str(avatar).replace("size=1024", "size=256"))
                embed.add_field(name='Level', value=str(self.database["user"][user]["lvl"]), inline=True)
                embed.add_field(name='Balance', value=self.currency+" "+self.nice_number(self.database["user"][user]["balance"]), inline=True)
                embed.add_field(name='Prestige', value="Player is currently at prestige level "+str(self.database["user"][user]["prestige"]), inline=False)
                embed.add_field(name='Inventory', value="Player has `"+str(len(self.database["user"][user]["inventory"]["items"]))+"` different items in his inventory", inline=False)
                if self.database["user"][user]["job"] != None:
                    embed.add_field(name='Employment', value="Player is working as a "+str(self.database["user"][user]["job"]), inline=False)
                await message.channel.send(embed=embed)
            elif command[0] in ["jobs", "joblist"]:
                embed = discord.Embed(title="Job List", color=discord.Color.blue())
                embed.add_field(name=':desktop: YouTuber', value="400 "+self.currency+" per video | cooldown: 1 minute (id => `youtuber`)", inline=False)
                embed.add_field(name=':window: Window Cleaner', value="500 "+self.currency+" per clean | cooldown: 2 minutes (id => `windowcleaner`)", inline=False)
                embed.add_field(name=':desktop: Programmer', value="5000 "+self.currency+" per application | cooldown: 10 minutes (id => `programmer`)", inline=False)
                embed.add_field(name=':gun: Mafian', value="25000 "+self.currency+" per crime | cooldown: 30 minutes (id => `mafian`)", inline=False)
                embed.set_footer(text="You can apply to a job with the command `"+self.prefix+"job <JOB_ID>`")
                await message.channel.send(embed=embed)
            elif command[0] == "job":
                if len(command) != 2:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"job <JOB_ID>`")
                elif command[1] == "unemploy":
                    if self.database["user"][str(message.author.id)]["job"] != None:
                        self.database["user"][str(message.author.id)]["job"] = None
                        self.database["user"][str(message.author.id)]["lastJob"] = 0
                        await message.channel.send(message.author.mention+" You are not employed anymore")
                    else:
                        await message.channel.send("You are not employed")
                elif self.database["user"][str(message.author.id)]["job"] != None:
                    await message.channel.send(message.author.mention+" You are already working as a "+self.database["user"][str(message.author.id)]["job"]+", use `"+self.prefix+"job unemploy` to leave your current job")
                else:
                    if command[1] in self.jobs:
                        self.database["user"][str(message.author.id)]["job"] = command[1]
                        self.database["user"][str(message.author.id)]["lastJob"] = time()
                        await message.channel.send(message.author.mention+" You are now working as a "+command[1])
                    else:
                        await message.channel.send(message.author.mention+" Job with ID `"+command[1]+"` does not exist, use `"+self.prefix+"jobs` to list all available jobs and their IDs")
            elif command[0] == "work":
                job = self.database["user"][str(message.author.id)]["job"]
                if job != None:
                    reward = self.jobs[job][1]
                    cooldown = self.jobs[job][0]
                    if self.database["user"][str(message.author.id)]["lastJob"]+cooldown < time():
                        await message.channel.send(message.author.mention+" You have worked your shift and you earned "+self.nice_number(reward)+" "+self.currency)
                        self.database["user"][str(message.author.id)]["balance"] += reward
                        self.database["user"][str(message.author.id)]["lastJob"] = time()
                    else:
                        remaining = str(datetime.timedelta(seconds=round((self.database["user"][str(message.author.id)]["lastJob"]+cooldown)-time()))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        await message.channel.send(message.author.mention+" You have to wait **"+remaining[0]+" hours "+remaining[1]+" minutes "+remaining[2]+" seconds"+"** before you can work")
                else:
                    await message.channel.send(message.author.mention+" You are not employed, you can employ using `"+self.prefix+"job <JOB_ID>`")
            elif command[0] == "shops":
                embed = discord.Embed(title="Shop List", color=discord.Color.dark_grey())
                embed.add_field(name=":potted_plant: Smoky", value="Everything that your weed growing needs. (id => `smoky`/`weed`)", inline=False)
                embed.add_field(name=":apple: Fruit Shop", value="A normal legal shop. (id => `fruit`/`normal`/`legal`)", inline=False)
                embed.add_field(name=":scientist: Science Needs", value="We sell high quality lab equpment. (id => `science`/`lab`)", inline=False)
                embed.add_field(name=":mag_right: Power of Powder", value="We sell powder that can be turned into large amounts of powder drugs. (id => `powder`)", inline=False)
                embed.add_field(name=":house: Prime Location", value="We sell great apartments, warehouses, labs... (id => `location`/`buildings`/`properties`)", inline=False)
                embed.add_field(name=":pick: Miners Heaven", value="You can buy crypto miners here. (id => `miners`/`mine`)", inline=False)
                embed.set_footer(text="You can visit any shop with "+self.prefix+"shop <SHOP_ID>")
                await message.channel.send(embed=embed)
            elif command[0] == "shop":
                if len(command) == 2 or len(command) == 3:
                    if command[1] in ["smoky", "weed"]:
                        embed = discord.Embed(title=":potted_plant: Smoky", color=discord.Color.green())
                        embed.set_thumbnail(url="https://image.freepik.com/free-vector/green-neon-sign-marijuana-leaves-cannabis-logo_1268-14217.jpg")
                        embed.add_field(name=":seedling: Ruderalis seeds - "+self.nice_number(self.prices["ruderalis"])+" "+self.currency, value="Avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", inline=False)
                        embed.add_field(name=":seedling: Indica seeds - "+self.nice_number(self.prices["indica"])+" "+self.currency, value="Grat seeds, slow growth, 30g per plant. (id => `indica`)", inline=False)
                        embed.add_field(name=":potted_plant: Flower Pot - "+self.nice_number(self.prices["pot"])+" "+self.currency, value="Needed to grow weed. (id => `pot`)", inline=False)
                        embed.add_field(name=":bulb: LED Lamp - "+self.nice_number(self.prices["led"])+" "+self.currency, value="Cheap and not power efficient lamp. (750W) (id => `led`)", inline=False)
                        embed.add_field(name=":bulb: HID Lamp - "+self.nice_number(self.prices["hid"])+" "+self.currency, value="High quality and power efficient lamp. (500W) (id => `hid`)", inline=False)
                        embed.add_field(name=":control_knobs: Electric Dryer - "+self.nice_number(self.prices["dryer"])+" "+self.currency, value="A better way to dry weed, gives you 20% more weed (id => `dryer`)", inline=False)
                        embed.add_field(name=":dash: Air Filter - "+self.nice_number(self.prices["filter"])+" "+self.currency, value="This boosts your weed growth. (id => `filter`)", inline=False)
                        embed.add_field(name=":gun: Gun - "+self.nice_number(self.prices["gun"])+" "+self.currency, value="You can rob with this thing. (id => `gun`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["science", "lab"]:
                        embed = discord.Embed(title=":scientist: Science Needs", color=discord.Color.blue())
                        embed.set_thumbnail(url="https://static.wixstatic.com/media/975a90_19cac9b1df2c4257a14a33569f274dea~mv2.png/v1/fill/w_164,h_190,al_c,q_85,usm_0.66_1.00_0.01/975a90_19cac9b1df2c4257a14a33569f274dea~mv2.webp")
                        embed.add_field(name=":microscope: Microscope - "+self.nice_number(self.prices["microscope"])+" "+self.currency, value="Used to analyze drugs. (id => `microscope`)", inline=False)
                        embed.add_field(name=":sake: Mixer - "+self.nice_number(self.prices["mixer"])+" "+self.currency, value="Needed to mix drugs. (id => `mixer`)", inline=False)
                        embed.add_field(name=":microscope: Lab Equpment Upgrade 1 - "+self.nice_number(self.prices["lab1"])+" "+self.currency, value="Makes your lab produce drugs faster (1 hour boost), does NOT stack. (id => `lab1`)", inline=False)
                        embed.add_field(name=":microscope: Lab Equpment Upgrade 2 - "+self.nice_number(self.prices["lab2"])+" "+self.currency, value="Makes your lab produce drugs faster (2 hour boost), does NOT stack. (id => `lab2`)", inline=False)
                        embed.add_field(name=":microscope: Lab Equpment Upgrade 3 - "+self.nice_number(self.prices["lab3"])+" "+self.currency, value="Makes your lab produce drugs faster (3 hour boost), does NOT stack. (id => `lab3`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["fruit", "normal", "legal", "basic"]:
                        embed = discord.Embed(title=":mag_right: Fruit Shop", color=discord.Color.purple())
                        embed.set_thumbnail(url="https://www.pinclipart.com/picdir/big/206-2065855_your-local-fruit-shop-logo-pack-download-your.png")
                        embed.add_field(name=":grapes: Grape Sugar - "+self.nice_number(self.prices["sugar"])+" "+self.currency, value="Needed to produce MDMA. (id => `grape`)", inline=False)
                        embed.add_field(name=":ice_cube: Sugar - "+self.nice_number(self.prices["sugar"])+" "+self.currency, value="Used to mix drugs with. (id => `sugar`)", inline=False)
                        embed.add_field(name=":soap: Washing Powder - "+self.nice_number(self.prices["wash"])+" "+self.currency, value="Used to mix drugs with. (id => `wash`)", inline=False)
                        embed.add_field(name=":fog: Baking Soda - "+self.nice_number(self.prices["soda"])+" "+self.currency, value="Used to mix drugs with. (id => `soda`)", inline=False)
                        embed.add_field(name=":basket: Wooden Basket - "+self.nice_number(self.prices["basket"])+" "+self.currency, value="A better way to collect shrooms. (id => `basket`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>")
                        await message.channel.send(embed=embed)
                    elif command[1] == "powder":
                        embed = discord.Embed(title=":mag_right: Power of Powder", description="You need a lab to turn powder to the real drug.", color=discord.Color.dark_gray())
                        embed.set_thumbnail(url="https://media.istockphoto.com/vectors/explosion-of-blue-powder-vector-id1081303692?k=6&m=1081303692&s=612x612&w=0&h=qv00YeAwnCRs6_Z4HfRf7IbWlJ6yZgt9xYbBWb0fnpE=")
                        embed.add_field(name=":cloud: Cocaine Powder - "+self.nice_number(self.prices["cocaine"])+" "+self.currency, value="1g powder ==> 3g cocaine (id => `cocaine`)", inline=False)
                        embed.add_field(name=":cloud: Crystal Meth Powder - "+self.nice_number(self.prices["meth"])+" "+self.currency, value="1g powder ==> 4g crystal meth (id => `meth`)", inline=False)
                        embed.add_field(name=":cloud: Amphetamine Powder - "+self.nice_number(self.prices["amp"])+" "+self.currency, value="1g powder ==> 5g amphetamine (id => `amp`/`amphetamine`)", inline=False)
                        embed.add_field(name=":cloud: Heroin Powder - "+self.nice_number(self.prices["heroin"])+" "+self.currency, value="1g powder ==> 4g herion (id => `heroin`)", inline=False)
                        embed.add_field(name=":cloud: Amfetamin - "+self.nice_number(self.prices["amf"])+" "+self.currency, value="1g amfetamin ==> 5g mdma (id => `amf`)", inline=False)
                        embed.set_footer(text="You can buy stuff with "+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["mine", "miners"]:
                        embed = discord.Embed(title=":pick: Miners Heaven", color=discord.Color.dark_teal())
                        embed.set_thumbnail(url="https://www.pngkit.com/png/full/19-198225_banner-transparent-bitcoin-miner-logo-karmashares-llc-bitcoin.png")
                        for minerType in self.miners:
                            for miner in self.miners[minerType]:
                                if minerType == "asic":
                                    embed.add_field(name=":hammer_pick: "+miner.upper()+" - "+self.nice_number(self.miners[minerType][miner])+" "+self.currency, value="You can mine bitcoin with this. (id => `"+miner+"`)", inline=False)
                                else:
                                    embed.add_field(name=":pick: "+miner+" - "+self.nice_number(self.miners[minerType][miner])+" "+self.currency, value="You can mine ethereum with this. (id => `"+miner+"`)", inline=False)
                        embed.set_footer(text="You can buy miners with "+self.prefix+"buy <MINER_ID> <AMOUNT (optional)>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["location", "building", "buildings", "houses", "properties", "property", "prime", "primelocation"]:
                        embed = discord.Embed(title=":house: PrimeLocation", color=discord.Color.gold())
                        embed.set_thumbnail(url="https://media.istockphoto.com/vectors/house-abstract-sign-design-vector-linear-style-vector-id1131184921?k=6&m=1131184921&s=612x612&w=0&h=X5MCxDEER4QrVvE2olwd-ZZuVAa-NFKzKGRgupestQ8=")
                        if len(command) <= 2:
                            embed.description = "Welcome to PrimeLocation, please use `"+self.prefix+"shop primelocation <BUILDING_TYPE>` a building type is a `house`/`warehouse`/`lab`\n\n\nTip: you don't need to use the whole `primelocation` thing, you can just use `prime` or `houses`..."
                        else:
                            if command[2] in ["house", "houses", "appartment", "appartments"]:
                                for building in self.buildings["house"]:
                                    embed.add_field(name=":house: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["warehouse", "warehouses"]:
                                for building in self.buildings["warehouse"]:
                                    embed.add_field(name=":hotel: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["lab", "labs", "laboratory", "laboratories"]:
                                for building in self.buildings["lab"]:
                                    embed.add_field(name=":microscope: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                        embed.set_footer(text="You can buy a building with "+self.prefix+"buy <BUILDING_ID>")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(message.author.mention+" There is no shop with that ID, use `"+self.prefix+"shops` to view all available shops")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"shop <SHOP_ID>` or use `"+self.prefix+"shops` to view all available shops")
            elif command[0] == "buy":
                if len(command) < 2 or len(command) > 3:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`")
                else:
                    user = str(message.author.id)
                    if command[1] in self.prices:
                        if self.database["user"][user]["lvl"] < 10:
                            if command[1] in self.drugLvls["10"]:
                                await message.channel.send(message.author.mention+" You need lvl 10+ to unlock "+command[1])
                                return
                            elif command[1] in self.drugLvls["25"]:
                                await message.channel.send(message.author.mention+" You need lvl 25+ to unlock "+command[1])
                                return
                        elif self.database["user"][user]["lvl"] < 25:
                            if command[1] in self.drugLvls["25"]:
                                await message.channel.send(message.author.mention+" You need lvl 25+ to unlock "+command[1])
                                return
                        price = self.prices[command[1]]
                        if command[1] not in ["lab1", "lab2", "lab3"]:
                            amount = 1
                            if len(command) == 3:
                                try:
                                    amount = int(command[2])
                                except:
                                    await message.channel.send(message.author.mention+" Please specify a valid amount `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`")
                                    return
                                price = self.prices[command[1]]*amount
                            if self.database["user"][user]["balance"]-price >= 0:
                                self.database["user"][user]["balance"] -= price
                                if command[1] not in self.database["user"][user]["inventory"]["items"]:
                                    self.database["user"][user]["inventory"]["items"][command[1]] = amount
                                else:
                                    self.database["user"][user]["inventory"]["items"][command[1]] += amount
                                await message.channel.send(message.author.mention+" You bought **"+str(amount)+"x "+command[1]+"**")
                            else:
                                await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                        else:
                            if self.database["user"][user]["balance"]-price >= 0:
                                self.database["user"][user]["balance"] -= price
                                self.database["user"][user]["upgrades"]["lab"] = int(command[1].replace("lab", ""))
                                await message.channel.send(message.author.mention+" You bought a **lab equipment upgrade (lvl "+command[1].replace("lab", "")+")**")
                            else:
                                await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                    elif command[1] in self.buildingDB:
                        building = self.buildingDB[command[1]]
                        if self.database["user"][user]["balance"]-building["price"] >= 0:
                            self.database["user"][user]["balance"] -= building["price"]
                            self.database["user"][user][building["btype"]] = building
                            await message.channel.send(message.author.mention+" You got yourself a new "+building["btype"]+"!")
                        else:
                            await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                    elif command[1].upper() in self.cryptos:
                        crypto = command[1].upper()
                        amount = 1
                        if len(command) == 3:
                            try:
                                amount = float(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Please specify a valid amount `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`")
                                return
                        if amount > 0.00001:
                            cryptoPrice = cryptocompare.get_price(crypto, "USD")[crypto]["USD"]
                            price = cryptoPrice*amount
                            if self.database["user"][user]["balance"]-price >= 0:
                                self.database["user"][user]["balance"] -= price
                                if crypto in self.database["user"][user]["crypto"]:
                                    self.database["user"][user]["crypto"][crypto] += amount
                                else:
                                    self.database["user"][user]["crypto"][crypto] = amount
                                await message.channel.send(message.author.mention+" You invested `"+str(price)+" "+self.currency+"` into `"+crypto+"` at price `"+str(cryptoPrice)+"` per "+crypto)
                            else:
                                await message.channel.send(message.author.mention+" You can't afford to buy that :joy:")
                        else:
                            await message.channel.send(message.author.mention+" Minimum amount is 0.00001 "+crypto)
                    else:
                        await message.channel.send(message.author.mention+" That item/building does not exist, use `.shop <SHOP_ID>` to see all available items and buildings")
            elif command[0] == "sell":
                if len(command) == 2 or len(command) == 3:
                    user = str(message.author.id)
                    amount = 1
                    if len(command) == 3 and command[1].upper() not in self.cryptos:
                        try:
                            if amount != "max":
                                amount = int(command[2])
                        except:
                            await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"sell <ITEM_ID> <AMOUNT>`")
                            return
                    if command[1] in self.prices:
                        if command[1] in self.database["user"][user]["inventory"]["items"]:
                            if amount == "max":
                                amount = self.database["user"][user]["inventory"]["items"][command[1]]
                            if self.database["user"][user]["inventory"]["items"][command[1]] >= amount:
                                self.database["user"][user]["inventory"]["items"][command[1]] -= amount
                                if self.database["user"][user]["inventory"]["items"][command[1]] == 0:
                                    self.database["user"][user]["inventory"]["items"].pop(command[1])
                                self.database["user"][user]["balance"] += round((self.prices[command[1]]/2)*amount)
                                await message.channel.send(message.author.mention+" You have sold **"+str(amount)+"x "+str(self.fullName[command[1]].split(":")[-1][1:].lower())+"** for **"+str(round((self.prices[command[1]]/2)*amount))+" "+self.currency+"**")
                            else:
                                await message.channel.send(message.author.mention+" You don't have that many of these items")
                        else:
                            await message.channel.send(message.author.mention+" You don't own that item")
                    elif command[1].upper() in self.cryptos:
                        if len(command) == 3:
                            try:
                                amount = float(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Please specify a valid amount to sell")
                                return
                        crypto = command[1].upper()
                        if crypto in self.database["user"][user]["crypto"]:
                            if self.database["user"][user]["crypto"][crypto] >= amount:
                                cryptoPrice = cryptocompare.get_price(crypto, "USD")[crypto]["USD"]
                                price = cryptoPrice*amount
                                self.database["user"][user]["balance"] += price
                                self.database["user"][user]["crypto"][crypto] -= amount
                                if self.database["user"][user]["crypto"][crypto] <= 0:
                                    self.database["user"][user]["crypto"].pop(crypto)
                                await message.channel.send(message.author.mention+" You have sold **"+str(amount)+" "+crypto+"** for `"+str(price)+"` at price `"+str(cryptoPrice)+"` per "+crypto)
                            else:
                                await message.channel.send(message.author.mention+" You don't have that much "+crypto)
                        else:
                            await message.channel.send(message.author.mention+" You don't have any "+crypto)
                    else:
                        await message.channel.send(message.author.mention+" That item does not exist")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"sell <ITEM_ID>")
            elif command[0] in ["inv", "inventory", "items"]:
                user = str(message.author.id)
                name = message.author.name
                page = 1
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                    if len(command) > 2:
                        try:
                            page = int(command[2])
                        except:
                            page = 1
                elif len(command) > 1:
                    try:
                        page = int(command[1])
                    except:
                        page = 1
                pages = [[]]
                if len(self.database["user"][user]["inventory"]["items"]) > 0:
                    for item in self.database["user"][user]["inventory"]["items"]:
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+self.fullName[item]+"** ("+str(self.database["user"][user]["inventory"]["items"][item])+")", self.description[item]))
                        else:
                            pages.append([("**"+self.fullName[item]+"** ("+str(self.database["user"][user]["inventory"]["items"][item])+")", self.description[item])])
                if page > len(pages):
                    await message.channel.send(message.author.mention+" Sorry, but you only have `"+str(len(pages))+"` pages")
                elif pages[page-1] == []:
                    await message.channel.send(message.author.mention+" Your inventory is empty")
                else:
                    embed = discord.Embed(title=name+"'s Inventory", color=discord.Color.blue())
                    for item in pages[page-1]:
                        embed.add_field(name=item[0], value=item[1], inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["drugs", "druglist"]:
                user = str(message.author.id)
                name = message.author.name
                page = 1
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                    if len(command) > 2:
                        try:
                            page = int(command[2])
                        except:
                            page = 1
                elif len(command) > 1:
                    try:
                        page = int(command[1])
                    except:
                        page = 1
                pages = [[]]
                if len(self.database["user"][user]["inventory"]["drugs"]["pure"]) > 0:
                    for drug in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                        amount = self.database["user"][user]["inventory"]["drugs"]["pure"][drug]
                        if amount >= 1000:
                            amount = str(amount/1000) + " kilos"
                        elif amount >= 1000000:
                            amount = str(amount/1000000) + " tons"
                        else:
                            amount = str(amount) + " grams"
                        if str(amount).split(".")[-1].split(" ")[0] == "0":
                            amount = amount.split(".")[0]+" "+amount.split(" ")[1]
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+self.drugName[drug]+"** ("+str(amount)+")", self.drugDescription[drug]))
                        else:
                            pages.append([("**"+self.drugName[drug]+"** ("+str(amount)+")", self.drugDescription[drug])])
                if len(self.database["user"][user]["inventory"]["drugs"]["mixes"]) > 0:
                    for drug in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                        amount = drug["amount"]
                        if amount >= 1000:
                            amount = str(amount/1000) + " kilos"
                        elif amount >= 1000000:
                            amount = str(amount/1000000) + " tons"
                        else:
                            amount = str(amount) + " grams"
                        if len(pages[-1]) < 5:
                            pages[-1].append(("**"+drug["icon"]+" "+self.drugName[drug["drug"]].split(":")[-1]+"** Mix ("+str(amount)+")", "Quality: "+str(drug["quality"])+" ("+self.mixQuality(drug["quality"])+")"))
                        else:
                            pages.append([("**"+drug["icon"]+" "+self.drugName[drug["drug"]].split(":")[-1]+"** Mix ("+str(amount)+")", "Quality: "+str(drug["quality"])+" ("+self.mixQuality(drug["quality"])+")")])
                if page > len(pages):
                    await message.channel.send(message.author.mention+" Sorry, but you only have `"+str(len(pages))+"` pages")
                elif pages[page-1] == []:
                    await message.channel.send(message.author.mention+" Your drug inventory is empty")
                else:
                    embed = discord.Embed(title=name+"'s Drugs", color=discord.Color.red())
                    for drug in pages[page-1]:
                        embed.add_field(name=drug[0], value=drug[1], inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["buildings", "houses", "houselist", "homelist"]:
                user = str(message.author.id)
                name = str(message.author.name)
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                embed = discord.Embed(title=name+"'s Buildings", description="List of owned buildings", color=discord.Color.gold())
                if self.database["user"][user]["house"] != None:
                    building = self.database["user"][user]["house"]
                    embed.add_field(name=":house: House: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["warehouse"] != None:
                    building = self.database["user"][user]["warehouse"]
                    embed.add_field(name=":hotel: Warehouse: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_number(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["lab"] != None:
                    building = self.database["user"][user]["lab"]
                    embed.add_field(name=":microscope: Lab: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_number(building["price"])+" "+self.currency+"\nEqupment Level: "+str(self.database["user"][user]["upgrades"]["lab"]), inline=False)
                await message.channel.send(embed=embed)
            elif command[0] == "grow":
                user = str(message.author.id)
                name = str(message.author.name)
                target = 1
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                    target = 2
                if (len(command) >= 3 and len(message.mentions) > 0) or (len(command) >= 2 and len(message.mentions) == 0):
                    embed = discord.Embed(title="Grow Menu", color=discord.Color.green())
                    embed.set_thumbnail(url="https://st2.depositphotos.com/1008559/11854/v/600/depositphotos_118543668-stock-illustration-round-pattern-from-cannabis-leaf.jpg")
                    if command[target] == "info":
                        capacity = self.database["user"][user]["house"]["size"]
                        if self.database["user"][user]["warehouse"] != None:
                            capacity += self.database["user"][user]["warehouse"]["size"]
                        growing, grown = 0, 0
                        topTime = 0
                        for plant in self.database["user"][user]["growing"]:
                            if plant["growTime"] < time():
                                grown += 1
                            else:
                                if plant["growTime"] < topTime or topTime == 0:
                                    topTime = plant["growTime"]
                                growing += 1
                        destTime = 0
                        if topTime != 0:
                            destTime = topTime-time()
                        remaining = str(datetime.timedelta(seconds=round(destTime))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        embed.add_field(name=":potted_plant: **Currently Growing**", value="Growing `"+str(growing)+"` out of `"+str(capacity)+"` plants", inline=False)
                        embed.add_field(name=":potted_plant: **Top Growing**", value="You need to wait about **"+remaining[1]+" minutes and "+remaining[2]+" seconds** before your next plant grows", inline=False)
                        embed.add_field(name=":potted_plant: **Harvestable**", value="There are `"+str(grown)+"` harvestable plants", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[target] == "grow":
                        user = str(message.author.id)
                        name = str(message.author.name)
                        if len(command) == target+3 or len(command) == target+4:
                            amount = 1
                            if len(command) == target+4:
                                try:
                                    amount = int(command[target+3])
                                except:
                                    await message.channel.send(message.author.mention+" That's not a valid number")
                                    return
                            if command[target+1] in ["ruderalis", "indica", "saucer", "knobby", "bohemica"]:
                                if command[target+2] in ["house", "warehouse"]:
                                    if self.database["user"][user][command[target+2]] != None:
                                        capacity = self.database["user"][user][command[target+2]]["size"]
                                        growing = 0
                                        for plant in self.database["user"][user]["growing"]:
                                            if plant["place"] == command[target+2]:
                                                growing += 1
                                        if capacity-growing >= amount:
                                            lamps = []
                                            lamp = None
                                            pots = 0
                                            pot = False
                                            for plant in self.database["user"][user]["growing"]:
                                                lamps.append(plant["lamp"])
                                                pots += 1
                                            if "hid" in self.database["user"][user]["inventory"]["items"]:
                                                if self.database["user"][user]["inventory"]["items"]["hid"] >= lamps.count("hid")+amount:
                                                    lamp = "hid"
                                            if lamp == None:
                                                if "led" in self.database["user"][user]["inventory"]["items"]:
                                                    if self.database["user"][user]["inventory"]["items"]["led"] >= lamps.count("led")+amount:
                                                        lamp = "led"
                                            if "pot" in self.database["user"][user]["inventory"]["items"]:
                                                if self.database["user"][user]["inventory"]["items"]["pot"] >= pots+amount:
                                                    pot = True
                                            if command[target+1] in self.database["user"][user]["inventory"]["items"] or command[target+1] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                                if lamp != None:
                                                    if pot:
                                                        if command[target+1] in self.database["user"][user]["inventory"]["items"]:
                                                            if self.database["user"][user]["inventory"]["items"][command[target+1]] >= amount:
                                                                self.database["user"][user]["inventory"]["items"][command[target+1]] -= amount
                                                                if self.database["user"][user]["inventory"]["items"][command[target+1]] == 0:
                                                                    self.database["user"][user]["inventory"]["items"].pop(command[target+1])
                                                            else:
                                                                await message.channel.send(message.author.mention+" You don't have enough seeds")
                                                                return
                                                        else:
                                                            if self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] >= amount:
                                                                self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] -= amount
                                                                if self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] == 0:
                                                                    self.database["user"][user]["inventory"]["drugs"]["pure"].pop(command[target+1])
                                                            else:
                                                                await message.channel.send(message.author.mention+" You don't have enough seeds")
                                                                return
                                                        speed = 1
                                                        watts = 1000
                                                        growTime = self.cooldowns["indica"]
                                                        if lamp == "hid":
                                                            speed = 1.5
                                                            watts = 400
                                                        if "filter" in self.database["user"][user]["inventory"]["items"]:
                                                            if self.database["user"][user]["inventory"]["items"]["filter"] > 0:
                                                                b = random.randint(0, 20)
                                                                speed += 0.5
                                                                watts += 200
                                                                if b == 50:
                                                                    self.database["user"][user]["inventory"]["items"]["filter"] -= 1
                                                                    if self.database["user"][user]["inventory"]["items"]["filter"] <= 0:
                                                                        self.database["user"][user]["inventory"]["items"].pop("filter")
                                                                    await message.channel.send(message.author.mention+" **Your filter broke!**")
                                                        if command[target+1] == "ruderalis":
                                                            growTime = self.cooldowns["ruderalis"]
                                                        elif command[target+1] == "bohemica":
                                                            growTime = self.cooldowns["bohemica"]
                                                        elif command[target+1] == "knobby":
                                                            growTime = self.cooldowns["knobby"]
                                                        elif command[target+1] == "saucer":
                                                            growTime = self.cooldowns["saucer"]
                                                        growTime = growTime/speed
                                                        self.database["user"][user]["growing"].append({"seeds":command[target+1], "growTime":round(time()+growTime), "lamp":lamp, "place":command[target+2], "amount":amount})
                                                        self.database["user"][user]["electricity"] += round((watts/1000)*(growTime/60)*amount)
                                                        remaining = str(datetime.timedelta(seconds=growTime)).split(":")
                                                        for i in range(len(remaining)):
                                                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                                remaining[i] = remaining[i][1:]
                                                        await message.channel.send(message.author.mention+" You planted a "+command[target+1]+" seed with a "+lamp+" lamp, it will take **"+remaining[1]+" minutes and "+remaining[2]+" seconds** to grow")
                                                    else:
                                                        await message.channel.send(message.author.mention+" You don't have enough pots to grow more weed")
                                                else:
                                                    await message.channel.send(message.author.mention+" You don't have enough lamps to grow more weed")
                                            else:
                                                await message.channel.send(message.author.mention+" You don't have enough seeds")
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have enough space to grow more weed")
                                    else:
                                        await message.channel.send(message.author.mention+" You don't own a "+command[target+2])
                                else:
                                    await message.channel.send(message.author.mention+" Please specify a valid place to grow the weed in (`house`/`warehouse`)")
                            else:
                                await message.channel.send(message.author.mention+" There are no seeds named `"+command[target+1]+"`")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow grow <SEED_ID> <HOUSE/WAREHOUSE> <AMOUNT (optional)>`")
                    elif command[target] == "harvest":
                        user = str(message.author.id)
                        name = str(message.author.name)
                        packageSize = 0
                        collectedPlants = []
                        shrooms = {"saucer":0, "knobby":0, "bohemica":0}
                        for plant in self.database["user"][user]["growing"]:
                            if plant["growTime"] < time():
                                if plant["seeds"] == "indica":
                                    packageSize += 30*plant["amount"]
                                elif plant["seeds"] == "ruderalis":
                                    packageSize += 20*plant["amount"]
                                elif plant["seeds"] == "saucer":
                                    shrooms["saucer"] += 8*plant["amount"]
                                elif plant["seeds"] == "knobby":
                                    shrooms["knobby"] += 15*plant["amount"]
                                elif plant["seeds"] == "bohemica":
                                    shrooms["bohemica"] += 20*plant["amount"]
                                collectedPlants.append(plant)
                        potBreaks = 0
                        for plant in collectedPlants:
                            del self.database["user"][user]["growing"][self.database["user"][user]["growing"].index(plant)]
                            potBreak = random.randint(0, round(plant/100))
                            if potBreak > 0:
                                self.database["user"][user]["inventory"]["items"]["pot"] -= potBreak
                                if self.database["user"][user]["inventory"]["items"]["pot"] <= 0:
                                    self.database["user"][user]["inventory"]["items"].pop("pot")
                                potBreaks += potBreak
                        info = ""
                        if potBreaks == 1:
                            info += "Your **pot broke** while harvesting weed/shrooms!\n"
                        elif potBreaks > 1:
                            info += "Your **"+str(potBreaks)+"x pots broke** while harvesting weed/shrooms!\n"
                        if packageSize > 0:
                            if "wetweed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] += packageSize
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] = packageSize
                            info += "You collected "+str(packageSize)+" grams of wet weed\n"
                        if shrooms["saucer"] > 0:
                            if "saucer" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["saucer"] += shrooms["saucer"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["saucer"] = shrooms["saucer"]
                            info += "You collected "+str(shrooms["saucer"])+" grams of saucer\n"
                        if shrooms["knobby"] > 0:
                            if "knobby" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["knobby"] += shrooms["knobby"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["knobby"] = shrooms["knobby"]
                            info += "You collected "+str(shrooms["knobby"])+" grams of knobby\n"
                        if shrooms["bohemica"] > 0:
                            if "bohemica" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["bohemica"] += shrooms["bohemica"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["bohemica"] = shrooms["bohemica"]
                            info += "You collected "+str(shrooms["bohemica"])+" grams of bohemica\n"
                        if shrooms["saucer"] == 0 and shrooms["knobby"] == 0 and shrooms["bohemica"] == 0 and packageSize == 0:
                            await message.channel.send(message.author.mention+" Your weed/mushrooms aren't fully grown yet")
                        else:
                            await message.channel.send(message.author.mention+" "+info[:-1])
                    elif command[target] == "dry":
                        user = str(message.author.id)
                        name = str(message.author.name)
                        dryer = False
                        if "dryer" in self.database["user"][user]["inventory"]["items"]:
                            if self.database["user"][user]["inventory"]["items"]["dryer"] > 0:
                                dryer = True
                        if "wetweed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                            if self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] > 0:
                                weed = self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"]
                                base = self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"]
                                bonus = 0
                                if dryer:
                                    self.database["user"][user]["electricity"] += 3
                                    bonus = round(weed/5)
                                    weed += bonus
                                if "weed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"]["weed"] += weed
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"]["weed"] = weed
                                self.database["user"][user]["inventory"]["drugs"]["pure"].pop("wetweed")
                                dryerBreak = random.randint(1, 25)
                                if dryerBreak == 25 and dryer:
                                    self.database["user"][user]["inventory"]["items"]["dryer"] -= 1
                                    if self.database["user"][user]["inventory"]["items"]["dryer"] <= 0:
                                        self.database["user"][user]["inventory"]["items"].pop("dryer")
                                    await message.channel.send(message.author.mention+" **Your dryer broke!**\nYou dryed `"+str(base)+"` grams of weed into `"+str(weed)+"` grams with `"+str(bonus)+"` bonus grams (dryer)")
                                else:
                                    await message.channel.send(message.author.mention+" You dryed `"+str(base)+"` grams of weed into `"+str(weed)+"` grams with `"+str(bonus)+"` bonus grams (dryer)")
                            else:
                                await message.channel.send(message.author.mention+" You don't have any wet weed to dry")
                        else:
                            await message.channel.send(message.author.mention+" You don't have any wet weed to dry")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*")
            elif command[0] in ["electricity", "bill", "bills", "tax", "taxes", "elec"]:
                user = str(message.author.id)
                name = str(message.author.name)
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = str(message.mentions[0].name)
                remaining = str(datetime.timedelta(seconds=(self.database["user"][user]["lastBill"]+86400)-round(time()))).split(":")
                for i in range(len(remaining)):
                    if remaining[i].startswith("0") and len(remaining[i]) != 1:
                        remaining[i] = remaining[i][1:]
                embed = discord.Embed(title=name+"'s Electricity Bills", description="Next bill will be automaticly payed in "+remaining[0]+" hours "+remaining[1]+" minutes", color=discord.Color.from_rgb(93, 109, 126))
                embed.add_field(name=":electric_plug: Estimated Payment", value=self.nice_number(round(self.database["user"][user]["electricity"]*self.electricityMultiplayer))+" "+self.currency)
                await message.channel.send(embed=embed)
            elif command[0] == "levelup":
                user = str(message.author.id)
                if len(command) >= 2:
                    if command[1] == "confirm":
                        if len(command) >= 3:
                            try:
                                amount = int(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"levelup confirm <AMOUNT>`")
                        for _ in range(amount):
                            cost = round(200*self.database["user"][user]["lvl"]*(self.database["user"][user]["lvl"]/2))
                            if self.database["user"][user]["balance"]-cost > 0:
                                self.database["user"][user]["balance"] -= cost
                                self.database["user"][user]["lvl"] += 1
                            else:
                                await message.channel.send(message.author.mention+" You need `"+str(0-(self.database["user"][user]["balance"]-cost))+" "+self.currency+"` more to level up")
                                return
                        await message.channel.send(message.author.mention+" You are now lvl "+str(self.database["user"][user]["lvl"]))
                else:
                    embed = discord.Embed(title="Level "+str(self.database["user"][user]["lvl"]+1)+" Requirements", color=discord.Color.blue())
                    embed.add_field(name="**Current Level**", value="You are currently level "+str(self.database["user"][user]["lvl"]), inline=False)
                    embed.add_field(name="**Level Up**", value="You need `"+str(2000*self.database["user"][user]["lvl"]*(self.database["user"][user]["lvl"]/2))+" "+self.currency+"`", inline=False)
                    embed.add_field(name="**Confirm Level Up**", value="Use `"+self.prefix+"levelup confirm <AMOUNT (optional)>` to confirm your level up", inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["prod", "produce", "lab"]:
                target = 1
                user = str(message.author.id)
                name = message.author.name
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                    target += 1
                if self.database["user"][user]["lab"] == None:
                    await message.channel.send(message.author.mention+" You need to own a lab before running this command")
                    return
                if len(command) >= target+1:
                    if command[target] == "info":
                        embed = discord.Embed(title=name+"'s Lab", color=discord.Color.dark_gray())
                        embed.set_thumbnail(url="https://www.graphicsprings.com/filestorage/stencils/56eabbf3d6478e853220af42debe688b.png?width=500&height=500")
                        producing, capacity, topProducing, collectable = 0, self.database["user"][user]["lab"]["size"], 0, 0
                        for drug in self.database["user"][user]["producing"]:
                            if drug["prodTime"] < time():
                                collectable += 1
                            else:
                                if drug["prodTime"] < topProducing or topProducing == 0:
                                    topProducing = drug["prodTime"]
                                producing += 1
                        if topProducing != 0:
                            topProducing = round(topProducing-time())
                        remaining = str(datetime.timedelta(seconds=topProducing)).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        embed.add_field(name="**Curently Producing**", value="There are `"+str(producing)+"` out of `"+str(capacity)+"` drugs currently producing", inline=False)
                        embed.add_field(name="**Top Producing**", value="You need to wait about **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds** before your next drug produces", inline=False)
                        embed.add_field(name="**Ready To Collect**", value="There are `"+str(collectable)+"` drugs ready to collect", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[target] in ["prod", "produce"]:
                        user = str(message.author.id)
                        name = message.author.name
                        if len(command) >= target+2:
                            powder = command[target+1]
                            if powder in self.producmentTime:
                                powderAmount = 1
                                produceAmount = 1
                                if len(command) >= target+3:
                                    try:
                                        powderAmount = int(command[target+2])
                                    except:
                                        return
                                if len(command) >= target+4:
                                    try:
                                        produceAmount = int(command[target+3])
                                    except:
                                        return
                                if powder in self.database["user"][user]["inventory"]["items"] and powder not in self.notProduceable:
                                    if self.database["user"][user]["inventory"]["items"][powder] >= powderAmount*produceAmount:
                                        if powderAmount <= 10:
                                            freeCapacity = self.database["user"][user]["lab"]["size"]-len(self.database["user"][user]["producing"])
                                            if produceAmount <= freeCapacity:
                                                if powder == "amf":
                                                    if "grape" in self.database["user"][user]["inventory"]["items"]:
                                                        if self.database["user"][user]["inventory"]["items"]["grape"] >= produceAmount:
                                                            self.database["user"][user]["inventory"]["items"]["grape"] -= produceAmount
                                                            if self.database["user"][user]["inventory"]["items"]["grape"] <= 0:
                                                                self.database["user"][user]["inventory"]["items"].pop("grape")
                                                        else:
                                                            await message.channel.send(message.author.mention+" You don't have enough of grape sugar")
                                                            return
                                                    else:
                                                        await message.channel.send(message.author.mention+" You need grape sugar in orded to produce MDMA")
                                                        return
                                                boost = self.cooldowns["labBoost"]*self.database["user"][user]["upgrades"]["lab"]
                                                targetTime = self.producmentTime[powder]+time()-boost
                                                elec = 1*round((self.producmentTime[powder]-boost)/60)
                                                self.database["user"][user]["electricity"] += elec
                                                for _ in range(produceAmount):
                                                    self.database["user"][user]["producing"].append({"drug":powder, "reward":self.produceReward[powder]*powderAmount, "prodTime":targetTime})
                                                self.database["user"][user]["inventory"]["items"][powder] -= powderAmount*produceAmount
                                                if self.database["user"][user]["inventory"]["items"][powder] == 0:
                                                    self.database["user"][user]["inventory"]["items"].pop(powder)
                                                remaining = str(datetime.timedelta(seconds=round(targetTime-time()))).split(":")
                                                for i in range(len(remaining)):
                                                    if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                        remaining[i] = remaining[i][1:]
                                                await message.channel.send(message.author.mention+" You started to produce `"+str(powderAmount)+"` grams of `"+powder+"`, production will take around **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds**")
                                            else:
                                                await message.channel.send(message.author.mention+" You can't produce more drugs due to lab capacity")
                                        else:
                                            await message.channel.send(message.author.mention+" The maximum powder amount is `10` grams")
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have enough"+self.fullName[powder].split(":")[-1])
                                else:
                                    await message.channel.send(message.author.mention+" You don't have enough"+self.fullName[powder].split(":")[-1])
                            else:
                                await message.channel.send(message.author.mention+" That's not a valid drug powder")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"lab <@MENTION (opt)> produce <POWDER_ID> <POWDER_AMOUNT (opt)> <PRODUCE_AMOUNT (opt)>`")
                    elif command[target] == "collect":
                        user = str(message.author.id)
                        name = str(message.author.name)
                        collectable = []
                        for drug in self.database["user"][user]["producing"]:
                            if drug["prodTime"] < time():
                                collectable.append(drug)
                        if len(collectable) > 0:
                            total = 0
                            for drug in collectable:
                                if drug["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][drug["drug"]] += drug["reward"]
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][drug["drug"]] = drug["reward"]
                                total += drug["reward"]
                                del self.database["user"][user]["producing"][self.database["user"][user]["producing"].index(drug)]
                            await message.channel.send(message.author.mention+" You successfully collected `"+str(total)+"` grams of drugs")
                        else:
                            await message.channel.send(message.author.mention+" You don't have any drugs to collect")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"lab <@MENTION (optional)> <ACTION>`\nLab actions: *info*/*produce*/*collect*")
            elif command[0] == "mix":
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 5:
                    try:
                        drugAmount = int(command[1])
                        drug = command[2]
                        substanceAmount = int(command[3])
                        substance = command[4]
                    except:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"mix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"mix 5 amp 5 soda`")
                        return
                    if "mixer" in self.database["user"][user]["inventory"]["items"]:
                        if drug in self.produceReward:
                            if substance in self.substances:
                                if drug in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    if self.database["user"][user]["inventory"]["drugs"]["pure"][drug] >= drugAmount:
                                        if substance in self.database["user"][user]["inventory"]["items"]:
                                            if drugAmount >= substanceAmount:
                                                if drugAmount > 0 and substanceAmount > 0:
                                                    if self.database["user"][user]["inventory"]["items"][substance] >= substanceAmount:
                                                        self.database["user"][user]["inventory"]["drugs"]["pure"][drug] -= drugAmount
                                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][drug] == 0:
                                                            self.database["user"][user]["inventory"]["drugs"]["pure"].pop(drug)
                                                        self.database["user"][user]["inventory"]["items"][substance] -= substanceAmount
                                                        if self.database["user"][user]["inventory"]["items"][substance] == 0:
                                                            self.database["user"][user]["inventory"]["items"].pop(substance)
                                                        quality = round(drugAmount/(drugAmount+substanceAmount)*100)
                                                        if quality <= 85:
                                                            bonus = self.substances[substance]
                                                            quality += bonus
                                                        elif quality <= 90:
                                                            bonus = self.substances[substance]
                                                            if bonus == 10:
                                                                bonus = 5
                                                            quality += bonus
                                                        self.database["user"][user]["inventory"]["drugs"]["mixes"].append({"drug":drug, "quality":quality, "amount":substanceAmount+drugAmount, "icon":random.choice([":blue_square:", ":brown_square:", ":green_square:", ":orange_square:", ":red_square:", ":purple_square:", ":white_large_square:", ":yellow_square:", ":black_large_square:"])})
                                                        mixerBreak = random.randint(0, 25)
                                                        if mixerBreak == 25:
                                                            self.database["user"][user]["inventory"]["items"]["mixer"] -= 1
                                                            if self.database["user"][user]["inventory"]["items"]["mixer"] == 0:
                                                                self.database["user"][user]["inventory"]["items"].pop("mixer")
                                                            await message.channel.send(message.author.mention+" **Your Mixer broke!**\nYou successfully mixed **"+self.drugName[drug].split(":")[-1].lower()+"** with **"+self.fullName[substance].split(":")[-1].lower()+"**, the mix **quality is "+str(quality)+"/100** ("+self.mixQuality(quality)+")")
                                                        else:
                                                            await message.channel.send(message.author.mention+" You successfully mixed **"+self.drugName[drug].split(":")[-1].lower()+"** with **"+self.fullName[substance].split(":")[-1].lower()+"**, the mix **quality is "+str(quality)+"/100** ("+self.mixQuality(quality)+")")
                                                    else:
                                                        await message.channel.send(message.author.mention+" You need more than 0 grams")
                                                else:
                                                    await message.channel.send(message.author.mention+" You need to have at least a 50/50 mix")
                                            else:
                                                await message.channel.send(message.author.mention+" You don't have that much "+self.fullName[substance].split(":")[-1].lower())
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have any "+self.fullName[substance].split(":")[-1].lower())
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have that much "+self.drugName[drug].split(":")[-1].lower())
                                else:
                                    await message.channel.send(message.author.mention+" You don't have any "+self.drugName[drug].split(":")[-1].lower())
                            else:
                                await message.channel.send(message.author.mention+" Either the substance is not mixable or it does not exist")
                        else:
                            await message.channel.send(message.author.mention+" Either the drug is not mixable or it does not exist")
                    else:
                        await message.channel.send(message.author.mention+" You need to own a mixer to be able to mix drugs")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"mix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"mix 5 amp 5 soda`")
            elif command[0] in ["mixcalc", "calcmix", "mixcalculator", "calculatormix"]:
                if len(command) == 5:
                    try:
                        drugAmount = int(command[1])
                        drug = command[2]
                        substanceAmount = int(command[3])
                        substance = command[4]
                    except:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"calcmix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"calcmix 5 amp 5 soda`")
                        return
                    if drug in self.produceReward:
                        if substance in self.substances:
                            if drugAmount >= substanceAmount:
                                if drugAmount > 0 and substanceAmount > 0:
                                    quality = round(drugAmount/(drugAmount+substanceAmount)*100)
                                    if quality <= 85:
                                        bonus = self.substances[substance]
                                        quality += bonus
                                    elif quality <= 90:
                                        bonus = self.substances[substance]
                                        if bonus == 10:
                                            bonus = 5
                                        quality += bonus
                                    await message.channel.send(message.author.mention+" The mix quality is going to be **"+str(quality)+"/100** ("+self.mixQuality(quality)+")")
                                else:
                                    await message.channel.send(message.author.mention+" You need more than 0 grams")
                            else:
                                await message.channel.send(message.author.mention+" You need to have at least a 50/50 mix")
                        else:
                            await message.channel.send(message.author.mention+" Either the substance is not mixable or it does not exist")
                    else:
                        await message.channel.send(message.author.mention+" Either the drug is not mixable or it does not exist")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"calcmix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"calcmix 5 amp 5 soda`")
            elif command[0] in ["cryptocalc", "calccrypto", "ccalc", "calcc"]:
                if len(command) == 3:
                    try:
                        amount = int(command[2])
                    except:
                        await message.channel.send(message.author.mention+" Please specify a valid amount `"+self.prefix+"cryptocalc <CRYPTO> <AMOUNT>`")
                        return
                    crypto = command[1].upper()
                    if crypto in self.cryptos:
                        cryptoPrice = cryptocompare.get_price(crypto, "USD")[crypto]["USD"]
                        finalAmount = floor(amount/cryptoPrice*1000000)/1000000
                        await message.channel.send(message.author.mention+" You can buy "+str(finalAmount)+" "+crypto)
                    else:
                        await message.channel.send(message.author.mention+" That crypto does not exist")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"cryptocalc <CRYPTO> <AMOUNT>`")
            elif command[0] in ["qs", "qsell", "quicksell", "sell", "sellquick"]:
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 3:
                    drugFound = None
                    iMix = {}
                    targetMix = {"drug":"", "amount":0}
                    for mix in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                        if mix["drug"] == command[1]:
                            iMix = mix
                            targetMix = {"drug":mix["drug"], "amount":mix["amount"]}
                            drugFound = "mix"
                            break
                    if drugFound == None: 
                        if command[1] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                            drugFound = "pure"
                    if drugFound != None:
                        if command[2] in ["max", "all"]:
                            if drugFound == "pure":
                                amount = self.database["user"][user]["inventory"]["drugs"]["pure"][command[1]]
                            else:
                                amount = mix["amount"]
                        else:
                            try:
                                amount = int(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"quicksell <DRUG_ID> <AMOUNT>`")
                        if drugFound == "pure":
                            if amount <= self.database["user"][user]["inventory"]["drugs"]["pure"][command[1]]:
                                price = round(self.sellPrice[command[1]]/100*90*amount)
                                price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                                self.database["user"][user]["inventory"]["drugs"]["pure"][command[1]] -= amount
                                if self.database["user"][user]["inventory"]["drugs"]["pure"][command[1]] == 0:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"].pop(command[1])
                                self.database["user"][user]["balance"] += price
                                police = random.randint(1, 20)
                                if police < 15:
                                    await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+str(price)+" "+self.currency+"**")
                                elif police < 20:
                                    await message.channel.send(message.author.mention+" You almost got caught by the cops, but you have successfully sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+str(price)+" "+self.currency+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You got CAUGHT by the COPS! You will be put into prison! Also you have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+str(price)+" "+self.currency+"**")
                                    self.database["user"][user]["police"]["prison"] = True
                                    self.database["user"][user]["police"]["expire"] = time()+self.cooldowns["police"]
                            else:
                                await message.channel.send(message.author.mention+" You don't have that much"+self.drugName[command[1]].split(":")[-1].lower())
                        else:
                            if amount <= targetMix["amount"]:
                                if iMix["quality"] >= 90:
                                    price = round(self.sellPrice[command[1]]/100*90*amount)
                                else:
                                    price = round(self.sellPrice[command[1]]/100*iMix["quality"]*amount)
                                if iMix["amount"] == amount:
                                    del self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] -= amount
                                self.database["user"][user]["balance"] += price
                                police = random.randint(1, 20)
                                if police < 15:
                                    await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+str(price)+" "+self.currency+"**")
                                elif police < 20:
                                    await message.channel.send(message.author.mention+" You almost got caught by the cops, but you have successfully sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+str(price)+" "+self.currency+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You got CAUGHT by the COPS! You will be put into prison! Also you have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+str(price)+" "+self.currency+"**")
                                    self.database["user"][user]["police"]["prison"] = True
                                    self.database["user"][user]["police"]["expire"] = time()+self.cooldowns["police"]
                            else:
                                await message.channel.send(message.author.mention+" You don't have that much"+self.drugName[command[1]].split(":")[-1].lower())
                    else:
                        await message.channel.send(message.author.mention+" Either you don't have that drug or it does not exist")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"quicksell <DRUG_ID> <AMOUNT>`")
            elif command[0] in ["deals", "deallist", "trades", "tradelist"]:
                user = str(message.author.id)
                name = message.author.name
                embed = discord.Embed(title=name+"'s Deals", color=discord.Color.dark_green())
                i = 0
                for deal in self.database["user"][user]["deals"]:
                    i += 1
                    embed.add_field(name=str(i)+". "+self.drugName[deal["drug"]]+" Deal", value="Minimum Quality: "+str(deal["quality"])+", Payment: "+str(round(self.sellPrice[deal["drug"]]/100*(deal["quality"]+25), 1))+" "+self.currency+" per gram", inline=False)
                embed.set_footer(text="You can complete any offer with the command "+self.prefix+"deal <DEAL_NUMBER> <DRUG_AMOUNT>\nExample: "+self.prefix+"deal 1 10")
                await message.channel.send(embed=embed)
            elif command[0] in ["dealrefresh", "dealsrefresh", "newdeals", "newdeal", "newtrade", "newtrades", "refreshtrades", "tradesrefresh"]:
                user = str(message.author.id)
                name = message.author.name
                if self.database["user"][user]["dealRefresh"]+self.cooldowns["dealRefresh"] < time():
                    if len(command) == 2:
                        deals = self.newDeals(user, False, command[1])
                        if deals != None:
                            self.database["user"][user]["deals"] = deals
                        else:
                            await message.channel.send(message.author.mention+" That drug does not exist/you are not the required level")
                    else:
                        self.database["user"][user]["deals"] = self.newDeals(user)
                    self.database["user"][user]["dealRefresh"] = round(time())
                    await message.channel.send(message.author.mention+" You have successfully refreshed your deals")
                else:
                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["dealRefresh"]+self.cooldowns["dealRefresh"]-time()))).split(":")
                    for i in range(len(remaining)):
                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                            remaining[i] = remaining[i][1:]
                    await message.channel.send(message.author.mention+" You need to wait **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds** to refresh the deals again")
            elif command[0] in ["deal", "trade"]:
                if len(command) == 3:
                    user = str(message.author.id)
                    name = message.author.name
                    try:
                        dealNumber = int(command[1])
                        amount = command[2]
                        if amount != "max":
                            amount = int(command[2])
                    except:
                        await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"deal <DEAL_NUMBER> <AMOUNT>`")
                        return
                    deal = self.database["user"][user]["deals"][dealNumber-1]
                    iMix = None
                    for mix in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                        if amount != "max":
                            if mix["drug"] == deal["drug"] and mix["amount"] >= amount and mix["quality"] >= deal["quality"]:
                                iMix = mix
                        elif amount == "max" and mix["drug"] == deal["drug"] and mix["quality"] >= deal["quality"]:
                            iMix = mix
                            amount = iMix["amount"]
                    if iMix != None:
                        self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] -= amount
                        if self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] == 0:
                            del self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]
                        price = round(self.sellPrice[deal["drug"]]/100*(deal["quality"]+25)*amount)
                        price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                        self.database["user"][user]["balance"] += price
                        del self.database["user"][user]["deals"][self.database["user"][user]["deals"].index(deal)]
                        await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams for **"+str(price)+" "+self.currency+"**")
                        if self.database["user"][user]["gang"] == None:
                            gang = random.randint(1, 200)
                            if gang == 200:
                                self.database["user"][user]["gang"] = {"drug":deal["drug"], "maxAmount":amount*8, "lastDeal":0}
                                await message.channel.send(message.author.mention+" A **gang** just showed up and they want to cooperate with you, you can make **BIG MONEY**!!!\n`"+self.prefix+"gang` for more info")
                    elif deal["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                        if amount == "max":
                            amount = self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]]
                        if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] >= amount:
                            self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] -= amount
                            if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] == 0:
                                self.database["user"][user]["inventory"]["drugs"]["pure"].pop(deal["drug"])
                            price = round(self.sellPrice[deal["drug"]]/100*(deal["quality"]+25)*amount)
                            price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                            self.database["user"][user]["balance"] += price
                            del self.database["user"][user]["deals"][self.database["user"][user]["deals"].index(deal)]
                            await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams for **"+str(price)+" "+self.currency+"**")
                            if self.database["user"][user]["gang"] == None:
                                gang = random.randint(1, 200)
                                if gang == 200:
                                    self.database["user"][user]["gang"] = {"drug":deal["drug"], "maxAmount":amount*8, "lastDeal":0}
                                    await message.channel.send(message.author.mention+" A **gang** just showed up and they want to cooperate with you, you can make **BIG MONEY**!!!\n`"+self.prefix+"gang` for more info")
                        else:
                            await message.channel.send(message.author.mention+" You don't have that much "+self.drugName[deal["drug"]].split(":")[-1][1:].lower())
                    else:
                        await message.channel.send(message.author.mention+" You don't have the requested drug")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"deal <DEAL_NUMBER> <AMOUNT>`")
            elif command[0] == "market":
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 1:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market <DRUG_ID>` to view the market, for info: `"+self.prefix+"market info`")
                elif len(command) == 2: # View the market
                    embed = discord.Embed(title="Player Market", color=discord.Color.from_rgb(145, 238, 154))
                    if command[1] == "info":
                        embed.add_field(name="**Beginer Info**", value="You can sell/buy drugs from other players here.", inline=False)
                        embed.add_field(name="**Fee Info**", value="If you buy you will pay a small \"Market Taker\" fee, it is 1% of your payment.", inline=False)
                        embed.add_field(name="**Quality Info**", value="You can't see the exact drug quality until you buy it. (only the horrible/bad/ok/good/verygood/excelent/pure)", inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        if command[1] in self.drugName:
                            if command[1] in self.database["market"]:
                                drugs = self.drugLvls["1"]
                                if self.database["user"][user]["lvl"] >= 10:
                                    for d in self.drugLvls["10"]:
                                        drugs.append(d)
                                if self.database["user"][user]["lvl"] >= 25:
                                    for d in self.drugLvls["25"]:
                                        drugs.append(d)
                                if command[1] in drugs:
                                    m = self.database["market"][command[1]]
                                    final = ""
                                    done = []
                                    if len(m) > 10:
                                        while final.count("\n") != 10:
                                            deal = random.choice(m)
                                            if deal not in done:
                                                final += "**"+str(deal["amount"])+" grams** at a price of **"+str(deal["price"])+" "+self.currency+"** with a **"+str(self.mixQuality(deal["quality"])+"** (id => `"+str(deal["id"])+"`)\n")
                                    else:
                                        for deal in m:
                                            final += "**"+str(deal["amount"])+" grams** at a price of **"+str(deal["price"])+" "+self.currency+"** with a **"+str(self.mixQuality(deal["quality"])+"** (id => `"+str(deal["id"])+"`)\n")
                                    embed.description = final[:-1]
                                else:
                                    embed.add_field(name="**Small Level**", value="Sorry, but you are not the requested level `.levelup` to unlock drugs.", inline=False)
                            else:
                                embed.add_field(name="**Empty**", value="Sorry, but the market for this drug is currently empty.", inline=False)
                            await message.channel.send(embed=embed)
                        else:
                            if command[1].startswith("&"):
                                if command[1] in self.database["market"]["usedIDs"]:
                                    deal = None
                                    for drug in self.database["market"]:
                                        if drug != "usedIDs":
                                            for d in self.database["market"][drug]:
                                                if d["id"] == command[1]:
                                                    deal = d
                                                    break
                                            if deal != None:
                                                break
                                    if deal != None:
                                        final = "**"+str(deal["amount"])+" grams** at a price of **"+str(deal["price"])+" "+self.currency+"** with a **"+str(self.mixQuality(deal["quality"])+"** (id => `"+str(deal["id"])+")\n")
                                        await message.channel.send(message.author.mention+" "+final)
                                    else:
                                        await message.channel.send(message.author.mention+" Deal was not found")
                                else:
                                    await message.channel.send(message.author.mention+" That deal does not exist")
                            else:
                                await message.channel.send(message.author.mention+" That drug does not exist")
                else: # Makret Make/Take
                    if command[1] in ["make", "sell", "create"]:
                        if len(command) == 5:
                            if command[2] in self.drugName:
                                try:
                                    amount = int(command[3])
                                    price = int(command[4])
                                except:
                                    await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"market make <DRUG_NAME> <AMOUNT> <PRICE>`")
                                    return
                                iMix = None
                                for mix in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                                    if mix["drug"] == command[2] and mix["amount"] >= amount:
                                        iMix = mix
                                        break
                                if iMix != None:
                                    deal = {"drug":command[2], "amount":amount, "price":price, "author":user, "id":self.marketID(), "quality":iMix["quality"]}
                                    if command[2] in self.database["market"]:
                                        self.database["market"][command[2]].append(deal)
                                    else:
                                        self.database["market"][command[2]] = [deal]
                                    self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(mix)]["amount"] -= amount
                                    if self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(mix)]["amount"] == 0:
                                        del self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(mix)]
                                    await message.channel.send(message.author.mention+" You successfully create an market offer")
                                elif command[2] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    if self.database["user"][user]["inventory"]["drugs"]["pure"][command[2]] >= amount:
                                        deal = {"drug":command[2], "amount":amount, "price":price, "author":user, "id":self.marketID(), "quality":100}
                                        if command[2] in self.database["market"]:
                                            self.database["market"][command[2]].append(deal)
                                        else:
                                            self.database["market"][command[2]] = [deal]
                                        self.database["user"][user]["inventory"]["drugs"]["pure"][command[2]] -= amount
                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][command[2]] == 0:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"].pop(command[2])
                                        await message.channel.send(message.author.mention+" You successfully create an market offer")
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have enough "+self.drugName[command[2]].split(":")[-1][1:])
                                else:
                                    await message.channel.send(message.author.mention+" You don't have any "+self.drugName[command[2]].split(":")[-1][1:])
                            else:
                                await message.channel.send(message.author.mention+" That drug does not exist")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market make <DRUG_NAME> <AMOUNT> <PRICE>`")
                    elif command[1] in ["take", "buy", "get"]:
                        if len(command) == 3:
                            dealID = command[2]
                            if dealID in self.database["market"]["usedIDs"]:
                                deal = None
                                for drug in self.database["market"]:
                                    if drug != "usedIDs":
                                        for d in self.database["market"][drug]:
                                            if d["id"] == dealID:
                                                deal = d
                                                break
                                        if deal != None:
                                            break
                                if self.database["user"][user]["balance"]-(deal["price"]/100*101) > 0:
                                    self.database["user"][user]["balance"] -= deal["price"]/100*101
                                    self.database["user"][deal["author"]]["balance"] += deal["price"]/100*101
                                    if deal["quality"] == 100:
                                        if deal["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] += deal["amount"]
                                        else:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] = deal["amount"]
                                    else:
                                        self.database["user"][user]["inventory"]["drugs"]["mixes"].append({"drug":deal["drug"], "quality":deal["quality"], "amount":deal["amount"], "icon":random.choice([":blue_square:", ":brown_square:", ":green_square:", ":orange_square:", ":red_square:", ":purple_square:", ":white_large_square:", ":yellow_square:", ":black_large_square:"])})
                                    del self.database["market"]["usedIDs"][self.database["market"]["usedIDs"].index(deal["id"])]
                                    del self.database["market"][deal["drug"]][self.database["market"][deal["drug"]].index(deal)]
                                    if len(self.database["market"][deal["drug"]]) == 0:
                                        self.database["market"].pop(deal["drug"])
                                    await message.channel.send(message.author.mention+" You have bought "+str(deal["amount"])+" grams of "+self.drugName[deal["drug"]].split(":")[-1][1:])
                                else:
                                    await message.channel.send(message.author.mention+" You don't have enough money")
                            else:
                                await message.channel.send(message.author.mention+" There is no trade with that ID")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market take <DEAL_ID>`")
                    elif command[1] in ["remove", "delete", "del", "rm"]:
                        if len(command) == 3:
                            deal = None
                            for drug in self.database["market"]:
                                if drug != "usedIDs":
                                    for d in self.database["market"][drug]:
                                        if d["id"] == command[2]:
                                            deal = d
                                            break
                                    if deal != None:
                                        break
                            if deal != None:
                                if str(deal["author"]) == user:
                                    del self.database["market"][deal["drug"]][self.database["market"][deal["drug"]].index(deal)]
                                    if len(self.database["market"][deal["drug"]]) == 0:
                                        self.database["market"].pop(deal["drug"])
                                    del self.database["market"]["usedIDs"][self.database["market"]["usedIDs"].index(deal["id"])]
                                    if deal["quality"] == 100:
                                        if deal["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] += deal["amount"]
                                        else:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] = deal["amount"]
                                    else:
                                        self.database["user"][user]["inventory"]["drugs"]["mixes"].append({"drug":deal["drug"], "quality":deal["quality"], "amount":deal["amount"], "icon":random.choice([":blue_square:", ":brown_square:", ":green_square:", ":orange_square:", ":red_square:", ":purple_square:", ":white_large_square:", ":yellow_square:", ":black_large_square:"])})
                                    await message.channel.send(message.author.mention+" You have successfully removed your deal from the market")
                                else:
                                    await message.channel.send(message.author.mention+" You only can delete deals created by yourself")
                            else:
                                await message.channel.send(message.author.mention+" There is no deal with that ID")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market remove <DEAL_ID>`")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market <ACTION> ...` actions: *make*/*take*")
            elif command[0] in ["give", "transfer", "share"]:
                user = str(message.author.id)
                if len(message.mentions) > 0:
                    dest = str(message.mentions[0].id)
                    ment = message.mentions[0].mention
                    try:
                        amount = int(command[2])
                    except:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"give <@MENTION> <AMOUNT>`")
                        return
                    if self.database["user"][user]["balance"] >= amount:
                        self.database["user"][user]["balance"] -= amount
                        self.database["user"][dest]["balance"] += amount
                        await message.channel.send(message.author.mention+" has given "+ment+" **"+self.nice_number(amount)+" "+self.currency+"**")
                    else:
                        await message.channel.send(message.author.mention+" You don't have that much money")
                else:
                    await message.channel.send(message.author.mention+" Please specify the reciever of the money")
            elif command[0] in ["gift"]:
                user = str(message.author.id)
                if len(message.mentions) > 0:
                    dest = str(message.mentions[0].id)
                    ment = message.mentions[0].mention
                    try:
                        item = command[2]
                        amount = int(command[3])
                    except:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"gift <@MENTION> <ITEM> <AMOUNT>`")
                        return
                    if item in self.database["user"][user]["inventory"]["items"]:
                        if self.database["user"][user]["inventory"]["items"][item] >= amount:
                            self.database["user"][user]["inventory"]["items"][item] -= amount
                            if self.database["user"][user]["inventory"]["items"][item] == 0:
                                self.database["user"][user]["inventory"]["items"].pop(item)
                            if item in self.database["user"][dest]["inventory"]["items"]:
                                self.database["user"][dest]["inventory"]["items"][item] += amount
                            else:
                                self.database["user"][dest]["inventory"]["items"][item] = amount
                            await message.channel.send(message.author.mention+" has given "+ment+" **"+self.nice_number(amount)+"x "+item+"**")
                        else:
                            await message.channel.send(message.author.mention+" You don't have that many of these items")
                    else:
                        await message.channel.send(message.author.mention+" You don't have that item")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"gift <@MENTION> <ITEM> <AMOUNT>`")
            elif command[0] in ["gamble", "bet", "risk"]:
                if len(command) == 2:
                    user = str(message.author.id)
                    name = message.author.name
                    try:
                        amount = int(command[1])
                    except:
                        await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"bet <AMOUNT>`")
                        return
                    if self.database["user"][user]["balance"] >= amount:
                        self.database["user"][user]["balance"] -= amount
                        r = random.randint(1, 50)
                        embed = discord.Embed()
                        embed.set_author(name=name+"'s Gambling Game", icon_url=message.author.avatar_url)
                        if r > 25:
                            embed.color = discord.Color.green()
                            self.database["user"][user]["balance"] += amount*2
                            embed.description = "You have won **"+str(amount)+" "+self.currency+"**\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency+"\n**Number rolled:** `"+str(r)+"`"
                        elif r == 25:
                            embed.color = discord.Color.orange()
                            self.database["user"][user]["balance"] += amount*11
                            embed.description = "JACKPOT! You have won **"+str(amount*10)+" "+self.currency+"**\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency+"\n**Number rolled:** `"+str(r)+"`"
                        else:
                            embed.color = discord.Color.red()
                            embed.description = "You have lost **"+str(amount)+" "+self.currency+"**\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency+"\n**Number rolled:** `"+str(r)+"`"
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(message.author.mention+" You don't have that much money")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"bet <AMOUNT>`")
            elif command[0] in ["cryptolist", "listcrypto", "cryptos", "clist"]:
                embed = discord.Embed(title="Crypto List", color=discord.Color.gold())
                prices = cryptocompare.get_price(self.cryptos, currency="USD")
                for crypto in self.cryptos:
                    embed.add_field(name=self.cryptoName[crypto]+" ("+crypto+")", value="**Price: **"+str(prices[crypto]["USD"])+" "+self.currency, inline=False)
                await message.channel.send(embed=embed)
            elif command[0] == "crypto":
                if len(command) == 2:
                    user = str(message.author.id)
                    command[1] = command[1].upper()
                    if command[1] in self.cryptos:
                        bal = 0
                        if command[1] in self.database["user"][user]["crypto"]:
                            bal = self.database["user"][user]["crypto"][command[1]]
                        embed = discord.Embed(title=self.cryptoName[command[1]], description="**Your balance: **"+str(bal), color=discord.Color.gold())
                        info = cryptocompare.get_price(command[1], "USD")[command[1]]["USD"]
                        embed.add_field(name="**Current Price:**", value=str(info)+" "+self.currency, inline=False)
                        embed.add_field(name="**Chart Here:**", value="https://cryptowat.ch/charts/KRAKEN:"+command[1]+"-USD?period=1m", inline=False)
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(message.author.mention+" That crypto does not exist")
                elif len(command) == 3:
                    user = str(message.author.id)
                    command[1] = command[1].upper()
                    if command[1] in self.cryptos:
                        bal = 0
                        if command[1] in self.database["user"][user]["crypto"]:
                            bal = self.database["user"][user]["crypto"][command[1]]
                        embed = discord.Embed(title=self.cryptoName[command[1]], description="**Your balance: **"+str(bal), color=discord.Color.gold())
                        if command[2] in ["min", "m", "minute"]:
                            embed.description = "**Chart Here:** https://cryptowat.ch/charts/KRAKEN:"+command[1]+"-USD?period=1m"
                            await message.channel.send(embed=embed)
                        elif command[2] in ["hour", "hr", "h"]:
                            embed.description = "**Chart Here:** https://cryptowat.ch/charts/KRAKEN:"+command[1]+"-USD?period=1h"
                            embed.add_field(name="**Current Price:**", value=str(price)+" "+self.currency, inline=False)
                            await message.channel.send(embed=embed)
                        elif command[2] in ["day", "dy", "d"]:
                            embed.description = "**Chart Here:** https://cryptowat.ch/charts/KRAKEN:"+command[1]+"-USD?period=1d"
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(message.author.mention+" Invalid time, please use `"+self.prefix+"crypto <CRYPTO_ID> <TIME>`")
                    else:
                        await message.channel.send(message.author.mention+" That crypto does not exist")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"crypto <CRYPTO_ID>`")
            elif command[0] in ["heist", "rob", "steal"]:
                if len(command) == 3:
                    user = str(message.author.id)
                    place = command[1]
                    if "gun" in self.database["user"][user]["inventory"]["items"]:
                        if place in ["bank", "shop"]:
                            if user not in self.database["heists"]:
                                if self.database["user"][user]["lastHeist"]+self.cooldowns["heist"] < time():
                                    if command[2] == "solo":
                                        if place == "shop":
                                            caughtChance = 10
                                            reward = random.randint(1000, 5000)
                                        elif place == "bank":
                                            reward = random.randint(5000, 50000)
                                            caughtChance = 5
                                        caught = random.randint(0, caughtChance)
                                        if caught < caughtChance-round(caughtChance/3):
                                            self.database["user"][user]["balance"] += reward
                                            await message.channel.send(message.author.mention+" You have **successfully robbed** a **"+place+"** your reward is `"+str(reward)+" "+self.currency+"`, nice job!")
                                        elif caught < caughtChance:
                                            self.database["user"][user]["balance"] -= reward*3
                                            await message.channel.send(message.author.mention+" Oh shit, you were **CAUGHT** while robbing a **"+place+"** your fine was `"+str(reward*3)+" "+self.currency+"`")
                                        else:
                                            self.database["user"][user]["inventory"]["items"]["gun"] -= 1
                                            if self.database["user"][user]["inventory"]["items"]["gun"] <= 0:
                                                self.database["user"][user]["inventory"]["items"].pop("gun")
                                            await message.channel.send(message.author.mention+" Oh shit, you were **CAUGHT BIG TIME** while robbing a **"+place+"** you are going to **JAIL**, and they have taken your gun too...")
                                            self.database["user"][user]["police"]["prison"] = True
                                            self.database["user"][user]["police"]["expire"] = round(time()+(self.cooldowns["heist"]))
                                        self.database["user"][user]["lastHeist"] = round(time())
                                    elif command[2] == "team":
                                        self.database["heists"][user] = {"robbers":[user], "place":place}
                                        await message.channel.send(message.author.mention+" Is robbing a **"+place+"**, join them with the command `"+self.prefix+"joinheist <@MENTION>`\nYou can start the heist anytime, just use `.startheist`")
                                    else:
                                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"rob <PLACE> <TEAM/SOLO>`")
                                else:
                                    t = round(self.database["user"][user]["lastHeist"]+self.cooldowns["heist"]-time())
                                    remaining = str(datetime.timedelta(seconds=t)).split(":")
                                    for i in range(len(remaining)):
                                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                            remaining[i] = remaining[i][1:]
                                    await message.channel.send(message.author.mention+" You need to wait **"+remaining[1]+" minutes and "+remaining[2]+" seconds** before participating in a heist again")
                            else:
                                await message.channel.send(message.author.mention+" You are already in a heist")
                        else:
                            await message.channel.send(message.author.mention+" You only can rob **shops** or **banks**")
                    else:
                        await message.channel.send(message.author.mention+" You need a **gun** in order to rob")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"rob <PLACE> <TEAM/SOLO>`\nPlace: *bank*/*shop*")
            elif command[0] in ["joinheist", "heistjoin"]:
                if len(message.mentions) > 0:
                    user = str(message.author.id)
                    if "gun" in self.database["user"][user]["inventory"]["items"]:
                        if str(message.mentions[0].id) in self.database["heists"]:
                            if user not in self.database["heists"]:
                                if self.database["user"][user]["lastHeist"]+self.cooldowns["heist"] < time():
                                    self.database["heists"][str(message.mentions[0].id)]["robbers"].append(user)
                                    await message.channel.send(message.author.mention+" You **successfully joined "+message.mentions[0].name+"'s** heist")
                                else:
                                    t = round(self.database["user"][user]["lastHeist"]+self.cooldowns["heist"]-time())
                                    remaining = str(datetime.timedelta(seconds=t)).split(":")
                                    for i in range(len(remaining)):
                                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                            remaining[i] = remaining[i][1:]
                                    await message.channel.send(message.author.mention+" You need to wait **"+remaining[1]+" minutes and "+remaining[2]+" seconds** before participating in a heist again")
                            else:
                                await message.channel.send(message.author.mention+" You are already in a heist")
                        else:
                            await message.channel.send(message.author.mention+" **"+message.mentions[0].name+"** currently has no planed team heists")
                    else:
                        await message.channel.send(message.author.mention+" You need a **gun** in order to rob")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"joinheist <@MENTION>`")
            elif command[0] in ["startheist", "heiststart"]:
                user = str(message.author.id)
                author = user
                if author in self.database["heists"]:
                    if self.database["heists"][author]["place"] == "shop":
                        caughtChance = 10
                        reward = random.randint(1000, 4000)
                    else:
                        reward = random.randint(2000, 10000)
                        caughtChance = 5
                    if len(self.database["heists"][author]["robbers"]) >= 2:
                        caughtChance += 2
                    info = ""
                    place = self.database["heists"][author]["place"]
                    for user in self.database["heists"][author]["robbers"]:
                        caught = random.randint(0, caughtChance)
                        if caught < caughtChance-round(caughtChance/3):
                            self.database["user"][user]["balance"] += reward
                            info += "<@"+user+"> You have **successfully robbed** a **"+place+"** your reward is `"+str(reward)+" "+self.currency+"`, nice job!\n"
                        elif caught < caughtChance:
                            self.database["user"][user]["balance"] -= reward*3
                            info += "<@"+user+"> Oh shit, you were **CAUGHT** while robbing a **"+place+"** your fine was `"+str(reward*3)+" "+self.currency+"`\n"
                        else:
                            self.database["user"][user]["inventory"]["items"]["gun"] -= 1
                            if self.database["user"][user]["inventory"]["items"]["gun"] <= 0:
                                self.database["user"][user]["inventory"]["items"].pop("gun")
                            info += "<@"+user+"> Oh shit, you were **CAUGHT BIG TIME** while robbing a **"+place+"** you are going to **JAIL**, and they have taken your gun too...\n"
                            self.database["user"][user]["police"]["prison"] = True
                            self.database["user"][user]["police"]["expire"] = round(time()+(self.cooldowns["heist"]/2))
                        self.database["user"][user]["lastHeist"] = round(time())
                    self.database["heists"].pop(author)
                    await message.channel.send(info)
                else:
                    await message.channel.send(message.author.mention+" You are not hosting any heists")
            elif command[0] == "save":
                if message.author.id == 151721375210536961:
                    self.saveDB()
                    await message.channel.send(message.author.mention+" Database saved")
            elif command[0] in ["mine", "mineing", "mining"]:
                if len(command) >= 2:
                    user = str(message.author.id)
                    if command[1] == "info":
                        embed = discord.Embed(title="Mining Info", color=discord.Color.dark_teal())
                        asicCount, btcMined, gpuCount, ethMined = 0, 0, 0, 0
                        for miner in self.database["user"][user]["mining"]:
                            if miner["name"].startswith("a"):
                                asicCount += 1
                                btcMined += round(((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/1800000), 6)
                            else:
                                gpuCount += 1
                                ethMined += round(((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/240000), 6)
                        embed.add_field(name=":hammer_pick: Asic miners ("+str(asicCount)+")", value="Your asic miners have earned "+str(round(btcMined, 6))+" BTC", inline=False)
                        embed.add_field(name=":pick: GPU miners ("+str(gpuCount)+")", value="Your GPU miners have earned "+str(round(ethMined, 4))+" ETH", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[1] == "add":
                        if len(command) >= 3:
                            amount = 1
                            if len(command) >= 4:
                                try:
                                    amount = int(command[3])
                                except:
                                    await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"mine add <MINER_ID> <AMOUNT (optional)>`")
                                    return
                            miner = command[2]
                            if miner in self.miners["asic"] or miner in self.miners["gpu"]:
                                if miner in self.database["user"][user]["inventory"]["items"]:
                                    if self.database["user"][user]["inventory"]["items"][miner] >= amount:
                                        if self.database["user"][user]["house"]["size"]-len(self.database["user"][user]["mining"]) >= amount:
                                            for _ in range(amount):
                                                self.database["user"][user]["mining"].append({"name":miner, "lastCollected":round(time())})
                                            self.database["user"][user]["inventory"]["items"][miner] -= amount
                                            if self.database["user"][user]["inventory"]["items"][miner] <= 0:
                                                self.database["user"][user]["inventory"]["items"].pop(miner)
                                            await message.channel.send(message.author.mention+" You have **successfully installed** your miner at your house (`"+str(len(self.database["user"][user]["mining"]))+"`/`"+str(self.database["user"][user]["house"]["size"])+"`)")
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have that much space in your house (`"+str(len(self.database["user"][user]["mining"]))+"`/`"+str(self.database["user"][user]["house"]["size"])+"`)")
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have that many of these miners")
                                else:
                                    await message.channel.send(message.author.mention+" You don't own that miner")
                            else:
                                await message.channel.send(message.author.mention+" That's not a valid miner ID")
                        else:
                            await message.channel.send(message.author.mention+" Please specify an miner to add, `"+self.prefix+"mine add <MINER_ID> <AMOUNT (optional)>`")
                    elif command[1] == "remove":
                        amount = 1
                        if len(command) >= 4:
                            if len(command) == 4:
                                try:
                                    amount = int(command[3])
                                except:
                                    await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"mine remove <MINER_ID> <AMOUNT (optional)>`")
                                    return
                        minerName = command[2]
                        if len(self.database["user"][user]["mining"]) >= amount:
                            remove = []
                            for miner in self.database["user"][user]["mining"]:
                                if miner["name"] == minerName and len(remove) < amount:
                                    remove.append(miner)
                            for miner in remove:
                                del self.database["user"][user]["mining"][self.database["user"][user]["mining"].index(miner)]
                                if miner["name"] in self.database["user"][user]["inventory"]["items"]:
                                    self.database["user"][user]["inventory"]["items"][miner["name"]] += 1
                                else:
                                    self.database["user"][user]["inventory"]["items"][miner["name"]] = 1
                            if len(remove) > 0:
                                await message.channel.send(message.author.mention+" `"+str(len(remove))+"x` miners were removed")
                            else:
                                await message.channel.send(message.author.mention+" There is no miner running with the model name `"+minerName+"`")
                        else:
                            await message.channel.send(message.author.mention+" You dont have that many miners running")
                    elif command[1] == "collect":
                        if len(self.database["user"][user]["mining"]) > 0:
                            btcMined, ethMined, i = 0, 0, 0
                            for miner in self.database["user"][user]["mining"]:
                                if miner["name"].startswith("a"):
                                    btcMined += round(((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/1800000), 6)
                                    self.database["user"][user]["electricity"] += ((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/150)
                                else:
                                    ethMined += round(((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/240000), 4)
                                    self.database["user"][user]["electricity"] += ((time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/300)
                                self.database["user"][user]["mining"][i]["lastCollected"] = round(time())
                                i += 1
                            btcMined = round(btcMined, 6)
                            ethMined = round(ethMined, 4)
                            if btcMined > 0:
                                if "BTC" in self.database["user"][user]["crypto"]:
                                    self.database["user"][user]["crypto"]["BTC"] += btcMined
                                else:
                                    self.database["user"][user]["crypto"]["BTC"] = btcMined
                            if ethMined > 0:
                                if "ETH" in self.database["user"][user]["crypto"]:
                                    self.database["user"][user]["crypto"]["ETH"] += ethMined
                                else:
                                    self.database["user"][user]["crypto"]["ETH"] = ethMined
                            await message.channel.send(message.author.mention+" You have collected `"+str(btcMined)+" BTC` and `"+str(ethMined)+" ETH`")
                        else:
                            await message.channel.send(message.author.mention+" You don't have any miners running")
                else:
                    await message.channel.send(message.author.mention+" Please specify an action (**info**/**add**/**remove**/**collect**)")
            elif command[0] in ["sizecalc", "calcsize", "scalc", "calcs"]:
                if len(command) == 4:
                    try:
                        amount = float(command[1])
                    except:
                        await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"sizecalc <NUMBER> <SIZE> <TO_SIZE>`\nExample: `"+self.prefix+"sizecalc 1000 grams kilo`")
                        return
                    base = amount
                    source, dest = "grams", "grams"
                    if command[2] in ["kilo", "kilos", "kg", "k", "kilogram", "kilograms"]:
                        amount *= 1000
                        source = "kilos"
                    elif command[2] in ["ton", "t", "tons"]:
                        amount *= 1000000
                        source = "tons"
                    if command[3] in ["kilo", "kilos", "kg", "k", "kilogram", "kilograms"]:
                        amount /= 1000
                        dest = "kilos"
                    elif command[3] in ["ton", "t", "tons"]:
                        amount /= 1000000
                        dest = "tons"
                    if str(base).split(".")[-1] == "0":
                        base = int(base)
                    if str(amount).split(".")[-1] == "0":
                        amount = int(amount)
                    await message.channel.send(message.author.mention+" `"+str(base)+"` "+source+" is `"+str(amount)+"` "+dest)
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"sizecalc <NUMBER> <SIZE> <TO_SIZE>`\nExample: `"+self.prefix+"sizecalc 1000 grams kilo`")
            elif command[0] in ["woods", "mushroom", "mushrooms", "forest"]:
                user = str(message.author.id)
                if self.database["user"][user]["lvl"] >= 10:
                    if self.database["user"][user]["woodsTime"]+self.cooldowns["woods"] < time():
                        basketBroke = False
                        amount = 25
                        if "basket" in self.database["user"][user]["inventory"]["items"]:
                            if self.database["user"][user]["inventory"]["items"]["basket"] > 0:
                                amount += 25
                                r = random.randint(1, 10)
                                if r == 10:
                                    basketBroke = True
                        pick = []
                        for shroom in self.shrooms:
                            pick += [shroom]*self.shrooms[shroom]
                        shrooms = {"saucer":0, "knobby":0, "bohemica":0}
                        for _ in range(amount):
                            shroom = random.choice(pick)
                            shrooms[shroom] += 1
                        for shroom in shrooms:
                            if shrooms[shroom] > 0:
                                if shroom in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][shroom] += shrooms[shroom]
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][shroom] = shrooms[shroom]
                        if basketBroke:
                            self.database["user"][user]["inventory"]["items"]["basket"] -= 1
                            if self.database["user"][user]["inventory"]["items"]["basket"] <= 0:
                                self.database["user"][user]["inventory"]["items"].pop("basket")
                            await message.channel.send(message.author.mention+" **You fell in the woods and you broke your basket!**\nYou have collected `"+str(shrooms["saucer"])+"x` saucers, `"+str(shrooms["knobby"])+"x` knobbies and `"+str(shrooms["bohemica"])+"x` bohemicas")
                        else:
                            await message.channel.send(message.author.mention+" You went to the woods and collected `"+str(shrooms["saucer"])+"x` saucers, `"+str(shrooms["knobby"])+"x` knobbies and `"+str(shrooms["bohemica"])+"x` bohemicas")
                        self.database["user"][user]["woodsTime"] = round(time())
                    else:
                        remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["woodsTime"]+self.cooldowns["woods"]-time()))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        await message.channel.send(message.author.mention+" You need to wait **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds** to visit the woods again")
                else:
                    await message.channel.send(message.author.mention+" You need to be **level 10** before you can collect shrooms")
            elif command[0] in ["gangdeal", "gdeal", "gang", "dealgang", "dealgangs"]:
                user = str(message.author.id)
                name = message.author.name
                mention = False
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                    mention = True
                if self.database["user"][user]["gang"] != None:
                    if len(command) <= 1:
                        embed = discord.Embed(title=name+"'s Gang Info", color=discord.Color.dark_red())
                        embed.add_field(name="Drug", value="They want **"+self.drugName[self.database["user"][user]["gang"]["drug"]]+"**", inline=False)
                        embed.add_field(name="Max Amount", value="They will buy **"+self.nice_number(self.database["user"][user]["gang"]["maxAmount"])+" grams** at MAX", inline=False)
                        embed.add_field(name="Quality", value="They want at least **90** quality", inline=False)
                        embed.add_field(name="Price", value="They will buy at a price of **"+str(round(self.sellPrice[self.database["user"][user]["gang"]["drug"]]/100*150))+" per gram**", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[1] in ["remove", "new", "delete", "rm", "del"] and not mention:
                        self.database["user"][user]["gang"] = None
                        await message.channel.send(message.author.mention+" You have abandoned your gang, you better watch out...")
                    elif not mention:
                        try:
                            amount = command[1]
                            if amount != "max":
                                amount = int(command[1])
                        except:
                            await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"gang <AMOUNT>`")
                            return
                        deal = self.database["user"][user]["gang"]
                        if deal["lastDeal"]+self.cooldown["gang"] < time():
                            if amount <= self.database["user"][user]["gang"]["maxAmount"]:
                                iMix = None
                                for mix in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                                    if mix["drug"] == deal["drug"] and mix["amount"] >= amount and mix["quality"] >= 90:
                                        iMix = mix
                                    elif amount == "max" and mix["drug"] == deal["drug"] and mix["quality"] >= 90:
                                        iMix = mix
                                        amount = iMix["amount"]
                                if iMix != None:
                                    price = round(amount*(self.sellPrice[deal["drug"]]/100*150))
                                    price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                                    self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] -= amount
                                    if self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] <= 0:
                                        del self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]
                                    self.database["user"][user]["balance"] += price
                                    await message.channel.send(message.author.mention+" You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+" mix** for `"+self.nice_number(price)+" "+self.currency+"`")
                                    self.database["user"][user]["gang"]["lastDeal"] = round(time())
                                elif deal["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    if amount == "max":
                                        amount = self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]]
                                    if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] >= amount:
                                        price = round(amount*(self.sellPrice[deal["drug"]]/100*150))
                                        price = price+(price/100*5*(self.database["user"][user]["prestige"]-1))
                                        self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] -= amount
                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] <= 0:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"].pop(deal["drug"])
                                        self.database["user"][user]["balance"] += price
                                        await message.channel.send(message.author.mention+" You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+"** for `"+self.nice_number(price)+" "+self.currency+"`")
                                        self.database["user"][user]["gang"]["lastDeal"] = round(time())
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have that much "+deal["drug"])
                                else:
                                    await message.channel.send(message.author.mention+" You don't have the requested drug")
                            else:
                                await message.channel.send(message.author.mention+" They want **"+self.nice_number(self.database["user"][user]["gang"]["amount"])+" grams** at max")
                        else:
                            remaining = str(datetime.timedelta(seconds=round(deal["lastDeal"]+self.cooldown["gang"]-time()))).split(":")
                            for i in range(len(remaining)):
                                if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                    remaining[i] = remaining[i][1:]
                            await message.channel.send(message.author.mention+" You need to wait **"+remaining[0]+" hours "+remaining[1]+" minutes and "+remaining[2]+" seconds** before you can sell to the gang again")
                    else:
                        message.channel.send(message.author.mention+" Please use `"+self.prefix+"gang <AMOUNT/remove (optional)>`")
                else:
                    if not mention:
                        name = "you"
                    await message.channel.send(message.author.mention+" Currently there are no gangs interested in "+name)
            elif command[0] == "prestige":
                user = str(message.author.id)
                if len(command) <= 1:
                    embed = discord.Embed(title="Prestige Menu", description="**If you prestige you will lose everyting accept your prestige level** (+10% sell bonus)", color=discord.Color.greyple())
                    lvl, bal = 25, 10
                    for _ in range(self.database["user"][user]["prestige"]):
                        lvl *= 2
                        bal *= 2
                    embed.add_field(name="Requirements", value="You need to have the best buildings in the game + "+str(bal)+"mil balance + lvl "+str(lvl), inline=False)
                    embed.add_field(name="Command", value="Use `"+self.prefix+"prestige confirm` to prestige", inline=False)
                    await message.channel.send(embed=embed)
                elif command[1] == "confirm":
                    lvl, bal = 25, 10
                    for _ in range(self.database["user"][user]["prestige"]):
                        lvl *= 2
                        bal *= 2
                    if self.database["user"][user]["balance"] >= bal*1000000:
                        if self.database["user"][user]["lvl"] >= lvl:
                            if self.database["user"][user]["lab"] == self.buildings["lab"][-1] and self.database["user"][user]["house"] == self.buildings["house"][-1] and self.database["user"][user]["warehouse"] == self.buildings["warehouse"][-1]:
                                self.database["user"][user] = {"name":message.author.name, "balance":1000, "house":self.starterHouse, "warehouse":None, "lab":None, "upgrades":{"lab":0}, "inventory":{"items":{}, "drugs":{"pure":{}, "mixes":[]}}, "lvl":1, "job":None, "lastJob":0, "growing":[], "producing":[], "electricity":0, "lastBill":round(time()), "deals":self.newDeals(str(message.author.id), True), "dealRefresh":round(time()), "police":{"prison":False, "expire":round(time())}, "crypto":{}, "lastHeist":0, "mining":[], "lastMsg":round(time()), "woodsTime":0, "gang":None, "prestige":self.database["user"][user]["prestige"]+1}
                                await message.channel.send(message.author.mention+" You **successfully presiged** to the **"+self.database["user"][user]["prestige"]+"th prestige** level")
                            else:
                                await message.channel.send(message.author.mention+" You are missing some buildings")
                        else:
                            await message.channel.send(message.author.mention+" You need to have at least "+str(lvl)+" level")
                    else:
                        await message.channel.send(message.author.mention+" You need to have at least "+str(bal)+" milion")
            self.database["user"][str(message.author.id)]["lastMsg"] = round(time())

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
    client.run(token, bot=True)
    client.saveDB()