import discord, os, json, datetime, random, string, cryptocompare, time, asyncio
from shell import shell
from platform import system
from math import *

# TODO LIST
# guns (gun market)
    # Make an firm that produces guns
    # Each firm has: reputation, owner, manager (other players), workers (NPC's) (unlimited (price goes up every time))
    # You need to buy supplies, then wait, then sell the guns (with risk) (unlimited cap.) (gta concept)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as ' + str(self.user))
        self.jackpotChannel = client.get_channel(840148876321226772)

    def nice_number(self, num):
        final = ""
        indx = 0
        for char in str(num).split(".")[0][::-1]:
            indx += 1
            if indx % 3 != 0:
                final += char
            else:
                final += char+" "
        final = final[::-1]
        if "." in str(num):
            final += "." + str(num).split(".")[-1]
        if final.startswith(" "):
            final = final[1:]
        return final

    def nice_price(self, price, rounded=False, roundAmount=0):
        finalPrice = str(price)
        sufix = ""
        if price >= 1000000000000000000000:
            finalPrice = str(price/1000000000000000000000)
            sufix = "sex"
        elif price >= 1000000000000000000:
            finalPrice = str(price/1000000000000000000)
            sufix = "quin"
        elif price >= 1000000000000000:
            finalPrice = str(price/1000000000000000)
            sufix = "quad"
        elif price >= 1000000000000:
            finalPrice = str(price/1000000000000)
            sufix = "tril"
        elif price >= 1000000000:
            finalPrice = str(price/1000000000)
            sufix = "bil"
        elif price >= 1000000:
            finalPrice = str(price/1000000)
            sufix = "mil"
        elif price >= 1000:
            finalPrice = str(price/1000)
            sufix = "k"
        if finalPrice.split(".")[-1] == "0":
            finalPrice = finalPrice.split(".")[0]
        if "." in finalPrice and rounded:
            finalPrice = str(round(float(finalPrice), roundAmount))
        return finalPrice + sufix

    def startup(self):
        self.prefix = "."
        self.currency = "$"
        self.databasePath = os.path.join(os.getcwd(), "database.json")
        self.autosaveInterval = 1800
        self.lastSave = time.time()
        self.database = self.loadDB()
        self.shell = shell()
        self.fullName = {"pot":":potted_plant: Flower Pot", "led":":bulb: LED Lamp", "hid":":bulb: HID Lamp", "dryer":":control_knobs: Electric Dryer", "ruderalis":":seedling: Ruderalis seeds", "sativa":":seedling: Sativa seeds", "indica":":seedling: Indica seeds", "microscope":":microscope: Microscope", "meth":":cloud: Crystal Meth Powder", "cocaine":":cloud: Cocaine Powder", "heroin":":cloud: Heroin Powder", "amp":":cloud: Amphetamine Powder", "mixer":":sake: Mixer", "wash":":soap: Washing Powder", "soda":":fog: Baking Soda", "sugar":":ice_cube: Sugar", "amf":":cloud: Amfetamin", "grape":":grapes: Grape Sugar", "gun":":gun: Gun", "a11":":hammer_pick: A11", "a10":":hammer_pick: A10", "a9":":hammer_pick: A9", ":pick: 3090rig":":pick: 3090rig", "3080rig":":pick: 3080rig", "3070rig":":pick: 3070rig", "2080rig":":pick: 2080rig", "2070rig":":pick: 2070rig", "filter":":dash: Air Filter", "basket":":basket: Wooden Basket", "tractor":":tractor: Tractor"}
        self.drugName = {"wetweed":":shamrock: Wet Weed", "weed":":herb: Weed", "meth":":cloud: Crystal Meth", "cocaine":":cloud: Cocaine", "heroin":":cloud: Herion", "amp":":cloud: Amphetamine", "sugar":":ice_cube: Sugar", "amf":":cloud: Amfetamin", "mdma":":pill: Ecstasy", "saucer":":mushroom: Flying Saucer Mushroom", "knobby":":mushroom: Knobby Tops", "bohemica":":mushroom: The Bohemian Psilocybe"}
        self.description = {"pot":"A flower pot, used to grow weed. (id => `pot`)", "led":"Cheap and not power efficient lamp. (750W) (id => `led`)", "hid":"High quality and power efficient lamp. (500W) (id => `hid`)", "dryer":"A better way to dry weed, gives you 20% more weed. (id => `dryer`)", "ruderalis":"Avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", "indica":"Grat seeds, slow growth, 30g per plant. (id => `indica`)", "microscope":"Used to analyze drugs. (id => `microscope`)", "meth":"1g powder ==> 4g crystal meth (id => `meth`)", "cocaine":"1g powder ==> 3g cocaine (id => `cocaine`)", "heroin":"1g powder ==> 4g herion (id => `heroin`)", "amp":"1g powder ==> 5g amphetamine (id => `amp`/`amphetamine`)", "mixer":"Needed to mix drugs. (id => `mixer`)", "sugar":"Used to mix drugs with. (id => `sugar`)", "wash":"Used to mix drugs with. (id => `wash`)", "soda":"Used to mix drugs with. (id => `soda`)", "amf":"1g amfetamin ==> 5g mdma (id => `amf`)", "grape":"Needed to produce MDMA (id => `grape`)", "gun":"You can rob with this thing (id => `gun`)", "a11":"You can mine bitcoin with this. (id => `a11`)", "a10":"You can mine bitcoin with this. (id => `a10`)", "a9":"You can mine bitcoin with this. (id => `a9`)", "3090rig":"You can mine ethereum with this. (id => `3090rig`)", "3080rig":"You can mine ethereum with this. (id => `3080rig`)", "3070rig":"You can mine ethereum with this. (id => `3070rig`)", "2080rig":"You can mine ethereum with this. (id => `2080rig`)", "2070rig":"You can mine ethereum with this. (id => `2070rig`)", "filter":"This boosts your weed growth. (id => `filter`)", "basket":"A better way to collect shrooms. (id => `basket`)", "tractor":"Needed in order to use a field (id => `tractor`)", "sativa":"Outdoor seeds, medium growth, 25g per plant. (id => `sativa`)"}
        self.drugDescription = {"wetweed":"You need to dry wet weed to turn it into sellable weed", "weed":"The green stuff", "meth":"White powder with good effects", "cocaine":"The most expensive drug", "heroin":"The more serious drug", "amp":"So you wanna be fast?", "mdma":"Relaxing pills", "saucer":"The most rare magic mushroom out there. (id => `saucer`)", "knobby":"Expensive and rare shroom. (id => `knobby`)", "bohemica":"The most common magic mushroom (id => `bohemica`)"}
        self.drugLvls = {"1":["weed", "amp"], "10":["meth", "saucer", "knobby", "bohemica"], "25":["cocaine", "heroin", "mdma"]}
        self.prices = {"pot":30, "led":150, "hid":1000, "dryer":2500, "ruderalis":12, "sativa":15, "indica":20, "microscope":2000, "meth":15, "cocaine":30, "heroin":10, "amp":7, "lab1":15000, "lab2":50000, "lab3":250000, "mixer":5000, "soda":5, "wash":2, "sugar":3, "amf":25, "gun":1000, "a11":20000, "a10":15000, "a9":10000, "3090rig":20000, "3080rig":12000, "3070rig":10000, "2080rig":7500, "2070rig":5000, "filter":3000, "basket":500, "tractor":50000}
        self.miners = {"asic":{"a11":200000, "a10":150000, "a9":100000}, "gpu":{"3090rig":200000, "3080rig":120000, "3070rig":100000, "2080rig":75000, "2070rig":50000}}
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
                {"type":"Large appartment", "name":"A more luxurious appartment", "size":15, "electricity":0.35, "price":150000, "id":"largeappartment"},
                {"type":"Small house", "name":"Grandma's small house", "size":40, "electricity":0.4, "price":200000, "id":"smallhouse"},
                {"type":"Medium house", "name":"Avarge house", "size":75, "electricity":0.35, "price":300000, "id":"mediumhouse"},
                {"type":"Large house", "name":"Nice and big house", "size":250, "electricity":0.3, "price":500000, "id":"largehouse"},
                {"type":"Medium mansion", "name":"A fucking mansion!", "size":750, "electricity":0.35, "price":1000000, "id":"mediummansion"},
                {"type":"Large mansion", "name":"Now this is just flex...", "size":2500, "electricity":0.3, "price":2500000, "id":"largemansion"}],
            "warehouse":[
                {"type":"Mini warehouse", "name":"Friend's garage", "size":20, "electricity":0.2, "price":20000, "id":"miniwarehouse"},
                {"type":"Small warehouse", "name":"Abadoned warehouse", "size":100, "electricity":0.2, "price":100000, "id":"smallwarehouse"},
                {"type":"Medium warehouse", "name":"A regular warehouse", "size":500, "electricity":0.15, "price":750000, "id":"mediumwarehouse"},
                {"type":"Large warehouse", "name":"A nice big place to grow stuff", "size":1250, "electricity":0.15, "price":1500000, "id":"largewarehouse"},
                {"type":"Mega warehouse", "name":"Now this is a warehouse!", "size":5000, "electricity":0.15, "price":5000000, "id":"megawarehouse"},
                {"type":"Sebko warehouse", "name":"This is a warehouse owned by sebko himself!", "size":25000, "electricity":0.20, "price":25000000, "id":"sebkowarehouse"},
                {"type":"Tesco", "name":"Tesco with weed inside?", "size":75000, "electricity":0.15, "price":500000000, "id":"tesco"},
                {"type":"Amazon", "name":"Amazon delivering weed", "size":250000, "electricity":0.15, "price":10000000000, "id":"amazon"}],
            "lab":[
                {"type":"Small lab", "name":"Friend's kitchen", "size":5, "electricity":0.35, "price":15000, "id":"smalllab"},
                {"type":"Medium lab", "name":"Normal chemical lab", "size":35, "electricity":0.3, "price":50000, "id":"mediumlab"},
                {"type":"Large lab", "name":"Modern lab", "size":100, "electricity":0.3, "price":125000, "id":"largelab"},
                {"type":"XXL lab", "name":"This is science!", "size":500, "electricity":0.25, "price":500000, "id":"xlllab"},
                {"type":"Mega lab", "name":"This is ULTRA science!", "size":1000, "electricity":0.25, "price":1000000, "id":"megalab"},
                {"type":"Ultimate lab", "name":"No were takling", "size":2500, "electricity":0.20, "price":5000000, "id":"ultimatelab"},
                {"type":"OP lab", "name":"This is getting too op", "size":7500, "electricity":0.20, "price":100000000, "id":"oplab"},
                {"type":"Wut lab", "name":"The best lab in the game", "size":25000, "electricity":0.20, "price":2500000000, "id":"wutlab"}],
            "field": [
                {"type":"Small Field", "name":"An old and cheap field", "size":50000, "electricity":0.4, "price":10000000, "id":"smallfield"},
                {"type":"Medium Field", "name":"Nice and modern field", "size":300000, "electricity":0.35, "price":250000000, "id":"mediumfield"},
                {"type":"Large Field", "name":"This is a laaaarge field", "size":1000000, "electricity":0.3, "price":3000000000, "id":"largefield"},
                {"type":"Mega Field", "name":"So much space", "size":5000000, "electricity":0.25, "price":7500000000, "id":"megafield"},
                {"type":"Omega Field", "name":"How big is this again?", "size":30000000, "electricity":0.20, "price":50000000000, "id":"omegafield"}
                ]}
        self.starterHouse = self.buildings["house"][0]
        self.buildingDB = {}
        for buildingType in self.buildings:
            for building in self.buildings[buildingType]:
                building["btype"] = buildingType
                self.buildingDB[building["id"]] = building
        self.car = {"favorit": {"engine":"stock", "turbo":None, "nitro":None}, "mustang":{"engine":"stock", "turbo":None, "nitro":None}, "gallardo":{"engine":"stock", "turbo":None, "nitro":None}, "italia":{"engine":"stock", "turbo":None, "nitro":None}, "aventador":{"engine":"stock", "turbo":"twin", "nitro":None}, "p1":{"engine":"stock", "turbo":"twin", "nitro":None}, "veyron":{"engine":"stock", "turbo":"quad", "nitro":None}, "regera":{"engine":"stock", "turbo":"twin", "nitro":None}, "bolide":{"engine":"stock", "turbo":"quad", "nitro":None}, "s15":{"engine":"stock", "turbo":None, "nitro":None}, "rs4":{"engine":"stock", "turbo":None, "nitro":None}, "e36":{"engine":"stock", "turbo":None, "nitro":None}, "supra":{"engine":"stock", "turbo":None, "nitro":None}, "urus":{"engine":"stock", "turbo":"twin", "nitro":None}, "gtr":{"engine":"stock", "turbo":None, "nitro":None}}
        self.cars = {"coupe":[("Skoda Favorit", 10000, 58, "https://upload.wikimedia.org/wikipedia/commons/f/fb/Skoda_Favorit_Utrecht_1989.jpg", "favorit"), ("Nissan Silvia s15", 100000, 250, "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Nissan_Silvia_S15_Rocket_Bunny.jpg/480px-Nissan_Silvia_S15_Rocket_Bunny.jpg", "s15"), ("Audi rs4", 1000000, 375, "https://images.pistonheads.com/nimg/36563/B5_011.jpg", "rs4"), ("BMW e36", 2500000, 282, "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/s-l1600-1592412559.jpg", "e36"), ("Toyota Supra MK4", 10000000, 220, "https://i.pinimg.com/564x/d8/76/0f/d8760f5a8ef36f8dce54e5e3e5e99dc1.jpg", "supra")],
            "sport": [("Mustang GT 5.0", 75000, 460, "https://car-images.bauersecure.com/pagefiles/25079/fordmustang2016-01.jpg", "mustang"), ("Nissan GT-R r35", 200000, 565, "https://i.pinimg.com/originals/da/c0/c9/dac0c9707901393feb2e506a8f6e8cbd.jpg", "gtr"), ("Lamborghini Gallardo", 2500000, 493, "https://www.autocar.co.uk/sites/autocar.co.uk/files/styles/gallery_slide/public/images/car-reviews/first-drives/legacy/gallardo-0638.jpg?itok=-So1NoXA", "gallardo"), ("Ferrari 458 Italia", 5000000, 562, "https://img.drivemag.net/media/default/0001/03/thumb_2493_default_large.jpeg", "italia")],
            "supercar": [("Lamborghini Aventador SVJ", 25000000, 770, "https://media.caradvice.com.au/image/private/q_auto/v1618445951/wlugwnfjwowhdctoesfm.jpg", "aventador"), ("McLaren P1", 100000000, 903, "https://ag-spots-2021.o.auroraobjects.eu/2021/03/16/thumbs/mclaren-p1-gtr-c249116032021125657_1.jpg", "p1"), ("Bugatti Veyron", 250000000, 1000, "https://preview.thenewsmarket.com/Previews/BGTI/StillAssets/1920x1080/562761_v4.jpg", "veyron"), ("Koenigsegg Regera", 500000000, 1500, "https://www.autoblog.nl/files/2020/08/koenigsegg-regera-in-het-vk-001-890x612.jpg", "regera"), ("Bugatti Bolide", 1000000000, 1825, "https://www.topgear.com/sites/default/files/styles/16x9_1280w/public/images/news-article/2020/10/b98c78ffd730bcece647d7128bb42514/20_bolide_garage_3.jpg?itok=-f_Oshzm", "bolide")],
            "suv": [("Lamborghini Urus", 25000000, 650, "https://www.topspeed.sk/userfiles/articles/16-01/17073/1579183878-lamborghini.urus.2019.1280.01.jpg", "urus")]}
        self.carPrices = {"favorit": 10000, "mustang":250000, "gallardo":2500000, "italia":5000000, "aventador":25000000, "p1":100000000, "veyron":250000000, "regera":500000000, "bolide":1000000000, "s15":100000, "rs4":1000000, "e36":2500000, "supra":10000000, "urus":25000000, "gtr":200000}
        self.carName = {"favorit": "Skoda Favorit", "mustang":"Ford Mustang GT 5.0", "gallardo":"Lamborghini Gallardo", "italia":"Ferrari 458 italia", "aventador":"Lamborghini Aventador SVJ", "p1":"McLaren P1", "veyron":"Bugatti Veyron", "regera":"Koenigsegg Regera", "bolide":"Bugatti Bolide", "s15":"Nissan Silvia s15", "rs4":"Audi rs4", "e36":"BMW e36", "supra":"Toyota Supra MK4", "urus":"Lamborghini Urus"}
        self.stockEngine = {"favorit":58, "mustang":460, "gallardo":493, "italia":562, "aventador":520, "p1":653, "veyron":250, "regera":1250, "bolide":1075, "s15":250, "rs4":375, "e36":282, "supra":220, "urus":400, "gtr":565}
        self.engines = {"v4":200, "v6":450, "v8":550, "v10":650, "v12":800, "v16":1000, "2jz":600}
        self.enginePrices = {"v4": 25000, "v6": 100000, "v8":250000, "v10":750000, "v12":1250000, "v16":2500000, "2jz":5000000, "stock":0}
        self.turbos = {"single":150, "twin":250, "quad":750}
        self.turboPrices = {"single":250000, "twin":1000000, "quad":5000000}
        self.nitros = {"single_b":250, "double":500, "triple":750}
        self.nitroPrices = {"single_b":500000, "double":2500000, "triple":10000000}
        self.sellPrice = {"weed":9, "amp":10, "meth":12, "heroin":20, "cocaine":75, "mdma":30, "saucer":130, "knobby":30, "bohemica":15}
        self.farmingItems = {"tractor":50000}
        self.cooldowns = {"dealRefresh":300, "labBoost":120, "ruderalis":600, "indica":900, "police":300, "heist":600, "msg":2, "woods":300, "saucer":2400, "knobby":1800, "bohemica":1200, "gang":7200, "sativa":1200, "smuggle":14400}
        self.cryptoName = {"BTC":"Bitcoin", "ETH":"Ethereum", "LTC":"Litecoin", "DOGE":"Dogecoin"}
        self.settings = [{"name":"Allow Tips", "desc":"Allow other players to give you money and items", "default":True, "id":"tips"}]
        self.cryptos = ["BTC", "ETH", "LTC", "DOGE"]
        self.electricityMultiplayer = 1.5
        self.jobs = {"windowcleaner":(120, 500), "youtuber":(60, 400), "programmer":(600, 5000), "mafian":(1800, 25000)}
        self.smuggleDeals = [{"dest":":flag_pl: Poland", "amount":2000000, "price":180, "risk":25}, {"dest":":flag_nl: Netherlands", "amount":5000000, "price":150, "risk":10}, {"dest":":flag_be: Belgium", "amount":1000000, "price":200, "risk":50}, {"dest":":flag_mf: France", "amount":10000000, "price":150, "risk":50}]
        self.smuggleUpgrades = [{"name":":trolleybus: Trolley Bus", "price":250000000, "size":500000}, {"name":":oncoming_bus: School Bus", "price":1000000000, "size":1000000}, {"name":":truck: Big Truck", "price":4000000000, "size":2000000}, {"name":":bus: Modern Bus", "price":10000000000, "size":4000000}]
        self.VIP = ["151721375210536961", "682644855713038384", "264127862498525186", "670545442307702794", "794223995691991052", "311033331980435479"]
        self.tips = [
            (":potted_plant: Growing Weed Tip", "Warehouses are better than a reagular house, you can list all warehouses with `"+self.prefix+"shop buildigs warehouse` and buy any warehouse with `"+self.prefix+"buy WAREHOUSE`"),
            (":potted_plant: Drying Weed Tip", "You can buy a `dryer` to get 20%+ weed when you dry it."),
            (":potted_plant: Growing Weed Tip", "You can buy a `filter` (air filter) to make your weed grow faster."),
            (":lab_coat: Lab Tip", "You can buy a `lab1`/`lab2`/`lab3` upgrade for your lab to boost your production."),
            (":moneybag: Mining Crypto Tip", "You can buy crypto miners from `mine` shop, then install them in your house with `"+self.prefix+"mine add MINER`"),
            (":electric_plug: Electricity Tip", "You can sell your `LED` lamps and buy `HID` which will not only save you a lot of money, buy also boost your weed growth"),
            (":mushroom: Magic Mushrooms Tip", "You can go to the woods and collect magic mushroom with `.woods`")]
        print("BOT IS READY")

    def loadDB(self):
        if not os.path.exists(self.databasePath):
            print("Database not found, creating a new one...")
            database = {"user":{}, "market":{"usedIDs":[]}, "heists":{}, "jackpot":{"lastPull":0}, "races":{}}
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
            if message.guild.id == 841663643644067880:
                if message.channel.id not in [841688664630231070, 841689275568488528, 841689347592814613]:
                    return
            if message.guild.id not in self.database["user"][str(message.author.id)]["guilds"]:
                self.database["user"][str(message.author.id)]["guilds"].append(message.guild.id)
            if str(message.author.id) not in self.database["user"]:
                await message.channel.send("Hey "+message.author.name+", I see that you are new aroud here. If you want to learn some tips and tricks check this out `"+self.prefix+"help tutorial`")
                self.database["user"][str(message.author.id)] = {"name":message.author.name, "balance":1000, "house":self.starterHouse, "warehouse":None, "lab":None, "field":None, "upgrades":{"lab":0, "smug":0}, "inventory":{"items":{}, "drugs":{"pure":{}, "mixes":[]}}, "lvl":1, "job":None, "lastJob":0, "growing":[], "producing":[], "electricity":0, "lastBill":round(time.time()), "deals":self.newDeals(str(message.author.id), True), "dealRefresh":round(time.time()), "police":{"prison":False, "expire":round(time.time())}, "crypto":{}, "lastHeist":0, "mining":[], "lastMsg":round(time.time()), "woodsTime":0, "gang":None, "prestige":1, "cars":{}, "activeCar":None, "scripts":[], "lastSmuggles":{"1":0, "2":0, "3":0, "4":0}, "settings":{"tips":True}, "guilds":[message.guild.id]}
            if self.database["user"][str(message.author.id)]["lastMsg"]+self.cooldowns["msg"] > time.time() and str(message.author.id) not in self.VIP:
                t = self.database["user"][str(message.author.id)]["lastMsg"]+self.cooldowns["msg"]-time.time()
                await message.channel.send(message.author.mention+" Woah, slow down, you need to wait **"+str(round(t))+" seconds** to send another command")
                return
            if self.database["user"][str(message.author.id)]["lastBill"]+86400 < time.time():
                self.database["user"][str(message.author.id)]["balance"] -= self.database["user"][str(message.author.id)]["electricity"]*self.electricityMultiplayer
                self.database["user"][str(message.author.id)]["electricity"] = 0
                self.database["user"][str(message.author.id)]["lastBill"] = round(time.time())
            if self.database["user"][str(message.author.id)]["police"]["prison"]:
                if self.database["user"][str(message.author.id)]["police"]["expire"] < time.time():
                    await message.channel.send(message.author.mention+" You ware just released from prison, be careful next time...")
                    self.database["user"][str(message.author.id)]["police"]["prison"] = False
                else:
                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][str(message.author.id)]["police"]["expire"]-time.time()))).split(":")
                    for i in range(len(remaining)):
                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                            remaining[i] = remaining[i][1:]
                    embed = discord.Embed(title="Prison", description="**"+message.author.name+" you ware caught!**\n\n**Released in:** "+str(remaining[0])+" hours "+str(remaining[1])+" minutes "+str(remaining[2])+" seconds", color=discord.Color.blue())
                    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Patch_of_the_New_York_City_Police_Department.svg/1200px-Patch_of_the_New_York_City_Police_Department.svg.png")
                    await message.channel.send(embed=embed)
                    return
            if self.lastSave+self.autosaveInterval < time.time():
                self.saveDB()
                self.lastSave = time.time()
            if self.database["jackpot"]["lastPull"]+86400 < time.time():
                if len(self.database["jackpot"]) > 1:
                    tickets, allUsers = [], []
                    for user in self.database["jackpot"]:
                        if user != "lastPull":
                            tickets += [user]*self.database["jackpot"][user]
                            if user not in allUsers:
                                allUsers.append(user)
                    winner = random.choice(tickets)
                    self.database["user"][winner]["balance"] += len(tickets)*2000
                    await self.jackpotChannel.send("New jackpot pull, its for "+str(len(tickets))+" :tickets: ("+self.nice_number(len(tickets)*2000)+" "+self.currency+")\nAnd the winner is... <@"+winner+">!\n\nCongratulations <@"+winner+"> you have just won "+self.nice_number(len(tickets)*2000)+" "+self.currency+"!!! (with "+str(round(self.database["jackpot"][winner]/len(tickets)*100, 2))+"% win chance)")
                    for user in allUsers:
                        self.database["jackpot"].pop(user)
                self.database["jackpot"]["lastPull"] = round(time.time())
            command = message.content.lower().replace("-", "")[len(self.prefix):].split(" ")
            if command[0] == "ping":
                await message.channel.send("Pong!")
            elif command[0] == "help":
                if len(command) != 2:
                    embed = discord.Embed(title="Dark Dealer Help Menu", description="Here is a simple help menu", color=discord.Color.light_gray())
                    embed.add_field(name=":rocket: Tutorial (Recommended)", value="`"+self.prefix+"help tutorial`", inline=True)
                    embed.add_field(name=":video_game: Basic game info", value="`"+self.prefix+"help info`", inline=True)
                    embed.add_field(name=":gear: List of commands", value="`"+self.prefix+"help commands`", inline=False)
                else:
                    if command[1] == "info":
                        embed = discord.Embed(title="Dark Dealer Info", description="Some informations about the game", color=discord.Color.light_gray())
                        embed.add_field(name=":satellite: Basic Info", value="This is a drug dealing game, you start by selling marijuana (weed) and amphetamine (amp), weed sells at 8 $ per gram and amp sells at 10 $ per gram.", inline=False)
                        embed.add_field(name=":electric_plug: Power", value="Yes, there is electricity in this game (you need to pay your bills). Some equipment (lamps, labs...) have a electricity consumption (in watts), you pay the bill automaticly each 24hours IRL. And yes you can go into negatives, so be careful how much money you have and what you can and cant afford...")
                        embed.add_field(name=":police_officer: Police", value="Cops can fine you and they can put you in prison, they can catch you if you use `.rob` or `.qicksell` if you don't want to get caught just awoid these 2 commands.", inline=False)
                        embed.add_field(name=":herb: Growing Weed", value="So the first step in making money, growing the green stuff. For more in depth info use `"+self.prefix+"help tutorial`", inline=False)
                        embed.add_field(name=":mag_right: Producing Powder Drugs", value="To produce powder drugs, firstly you need a lab starting from 15k. Then you need some powder to produce the drug from. Lastly you need to produce the drug `"+self.prefix+"lab produce amp 10 4`", inline=False)
                        embed.add_field(name=":dollar: Selling Drugs", value="So, selling the good stuff isn't that hard as it seems, BUT the police might be interested in participating in the deal aswell so be careful who and how you sell it to... There are 5 ways of selling drugs:\n 1. Qucksell - qucksell is the easiest and fastest method of selling drugs, but you dont make as much money here and also police are interested in investigating quicksells.\n 2. Market - Sell to other players `"+self.prefix+"market`\n 3. Deals - Sell to NPC's, more info at `"+self.prefix+"deals`\n 4. Smuggling - Risky but very proffitable, more info with `"+self.prefix+"smuggle info`\n 5. Gangs - the more endgame way of selling drugs, more info with `"+self.prefix+"gang`", inline=False)
                        embed.add_field(name=":blue_circle: Discord", value="If you need any help or want more info visit our server: https://discord.gg/hvBbaUmW9V", inline=False)
                    elif command[1] == "tutorial":
                        embed = discord.Embed(title="Dark Dealer Tutorial", color=discord.Color.light_gray())
                        embed.add_field(name=":shopping_cart: First steps (buying)", value="First you need to buy: **pots** (`pot`), **lamps** (`led`), **seeds** (`indica`/`ruderalis`). You can buy stuff with the command `"+self.prefix+"buy ITEM`.", inline=False)
                        embed.add_field(name=":potted_plant: Growing stuff (planting weed)", value="You now can plant weed in you house using the command `"+self.prefix+"grow grow SEEDS house AMOUNT`. Example command ("+self.prefix+"grow grow indica house 2)\nYou can view your growing info with the command `"+self.prefix+"grow info`.", inline=False)
                        embed.add_field(name=":scissors: Collecting (harvesting weed)", value="When your weeds has grown, you now can harvest it with the command `"+self.prefix+"grow harvest`. Now you have **Wet Weed** which you can't sell yet, you need to dry it first with the command `"+self.prefix+"grow dry`", inline=False)
                        embed.add_field(name=":money_mouth: Making $$$ (selling)", value="Last thing you need to do is sell your weed, you can view your **drug inventory** with the command `"+self.prefix+"drugs`, now you need to **create some deals** using command `"+self.prefix+"newdeals weed`, now do `.deals` to **list** all of the **new deals**. Finaly **pick the best deal** (most $ per gram) and finish it with the command `"+self.prefix+"deals DEAL_NUMBER GRAMS`", inline=False)
                    elif command[1] in ["commands", "cmds"]:
                        embed = discord.Embed(title="Dark Dealer Commands", description="`discord`, `balance`, `shops`, `shop`, `buy`, `jobs`, `job`, `work`, `inventory`, `drugs`, `buildings`, `grow`, `bills`, `levelup`, `lab`, `heist`, `levelup`, `bet`, `roll`, `calcmix`, `mix`, `crypto`, `calccrypto`, `give`, `gift`, `startheist`, `joinheist`, `mine`, `jackpot`, `smuggle`, `scirpts`, `execute`, `car`, `garage`, `race`, `tuning`, `settings`", color=discord.Color.light_gray())
                        embed.set_footer(text="Use "+self.prefix+" before each command!")
                await message.channel.send(embed=embed)
            elif command[0] == "discord":
                await message.channel.send("https://discord.gg/hvBbaUmW9V")
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
                embed.add_field(name='Prestige', value="Player is currently at prestige **level "+str(self.database["user"][user]["prestige"])+"**", inline=False)
                embed.add_field(name='Inventory', value="Player has `"+str(len(self.database["user"][user]["inventory"]["items"]))+"` different items in his inventory", inline=False)
                if self.database["user"][user]["job"] != None:
                    embed.add_field(name='Employment', value="Player is working as a **"+str(self.database["user"][user]["job"])+"**", inline=False)
                if len(self.database["user"][user]["cars"]) > 0:
                    embed.add_field(name='Garage', value="Player has **"+str(len(self.database["user"][user]["cars"]))+"x** cars in his garage", inline=False)
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
                        self.database["user"][str(message.author.id)]["lastJob"] = time.time()
                        await message.channel.send(message.author.mention+" You are now working as a "+command[1])
                    else:
                        await message.channel.send(message.author.mention+" Job with ID `"+command[1]+"` does not exist, use `"+self.prefix+"jobs` to list all available jobs and their IDs")
            elif command[0] == "work":
                job = self.database["user"][str(message.author.id)]["job"]
                if job != None:
                    reward = self.jobs[job][1]
                    cooldown = self.jobs[job][0]
                    if self.database["user"][str(message.author.id)]["lastJob"]+cooldown < time.time():
                        await message.channel.send(message.author.mention+" You have worked your shift and you earned "+self.nice_number(reward)+" "+self.currency)
                        self.database["user"][str(message.author.id)]["balance"] += reward
                        self.database["user"][str(message.author.id)]["lastJob"] = time.time()
                    else:
                        remaining = str(datetime.timedelta(seconds=round((self.database["user"][str(message.author.id)]["lastJob"]+cooldown)-time.time()))).split(":")
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
                embed.add_field(name=":race_car: Car Dealership", value="Great cars here. (id => `cars`/`car`)", inline=False)
                embed.add_field(name=":ear_of_rice: Farms", value="Everyting your farm needs. (id => `farms`/`farm`)", inline=False)
                embed.set_footer(text="You can visit any shop with "+self.prefix+"shop <SHOP_ID>")
                await message.channel.send(embed=embed)
            elif command[0] == "shop":
                if len(command) == 2 or len(command) == 3:
                    if command[1] in ["smoky", "weed"]:
                        embed = discord.Embed(title=":potted_plant: Smoky", color=discord.Color.green())
                        embed.set_thumbnail(url="https://image.freepik.com/free-vector/green-neon-sign-marijuana-leaves-cannabis-logo_1268-14217.jpg")
                        embed.add_field(name=":seedling: Ruderalis seeds - "+self.nice_number(self.prices["ruderalis"])+" "+self.currency, value="Indoor, avarage seeds, fast growth, 20g per plant. (id => `ruderalis`)", inline=False)
                        embed.add_field(name=":seedling: Sativa seeds - "+self.nice_number(self.prices["sativa"])+" "+self.currency, value="Outdoor seeds, medium growth, 25g per plant. (id => `sativa`)", inline=False)
                        embed.add_field(name=":seedling: Indica seeds - "+self.nice_number(self.prices["indica"])+" "+self.currency, value="Indoor, great seeds, slow growth, 30g per plant. (id => `indica`)", inline=False)
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
                            embed.description = "Welcome to PrimeLocation, please use `"+self.prefix+"shop primelocation <BUILDING_TYPE>` a building type is a `house`/`warehouse`/`lab`/`field`\n\n\nTip: you don't need to use the whole `primelocation` thing, you can just use `prime` or `houses`..."
                        else:
                            if command[2] in ["house", "houses", "appartment", "appartments"]:
                                for building in self.buildings["house"]:
                                    embed.add_field(name=":house: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["warehouse", "warehouses"]:
                                for building in self.buildings["warehouse"]:
                                    embed.add_field(name=":hotel: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["lab", "labs", "laboratory", "laboratories"]:
                                for building in self.buildings["lab"]:
                                    embed.add_field(name=":microscope: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                            elif command[2] in ["field", "fields"]:
                                for building in self.buildings["field"]:
                                    embed.add_field(name=":ear_of_rice: **"+building["type"]+"**", value=building["name"]+" (id => `"+building["id"]+"`)\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                        embed.set_footer(text="You can buy a building with "+self.prefix+"buy <BUILDING_ID>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["car", "cars"]:
                        embed = discord.Embed(title=":race_car: Car Dealership", color=discord.Color.red())
                        embed.set_thumbnail(url="https://www.logolynx.com/images/logolynx/91/9143ccc562cc048c073a69461ee082cd.png")
                        if len(command) >= 3:
                            if command[2] in ["suv", "coupe", "sport", "supercar"]:
                                for i in range(len(self.cars[command[2]])):
                                    car = self.cars[command[2]][i]
                                    embed.add_field(name=":red_car: "+car[0]+" - "+self.nice_number(car[1])+" "+self.currency, value="Power: "+str(car[2])+" hp (id => `"+car[4]+"`)", inline=False)
                            else:
                                embed.add_field(name="Please specify a car type", value="`"+self.prefix+"shop cars <CAR_TYPE>` (suv/coupe/sport/supercar)", inline=False)
                        else:
                            embed.add_field(name="Please specify a car type", value="`"+self.prefix+"shop cars <CAR_TYPE>` (suv/coupe/sport/supercar)", inline=False)
                        await message.channel.send(embed=embed)
                    elif command[1] in ["farm", "farms"]:
                        embed = discord.Embed(title=":ear_of_rice: Farms", color=discord.Color.red())
                        embed.set_thumbnail(url="https://www.graphicsprings.com/filestorage/stencils/5e162fad3359047d638e2b88cf2315b1.png?width=500&height=500")
                        for item in self.farmingItems:
                            embed.add_field(name=self.fullName[item]+" - "+self.nice_number(self.farmingItems[item])+" "+self.currency, value=self.description[item], inline=False)
                        await message.channel.send(embed=embed)
                    elif command[1] in self.prices:
                        amount = 0
                        user = str(message.author.id)
                        if command[1] in self.database["user"][user]["inventory"]["items"]:
                            amount = self.database["user"][user]["inventory"]["items"][command[1]]
                        embed = discord.Embed(title=self.fullName[command[1]]+" ("+self.nice_number(amount)+")", color=discord.Color.dark_gray())
                        embed.add_field(name=":moneybag: Price:", value="The price of "+self.fullName[command[1]].split(":")[-1][1:].lower()+" is **"+self.nice_number(self.prices[command[1]])+" "+self.currency+"**", inline=False)
                        embed.add_field(name=self.fullName[command[1]].split(" ")[0]+" Owned:", value="You own **"+self.nice_number(amount)+"x** this item", inline=False)
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
                    elif command[1] in self.car:
                        if command[1] not in self.database["user"][user]["cars"]:
                            if self.database["user"][user]["balance"]-self.carPrices[command[1]] >= 0:
                                self.database["user"][user]["balance"] -= self.carPrices[command[1]]
                                self.database["user"][user]["cars"][command[1]] = self.car[command[1]]
                                await message.channel.send(message.author.mention+" You have bought a "+str(self.carName[command[1]]))
                            else:
                                await message.channel.send(message.author.mention+" You can't afford that :joy:")
                        else:
                            await message.channel.send(message.author.mention+" You already own that car")
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
                    elif command[1] in self.carName:
                        self.database["user"][user]["cars"].pop(command[1])
                        if self.database["user"][user]["activeCar"] == command[1]:
                            self.database["user"][user]["activeCar"] = None
                        self.database["user"][user]["balance"] += round(self.carPrices[command[1]]/2)
                        await message.channel.send(message.author.mention+" You have sold your "+self.carName[command[1]].lower())
                    elif command[1].upper() in self.cryptos:
                        if len(command) == 3:
                            try:
                                amount = float(command[2])
                            except:
                                await message.channel.send(message.author.mention+" Please specify a valid amount to sell")
                                return
                        amount = round(amount, 6)
                        crypto = command[1].upper()
                        if crypto in self.database["user"][user]["crypto"]:
                            if self.database["user"][user]["crypto"][crypto] >= amount:
                                cryptoPrice = cryptocompare.get_price(crypto, "USD")[crypto]["USD"]
                                price = cryptoPrice*amount
                                self.database["user"][user]["balance"] += price
                                self.database["user"][user]["crypto"][crypto] -= amount
                                if self.database["user"][user]["crypto"][crypto] <= 0:
                                    self.database["user"][user]["crypto"].pop(crypto)
                                await message.channel.send(message.author.mention+" You have sold **"+str(amount)+" "+crypto+"** for `"+self.nice_number(price)+"` at price `"+str(cryptoPrice)+"` per "+crypto)
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
                        if amount >= 1000000:
                            amount = str(amount/1000000) + " tons"
                        elif amount >= 1000:
                            amount = str(amount/1000) + " kilos"
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
                        if amount >= 1000000:
                            amount = str(amount/1000000) + " tons"
                        elif amount >= 1000:
                            amount = str(amount/1000) + " kilos"
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
                    embed.add_field(name=":house: House: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["warehouse"] != None:
                    building = self.database["user"][user]["warehouse"]
                    embed.add_field(name=":hotel: Warehouse: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Grow space: "+str(building["size"])+" plants | Price: "+self.nice_price(building["price"])+" "+self.currency, inline=False)
                if self.database["user"][user]["lab"] != None:
                    building = self.database["user"][user]["lab"]
                    embed.add_field(name=":microscope: Lab: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_price(building["price"])+" "+self.currency+"\nEqupment Level: "+str(self.database["user"][user]["upgrades"]["lab"]), inline=False)
                if self.database["user"][user]["field"] != None:
                    building = self.database["user"][user]["field"]
                    embed.add_field(name=":ear_of_rice: field: **"+building["type"]+"**", value=building["name"]+"\nElectricity: "+str(building["electricity"])+" "+self.currency+" | Production capacity: "+str(building["size"])+" | Price: "+self.nice_price(building["price"])+" "+self.currency+"\nEqupment Level: "+str(self.database["user"][user]["upgrades"]["lab"]), inline=False)
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
                        places = ["house", "warehouse", "field"]
                        if len(command) > target+1:
                            if command[target+1] in places:
                                places = [command[target+1]]
                        capacity = 0
                        if "house" in places:
                            capacity = self.database["user"][user]["house"]["size"]
                        if self.database["user"][user]["warehouse"] != None and "warehouse" in places:
                            capacity += self.database["user"][user]["warehouse"]["size"]
                        if self.database["user"][user]["field"] != None and "field" in places:
                            capacity += self.database["user"][user]["field"]["size"]
                        growing, grown = 0, 0
                        topTime = 0
                        for plant in self.database["user"][user]["growing"]:
                            if plant["place"] in places:
                                if plant["growTime"] < time.time():
                                    grown += 1*plant["amount"]
                                else:
                                    if plant["growTime"] < topTime or topTime == 0:
                                        topTime = plant["growTime"]
                                    growing += 1*plant["amount"]
                        destTime = 0
                        if topTime != 0:
                            destTime = topTime-time.time()
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
                                    if command[target+3] != "max":
                                        amount = int(command[target+3])
                                except:
                                    await message.channel.send(message.author.mention+" That's not a valid number")
                                    return
                            if command[target+1] in ["sativa", "ruderalis", "indica", "saucer", "knobby", "bohemica"]:
                                if command[target+2] in ["house", "warehouse", "field"]:
                                    if self.database["user"][user][command[target+2]] != None:
                                        capacity = self.database["user"][user][command[target+2]]["size"]
                                        growing = 0
                                        for plant in self.database["user"][user]["growing"]:
                                            if plant["place"] == command[target+2]:
                                                growing += plant["amount"]
                                        if command[target+3] == "max":
                                            amount = int(capacity-growing)
                                        if amount <= 0:
                                            if command[target+3] == "max":
                                                await message.channel.send(message.author.mention+" You'r "+command[target+2]+" is full")
                                            else:
                                                await message.channel.send(message.author.mention+" You have to grow at least 1 seed")
                                            return
                                        if capacity-growing >= amount:
                                            lamps = []
                                            lamp = None
                                            pots = 0
                                            pot = False
                                            for plant in self.database["user"][user]["growing"]:
                                                if plant["place"] != "field":
                                                    lamps += [plant["lamp"]]*plant["amount"]
                                                    pots += 1*plant["amount"]
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
                                            if command[target+2] == "field":
                                                if command[target+1] != "sativa":
                                                    await message.channel.send(message.author.mention+" You can **only grow sativa** seeds on fields")
                                                    return
                                                pot = True
                                                lamp = "led"
                                            else:
                                                if command[target+1] == "sativa":
                                                    await message.channel.send(message.author.mention+" You can grow sativa seeds **only on fields*")
                                                    return
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
                                                        if "filter" in self.database["user"][user]["inventory"]["items"] and command[target+2] != "field":
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
                                                        elif command[target+1] == "sativa":
                                                            growTime = self.cooldowns["sativa"]
                                                        growTime = growTime/speed
                                                        self.database["user"][user]["growing"].append({"seeds":command[target+1], "growTime":round(time.time()+growTime), "lamp":lamp, "place":command[target+2], "amount":amount})
                                                        if command[target+2] != "field":
                                                            self.database["user"][user]["electricity"] += round((watts/1000)*(growTime/60)*amount)
                                                        remaining = str(datetime.timedelta(seconds=growTime)).split(":")
                                                        for i in range(len(remaining)):
                                                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                                remaining[i] = remaining[i][1:]
                                                        if command[target+2] != "field":
                                                            await message.channel.send(message.author.mention+" You planted "+command[target+1]+" seeds with a "+lamp+" lamp, it will take **"+remaining[1]+" minutes and "+remaining[2]+" seconds** to grow")
                                                        else:
                                                            await message.channel.send(message.author.mention+" You planted "+command[target+1]+" seeds on your field, it will take **"+remaining[1]+" minutes and "+remaining[2]+" seconds** to grow")
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
                        places = ["house", "warehouse", "field"]
                        if len(command) > target+1:
                            if command[target+1] in places:
                                places = [command[target+1]]
                        if len(self.database["user"][user]["growing"]) < 1:
                            await message.channel.send(message.author.mention+" There is nothing to harvest")
                            return
                        for plant in self.database["user"][user]["growing"]:
                            if plant["growTime"] < time.time() and plant["place"] in places:
                                if plant["seeds"] == "indica":
                                    packageSize += 30*plant["amount"]
                                elif plant["seeds"] == "ruderalis":
                                    packageSize += 20*plant["amount"]
                                elif plant["seeds"] == "saucer":
                                    shrooms["saucer"] += 7*plant["amount"]
                                elif plant["seeds"] == "knobby":
                                    shrooms["knobby"] += 15*plant["amount"]
                                elif plant["seeds"] == "bohemica":
                                    shrooms["bohemica"] += 20*plant["amount"]
                                elif plant["seeds"] == "sativa":
                                    packageSize += 25*plant["amount"]
                                collectedPlants.append(plant)
                                if plant["place"] == "field":
                                    if "tractor" not in self.database["user"][user]["inventory"]["items"]:
                                        await message.channel.send(message.author.mention+" You need an `tractor` in order to harvest weed from a field")
                                        return
                                    elif self.database["user"][user]["inventory"]["items"]["tractor"] <= 0:
                                        await message.channel.send(message.author.mention+" You need an `tractor` in order to harvest weed from a field")
                                        return
                        potBreaks = 0
                        for plant in collectedPlants:
                            del self.database["user"][user]["growing"][self.database["user"][user]["growing"].index(plant)]
                            if plant["place"] != "field":
                                potBreak = random.randint(0, round(plant["amount"]/100))
                                if potBreak > 0:
                                    self.database["user"][user]["inventory"]["items"]["pot"] -= potBreak
                                    if self.database["user"][user]["inventory"]["items"]["pot"] <= 0:
                                        self.database["user"][user]["inventory"]["items"].pop("pot")
                                potBreaks += potBreak
                        info = ""
                        if potBreaks == 1:
                            info += "Your **pot broke** while harvesting weed/shrooms!\n"
                        elif potBreaks > 1:
                            info += "Your **"+self.nice_number(potBreaks)+"x pots broke** while harvesting weed/shrooms!\n"
                        if plant["place"] == "field":
                            tractorBreak = random.randint(1, 5)
                            if tractorBreak == 5:
                                self.database["user"][user]["inventory"]["items"]["tractor"] -= 1
                                if self.database["user"][user]["inventory"]["items"]["tractor"] <= 0:
                                    self.database["user"][user]["inventory"]["items"].pop("tractor")
                                info += "Your **tractor broke** while harvesting weed!\n"
                        if packageSize > 0:
                            if "wetweed" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] += packageSize
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["wetweed"] = packageSize
                            info += "You collected "+self.nice_number(packageSize)+" grams of wet weed\n"
                        if shrooms["saucer"] > 0:
                            if "saucer" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["saucer"] += shrooms["saucer"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["saucer"] = shrooms["saucer"]
                            info += "You collected "+self.nice_number(shrooms["saucer"])+" grams of saucer\n"
                        if shrooms["knobby"] > 0:
                            if "knobby" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["knobby"] += shrooms["knobby"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["knobby"] = shrooms["knobby"]
                            info += "You collected "+self.nice_number(shrooms["knobby"])+" grams of knobby\n"
                        if shrooms["bohemica"] > 0:
                            if "bohemica" in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["bohemica"] += shrooms["bohemica"]
                            else:
                                self.database["user"][user]["inventory"]["drugs"]["pure"]["bohemica"] = shrooms["bohemica"]
                            info += "You collected "+self.nice_number(shrooms["bohemica"])+" grams of bohemica\n"
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
                remaining = str(datetime.timedelta(seconds=(self.database["user"][user]["lastBill"]+86400)-round(time.time()))).split(":")
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
                            if drug["prodTime"] < time.time():
                                collectable += 1*drug["amount"]
                            else:
                                if drug["prodTime"] < topProducing or topProducing == 0:
                                    topProducing = drug["prodTime"]
                                producing += 1*drug["amount"]
                        if topProducing != 0:
                            topProducing = round(topProducing-time.time())
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
                                        if command[target+3] != "max":
                                            produceAmount = int(command[target+3])
                                    except:
                                        return
                                if powder in self.database["user"][user]["inventory"]["items"] and powder not in self.notProduceable:
                                    producing = 0
                                    for prod in self.database["user"][user]["producing"]:
                                        producing += prod["amount"]
                                    freeCapacity = self.database["user"][user]["lab"]["size"]-producing
                                    if command[target+3] == "max":
                                        produceAmount = freeCapacity
                                    if self.database["user"][user]["inventory"]["items"][powder] >= powderAmount*produceAmount:
                                        if powderAmount <= 10:
                                            if produceAmount <= freeCapacity:
                                                if produceAmount > 0:
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
                                                    targetTime = self.producmentTime[powder]+time.time()-boost
                                                    elec = 1*round((self.producmentTime[powder]-boost)/60)
                                                    self.database["user"][user]["electricity"] += elec
                                                    self.database["user"][user]["producing"].append({"drug":powder, "reward":self.produceReward[powder]*powderAmount, "prodTime":targetTime, "amount":produceAmount})
                                                    self.database["user"][user]["inventory"]["items"][powder] -= powderAmount*produceAmount
                                                    if self.database["user"][user]["inventory"]["items"][powder] == 0:
                                                        self.database["user"][user]["inventory"]["items"].pop(powder)
                                                    remaining = str(datetime.timedelta(seconds=round(targetTime-time.time()))).split(":")
                                                    for i in range(len(remaining)):
                                                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                            remaining[i] = remaining[i][1:]
                                                    await message.channel.send(message.author.mention+" You started to produce `"+str(powderAmount)+"` grams of `"+powder+"`, production will take around **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds**")
                                                else:
                                                    if command[target+3] == "max":
                                                        await message.channel.send(message.author.mention+" You'r lab is full")
                                                    else:
                                                        await message.channel.send(message.author.mention+" You have to produce at least 1 drug")
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
                        collectable, size = [], 0
                        for drug in self.database["user"][user]["producing"]:
                            if drug["prodTime"] < time.time():
                                collectable.append(drug)
                                size += drug["amount"]
                        if len(collectable) > 0:
                            total = 0
                            for drug in collectable:
                                if drug["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][drug["drug"]] += drug["reward"]*size
                                else:
                                    self.database["user"][user]["inventory"]["drugs"]["pure"][drug["drug"]] = drug["reward"]*size
                                total += drug["reward"]*size
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
                                    await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+self.nice_number(price)+" "+self.currency+"**")
                                elif police < 20:
                                    await message.channel.send(message.author.mention+" You almost got caught by the cops, but you have successfully sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+self.nice_number(price)+" "+self.currency+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You got CAUGHT by the COPS! You will be put into prison! Also you have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" for **"+self.nice_number(price)+" "+self.currency+"**")
                                    self.database["user"][user]["police"]["prison"] = True
                                    self.database["user"][user]["police"]["expire"] = time.time()+self.cooldowns["police"]
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
                                    await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+self.nice_number(price)+" "+self.currency+"**")
                                elif police < 20:
                                    await message.channel.send(message.author.mention+" You almost got caught by the cops, but you have successfully sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+self.nice_number(price)+" "+self.currency+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You got CAUGHT by the COPS! You will be put into prison! Also you have sold "+str(amount)+" grams of"+self.drugName[command[1]].split(":")[-1].lower()+" mix for **"+self.nice_number(price)+" "+self.currency+"**")
                                    self.database["user"][user]["police"]["prison"] = True
                                    self.database["user"][user]["police"]["expire"] = time.time()+self.cooldowns["police"]
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
                if self.database["user"][user]["dealRefresh"]+self.cooldowns["dealRefresh"] < time.time():
                    if len(command) == 2:
                        deals = self.newDeals(user, False, command[1])
                        if deals != None:
                            self.database["user"][user]["deals"] = deals
                            self.database["user"][user]["dealRefresh"] = round(time.time())
                            await message.channel.send(message.author.mention+" You have successfully refreshed your deals")
                        else:
                            await message.channel.send(message.author.mention+" That drug does not exist/you are not the required level")
                    else:
                        self.database["user"][user]["deals"] = self.newDeals(user)
                        self.database["user"][user]["dealRefresh"] = round(time.time())
                        await message.channel.send(message.author.mention+" You have successfully refreshed your deals")
                else:
                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["dealRefresh"]+self.cooldowns["dealRefresh"]-time.time()))).split(":")
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
                        await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams for **"+self.nice_number(price)+" "+self.currency+"**")
                        if self.database["user"][user]["gang"] == None:
                            gang = random.randint(1, 25)
                            if gang == 25:
                                self.database["user"][user]["gang"] = {"drug":deal["drug"], "maxAmount":amount*10, "lastDeal":0}
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
                            await message.channel.send(message.author.mention+" You have sold "+str(amount)+" grams for **"+self.nice_number(price)+" "+self.currency+"**")
                            if self.database["user"][user]["gang"] == None:
                                gang = random.randint(1, 25)
                                if gang == 25:
                                    self.database["user"][user]["gang"] = {"drug":deal["drug"], "maxAmount":amount*10, "lastDeal":0}
                                    await message.channel.send(message.author.mention+" A **gang** just showed up and they want to cooperate with you, you can make **BIG MONEY**!!!\n`"+self.prefix+"gang` for more info")
                        else:
                            await message.channel.send(message.author.mention+" You don't have that much "+self.drugName[deal["drug"]].split(":")[-1][1:].lower())
                    else:
                        await message.channel.send(message.author.mention+" You don't have the requested drug")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"deal <DEAL_NUMBER> <AMOUNT>`")
            elif command[0] in ["smuggle", "smuggleing", "smuggling", "smug"]:
                user = str(message.author.id)
                if self.database["user"][user]["lvl"] >= 50:
                    if len(command) > 1:
                        if command[1] in ["info", "list"]:
                            embed = discord.Embed(title="Smuggle Deals", color=discord.Color.dark_orange())
                            bonus = 0
                            if self.database["user"][user]["upgrades"]["smug"] != 0:
                                bonus = self.smuggleUpgrades[self.database["user"][user]["upgrades"]["smug"]-1]["size"]
                            for i in range(len(self.smuggleDeals)):
                                deal = self.smuggleDeals[i]
                                status = ":no_entry_sign:"
                                if self.database["user"][user]["lastSmuggles"][str(i+1)]+self.cooldowns["smuggle"] < time.time():
                                    status = ":white_check_mark:"
                                embed.add_field(name=str(i+1)+". "+deal["dest"]+" "+status, value="Maximum amount: **"+str((deal["amount"]+bonus)/1000000)+"tons**, Payment: **"+str(deal["price"]/100)+"x "+self.currency+"**, Risk: **"+str(deal["risk"])+" %**", inline=False)
                            embed.set_footer(text="Smuggle drugs with "+self.prefix+"smuggle <DEAL_ID> <DRUG> <DRUG_AMUNT>")
                            await message.channel.send(embed=embed)
                        elif command[1] in ["upgrade", "upgr", "upgrades", "up" ,"upg"]:
                            if len(command) < 3:
                                embed = discord.Embed(title="Smuggle Upgrades", color=discord.Color.dark_orange())
                                for i in range(len(self.smuggleUpgrades)):
                                    upgrade = self.smuggleUpgrades[i]
                                    embed.add_field(name=str(i+1)+". "+upgrade["name"]+" - "+self.nice_price(upgrade["price"])+" "+self.currency, value="Size: +"+self.nice_number(upgrade["size"])+" grams", inline=False)
                                if self.database["user"][user]["upgrades"]["smug"] != 0:
                                    embed.add_field(name="Your upgrade:", value=str(self.database["user"][user]["upgrades"]["smug"])+". upgrade", inline=False)
                                embed.set_footer(text="Buy upgrades with "+self.prefix+"smuggle upgrade <UPGRADE_ID>")
                                await message.channel.send(embed=embed)
                            else:
                                try:
                                    upgradeID = int(command[2])-1
                                    upgrade = self.smuggleUpgrades[upgradeID]
                                except:
                                    await message.channel.send(message.author.mention+" Invalid upgrade number")
                                    return
                                self.database["user"][user]["upgrades"]["smug"] = upgradeID+1
                        else:
                            if len(command) >= 4:
                                try:
                                    dealID = int(command[1])
                                    if command[3] != "max":
                                        amount = int(command[3])
                                    drug = command[2]
                                    deal = self.smuggleDeals[dealID-1]
                                except:
                                    await message.channel.send(message.author.mention+" **Invalid number**, please use `"+self.prefix+"smuggle <DEAL_ID> <DRUG> <AMOUNT>`")
                                    return
                                if drug in self.sellPrice:
                                    if drug in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                        if command[3] == "max":
                                            amount = self.database["user"][user]["inventory"]["drugs"]["pure"][drug]
                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][drug] >= amount:
                                            truck = ":pickup_truck: small truck"
                                            if self.database["user"][user]["upgrades"]["smug"] > 0:
                                                deal["amount"] += self.smuggleUpgrades[self.database["user"][user]["upgrades"]["smug"]-1]["size"]
                                                truck = self.smuggleUpgrades[self.database["user"][user]["upgrades"]["smug"]-1]["name"].lower()
                                            if deal["amount"] >= amount:
                                                if self.database["user"][user]["lastSmuggles"][str(dealID)]+self.cooldowns["smuggle"] < time.time():
                                                    price = round(self.sellPrice[drug]/100*deal["price"]*amount)
                                                    price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                                                    self.database["user"][user]["inventory"]["drugs"]["pure"][drug] -= amount
                                                    if self.database["user"][user]["inventory"]["drugs"]["pure"][drug] <= 0:
                                                        self.database["user"][user]["inventory"]["drugs"]["pure"].pop(drug)
                                                    c = round(1/(deal["risk"]/100))
                                                    caught = random.randint(1, c)
                                                    if caught == c:
                                                        await message.channel.send(message.author.mention+" Oh shiiit, you where **CAUGHT** on the border, you lost `"+self.nice_number(amount)+"grams` of `"+drug+"` ("+self.nice_number(price)+" "+self.currency+")")
                                                    else:
                                                        self.database["user"][user]["balance"] += price
                                                        await message.channel.send(message.author.mention+" You have **successfully smuggled** `"+self.nice_number(amount)+"grams` of `"+drug+"` into **"+deal["dest"]+"**\nProfit: `"+self.nice_number(price)+" "+self.currency+"`")
                                                    self.database["user"][user]["lastSmuggles"][str(dealID)] = round(time.time())
                                                else:
                                                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["lastSmuggles"][str(dealID)]+self.cooldowns["smuggle"]-time.time()))).split(":")
                                                    for i in range(len(remaining)):
                                                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                                            remaining[i] = remaining[i][1:]
                                                    await message.channel.send(message.author.mention+" You need to wait **"+remaining[0]+" hours, "+remaining[1]+" minutes and "+remaining[2]+" seconds** before smuggling into "+deal["dest"]+" again")
                                            else:
                                                await message.channel.send(message.author.mention+" **Invalid amount**, you can only smuggle `"+self.nice_number(deal["amount"])+"grams` at max")
                                        else:
                                            await message.channel.send(message.author.mention+" **Invalid amount**, you have only `"+self.nice_number(self.database["user"][user]["inventory"]["drugs"]["pure"][drug])+"grams` of "+drug)
                                    else:
                                        await message.channel.send(message.author.mention+" You don't have the **requested drug** (you can only smuggle quality 100 drugs)")
                                else:
                                    await message.channel.send(message.author.mention+" **Invalid drug**, please use `"+self.prefix+"smuggle <DEAL_ID> <DRUG> <AMOUNT>`")
                            else:
                                await message.channel.send(message.author.mention+" Please use `"+self.prefix+"smuggle list/upgrade/DEAL_ID`")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"smuggle list/upgrade/DEAL_ID`")
                else:
                    await message.channel.send(message.author.mention+" You need to be at least **level 50** to smuggle drugs")
            elif command[0] == "market":
                user = str(message.author.id)
                name = message.author.name
                if len(command) == 1:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"market <DRUG_ID>` to view the market, for info: `"+self.prefix+"market info`")
                elif len(command) == 2:
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
                else:
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
                    targetName = message.mentions[0].name
                    try:
                        amount = int(command[2])
                    except:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"give <@MENTION> <AMOUNT>`")
                        return
                    if self.database["user"][dest]["lvl"] >= 15:
                        if self.database["user"][dest]["settings"]["tips"]:
                            if self.database["user"][user]["balance"] >= amount:
                                self.database["user"][user]["balance"] -= amount
                                self.database["user"][dest]["balance"] += amount
                                await message.channel.send(message.author.mention+" has given "+ment+" **"+self.nice_number(amount)+" "+self.currency+"**")
                            else:
                                await message.channel.send(message.author.mention+" You don't have that much money")
                        else:
                            await message.channel.send(message.author.mention+" "+targetName+" doesen't accept any donations")
                    else:
                        await message.channel.send(message.author.mention+" "+targetName+" needs to be at least lvl 15 to accept donations")
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
                    if self.database["user"][dest]["lvl"] >= 15:
                        if self.database["user"][dest]["settings"]["tips"]:
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
                            await message.channel.send(message.author.mention+" "+targetName+" doesen't accept any donations")
                    else:
                        await message.channel.send(message.author.mention+" "+targetName+" needs to be at least lvl 15 to accept donations")
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
            elif command[0] in ["luckyroll", "luck", "roll", "rl", "lroll", "luckyr"]:
                if len(command) >= 2:
                    roll = 1
                    if len(command) == 3:
                        try:
                            roll = int(command[2])
                        except:
                            await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"roll <AMOUNT> <AMOUNT (optional)>`")
                            return
                    user = str(message.author.id)
                    name = message.author.name
                    try:
                        amount = int(command[1])
                    except:
                        await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"roll <AMOUNT>`")
                        return
                    if roll == 1:
                        if self.database["user"][user]["balance"] >= amount:
                            self.database["user"][user]["balance"] -= amount
                            r = random.randint(1, 100)
                            embed = discord.Embed()
                            embed.set_author(name=name+"'s Lucky Roll", icon_url=message.author.avatar_url)
                            if r == 100:
                                embed.color = discord.Color.orange()
                                self.database["user"][user]["balance"] += amount*100
                                embed.description = "JACKPOT! You have won **"+str(amount*100)+" "+self.currency+"**\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency+"\n**Number rolled:** `"+str(r)+"`"
                            else:
                                embed.color = discord.Color.red()
                                embed.description = "You have lost **"+str(amount)+" "+self.currency+"**\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency+"\n**Number rolled:** `"+str(r)+"`"
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(message.author.mention+" You don't have that much money")
                    else:
                        embed = discord.Embed()
                        embed.set_author(name=name+"'s Lucky Roll", icon_url=message.author.avatar_url)
                        win = 0
                        lost = 0
                        for _ in range(roll):
                            if self.database["user"][user]["balance"] >= amount:
                                r = random.randint(1, 100)
                                if r == 100:
                                    win += amount*100
                                    self.database["user"][user]["balance"] += amount*100
                                else:
                                    lost += amount
                                    self.database["user"][user]["balance"] -= amount
                            else:
                                break
                        if win > lost:
                            embed.color = discord.Color.green()
                        else:
                            embed.color = discord.Color.red()
                        embed.description = "You have won **"+str(win)+" "+self.currency+"**\n"+"You have lost **"+str(lost)+" "+self.currency+"**"+"\n\n**Your new balance:** "+str(self.database["user"][user]["balance"])+" "+self.currency
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"roll <AMOUNT>`")
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
            elif command[0] in ["rich", "top", "best"]:
                guild = message.guild.id
                unsorted = []
                for user in self.database["user"]:
                    if guild in self.database["user"][user]["guilds"]:
                        unsorted.append(self.database["user"][user])
                        unsorted[-1]["id"] = int(user)
                sort = sorted(unsorted, key = lambda i: i["balance"])
                leaderBoard = []
                for x in range(len(sort)):
                    i = len(sort)-(x+1)
                    leaderBoard.append(sort[i])
                embed = discord.Embed(title="Richest people in "+message.guild.name, color=discord.Color.gold())
                richTable = ""
                myPos = 0
                for i in range(len(leaderBoard)):
                    if i < 10:
                        richTable += str(i+1)+". **"+ leaderBoard[i]["name"] + "** - " + self.nice_price(leaderBoard[i]["balance"], True, 1) + " " + self.currency+"\n"
                    elif myPos != 0:
                        break
                    if myPos == 0:
                        if leaderBoard[i]["id"] == message.author.id:
                            myPos = i+1
                embed.description = richTable[:-1]
                embed.set_footer(text="You are "+str(myPos)+".")
                await message.channel.send(embed=embed)
            elif command[0] in ["heist", "rob", "steal"]:
                if len(command) == 3:
                    user = str(message.author.id)
                    place = command[1]
                    if "gun" in self.database["user"][user]["inventory"]["items"]:
                        if place in ["bank", "shop"]:
                            if user not in self.database["heists"]:
                                if self.database["user"][user]["lastHeist"]+self.cooldowns["heist"] < time.time():
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
                                            self.database["user"][user]["police"]["expire"] = round(time.time()+(self.cooldowns["heist"]))
                                        self.database["user"][user]["lastHeist"] = round(time.time())
                                    elif command[2] == "team":
                                        self.database["heists"][user] = {"robbers":[user], "place":place}
                                        await message.channel.send(message.author.mention+" Is robbing a **"+place+"**, join them with the command `"+self.prefix+"joinheist <@MENTION>`\nYou can start the heist anytime, just use `.startheist`")
                                    else:
                                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"rob <PLACE> <TEAM/SOLO>`")
                                else:
                                    t = round(self.database["user"][user]["lastHeist"]+self.cooldowns["heist"]-time.time())
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
                                if self.database["user"][user]["lastHeist"]+self.cooldowns["heist"] < time.time():
                                    self.database["heists"][str(message.mentions[0].id)]["robbers"].append(user)
                                    await message.channel.send(message.author.mention+" You **successfully joined "+message.mentions[0].name+"'s** heist")
                                else:
                                    t = round(self.database["user"][user]["lastHeist"]+self.cooldowns["heist"]-time.time())
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
                            self.database["user"][user]["police"]["expire"] = round(time.time()+(self.cooldowns["heist"]/2))
                        self.database["user"][user]["lastHeist"] = round(time.time())
                    self.database["heists"].pop(author)
                    await message.channel.send(info)
                else:
                    await message.channel.send(message.author.mention+" You are not hosting any heists")
            elif command[0] == "save":
                if message.author.id == 151721375210536961:
                    self.saveDB()
                    await message.channel.send(message.author.mention+" Database saved")
            elif command[0] == "load":
                if message.author.id == 151721375210536961:
                    self.database = self.loadDB()
                    await message.channel.send(message.author.mention+" Database loaded")
            elif command[0] in ["mine", "mineing", "mining"]:
                if len(command) >= 2:
                    user = str(message.author.id)
                    if command[1] == "info":
                        embed = discord.Embed(title="Mining Info", color=discord.Color.dark_teal())
                        asicCount, btcMined, gpuCount, ethMined = 0, 0, 0, 0
                        for miner in self.database["user"][user]["mining"]:
                            if miner["name"].startswith("a"):
                                asicCount += 1*miner["amount"]
                                btcMined += round(((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/1800000)*miner["amount"], 6)
                            else:
                                gpuCount += 1*miner["amount"]
                                ethMined += round(((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/240000)*miner["amount"], 6)
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
                                            minerFound = False
                                            for m in self.database["user"][user]["mining"]:
                                                if m["name"] == miner:
                                                    minerFound = True
                                                    break
                                            if minerFound:
                                                self.database["user"][user]["mining"][self.database["user"][user]["mining"].index(m)]["amount"] += amount
                                            else:
                                                self.database["user"][user]["mining"].append({"name":miner, "lastCollected":round(time.time()), "amount":amount})
                                            self.database["user"][user]["inventory"]["items"][miner] -= amount
                                            if self.database["user"][user]["inventory"]["items"][miner] <= 0:
                                                self.database["user"][user]["inventory"]["items"].pop(miner)
                                            await message.channel.send(message.author.mention+" You have **successfully installed** your miner at your house")
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have that much space in your house")
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
                                if miner["name"] == minerName and miner["amount"] >= amount:
                                    remove.append(miner)
                                    break
                            for miner in remove:
                                self.database["user"][user]["mining"][self.database["user"][user]["mining"]]["amount"] -= amount
                                if self.database["user"][user]["mining"][self.database["user"][user]["mining"]]["amount"] <= 0:
                                    del self.database["user"][user]["mining"][self.database["user"][user]["mining"].index(miner)]
                                if miner["name"] in self.database["user"][user]["inventory"]["items"]:
                                    self.database["user"][user]["inventory"]["items"][miner["name"]] += 1*amount
                                else:
                                    self.database["user"][user]["inventory"]["items"][miner["name"]] = 1*amount
                            if len(remove) > 0:
                                await message.channel.send(message.author.mention+" `"+str(len(remove)*amount)+"x` miners were removed")
                            else:
                                await message.channel.send(message.author.mention+" There are not that many miners running with the model name `"+minerName+"`")
                        else:
                            await message.channel.send(message.author.mention+" You dont have that many miners running")
                    elif command[1] == "collect":
                        if len(self.database["user"][user]["mining"]) > 0:
                            btcMined, ethMined, i = 0, 0, 0
                            for miner in self.database["user"][user]["mining"]:
                                if miner["name"].startswith("a"):
                                    btcMined += round(((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/1800000), 6)*miner["amount"]
                                    self.database["user"][user]["electricity"] += ((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/500)*miner["amount"]
                                else:
                                    ethMined += round(((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/240000), 4)*miner["amount"]
                                    self.database["user"][user]["electricity"] += ((time.time()-miner["lastCollected"])/60/60)*(self.hashRate[miner["name"]]/1000)*miner["amount"]
                                self.database["user"][user]["mining"][i]["lastCollected"] = round(time.time())
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
            elif command[0] in ["garage", "cars", "carlist", "mycars"]:
                user = str(message.author.id)
                name = message.author.name
                if len(message.mentions) > 0:
                    user = str(message.mentions[0].id)
                    name = message.mentions[0].name
                embed = discord.Embed(title=name+"'s Garage", color=discord.Color.dark_blue())
                if len(self.database["user"][user]["cars"]) == 0:
                    embed.add_field(name="Empty", value=name+" has no cars in his garage")
                else:
                    for carName in self.database["user"][user]["cars"]:
                        car = self.database["user"][user]["cars"][carName]
                        power = 0
                        if car["engine"] == "stock":
                            power += self.stockEngine[carName]
                        else:
                            power += self.engines[car["engine"]]
                        if car["nitro"] != None:
                            power += self.nitros[car["nitro"]]
                        if car["turbo"] != None:
                            power += self.turbos[car["turbo"]]
                        embed.add_field(name=":red_car: "+self.carName[carName]+" (`"+carName+"`)", value=":video_camera: Engine: "+str(car["engine"])+" | :dash: Turbo: "+str(car["turbo"])+" | :fire: Nitro: "+str(car["nitro"])+" bottle | :zap: Power: "+str(round(power))+" hp", inline=False)
                await message.channel.send(embed=embed)
            elif command[0] in ["car", "changecar"]:
                user = str(message.author.id)
                if len(self.database["user"][user]["cars"]) > 0:
                    if len(command) >= 2:
                        if command[1] in self.carName:
                            if command[1] in self.database["user"][user]["cars"]:
                                embed = discord.Embed(title=self.carName[command[1]], color=discord.Color.dark_blue())
                                carFound = False
                                for carType in self.cars:
                                    for scar in self.cars[carType]:
                                        if scar[4] == command[1]:
                                            carFound = True
                                            break
                                    if carFound:
                                        break
                                embed.set_thumbnail(url=scar[3])
                                car = self.database["user"][user]["cars"][command[1]]
                                power = 0
                                if car["engine"] == "stock":
                                    power += self.stockEngine[command[1]]
                                else:
                                    power += self.engines[car["engine"]]
                                if car["nitro"] != None:
                                    power += self.nitros[car["nitro"]]
                                if car["turbo"] != None:
                                    power += self.turbos[car["turbo"]]
                                embed.add_field(name=":video_camera: Engine", value=str(car["engine"]), inline=False)
                                embed.add_field(name=":dash: Turbo", value=str(car["turbo"]), inline=False)
                                embed.add_field(name=":fire: Nitro", value=str(car["nitro"])+" bottle", inline=False)
                                embed.add_field(name=":zap: Power", value=str(power)+" hp", inline=False)
                                self.database["user"][user]["activeCar"] = command[1]
                                await message.channel.send(embed=embed)
                            else:
                                await message.channel.send(message.author.mention+" You dont own that car")
                        else:
                            await message.channel.send(message.author.mention+" That car does not exist")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"car <CAR_ID>`")
                else:
                    await message.channel.send(message.author.mention+" You don't own any cars :joy:")
            elif command[0] in ["tuning", "tune"]:
                user = str(message.author.id)
                if self.database["user"][user]["activeCar"] != None:
                    if len(command) <= 1:
                        carName = self.database["user"][user]["activeCar"]
                        carFound = False
                        for carType in self.cars:
                            for scar in self.cars[carType]:
                                if scar[4] == carName:
                                    carFound = True
                                    break
                            if carFound:
                                break
                        car = self.database["user"][user]["cars"][carName]
                        power = 0
                        if car["engine"] == "stock":
                            power += self.stockEngine[carName]
                        else:
                            power += self.engines[car["engine"]]
                        if car["nitro"] != None:
                            power += self.nitros[car["nitro"]]
                        if car["turbo"] != None:
                            power += self.turbos[car["turbo"]]
                        turboList, nitroList, engineList = "", "", ""
                        for turbo in self.turbos:
                            turboList += "**"+turbo+"** - "+str(self.turbos[turbo])+" hp ("+self.nice_price(self.turboPrices[turbo])+" "+self.currency+") | "
                        for nitro in self.nitros:
                            nitroList += "**"+nitro+"** - "+str(self.nitros[nitro])+" hp ("+self.nice_price(self.nitroPrices[nitro])+" "+self.currency+") | "
                        for engine in self.engines:
                            if engine == "2jz":
                                engineList += "**"+engine+" (customised)** - "+str(self.engines[engine])+" hp ("+self.nice_price(self.enginePrices[engine])+" "+self.currency+") | "
                            else:
                                engineList += "**"+engine+"** - "+str(self.engines[engine])+" hp ("+self.nice_price(self.enginePrices[engine])+" "+self.currency+") | "
                        turboList = turboList[:-3]
                        nitroList = nitroList[:-3]
                        engineList = engineList[:-3]
                        embed = discord.Embed(title="Tuning Shop", description="**"+self.carName[carName]+"**\n__**SHOP:**__\n - :video_camera: **Swapable Engines:**\n"+engineList+"\n - :dash: **Turbo List:**\n"+turboList+"\n - :fire: **Nitro List:**\n"+nitroList+"\n"+"-"*77, color=discord.Color.dark_blue())
                        embed.set_thumbnail(url=scar[3])

                        embed.add_field(name=":video_camera: Engine", value=str(car["engine"]), inline=False)
                        embed.add_field(name=":dash: Turbo", value=str(car["turbo"]), inline=False)
                        embed.add_field(name=":fire: Nitro", value=str(car["nitro"])+" bottle", inline=False)

                        embed.add_field(name=":zap: Stock Power", value=str(scar[2])+" hp", inline=True)
                        embed.add_field(name=":zap: Current Power", value=str(power)+" hp", inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        if command[1] in self.enginePrices:
                            if self.database["user"][user]["balance"] >= self.enginePrices[command[1]]:
                                if self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["engine"] != command[1]:
                                    self.database["user"][user]["balance"] -= self.enginePrices[command[1]]
                                    self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["engine"] = command[1]
                                    await message.channel.send(message.author.mention+" You have swapped an **"+command[1]+" engine** in your **"+self.carName[self.database["user"][user]["activeCar"]].lower()+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You already have that engine in your car")
                            else:
                                await message.channel.send(message.author.mention+" You can't afford that :joy:")
                        elif command[1] in self.turboPrices:
                            if self.database["user"][user]["balance"] >= self.turboPrices[command[1]]:
                                if str(self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["turbo"]) != command[1]:
                                    self.database["user"][user]["balance"] -= self.turboPrices[command[1]]
                                    self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["turbo"] = command[1]
                                    await message.channel.send(message.author.mention+" You have put an **"+command[1]+" turbo** in your **"+self.carName[self.database["user"][user]["activeCar"]].lower()+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You already have that turbo in your car")
                            else:
                                await message.channel.send(message.author.mention+" You can't afford that :joy:")
                        elif command[1] in self.nitroPrices:
                            if self.database["user"][user]["balance"] >= self.nitroPrices[command[1]]:
                                if str(self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["nitro"]) != command[1]:
                                    self.database["user"][user]["balance"] -= self.nitroPrices[command[1]]
                                    self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]["nitro"] = command[1]
                                    await message.channel.send(message.author.mention+" You have put an **"+command[1]+" bottle nitro** in your **"+self.carName[self.database["user"][user]["activeCar"]].lower()+"**")
                                else:
                                    await message.channel.send(message.author.mention+" You already have that nitro in your car")
                            else:
                                await message.channel.send(message.author.mention+" You can't afford that :joy:")
                        else:
                            await message.channel.send(message.author.mention+" Invalid part ID, please use `"+self.prefix+"tune <PART_ID>`")
                else:
                    await message.channel.send(message.author.mention+" Please use `.car <CAR_ID>` to get in your car first")
            elif command[0] == "race":
                if len(command) >= 2:
                    if len(command) == 3 and command[1].startswith("<") and len(message.mentions) > 0:
                        try:
                            bet = int(command[2])
                        except:
                            await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"race <@MENTION> <AMOUNT>`")
                            return
                        user = str(message.author.id)
                        name = message.author.name
                        target = str(message.mentions[0].id)
                        targetName = message.mentions[0].name
                        if self.database["user"][user]["activeCar"] != None:
                            if user not in self.database["races"]:
                                if target not in self.database["races"]:
                                    self.database["races"][user] = {"target":target, "bet":bet}
                                    await message.channel.send(message.author.mention+" You have challenged "+targetName+" to race you")
                                else:
                                    await message.channel.send(message.author.mention+" "+targetName+" is already in a race")
                            else:
                                await message.channel.send(message.author.mention+" You are already in a race, use `"+self.prefix+"race cancel` to cancel the race")
                        else:
                            await message.channel.send(message.author.mention+" You need an active car in order to race someone")
                    elif command[1] in ["accept", "race"]:
                        if len(message.mentions) > 0:
                            user = str(message.mentions[0].id)
                            name = message.mentions[0].name
                            targetName = message.author.name
                            target = str(message.author.id)
                            if self.database["user"][target]["activeCar"] != None:
                                if user in self.database["races"]:
                                    if target == self.database["races"][user]["target"]:
                                        if self.database["user"][target]["balance"]-self.database["races"][user]["bet"] > 0:
                                            userCar = self.database["user"][user]["cars"][self.database["user"][user]["activeCar"]]
                                            targetCar = self.database["user"][target]["cars"][self.database["user"][target]["activeCar"]]
                                            userPower, targetPower = 0, 0
                                            if userCar["engine"] == "stock":
                                                userPower += self.stockEngine[self.database["user"][user]["activeCar"]]
                                            else:
                                                userPower += self.engines[userCar["engine"]]
                                            if userCar["nitro"] != None:
                                                userPower += self.nitros[userCar["nitro"]]
                                            if userCar["turbo"] != None:
                                                userPower += self.turbos[userCar["turbo"]]
                                            if targetCar["engine"] == "stock":
                                                targetPower += self.stockEngine[self.database["user"][target]["activeCar"]]
                                            else:
                                                targetPower += self.engines[targetCar["engine"]]
                                            if targetCar["nitro"] != None:
                                                targetPower += self.nitros[targetCar["nitro"]]
                                            if targetCar["turbo"] != None:
                                                targetPower += self.turbos[targetCar["turbo"]]
                                            if userPower > targetPower:
                                                winner = user
                                                winnerName = name
                                            elif userPower == targetPower:
                                                winner = random.choice([user, target])
                                                if winner == target:
                                                    winnerName = targetName
                                                else:
                                                    winnerName = name
                                            else:
                                                winner = target
                                                winnerName = targetName
                                            bet = self.database["races"][user]["bet"]
                                            self.database["user"][winner]["balance"] += bet
                                            if winner == target:
                                                self.database["user"][user]["balance"] -= bet
                                            else:
                                                self.database["user"][target]["balance"] -= bet
                                            await message.channel.send("<@"+winner+"> has won the race with his "+self.carName[self.database["user"][winner]["activeCar"]].lower()+" ("+self.nice_price(bet)+" "+self.currency+")")
                                            userPolice = random.randint(0, 4)
                                            if userPolice == 4:
                                                await message.channel.send("<@"+user+"> You are being followed by the **COPS** type `pull` to pull over and pay a fee for speeding\nOR type `run` to try and run from the cops")
                                                fee = random.randint(round(bet/5), round(bet*3))
                                                def check(m):
                                                    return str(m.author.id) == user and m.channel.id == message.channel.id
                                                try:
                                                    msg = await client.wait_for('message', check=check, timeout=8)
                                                except asyncio.TimeoutError:
                                                    self.database["user"][user]["balance"] -= fee
                                                    await message.channel.send("<@"+user+"> You failed to send a message in time, so you pulled over and payed `"+self.nice_price(fee)+" "+self.currency+"`")
                                                else:
                                                    if msg.content == "run":
                                                        catch = 2
                                                        if userPower >= 1000:
                                                            catch = 5
                                                        c = random.randint(1, catch)
                                                        if c == 1:
                                                            action = random.choice([" crashed", " run out of fuel", "r tire poped"])
                                                            self.database["user"][user]["balance"] -= round(fee*5)
                                                            await message.channel.send("<@"+user+"> Oh shiiit, **you"+action+"** and **payed 5x** the fee `"+self.nice_price(round(fee*5))+" "+self.currency+"`")
                                                        else:
                                                            await message.channel.send("<@"+user+"> Thats a fast car you got there, you **escaped** the cops")
                                                    else:
                                                        self.database["user"][user]["balance"] -= fee
                                                        await message.channel.send("<@"+user+"> You pulled over and payed `"+self.nice_price(fee)+" "+self.currency+"`")
                                            else:
                                                targetPolice = random.randint(0, 4)
                                                if targetPolice == 4:
                                                    await message.channel.send("<@"+target+"> You are being followed by the **COPS** type `pull` to pull over and pay a fee for speeding\nOR type `run` to try and run from the cops")
                                                    fee = random.randint(round(bet/5), round(bet*3))
                                                    def check(m):
                                                        return str(m.author.id) == target and m.channel.id == message.channel.id
                                                    try:
                                                        msg = await client.wait_for('message', check=check, timeout=8)
                                                    except asyncio.TimeoutError:
                                                        self.database["user"][target]["balance"] -= fee
                                                        await message.channel.send("<@"+target+"> You failed to send a message in time, so you pulled over and payed `"+self.nice_price(fee)+" "+self.currency+"`")
                                                    else:
                                                        if msg.content == "run":
                                                            catch = 2
                                                            if targetPower >= 1000:
                                                                catch = 5
                                                            c = random.randint(1, catch)
                                                            if c == 1:
                                                                action = random.choice([" crashed", " run out of fuel", "r tire poped"])
                                                                self.database["user"][target]["balance"] -= round(fee*5)
                                                                await message.channel.send("<@"+target+"> Oh shiiit, **you"+action+"** and **payed 5x** the fee `"+self.nice_price(round(fee*5))+" "+self.currency+"`")
                                                            else:
                                                                await message.channel.send("<@"+target+"> Thats a fast car you got there, you **escaped** the cops")
                                                        else:
                                                            self.database["user"][target]["balance"] -= fee
                                                            await message.channel.send("<@"+target+"> You pulled over and payed `"+self.nice_price(fee)+" "+self.currency+"`")
                                            self.database["races"].pop(user)
                                        else:
                                            await message.channel.send(message.author.mention+" You don't have enough money to participate in that race")
                                    else:
                                        await message.channel.send(message.author.mention+" "+name+" did not challange you to a race")
                                else:
                                    await message.channel.send(message.author.mention+" "+name+" did not challange you to a race")
                            else:
                                await message.channel.send(message.author.mention+" You need an active car in order to race someone")
                        else:
                            await message.channel.send(message.author.mention+" Please use `"+self.prefix+"race accept <@MENTION>`")
                    elif command[1] in ["cancel", "end", "remove"]:
                        user = str(message.author.id)
                        if user in self.database["races"]:
                            self.database["races"].pop(user)
                            await message.channel.send(message.author.mention+" You have successfully canceled your race")
                        else:
                            await message.channel.send(message.author.mention+" You are not hosting any race")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"race <@MENTION / cancel / accept>`")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"race <@MENTION / cancel / accept>`")
            elif command[0] in ["scripting", "scripts", "script", "scr", "scrpt"]:
                if len(command) >= 2:
                    user = str(message.author.id)
                    name = message.author.name
                    if command[1] in ["list", "scripts", "scriptlist", "view", "all"]:
                        if len(message.mentions) > 0:
                            user = str(message.mentions[0].id)
                            name = message.mentions[0].name
                        embed = discord.Embed(title=name+"'s Scripts", color=discord.Color.dark_green())
                        for script in self.database["user"][user]["scripts"]:
                            embed.add_field(name=":scroll: "+script["name"], value="This script has `"+str(len(script["commands"]))+"` commands", inline=False)
                        if len(self.database["user"][user]["scripts"]) == 0:
                            embed.add_field(name=":scroll: Empty", value="This user doest not have any scripts", inline=False)
                        embed.set_footer(text="You can execute a script with the command: "+self.prefix+"execute <SCRIPT_NAME>")
                        await message.channel.send(embed=embed)
                    elif command[1] in ["new", "create", "make", "makenew"]:
                        if len(self.database["user"][user]["scripts"]) < 3:
                            await message.channel.send(message.author.mention+" Type the **name** of the script: (dont use spaces and `-`)")
                            def check(m):
                                return str(m.author.id) == user and m.channel.id == message.channel.id
                            try:
                                msg = await client.wait_for('message', check=check, timeout=15)
                            except asyncio.TimeoutError:
                                await message.channel.send("<@"+user+"> You failed to send a message in time, please be faster next time")
                                return
                            name = msg.content.lower()
                            if " " in name or "-" in name:
                                await message.channel.send("<@"+user+"> You can't use spaces or `-` in your script name")
                                return
                            if len(name) > 25:
                                await message.channel.send("<@"+user+"> That name is too long, please use 25 characters at max")
                                return
                            for script in self.database["user"][user]["scripts"]:
                                if script["name"] == name:
                                    await message.channel.send(message.author.mention+" You already have a script with that name")
                                    return
                            commands = []
                            for i in range(5):
                                await message.channel.send(message.author.mention+" Type a command for your script without the `.` (`"+str(i+1)+"`/`5`): (type `end` to end the script)")
                                try:
                                    msg = await client.wait_for('message', check=check, timeout=20)
                                except asyncio.TimeoutError:
                                    await message.channel.send("<@"+user+"> You failed to send a message in time, please be faster next time")
                                    return
                                if len(msg.content) > 75:
                                    await message.channel.send("<@"+user+"> Thats not a valid command (75 characters at max)")
                                    return
                                if "end" == msg.content or "break" == msg.content or "stop" == msg.content:
                                    break
                                if "." not in msg.content:
                                    commands.append(msg.content)
                                else:
                                    return
                            if len(commands) < 1:
                                await message.channel.send("<@"+user+"> You need to enter at least 1 command to the script")
                                return
                            await message.channel.send("<@"+user+"> You successfully created a script")
                            self.database["user"][user]["scripts"].append({"name":name, "commands":commands})
                        else:
                            await message.channel.send(message.author.mention+" Each user can only have 3 scripts, use `"+self.prefix+"script remove <SCRIPT_NAME>` to remove a script")
                    elif command[1] in ["remove", "rm", "delete", "del", "wipe"]:
                        if len(command) >= 3:
                            targetScript = None
                            for script in self.database["user"][user]["scripts"]:
                                if script["name"].lower() == command[2]:
                                    targetScript = script
                                    break
                            if targetScript != None:
                                del self.database["user"][user]["scripts"][self.database["user"][user]["scripts"].index(targetScript)]
                                await message.channel.send(message.author.mention+" You have **successfully deleted** your script")
                            else:
                                await message.channel.send(message.author.mention+" You don't have any script with that name")
                        else:
                            await message.channel.send(message.author.mention+" Please specify the **name** of the script you want to delete")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"script list/new`")
                else:
                    await message.channel.send(message.author.mention+" Please use `"+self.prefix+"script list/new`")
            elif command[0] in ["execute", "exec", "run"]:
                if len(command) >= 2:
                    user = str(message.author.id)
                    targetScript = None
                    for script in self.database["user"][user]["scripts"]:
                        if script["name"] == command[1]:
                            targetScript = script
                            break
                    if targetScript != None:
                        log = "```\n"
                        for command in targetScript["commands"]:
                            command = command.lower().replace("-", "").split(" ")
                            resp = self.shell.run(command, message, self.database)
                            log += resp[0]+"\n"
                            self.database["user"][user] = resp[1]["user"][user]
                        await message.channel.send(message.author.mention+" Your script was successfully executed, here are the logs:\n"+log+"```")
                    else:
                        await message.channel.send(message.author.mention+" There is no script with that **name**")
                else:
                    await message.channel.send(message.author.mention+" Please specify the **name** of the script you want to run")
            elif command[0] in ["jackpot", "jp", "jackpotpool", "jack", "jackp", "jppool", "jpool"]:
                user = str(message.author.id)
                if len(command) >= 2:
                    try:
                        amount = int(command[1])
                    except:
                        await message.channel.send(message.author.mention+" Invalid number, please use `"+self.prefix+"jackpot <TICKETS>`")
                        return
                    if self.database["user"][user]["balance"] >= amount*2000:
                        self.database["user"][user]["balance"] -= amount*2000
                        if user in self.database["jackpot"]:
                            self.database["jackpot"][user] += amount
                        else:
                            self.database["jackpot"][user] = amount
                        await message.channel.send(message.author.mention+" You have bought **"+str(amount)+"x** :tickets:")
                    else:
                        await message.channel.send(message.author.mention+" You can't afford that :joy:")
                else:
                    tickets, totalTickets = 0, 1
                    if user in self.database["jackpot"]:
                        tickets = self.database["jackpot"][user]
                    for u in self.database["jackpot"]:
                        if u != "lastPull":
                            totalTickets += self.database["jackpot"][u]
                    embed = discord.Embed(title="Jackpot Pool", description="Each :tickets: costs **2 000 "+self.currency+"**", color=discord.Color.gold())
                    embed.set_thumbnail(url="https://i.pinimg.com/originals/7d/db/00/7ddb0029e2bf308cfbcddc1459c7404f.jpg")
                    embed.add_field(name="Pool", value="There are **"+self.nice_number(totalTickets)+"x** :tickets: in the pool today ("+self.nice_number(totalTickets*2000)+" "+self.currency+")", inline=False)
                    embed.add_field(name="Your Tickets", value="You own **"+self.nice_number(tickets)+"x** :tickets: ("+str(round(tickets/totalTickets*100, 2))+"% win chance)", inline=False)
                    embed.add_field(name="Next Pull", value="The next pull will be at `"+str(datetime.datetime.fromtimestamp(self.database["jackpot"]["lastPull"])).split(" ")[1]+"` (UTC)", inline=False)
                    await message.channel.send(embed=embed)
            elif command[0] in ["woods", "mushroom", "mushrooms", "forest"]:
                user = str(message.author.id)
                if self.database["user"][user]["lvl"] >= 10:
                    if self.database["user"][user]["woodsTime"]+self.cooldowns["woods"] < time.time():
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
                        self.database["user"][user]["woodsTime"] = round(time.time())
                    else:
                        remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["woodsTime"]+self.cooldowns["woods"]-time.time()))).split(":")
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
                    if len(command) <= 1 or mention:
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
                        if deal["lastDeal"]+self.cooldowns["gang"] < time.time():
                            iMix = None
                            for mix in self.database["user"][user]["inventory"]["drugs"]["mixes"]:
                                if mix["drug"] == deal["drug"] and mix["amount"] >= amount and mix["quality"] >= 90:
                                    iMix = mix
                                elif amount == "max" and mix["drug"] == deal["drug"] and mix["quality"] >= 90:
                                    iMix = mix
                                    amount = iMix["amount"]
                            if iMix != None:
                                if amount <= self.database["user"][user]["gang"]["maxAmount"]:
                                    price = round(amount*(self.sellPrice[deal["drug"]]/100*150))
                                    price = price+(price/100*10*(self.database["user"][user]["prestige"]-1))
                                    self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] -= amount
                                    if self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]["amount"] <= 0:
                                        del self.database["user"][user]["inventory"]["drugs"]["mixes"][self.database["user"][user]["inventory"]["drugs"]["mixes"].index(iMix)]
                                    self.database["user"][user]["balance"] += price
                                    await message.channel.send(message.author.mention+" You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+" mix** for `"+self.nice_number(price)+" "+self.currency+"`")
                                    self.database["user"][user]["gang"]["lastDeal"] = round(time.time())
                                else:
                                    await message.channel.send(message.author.mention+" They want **"+self.nice_number(self.database["user"][user]["gang"]["amount"])+" grams** at max")
                            elif deal["drug"] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                if amount == "max":
                                    amount = self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]]
                                if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] >= amount:
                                    if amount <= self.database["user"][user]["gang"]["maxAmount"]:
                                        price = round(amount*(self.sellPrice[deal["drug"]]/100*150))
                                        price = price+(price/100*5*(self.database["user"][user]["prestige"]-1))
                                        self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] -= amount
                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][deal["drug"]] <= 0:
                                            self.database["user"][user]["inventory"]["drugs"]["pure"].pop(deal["drug"])
                                        self.database["user"][user]["balance"] += price
                                        await message.channel.send(message.author.mention+" You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+"** for `"+self.nice_number(price)+" "+self.currency+"`")
                                        self.database["user"][user]["gang"]["lastDeal"] = round(time.time())
                                    else:
                                        await message.channel.send(message.author.mention+" They want **"+self.nice_number(self.database["user"][user]["gang"]["maxAmount"])+" grams** at max")
                                else:
                                    await message.channel.send(message.author.mention+" You don't have that much "+deal["drug"])
                            else:
                                await message.channel.send(message.author.mention+" You don't have the requested drug")
                        else:
                            remaining = str(datetime.timedelta(seconds=round(deal["lastDeal"]+self.cooldowns["gang"]-time.time()))).split(":")
                            for i in range(len(remaining)):
                                if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                    remaining[i] = remaining[i][1:]
                            await message.channel.send(message.author.mention+" You need to wait **"+remaining[0]+" hours "+remaining[1]+" minutes and "+remaining[2]+" seconds** before you can sell to the gang again")
                    else:
                        await message.channel.send(message.author.mention+" Please use `"+self.prefix+"gang <AMOUNT/remove (optional)>`")
                else:
                    if not mention:
                        name = "you"
                    await message.channel.send(message.author.mention+" Currently there are no gangs interested in "+name)
            elif command[0] == "settings":
                user = str(message.author.id)
                if len(command) <= 1:
                    embed = discord.Embed(title="You'r Settings", color=discord.Color.dark_gray())
                    for setting in self.settings:
                        embed.add_field(name=setting["name"]+" - "+str(self.database["user"][user]["settings"][setting["id"]])+" (id => `"+setting["id"]+"`)", value=setting["desc"], inline=False)
                    embed.set_footer(text="Change a setting with "+self.prefix+"settings <SETTING_ID> true/false")
                    await message.channel.send(embed=embed)
                elif len(command) == 2:
                    if command[1] in self.database["user"][user]["settings"]:
                        embed = discord.Embed(title="You'r Settings", color=discord.Color.dark_gray())
                        for setting in self.settings:
                            if setting["id"] == command[1]:
                                embed.add_field(name=setting["name"]+" - "+str(self.database["user"][user]["settings"][setting["id"]])+" (id => `"+setting["id"]+"`)", value=setting["desc"], inline=False)
                                break
                        embed.set_footer(text="Change a setting with "+self.prefix+"settings <SETTING_ID> true/false")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(message.author.mention+" There is no setting with that **ID**")
                else:
                    if command[1] in self.database["user"][user]["settings"]:
                        if command[2] in ["true", "false"]:
                            s = True
                            if command[2] == "false":
                                s = False
                            self.database["user"][user]["settings"][command[1]] = s
                            await message.channel.send(message.author.mention+" You have changed the setting `"+command[1]+"` to `"+command[2]+"`")
                        else:
                            await message.channel.send(message.author.mention+" Please use `true` or `false`")
                    else:
                        await message.channel.send(message.author.mention+" There is no setting with that **ID**")
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
                            if self.database["user"][user]["lab"] == self.buildings["lab"][-1] and self.database["user"][user]["house"] == self.buildings["house"][-1] and self.database["user"][user]["warehouse"] == self.buildings["warehouse"][-1] and self.database["user"][user]["field"] == self.buildings["field"][-1]:
                                self.database["user"][user] = {"name":message.author.name, "balance":1000, "house":self.starterHouse, "warehouse":None, "lab":None, "field":None, "upgrades":{"lab":0, "smug":0}, "inventory":{"items":{}, "drugs":{"pure":{}, "mixes":[]}}, "lvl":1, "job":None, "lastJob":0, "growing":[], "producing":[], "electricity":0, "lastBill":round(time.time()), "deals":self.newDeals(str(message.author.id), True), "dealRefresh":round(time.time()), "police":{"prison":False, "expire":round(time.time())}, "crypto":{}, "lastHeist":0, "mining":[], "lastMsg":round(time.time()), "woodsTime":0, "gang":None, "prestige":self.database["user"][user]["prestige"]+1, "cars":{}, "activeCar":None, "lastSmuggles":{"1":0, "2":0, "3":0, "4":0}, "settings":{"tips":True}, "guilds":self.database["user"][user]["guilds"]}
                                remove = {}
                                for drug in self.database["market"]:
                                    for deal in self.database["market"][drug]:
                                        if deal["author"] == user:
                                            if drug in remove:
                                                remove[drug] += [deal]
                                            else:
                                                remove[drug] = [deal]
                                for drug in remove:
                                    for deal in remove[drug]:
                                        del self.database["market"][drug][self.database["market"][drug].index(deal)]
                                await message.channel.send(message.author.mention+" You **successfully presiged** to the **"+str(self.database["user"][user]["prestige"])+"th prestige** level")
                            else:
                                await message.channel.send(message.author.mention+" You are missing some buildings")
                        else:
                            await message.channel.send(message.author.mention+" You need to have at least "+str(lvl)+" level")
                    else:
                        await message.channel.send(message.author.mention+" You need to have at least "+str(bal)+" milion")
            self.database["user"][str(message.author.id)]["lastMsg"] = round(time.time())

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