import discord
import re
import request
import xmltodict
import json
import os
from bs4 import BeautifulSoup
import random


# CORONA 
def get_data():
    prev_countries = []
    if os.path.exists('/tmp/prev_countries.json'):
        with open('/tmp/prev_countries.json', 'r') as f:
            prev_countries = json.load(f)
            
    gUrl = "1lwnfa-GlNRykWBL5y7tWpLxDoCfs8BvzWxFjeOZ1YJk"
    idIn = "1"
    url = "https://spreadsheets.google.com/feeds/list/" + gUrl + "/" + idIn + "/public/values"
    data = requests.get(url).content
    data = xmltodict.parse(data)['feed']['entry']

    processed_data = {}
    new_countries = []
    countries = []
    total_cases = 0
    total_deaths = 0

    for entry in data:
        country = entry['gsx:country']
        p_confirmed_cases = str(entry['gsx:confirmedcases']).replace(',', '')
        if (p_confirmed_cases == 'None') or (not p_confirmed_cases):
            confirmed_cases = 0
        else:
            confirmed_cases = int(p_confirmed_cases)
        p_confirmed_deaths = str(entry['gsx:reporteddeaths']).replace(',', '')
        if (p_confirmed_deaths == 'None') or (not p_confirmed_deaths):
            confirmed_deaths = 0
        else:
            confirmed_deaths = int(p_confirmed_deaths)
        processed_data[country] = {'confirmed_deaths': confirmed_deaths, 'confirmed_cases': confirmed_cases}
        countries.append(country)
        total_cases += confirmed_cases
        total_deaths += confirmed_deaths

        if country not in prev_countries:
            new_countries.append(country)

    json.dump(countries, open('/tmp/prev_countries.json', 'w'))

    return post_discord(new_countries, processed_data, total_cases, total_deaths)

def check_change(prev_deaths, total_deaths, prev_cases, total_cases):
    if (prev_deaths != total_deaths) or (prev_cases != total_cases):
        if (total_deaths - prev_deaths >= 50) or (total_cases - prev_cases >= 100):
            return True
    return False

def post_discord(new_countries, processed_data, total_cases, total_deaths):
    if os.path.exists('/tmp/prev_data.json'):
        with open('/tmp/prev_data.json', 'r') as f:
            prev_data = json.load(f)
            prev_deaths = prev_data['prev_deaths']
            prev_cases = prev_data['prev_cases']
    else:
        prev_deaths = 0
        prev_cases = 0

    if check_change(prev_deaths, total_deaths, prev_cases, total_cases):
        messages = ['Death Count is {} :skull:'.format(total_deaths),
                    'Total Cases {} :nauseated_face:'.format(total_cases)]
        json.dump({'prev_deaths': total_deaths, 'prev_cases': total_cases}, open('/tmp/prev_data.json', 'w'))
    else:
        messages = []
    for country in new_countries:
        message = "New country infected: {} :airplane:".format(country)
        messages.append(message)

    return messages

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("soso doki"):
        await message.channel.send("mokri mi se za svinje")
    if message.content.lower().startswith("soso romziila"):
        await message.channel.send("ko je to snobio sorio?")
    if message.content.lower().startswith("soso galovik"):
        await message.channel.send("nisam to vidio 500 dolara")
    if message.content.lower().startswith("soso sicko"):
        await message.channel.send("toppy pop")
    if message.content.lower().startswith("soso boki"):
        await message.channel.send("pismen ko tetrapak")
    if message.content.lower().startswith("soso brane"):
        await message.channel.send("ne zezzzijzijasd")

    if message.content.lower().startswith('soso penis'):
        r = random.randint(0, 30)
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
        #await message.channel.send("Broj roastova: " + str(len(roasts)) + "\nOdabrani roast: " + str(r))

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
        msg = "***SOSO CUSTOMS by ROMZiiLA (i Siko)***\nKomande: *soso join*, *soso add*, *soso teams*"
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


async def corona_check():
    await client.wait_until_ready()
    while not client.is_closed():
        channel = client.get_channel(CHANNEL_ID)
        try:
            messages = get_data()
        except Exception as ex:
            print(ex)
            messages = []

        for message in messages:
            await channel.send((message))
        await asyncio.sleep(1800)

client.loop.create_task(corona_check())
client.run(TOKEN)

