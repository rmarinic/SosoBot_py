import requests
import xmltodict
from googletrans import Translator
from collections import defaultdict
import json
import os
from bs4 import BeautifulSoup
import asyncio
import re
import discord
import random
from discord.ext.commands import Bot

WEATHER_API = "8e4b7fb1aac9f2b768cb6224655724b7"
WEATHER_BASE = "http://api.weatherstack.com/current?access_key=" + WEATHER_API + "&query="

points = defaultdict(int)
TOKEN = "NTk0OTU0NjM1NzY5NTQ0NzA0.XRj8rg.XyIfOse8tGUQAjKSVDMKalrtCj0"
client = discord.Client()
CHANNEL_ID = "674055860925890600"

team1 =  []
team2 = []
svi = []
psovanjeBool = False

allowQuiz = True
allowTrivia = True
bot = Bot("!")



def saveDict(dic):
    jsonFile = json.dumps(dic)
    f = open("trivia.json", "w")
    f.write(jsonFile)
    f.close()


def firstInit(data):
    jsonFile = json.dumps(data)
    f = open("psovanje.json", "w")
    f.write(jsonFile)
    f.close()

def readPsovanje():
    pData = []
    with open('psovanjeData.json') as json_file:
        pData = json.loads(json_file.read())
    return pData

def writePsovanje(name, mention):
    msg = ''
    foundUser = False
    psovanjeData = readPsovanje()
    for user in psovanjeData["user"]:
        if user["name"] == name:
            user["count"] = user["count"] + 1
            jsonFile = json.dumps(psovanjeData)
            f = open("psovanjeData.json", "w")
            f.write(jsonFile)
            f.close()
            msg = mention + ", molim te smanji psovanje ovo je krscanski server. Opsovao si **" + str(user["count"]) + "** puta."
            foundUser = True

    if(not foundUser):
        psovanjeData["user"]["name"] = name
        psovanjeData["user"]["count"] = 1
        jsonFile = json.dumps(psovanjeData)
        f = open("psovanjeData.json", "w")
        f.write(jsonFile)
        f.close()
        msg = mention + ", molim te smanji psovanje ovo je krscanski server. Opsovao si **" + str(user["count"]) + "** puta."
               
    return msg

@client.event
async def on_ready():
    global points
    print('We have logged in as {0.user}'.format(client))
    with open("trivia.json", "r") as fh:
        points = json.load(fh)

