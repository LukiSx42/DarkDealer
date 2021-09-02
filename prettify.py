import random

def nice_number(num):
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

def nice_price(price, rounded=False, roundAmount=0):
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

def nice_amount(amount, rounded=False, roundAmount=0):
    finalAmount = str(amount)
    sufix = ""
    if amount >= 1000000000000000000000:
        finalAmount = str(amount/1000000000000000000000)
        sufix = "petatons"
    elif amount >= 1000000000000000000:
        finalAmount = str(amount/1000000000000000000)
        sufix = "teratons"
    elif amount >= 1000000000000000:
        finalAmount = str(amount/1000000000000000)
        sufix = "gigatons"
    elif amount >= 1000000000000:
        finalAmount = str(amount/1000000000000)
        sufix = "megatons"
    elif amount >= 1000000:
        finalAmount = str(amount/1000000)
        sufix = "tons"
    elif amount >= 1000:
        finalAmount = str(amount/1000)
        sufix = "kg"
    if finalAmount.split(".")[-1] == "0":
        finalAmount = finalAmount.split(".")[0]
    if "." in finalAmount and rounded:
        finalAmount = str(round(float(finalAmount), roundAmount))
    return finalAmount + sufix

def ez_price(rawPrice):
    price = rawPrice
    if "k" == rawPrice[-1]:
        price = rawPrice[:-1]+"0"*3
    elif "mil" == rawPrice[-3:]:
        price = rawPrice[:-3]+"0"*6
    elif "bil" == rawPrice[-3:]:
        price = rawPrice[:-3]+"0"*9
    elif "tril" == rawPrice[-4:]:
        price = rawPrice[:-4]+"0"*12
    elif "quad" == rawPrice[-4:]:
        price = rawPrice[:-4]+"0"*15
    elif "quin" == rawPrice[-4:]:
        price = rawPrice[:-4]+"0"*18
    elif "sex" == rawPrice[-3:]:
        price = rawPrice[:-3]+"0"*21
    try:
        price = int(price)
        return price
    except:
        return None

def ez_amount(rawAmount):
    try:
        amount = rawAmount
        if "kg" == rawAmount[-2:]:
            amount = float(rawAmount[:-2])*10**3
        elif "t" == rawAmount[-1]:
            amount = float(rawAmount[:-1])*10**6
        elif "mt" == rawAmount[-2:]:
            amount = float(rawAmount[:-2])*10**12
        elif "megaton" == rawAmount[-7:]:
            amount = float(rawAmount[:-7])*10**12
        elif "mton" == rawAmount[-4:]:
            amount = float(rawAmount[:-4])*10**12
        elif "gigaton" == rawAmount[-7:]:
            amount = float(rawAmount[:-7])*10**15
        elif "gton" == rawAmount[-4:]:
            amount = float(rawAmount[:-4])*10**15
        elif "teraton" == rawAmount[-7:]:
            amount = float(rawAmount[:-7])*10**18
        elif "tton" == rawAmount[-4:]:
            amount = float(rawAmount[:-4])*10**18
        elif "petaton" == rawAmount[-7:]:
            amount = float(rawAmount[:-7])*10**21
        elif "pton" == rawAmount[-4:]:
            amount = float(rawAmount[:-4])*10**21
        elif "ton" == rawAmount[-3:]:
            amount = float(rawAmount[:-3])*10**6
        amount = int(amount)
        return amount
    except:
        return None

def mixQuality(q):
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