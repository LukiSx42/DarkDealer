import discord, time, datetime, cryptocompare, random

class shell:
    def __init__(self):
        self.prefix = "."
        self.currency = "$"
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
                {"type":"Ultimate lab", "name":"No were takling", "size":1000, "electricity":0.20, "price":5000000, "id":"ultimatelab"},
                {"type":"OP lab", "name":"This is getting too op", "size":3000, "electricity":0.20, "price":100000000, "id":"oplab"},
                {"type":"Wut lab", "name":"The best lab in the game", "size":12500, "electricity":0.20, "price":2500000000, "id":"wutlab"}],
            "field": [
                {"type":"Small Field", "name":"An old and cheap field", "size":35000, "electricity":0.4, "price":10000000, "id":"smallfield"},
                {"type":"Medium Field", "name":"Nice and modern field", "size":80000, "electricity":0.35, "price":250000000, "id":"mediumfield"},
                {"type":"Large Field", "name":"This is a laaaarge field", "size":250000, "electricity":0.3, "price":5000000000, "id":"largefield"}
                ]}
        self.starterHouse = self.buildings["house"][0]
        self.buildingDB = {}
        for buildingType in self.buildings:
            for building in self.buildings[buildingType]:
                building["btype"] = buildingType
                self.buildingDB[building["id"]] = building
        self.car = {"favorit": {"engine":"stock", "turbo":None, "nitro":None}, "mustang":{"engine":"stock", "turbo":None, "nitro":None}, "gallardo":{"engine":"stock", "turbo":None, "nitro":None}, "italia":{"engine":"stock", "turbo":None, "nitro":None}, "aventador":{"engine":"stock", "turbo":"twin", "nitro":None}, "p1":{"engine":"stock", "turbo":"twin", "nitro":None}, "veyron":{"engine":"stock", "turbo":"quad", "nitro":None}, "regera":{"engine":"stock", "turbo":"twin", "nitro":None}, "bolide":{"engine":"stock", "turbo":"quad", "nitro":None}, "s15":{"engine":"stock", "turbo":None, "nitro":None}, "rs4":{"engine":"stock", "turbo":None, "nitro":None}, "e36":{"engine":"stock", "turbo":None, "nitro":None}, "supra":{"engine":"stock", "turbo":None, "nitro":None}, "urus":{"engine":"stock", "turbo":"twin", "nitro":None}}
        self.cars = {"coupe":[("Skoda Favorit", 10000, 58, "https://upload.wikimedia.org/wikipedia/commons/f/fb/Skoda_Favorit_Utrecht_1989.jpg", "favorit"), ("Nissan Silvia s15", 100000, 250, "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Nissan_Silvia_S15_Rocket_Bunny.jpg/480px-Nissan_Silvia_S15_Rocket_Bunny.jpg", "s15"), ("Audi rs4", 1000000, 375, "https://images.pistonheads.com/nimg/36563/B5_011.jpg", "rs4"), ("BMW e36", 2500000, 282, "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/s-l1600-1592412559.jpg", "e36"), ("Toyota Supra MK4", 10000000, 220, "https://i.pinimg.com/564x/d8/76/0f/d8760f5a8ef36f8dce54e5e3e5e99dc1.jpg", "supra")],
            "sport": [("Mustang GT 5.0", 250000, 460, "https://car-images.bauersecure.com/pagefiles/25079/fordmustang2016-01.jpg", "mustang"), ("Lamborghini Gallardo", 2500000, 493, "https://www.autocar.co.uk/sites/autocar.co.uk/files/styles/gallery_slide/public/images/car-reviews/first-drives/legacy/gallardo-0638.jpg?itok=-So1NoXA", "gallardo"), ("Ferrari 458 Italia", 5000000, 562, "https://img.drivemag.net/media/default/0001/03/thumb_2493_default_large.jpeg", "italia")],
            "supercar": [("Lamborghini Aventador SVJ", 25000000, 770, "https://media.caradvice.com.au/image/private/q_auto/v1618445951/wlugwnfjwowhdctoesfm.jpg", "aventador"), ("McLaren P1", 100000000, 903, "https://ag-spots-2021.o.auroraobjects.eu/2021/03/16/thumbs/mclaren-p1-gtr-c249116032021125657_1.jpg", "p1"), ("Bugatti Veyron", 250000000, 1000, "https://preview.thenewsmarket.com/Previews/BGTI/StillAssets/1920x1080/562761_v4.jpg", "veyron"), ("Koenigsegg Regera", 500000000, 1500, "https://www.autoblog.nl/files/2020/08/koenigsegg-regera-in-het-vk-001-890x612.jpg", "regera"), ("Bugatti Bolide", 1000000000, 1825, "https://www.topgear.com/sites/default/files/styles/16x9_1280w/public/images/news-article/2020/10/b98c78ffd730bcece647d7128bb42514/20_bolide_garage_3.jpg?itok=-f_Oshzm", "bolide")],
            "suv": [("Lamborghini Urus", 25000000, 650, "https://www.topspeed.sk/userfiles/articles/16-01/17073/1579183878-lamborghini.urus.2019.1280.01.jpg", "urus")]}
        self.carPrices = {"favorit": 10000, "mustang":250000, "gallardo":2500000, "italia":5000000, "aventador":25000000, "p1":100000000, "veyron":250000000, "regera":500000000, "bolide":1000000000, "s15":100000, "rs4":1000000, "e36":2500000, "supra":10000000, "urus":25000000}
        self.carName = {"favorit": "Skoda Favorit", "mustang":"Ford Mustang GT 5.0", "gallardo":"Lamborghini Gallardo", "italia":"Ferrari 458 italia", "aventador":"Lamborghini Aventador SVJ", "p1":"McLaren P1", "veyron":"Bugatti Veyron", "regera":"Koenigsegg Regera", "bolide":"Bugatti Bolide", "s15":"Nissan Silvia s15", "rs4":"Audi rs4", "e36":"BMW e36", "supra":"Toyota Supra MK4", "urus":"Lamborghini Urus"}
        self.stockEngine = {"favorit":58, "mustang":460, "gallardo":493, "italia":562, "aventador":520, "p1":653, "veyron":250, "regera":1250, "bolide":1075, "s15":250, "rs4":375, "e36":282, "supra":220, "urus":400}
        self.engines = {"v4":200, "v6":450, "v8":550, "v10":650, "v12":800, "v16":1000, "2jz":600}
        self.enginePrices = {"v4": 25000, "v6": 100000, "v8":250000, "v10":750000, "v12":1250000, "v16":2500000, "2jz":5000000, "stock":0}
        self.turbos = {"single":150, "twin":250, "quad":750}
        self.turboPrices = {"single":250000, "twin":1000000, "quad":5000000}
        self.nitros = {"single_b":250, "double":500, "triple":750}
        self.nitroPrices = {"single_b":500000, "double":2500000, "triple":10000000}
        self.sellPrice = {"weed":9, "amp":10, "meth":12, "heroin":20, "cocaine":75, "mdma":30, "saucer":130, "knobby":30, "bohemica":15}
        self.farmingItems = {"tractor":50000}
        self.cooldowns = {"dealRefresh":300, "labBoost":120, "ruderalis":600, "indica":900, "police":300, "heist":600, "msg":2, "woods":300, "saucer":2400, "knobby":1800, "bohemica":1200, "gang":7200, "sativa":1200}
        self.cryptoName = {"BTC":"Bitcoin", "ETH":"Ethereum", "LTC":"Litecoin", "DOGE":"Dogecoin"}
        self.cryptos = ["BTC", "ETH", "LTC", "DOGE"]
        self.electricityMultiplayer = 1.5
        self.jobs = {"windowcleaner":(120, 500), "youtuber":(60, 400), "programmer":(600, 5000), "mafian":(1800, 25000)}
        self.VIP = ["151721375210536961", "682644855713038384", "264127862498525186", "670545442307702794", "794223995691991052", "311033331980435479"]

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

    def nice_price(self, price):
        finalPrice = str(price)
        sufix = ""
        if price >= 1000000000:
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
        return finalPrice + sufix

    def run(self, command, message, database):
        self.database = database
        if command[0] in ["balance", "bal", "money"]:
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
            return ("Balance: "+self.currency+" "+str(bal), self.database)
        elif command[0] == "work":
            job = self.database["user"][str(message.author.id)]["job"]
            if job != None:
                reward = self.jobs[job][1]
                cooldown = self.jobs[job][0]
                if self.database["user"][str(message.author.id)]["lastJob"]+cooldown < time.time():
                    return ("You have worked your shift and you earned "+self.nice_number(reward)+" "+self.currency, self.database)
                    self.database["user"][str(message.author.id)]["balance"] += reward
                    self.database["user"][str(message.author.id)]["lastJob"] = time.time()
                else:
                    remaining = str(datetime.timedelta(seconds=round((self.database["user"][str(message.author.id)]["lastJob"]+cooldown)-time.time()))).split(":")
                    for i in range(len(remaining)):
                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                            remaining[i] = remaining[i][1:]
                    return ("You have to wait **"+remaining[0]+" hours "+remaining[1]+" minutes "+remaining[2]+" seconds"+"** before you can work", self.database)
            else:
                return ("You are not employed, you can employ using `"+self.prefix+"job <JOB_ID>`", self.database)
        elif command[0] == "buy":
            if len(command) < 2 or len(command) > 3:
                return ("Please use `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`", self.database)
            else:
                user = str(message.author.id)
                if command[1] in self.prices:
                    if self.database["user"][user]["lvl"] < 10:
                        if command[1] in self.drugLvls["10"]:
                            return ("You need lvl 10+ to unlock "+command[1], self.database)
                            return
                        elif command[1] in self.drugLvls["25"]:
                            return ("You need lvl 25+ to unlock "+command[1], self.database)
                            return
                    elif self.database["user"][user]["lvl"] < 25:
                        if command[1] in self.drugLvls["25"]:
                            return ("You need lvl 25+ to unlock "+command[1], self.database)
                            return
                    price = self.prices[command[1]]
                    if command[1] not in ["lab1", "lab2", "lab3"]:
                        amount = 1
                        if len(command) == 3:
                            try:
                                amount = int(command[2])
                            except:
                                return ("Please specify a valid amount `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`", self.database)
                                return
                            price = self.prices[command[1]]*amount
                        if self.database["user"][user]["balance"]-price >= 0:
                            self.database["user"][user]["balance"] -= price
                            if command[1] not in self.database["user"][user]["inventory"]["items"]:
                                self.database["user"][user]["inventory"]["items"][command[1]] = amount
                            else:
                                self.database["user"][user]["inventory"]["items"][command[1]] += amount
                            return ("You bought **"+str(amount)+"x "+command[1]+"**", self.database)
                        else:
                            return ("You can't afford to buy that :joy:", self.database)
                    else:
                        if self.database["user"][user]["balance"]-price >= 0:
                            self.database["user"][user]["balance"] -= price
                            self.database["user"][user]["upgrades"]["lab"] = int(command[1].replace("lab", ""))
                            return ("You bought a **lab equipment upgrade (lvl "+command[1].replace("lab", "")+")**", self.database)
                        else:
                            return ("You can't afford to buy that :joy:", self.database)
                elif command[1] in self.buildingDB:
                    building = self.buildingDB[command[1]]
                    if self.database["user"][user]["balance"]-building["price"] >= 0:
                        self.database["user"][user]["balance"] -= building["price"]
                        self.database["user"][user][building["btype"]] = building
                        return ("You got yourself a new "+building["btype"]+"!", self.database)
                    else:
                        return ("You can't afford to buy that :joy:", self.database)
                elif command[1].upper() in self.cryptos:
                    crypto = command[1].upper()
                    amount = 1
                    if len(command) == 3:
                        try:
                            amount = float(command[2])
                        except:
                            return ("Please specify a valid amount `"+self.prefix+"buy <ITEM_ID> <AMOUNT (optional)>`", self.database)
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
                            return ("You invested `"+str(price)+" "+self.currency+"` into `"+crypto+"` at price `"+str(cryptoPrice)+"` per "+crypto, self.database)
                        else:
                            return ("You can't afford to buy that :joy:", self.database)
                    else:
                        return ("Minimum amount is 0.00001 "+crypto, self.database)
                elif command[1] in self.car:
                    if command[1] not in self.database["user"][user]["cars"]:
                        if self.database["user"][user]["balance"]-self.carPrices[command[1]] >= 0:
                            self.database["user"][user]["balance"] -= self.carPrices[command[1]]
                            self.database["user"][user]["cars"][command[1]] = self.car[command[1]]
                            return ("You have bought a "+str(self.carName[command[1]]), self.database)
                        else:
                            return ("You can't afford that :joy:", self.database)
                    else:
                        return ("You already own that car", self.database)
                else:
                    return ("That item/building does not exist, use `.shop <SHOP_ID>` to see all available items and buildings", self.database)
        elif command[0] == "sell":
            if len(command) == 2 or len(command) == 3:
                user = str(message.author.id)
                amount = 1
                if len(command) == 3 and command[1].upper() not in self.cryptos:
                    try:
                        if amount != "max":
                            amount = int(command[2])
                    except:
                        return ("Invalid number, please use `"+self.prefix+"sell <ITEM_ID> <AMOUNT>`", self.database)
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
                            return ("You have sold **"+str(amount)+"x "+str(self.fullName[command[1]].split(":")[-1][1:].lower())+"** for **"+str(round((self.prices[command[1]]/2)*amount))+" "+self.currency+"**", self.database)
                        else:
                            return ("You don't have that many of these items", self.database)
                    else:
                        return ("You don't own that item", self.database)
                elif command[1] in self.carName:
                    self.database["user"][user]["cars"].pop(command[1])
                    if self.database["user"][user]["activeCar"] == command[1]:
                        self.database["user"][user]["activeCar"] = None
                    self.database["user"][user]["balance"] += round(self.carPrices[command[1]]/2)
                    return ("You have sold your "+self.carName[command[1]].lower(), self.database)
                elif command[1].upper() in self.cryptos:
                    if len(command) == 3:
                        try:
                            amount = float(command[2])
                        except:
                            return ("Please specify a valid amount to sell", self.database)
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
                            return ("You have sold **"+str(amount)+" "+crypto+"** for `"+self.nice_number(price)+"` at price `"+str(cryptoPrice)+"` per "+crypto, self.database)
                        else:
                            return ("You don't have that much "+crypto, self.database)
                    else:
                        return ("You don't have any "+crypto, self.database)
                else:
                    return ("That item does not exist", self.database)
            else:
                return ("Please use `"+self.prefix+"sell <ITEM_ID>", self.database)
        elif command[0] == "grow":
            user = str(message.author.id)
            name = str(message.author.name)
            target = 1
            if len(message.mentions) > 0:
                user = str(message.mentions[0].id)
                name = str(message.mentions[0].name)
                target = 2
            if (len(command) >= 3 and len(message.mentions) > 0) or (len(command) >= 2 and len(message.mentions) == 0):
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
                    return ("Growing `"+str(growing)+"` out of `"+str(capacity)+"` plants\nYou need to wait about **"+remaining[1]+" minutes and "+remaining[2]+" seconds** before your next plant grows\nThere are `"+str(grown)+"` harvestable plants", self.database)
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
                                return ("That's not a valid number", self.database)
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
                                            return ("You'r "+command[target+2]+" is full", self.database)
                                        else:
                                            return("You have to grow at least 1 seed", self.database)
                                    if capacity-growing >= amount:
                                        lamps = {"hid":0, "led":0}
                                        lamp = None
                                        pots = 0
                                        pot = False
                                        for plant in self.database["user"][user]["growing"]:
                                            if plant["place"] != "field":
                                                lamps[plant["lamp"]] += plant["amount"]
                                                pots += 1*plant["amount"]
                                        if "hid" in self.database["user"][user]["inventory"]["items"]:
                                            if self.database["user"][user]["inventory"]["items"]["hid"] >= lamps["hid"]+amount:
                                                lamp = "hid"
                                        if lamp == None:
                                            if "led" in self.database["user"][user]["inventory"]["items"]:
                                                if self.database["user"][user]["inventory"]["items"]["led"] >= lamps["led"]+amount:
                                                    lamp = "led"
                                        if "pot" in self.database["user"][user]["inventory"]["items"]:
                                            if self.database["user"][user]["inventory"]["items"]["pot"] >= pots+amount:
                                                pot = True
                                        if command[target+2] == "field":
                                            if command[target+1] != "sativa":
                                                return ("You can **only grow sativa** seeds on fields", self.database)
                                            pot = True
                                            lamp = "led"
                                        else:
                                            if command[target+1] == "sativa":
                                                return ("You can grow sativa seeds **only on fields*", self.database)
                                        if command[target+1] in self.database["user"][user]["inventory"]["items"] or command[target+1] in self.database["user"][user]["inventory"]["drugs"]["pure"]:
                                            if lamp != None:
                                                if pot:
                                                    if command[target+1] in self.database["user"][user]["inventory"]["items"]:
                                                        if self.database["user"][user]["inventory"]["items"][command[target+1]] >= amount:
                                                            self.database["user"][user]["inventory"]["items"][command[target+1]] -= amount
                                                            if self.database["user"][user]["inventory"]["items"][command[target+1]] == 0:
                                                                self.database["user"][user]["inventory"]["items"].pop(command[target+1])
                                                        else:
                                                            return ("You don't have enough seeds", self.database)
                                                    else:
                                                        if self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] >= amount:
                                                            self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] -= amount
                                                            if self.database["user"][user]["inventory"]["drugs"]["pure"][command[target+1]] == 0:
                                                                self.database["user"][user]["inventory"]["drugs"]["pure"].pop(command[target+1])
                                                        else:
                                                            return ("You don't have enough seeds", self.database)
                                                    speed = 1
                                                    watts = 1000
                                                    growTime = self.cooldowns["indica"]
                                                    info = ""
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
                                                                info += "**Your filter broke!**\n"
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
                                                        return (info+"You planted "+command[target+1]+" seeds with a "+lamp+" lamp, it will take **"+remaining[1]+" minutes and "+remaining[2]+" seconds** to grow", self.database)
                                                    else:
                                                        return (info+"You planted "+command[target+1]+" seeds on your field, it will take **"+remaining[1]+" minutes and "+remaining[2]+" seconds** to grow", self.database)
                                                else:
                                                    return (" You don't have enough pots to grow more weed", self.database)
                                            else:
                                                return (" You don't have enough lamps to grow more weed", self.database)
                                        else:
                                            return (" You don't have enough seeds", self.database)
                                    else:
                                        return (" You don't have enough space to grow more weed", self.database)
                                else:
                                    return (" You don't own a "+command[target+2], self.database)
                            else:
                                return (" Please specify a valid place to grow the weed in (`house`/`warehouse`)", self.database)
                        else:
                            return (" There are no seeds named `"+command[target+1]+"`", self.database)
                    else:
                        return (" Please use `"+self.prefix+"grow grow <SEED_ID> <HOUSE/WAREHOUSE> <AMOUNT (optional)>`", self.database)
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
                        return ("There is nothing to harvest", self.database)
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
                                    return (" You need an `tractor` in order to harvest weed from a field", self.database)
                                elif self.database["user"][user]["inventory"]["items"]["tractor"] <= 0:
                                    return (" You need an `tractor` in order to harvest weed from a field", self.database)
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
                        return ("Your weed/mushrooms aren't fully grown yet", self.database)
                    else:
                        return (info[:-1], self.database)
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
                                return ("**Your dryer broke!**\nYou dryed `"+str(base)+"` grams of weed into `"+str(weed)+"` grams with `"+str(bonus)+"` bonus grams (dryer)", self.database)
                            else:
                                return ("You dryed `"+str(base)+"` grams of weed into `"+str(weed)+"` grams with `"+str(bonus)+"` bonus grams (dryer)", self.database)
                        else:
                            return (" You don't have any wet weed to dry", self.database)
                    else:
                        return (" You don't have any wet weed to dry", self.database)
                else:
                    return (" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*", self.database)
            else:
                return (" Please use `"+self.prefix+"grow <@USER (optional)> <ACTION>`\nGrow actions: *info*/*grow*/*harvest*/*dry*", self.database)
        elif command[0] in ["prod", "produce", "lab"]:
            target = 1
            user = str(message.author.id)
            name = message.author.name
            if len(message.mentions) > 0:
                user = str(message.mentions[0].id)
                name = message.mentions[0].name
                target += 1
            if self.database["user"][user]["lab"] == None:
                return (" You need to own a lab before running this command", self.database)
                return
            if len(command) >= target+1:
                if command[target] == "info":
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
                    return ("There are `"+str(producing)+"` out of `"+str(capacity)+"` drugs currently producing\nYou need to wait about **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds** before your next drug produces\nThere are `"+str(collectable)+"` drugs ready to collect", self.database)
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
                                    return ("Invalid powder amount (1st number)", self.database)
                            if len(command) >= target+4:
                                try:
                                    if command[target+3] != "max":
                                        produceAmount = int(command[target+3])
                                except:
                                    return ("Invalid produce amount (2nd number)", self.database)
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
                                                            return (" You don't have enough of grape sugar", self.database)
                                                    else:
                                                        return (" You need grape sugar in orded to produce MDMA", self.database)
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
                                                return ("You started to produce `"+str(powderAmount)+"` grams of `"+powder+"`, production will take around **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds**", self.database)
                                            else:
                                                if command[target+3] == "max":
                                                    return ("You'r lab is full", self.database)
                                                else:
                                                    return ("You have to produce at least 1 drug", self.database)
                                        else:
                                            return ("You can't produce more drugs due to lab capacity", self.database)
                                    else:
                                        return ("The maximum powder amount is `10` grams", self.database)
                                else:
                                    return ("You don't have enough"+self.fullName[powder].split(":")[-1], self.database)
                            else:
                                return ("You don't have enough"+self.fullName[powder].split(":")[-1], self.database)
                        else:
                            return ("That's not a valid drug powder", self.database)
                    else:
                        return ("Please use `"+self.prefix+"lab <@MENTION (opt)> produce <POWDER_ID> <POWDER_AMOUNT (opt)> <PRODUCE_AMOUNT (opt)>`", self.database)
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
                        return (" You successfully collected `"+str(total)+"` grams of drugs", self.database)
                    else:
                        return (" You don't have any drugs to collect", self.database)
            else:
                return (" Please use `"+self.prefix+"lab <@MENTION (optional)> <ACTION>`\nLab actions: *info*/*produce*/*collect*", self.database)
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
                    return ("Please use `"+self.prefix+"mix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"mix 5 amp 5 soda`", self.database)
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
                                                        return ("**Your Mixer broke!**\nYou successfully mixed **"+self.drugName[drug].split(":")[-1].lower()+"** with **"+self.fullName[substance].split(":")[-1].lower()+"**, the mix **quality is "+str(quality)+"/100** ("+self.mixQuality(quality)+")", self.database)
                                                    else:
                                                        return ("You successfully mixed **"+self.drugName[drug].split(":")[-1].lower()+"** with **"+self.fullName[substance].split(":")[-1].lower()+"**, the mix **quality is "+str(quality)+"/100** ("+self.mixQuality(quality)+")", self.database)
                                                else:
                                                    return (" You need more than 0 grams", self.database)
                                            else:
                                                return (" You need to have at least a 50/50 mix", self.database)
                                        else:
                                            return (" You don't have that much "+self.fullName[substance].split(":")[-1].lower(), self.database)
                                    else:
                                        return (" You don't have any "+self.fullName[substance].split(":")[-1].lower(), self.database)
                                else:
                                    return (" You don't have that much "+self.drugName[drug].split(":")[-1].lower(), self.database)
                            else:
                                return (" You don't have any "+self.drugName[drug].split(":")[-1].lower(), self.database)
                        else:
                            return (" Either the substance is not mixable or it does not exist", self.database)
                    else:
                        return (" Either the drug is not mixable or it does not exist", self.database)
                else:
                    return (" You need to own a mixer to be able to mix drugs", self.database)
            else:
                return (" Please use `"+self.prefix+"mix <DRUG_AMOUNT> <DRUG> <SUBSTANCE_AMOUNT> <SUBSTANCE>`\nExample: `"+self.prefix+"mix 5 amp 5 soda`", self.database)
        elif command[0] in ["mine", "mineing", "mining"]:
            if len(command) >= 2:
                user = str(message.author.id)
                if command[1] == "collect":
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
                        return ("You have collected `"+str(btcMined)+" BTC` and `"+str(ethMined)+" ETH`", self.database)
                    else:
                        return ("You don't have any miners running", self.database)
                else:
                    return ("You can only collect crypto", self.database)
            else:
                return ("Please specify an action (**info**/**add**/**remove**/**collect**)", self.database)
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
                        return ("**You fell in the woods and you broke your basket!**\nYou have collected `"+str(shrooms["saucer"])+"x` saucers, `"+str(shrooms["knobby"])+"x` knobbies and `"+str(shrooms["bohemica"])+"x` bohemicas", self.database)
                    else:
                        return ("You went to the woods and collected `"+str(shrooms["saucer"])+"x` saucers, `"+str(shrooms["knobby"])+"x` knobbies and `"+str(shrooms["bohemica"])+"x` bohemicas", self.database)
                    self.database["user"][user]["woodsTime"] = round(time.time())
                else:
                    remaining = str(datetime.timedelta(seconds=round(self.database["user"][user]["woodsTime"]+self.cooldowns["woods"]-time.time()))).split(":")
                    for i in range(len(remaining)):
                        if remaining[i].startswith("0") and len(remaining[i]) != 1:
                            remaining[i] = remaining[i][1:]
                    return ("You need to wait **"+str(remaining[1])+" minutes and "+str(remaining[2])+" seconds** to visit the woods again", self.database)
            else:
                return ("You need to be **level 10** before you can collect shrooms", self.database)
        elif command[0] in ["gangdeal", "gdeal", "gang", "dealgang", "dealgangs"]:
            user = str(message.author.id)
            name = message.author.name
            mention = False
            if len(message.mentions) > 0:
                user = str(message.mentions[0].id)
                name = message.mentions[0].name
                mention = True
            if self.database["user"][user]["gang"] != None:
                if not mention:
                    try:
                        amount = command[1]
                        if amount != "max":
                            amount = int(command[1])
                    except:
                        return ("Invalid number, please use `"+self.prefix+"gang <AMOUNT>`", self.database)
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
                                return ("You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+" mix** for `"+self.nice_number(price)+" "+self.currency+"`", self.database)
                                self.database["user"][user]["gang"]["lastDeal"] = round(time.time())
                            else:
                                return (" They want **"+self.nice_number(self.database["user"][user]["gang"]["amount"])+" grams** at max", self.database)
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
                                    return (" You have sold `"+self.nice_number(amount)+" grams` of **"+self.drugName[deal["drug"]].split(":")[-1][1:].lower()+"** for `"+self.nice_number(price)+" "+self.currency+"`", self.database)
                                    self.database["user"][user]["gang"]["lastDeal"] = round(time.time())
                                else:
                                    return ("They want **"+self.nice_number(self.database["user"][user]["gang"]["amount"])+" grams** at max", self.database)
                            else:
                                return ("You don't have that much "+deal["drug"], self.database)
                        else:
                            return ("You don't have the requested drug", self.database)
                    else:
                        remaining = str(datetime.timedelta(seconds=round(deal["lastDeal"]+self.cooldowns["gang"]-time.time()))).split(":")
                        for i in range(len(remaining)):
                            if remaining[i].startswith("0") and len(remaining[i]) != 1:
                                remaining[i] = remaining[i][1:]
                        return ("You need to wait **"+remaining[0]+" hours "+remaining[1]+" minutes and "+remaining[2]+" seconds** before you can sell to the gang again", self.database)
                else:
                    message.channel.send(" You can only accept deals with your gang")
            else:
                if not mention:
                    name = "you"
                return ("Currently there are no gangs interested in "+name, self.database)
        else:
            return ("Invalid command, use `"+self.prefix+"help script` to get more info about scripting", self.database)