@client.event
async def on_message(message):
    global psovanjeBool

    if message.author == client.user:
        return

        
    if message.content.lower().startswith('dad joke'):
        url = "https://dad-jokes.p.rapidapi.com/random/jokes"

        headers = {
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
            'x-rapidapi-key': "876d589761mshdd97c4166cd00d9p1005b6jsn2d2d735826e9"
        }
        response = requests.request("GET", url, headers=headers)
        nS = response.text.find("setup")
        nS = nS + 8
        nP = response.text.find("punchline")
        nP = nP + 11
        nT = response.text.find("type")
        nT = nT- 3
        setup = response.text[nS:nT]
        translator = Translator()
        if message.content.lower().startswith('dad joke hr'):
            setup = translator.translate(setup, dest='hr')
            await message.channel.send(setup.text)
        else:
            await message.channel.send(setup)
        await asyncio.sleep(3)
        joke = response.text[nP:len(response.text)]
        joke = joke.replace('"', '')
        joke = joke.replace('{', '')
        joke = joke.replace('}', '')
        if message.content.lower().startswith('dad joke hr'):
            joke = translator.translate(joke, dest='hr')
            await message.channel.send(joke.text)
        else:
            await message.channel.send(joke)

    if message.content.lower().startswith("init psovanje"):
        psovanjeData = {}
        psovanjeData["user"] = []
        memberList = message.guild.members
        for m in memberList:
            psovanjeData["user"].append({
                'name': m.name,
                'count': 0
            })
        with open('psovanjeData.json', 'w') as outfile:
            json.dump(psovanjeData, outfile, indent=4)
        await message.channel.send("json dump u psovanjeData.json done")
            
    #WEATHER
    if message.content.lower().startswith("soso vrijeme"):
        if (len(message.content.split()) == 2):
            target = "Bjelovar"
        target = str(message.content.split()[2:])
        if (target == "bj"):
            target = "Bjelovar"
        if(target == "zg"):
            target = "Zagreb"
        try:
            translator = Translator()
            query = WEATHER_BASE + target

            response = requests.request("GET", query)
            data = json.loads(response.text)
            vr = translator.translate(data["current"]["weather_descriptions"][0], dest='hr')

            img = data["current"]["weather_icons"][0]

            embedVar = discord.Embed(title="SOSOBOT WEATHER", description="by ROMZiLLA", color=0x00ff00)
            embedVar.add_field(name="Mjesto", value=data["request"]["query"], inline=False)
            embedVar.add_field(name="Vrijeme", value=vr.text, inline=False)
            embedVar.add_field(name="Temperatura", value=str(data["current"]["temperature"]) + " °C", inline=False)
            embedVar.add_field(name="Vjetar", value=str(data["current"]["wind_speed"]) + " km/h", inline=False)
            embedVar.add_field(name="Precipitacija", value=str(data["current"]["precip"]) + "%", inline=False)
            embedVar.add_field(name="Vlaznost", value=str(data["current"]["humidity"]) + "%", inline=False)
            embedVar.set_image(url=img)
            await message.channel.send(embed=embedVar)
        except:
            await message.channel.send("upisi pravilno ime grada budalo")


   
    #TRIVIA
    if message.content.lower().startswith("soso trivia score"):
        if(message.author.name in points):
            await message.channel.send(message.author.mention + " imas **" + str(points[message.author.name]) + "** bodova!")
        else:
            points[message.author.name] = 0
            await message.channel.send(message.author.mention + " imas **" + "0" + "** bodova!")
        
        
    def check(m):
        return m.channel == message.channel


    def checkReset(reaction, user):
        return user == message.author and str(reaction.emoji) == '👍'

    if message.content.lower().startswith("soso reset"):
        m = await message.channel.send(message.author.mention + ", zelis resetirati svoje bodove?")
        await m.add_reaction('👍')
        await m.add_reaction('👎')
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=7.0, check=checkReset)
        except asyncio.TimeoutError:
            await message.delete()
        else:
            await message.channel.send("Resetirao si svoje bodove!")
            points[message.author.name] = 0
            saveDict(points)

    if message.content.lower().startswith("soso trivia everyone"):
        for key, value in points.items():
            await message.channel.send(key + " ima " + str(value) + " bodova")
            
            
    if message.content.lower().startswith("soso quiz"):
        global allowTrivia
        if allowTrivia:
            allowTrivia = False
            triviaURL = "http://jservice.io/api/random"
            response = requests.request("GET", triviaURL)
            data = json.loads(response.text)

            bodovi = data[0]["value"]
            if(bodovi == None):
                bodovi = 250
                            
            msg = "**Question: **" + data[0]["question"] + "\nTko prvi odgovori dobiva **" + str(bodovi) + "** bodova!"
            await message.channel.send(msg)

            while(1):
                try:
                    msg = await client.wait_for('message', check=check, timeout=15)
                    if msg.content.lower() == "skip":
                        await message.channel.send(msg.author.mention + ", preskace pitanje jer je picka i ne zna nista\nOdgovor je bio: **" + data[0]["answer"] + "**")
                        allowTrivia = True
                        break
                    if msg.content.lower() == "hint":
                        odg = data[0]["answer"]
                        brojR = len(re.findall(r'\w+', odg))
                        await message.channel.send("Broj rijeci: " + str(brojR))
                        await message.channel.send("Odgovor ima " + str(len(data[0]["answer"].strip(" ")))+ " slova.")
                        await message.channel.send("Prvo slovo odgovora: " + data[0]["answer"][0] + "\nZadnje slovo odgovora: " + data[0]["answer"][len(data[0]["answer"]) - 1])
                    if msg.content.lower() == data[0]["answer"].lower():
                        if(not msg.author.name in points):
                            points[msg.author.name] = 0
                        
                        points[msg.author.name] += bodovi
                        await message.channel.send(msg.author.mention + ", tocno si odgovorio i osvojio **" + str(bodovi) +"** bodova!")
                        saveDict(points)
                        allowTrivia = True
                        break
                    
                except asyncio.exceptions.TimeoutError:
                    allowTrivia = True
                    await message.channel.send("Niste stigli odgovoriti na vrijeme idioti glupi lol\nOdgovor je bio: **" + data[0]["answer"] + "**")
                    break
            
            

    if message.content.lower().startswith("soso doki"):
        await message.channel.send("mokri mi se za svinje")
    if message.content.lower().startswith("soso romzilla"):
        await message.channel.send("ko je to reko? op. šta?")
    if message.content.lower().startswith("soso galovik"):
        await message.channel.send("nisam to vidio 500 dolara")
    if message.content.lower().startswith("soso sicko"):
        await message.channel.send("toppy pop")
    if message.content.lower().startswith("soso boki"):
        await message.channel.send("pismen ko tetrapak")
    if message.content.lower().startswith("soso brane"):
        await message.channel.send("ne zezzzijzijasd")
    if message.content.lower().startswith("soso kejtej"):
        await message.channel.send("...")
        
    if message.content.lower().startswith('soso penis'):
        r = random.randint(0, 250)
        msg = message.author.mention + ", tvoj penis :nose:: ```8"
        for i in range(r):
            msg += "="
        msg += "D```"
        await message.channel.send(msg)
        
    if message.content.lower().startswith('kolki sam peder'):
        r = random.randint(0, 101)
        await message.channel.send(message.author.mention + ", ti si " + str(r) + "% pedercina :point_right: :ok_hand: :joy:")

    if message.content.lower().startswith('branko'):
        await message.channel.send(":white_small_square::white_small_square::white_small_square::zany_face: :white_small_square::white_small_square::white_small_square:\n:white_small_square::white_small_square::axe::shirt: :shield::white_small_square::white_small_square:\n:white_small_square::white_small_square::white_small_square::jeans: :white_small_square::white_small_square::white_small_square:\n  :regional_indicator_b: :regional_indicator_r: :regional_indicator_a: :regional_indicator_n: :regional_indicator_k: :regional_indicator_o:")
        
    if message.content.lower().startswith('ko je peder'):
        members = message.guild.members
        r = random.randint(0, len(members))
        msg = members[r].mention + " je peder"
        await message.channel.send(msg)

    if message.content.lower().startswith('roast'):
        target = message.content.split()[1]
        with open('roasts.txt', encoding="utf8") as file:
            data = file.read()
        roasts = data.split("*")
        r = random.randint(0, len(roasts) - 1)
        msg = target + ", " + roasts[r].lower()
        await message.channel.send(msg)
        if target == "test":
            await message.channel.send("DEBUG SHIT: \nBroj roastova: " + str(len(roasts)) + "\nOdabrani roast: " + str(r))

    if message.content.lower().startswith('soso joke'):
        with open('jokes.txt', encoding="utf8") as file:
            data = file.read()
        jokes = data.split('\n')
        r = random.randint(0, len(jokes) - 1)
        msg = jokes[r]
        await message.channel.send(msg)
        
    if message.content.lower().startswith('soso fact'):
        with open('facts.txt', encoding="utf8") as file:
            data = file.read()
        facts = data.split(';')
        r = random.randint(0, len(facts) - 1)
        msg = facts[r]
        await message.channel.send(msg)

    
    # --------------- SOSO CUSTOMS ------------------
    if message.content.lower().startswith('soso custom'):
        svi.clear()
        team1.clear()
        team2.clear()
        msg = "***SOSO CUSTOMS by ROMZiiLA (i Siko koji nije nist napravio)***\nKomande: *soso join*, *soso add*, *soso teams*"
        await message.channel.send(msg)

    if message.content.lower().startswith('soso join'):
        svi.append(message.author.name)
        msg = message.author.name + " joined"
        await message.channel.send(msg)

    if message.content.lower().startswith('soso add'):
        if message.author.name == "wxrlss":
            svi.append(message.content.split()[2])
            msg = message.content.split()[2] + " joined"
            await message.channel.send(msg)
        else:
            await message.channel.send("Samo ROMZiiLA to moze uraditi")

    if message.content.lower().startswith('soso teams'):
        msg = "**(" + str(len(svi)) + "/10**) - Nerazvrstani: "
        for i in range(len(svi)):
            msg += "***" + str(svi[i])+ "***" + " | "
        await message.channel.send(msg)
        
        msg = "Team 1: \n"
        for i in range(len(team1)):
            msg += "***" + str(team1[i])+ "***\n"
        msg += "Team 2: \n"
        for i in range(len(team2)):
            msg += "***" + str(team2[i])+ "***\n"
        await message.channel.send(msg)

    if message.content.lower().startswith('izreka dana'):
        await message.channel.send("Bolje jesti tortu s prijateljima, nego govna sam!")
        
    if message.content.lower().startswith('soso shuffle'):
        if message.author.name == "wxrlss":
            msg = "Shuffling teams..."
            await message.channel.send(msg)
            for i in range(len(svi)):
                faktor = random.randint(0, 1)
                if(faktor == 0):
                    if(len(team1) < 5):
                        team1.append(svi[i])
                    else:
                        team2.append(svi[i])
                elif(faktor == 1):
                    if(len(team2) < 5):
                        team2.append(svi[i])
                    else:
                        team1.append(svi[i])
            svi.clear()
        else:
            await message.channel.send("Samo ROMZiiLA to moze uraditi")
    # X-------------X SOSO CUSTOMS X----------------X

    #SOSO AMONG US OBAVIJEST
    if message.content.lower().startswith("soso among us"):
        strLen = len(message.content.split())
        if(strLen == 4):
            msg = "Pozivaju se sve kolege i kolegice na **Among Us** u **" + message.content.split()[3] + " h**.\nSvi koji su zainteresirani neka udu u voice kanal: **Među Nama** u tom periodu.\nDođite na **nezaboravne** trenutke **zabave i zezanja**!\n\nTko ne želi igrati, mora javno priznati da je peder :)\n @everyone"
        else:
            msg = "Pozivaju se sve kolege i kolegice na **Among Us**.\nSvi koji su zainteresirani neka udu u voice kanal: **Među Nama**.\nDođite na **nezaboravne** trenutke **zabave i zezanja**!\n\nTko ne želi igrati, mora javno priznati da je peder :)\n @everyone"
        chn = client.get_channel(750058915865034832)
        await chn.send(msg)

    if message.content.lower().startswith("moj id"):
        await message.channel.send(message.author.id)

        
    if message.content.lower().startswith("soso fino"):
        await message.channel.send("Mmmm fino 😋🍗")   

    if "ide gas" in message.content.lower():
        await message.channel.send("al ne ide zivot 😪")


    if "jebo" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
    elif "kurac" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
    elif "picka" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)

    elif "jebe" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
 
    elif "pičk" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
    elif "kur" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
 
    elif "pas mater" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
 
    elif "pizd" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
 
    elif "jeb" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
    elif "pick" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)
    
    elif "kurv" in message.content.lower():
        msg = writePsovanje(message.author.name, message.author.mention)
        await message.channel.send(msg)

    if message.content.lower().startswith("soso trivia categories"):
        url = "https://opentdb.com/api_category.php"
        response = requests.request("GET", url)
        data = json.loads(response.text)
        msg = "USAGE: **soso trivia [category number]**\n```\n"
        for item in data['trivia_categories']:
            msg = msg + str(item['id'] - 8) + ". " + item['name'] + "\n"
        msg = msg + "\n```"
        await message.channel.send(msg)

    elif message.content.lower().startswith("soso trivia"):
        triviaURL = ""
        x = message.content.lower().split()
        global allowQuiz
        allowQuiz = False
        if len(x) == 3:
            if x[2].lower() == "random":
                allowQuiz = True
                triviaURL = "https://opentdb.com/api.php?amount=1"
            elif x[2].isdigit():
                allowQuiz = True
                triviaURL = "https://opentdb.com/api.php?amount=1&category="+str((int(x[2]) + 8))
        else:
            msg = "📝HOW TO PLAY - **SOSO Trivia**💡 by **ROMZiLLA**:\n\n**soso trivia random** - get a random category question\n**soso trivia categories** - get a list of categories\n**soso trivia [category number]** - get a question based on the selected category\n**soso trivia score** - see your score"
            await message.channel.send(msg)
            
        if allowQuiz:
            point = 0
            allowQuiz = False
            response = requests.request("GET", triviaURL)
            data = json.loads(response.text)
            difficulty = data['results'][0]['difficulty']
            category = data['results'][0]['category']
            question = data['results'][0]['question']
            wrongSubstrings = ["&#039;", "&quot;", "&ouml;", "&eacute;", "&aring;"]
            for item in wrongSubstrings:
                if item in question:
                    question = question.replace(item, '')
            correctAns = data['results'][0]['correct_answer']
            if difficulty.lower() == "easy":
                point = 50
            elif difficulty.lower() == "medium":
                point = 100
            elif difficulty.lower() == "hard":
                point = 200
                
            msg = "**CATEGORY:** " + category + " | **DIFFICULTY: **" + difficulty.upper() + " | **POINTS: **" + str(point)
            msg = msg + "\n**Question: **" + question
            lista = data['results'][0]['incorrect_answers'] + [correctAns]
            random.shuffle(lista)
            for item in lista:
                for i in wrongSubstrings:
                    item.replace(i, '')
            correct = 0
            msg = msg + "\n**Answers: **"
            for i in range(len(lista)):
                if lista[i] == correctAns:
                    correct = i + 1
                msg = msg + "\n" + str(i+1) + ". " + lista[i]
            await message.channel.send(msg)

            while(1):
                try:
                    if allowQuiz:
                        break
                    ans = await client.wait_for('message', check=check, timeout=30)
                    if ans.content.lower() == 'skip':
                        await message.channel.send("Skipped!\nCorrect answer: **" + str(correct) + ". " + correctAns + "**")
                        allowQuiz = True
                    elif ans.content.isdigit():
                        if int(ans.content) == correct:
                            if(not ans.author.name in points):
                                points[ans.author.name] = 0
                            points[ans.author.name] += point
                            saveDict(points)
                            await message.channel.send(ans.author.mention + ", tocno si odgovorio i dobio " + str(point) + " bodova!🎉")
                            allowQuiz = True
                        else:
                            await message.channel.send("Wrong answer! ❌\nCorrect answer: **" + str(correct) + ". " + correctAns + "**")
                            allowQuiz = True
                        
                except asyncio.exceptions.TimeoutError:
                    allowQuiz = True
                    await message.channel.send("Niste stigli odgovoriti na vrijeme idioti glupi lol\nOdgovor je bio: **" + correctAns + "**")
                    break
    
        
client.run(TOKEN)
