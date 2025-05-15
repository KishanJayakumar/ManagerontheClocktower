import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

GUILD_ID = discord.Object(id=1287829703121567977)
response = requests.get("https://sheetdb.io/api/v1/uz4ah8dd3yjrv")
data = response.json()
userIDs = {"Kishan":638494854237913119, "Alex":484796792618221578, "Avaree":737508508924248064, "Bahara":769013180520595467, "Curtis":525057419517362176, "Danielle":917192049319641088, "Drew":582730941995155457, "Grace":680862553533841504, "Indi":537855775054495744, "James":397168137004646401, "Jayden":844204326242091040, "Justin":505097626560233473, "Kenji":730918368869220352, "Lexie":433741830052642816, "Marc":473535144255291393, "Supriya":750166640209166387, "Zoey":616044391462862891}

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    exit()

@bot.command()
@commands.is_owner()
async def addPrize(ctx, arg1, arg2, arg3, arg4):
    for dict in data:
        if(dict["Players"] == arg1):
            for key in dict:
                if(key == arg2):
                    temp = int(dict[key])+int(arg3)
                    dict[key] = str(temp)
                    await ctx.send("Done!")
                    newdata = {key:dict[key]}
                    requests.patch(f"https://sheetdb.io/api/v1/uz4ah8dd3yjrv/Players/{arg1}", json=newdata)
    member = bot.get_user(userIDs[arg1])
    if(arg3 == "1"):
        await member.send(f"You got the {arg2}(One Time Use) for {arg4}!")
    else:
        await member.send(f"You got the {arg2}(Multi-Use {arg3}) for {arg4}!")

@bot.command()
async def testingdm(ctx, arg1):
    await ctx.message.delete()
    member = bot.get_user(userIDs[arg1])
    await member.send(f"{ctx.author.display_name}\ntest")
    await ctx.send("Done :D")

@bot.command()
async def usePrize(ctx, arg1):
    await ctx.message.delete()
    used = False
    for dict in data:
        if(dict["Players"] == ctx.author.display_name):
            for key in dict:
                if(key == arg1):
                    if(dict[key] == "0" or dict[key] == ""):
                        await ctx.send("You don't have this!", delete_after=5)
                    else:
                        temp = int(dict[key])-1
                        dict[key] = str(temp)
                        newdata = {key:dict[key]}
                        requests.patch(f"https://sheetdb.io/api/v1/uz4ah8dd3yjrv/Players/{ctx.author.display_name}", json=newdata)
                        used = True
    member = bot.get_user(userIDs["Kishan"])
    member2 = bot.get_user(userIDs[ctx.author.display_name])
    if(used == True):
        await member.send(f"Player {ctx.author.display_name} has used {arg1}.", delete_after=300)
        await member2.send(f"Your prize use request has gone through successfully", delete_after=30)
    else:
        await member2.send(f"Your prize use request has not gone through successfully", delete_after=30)

@bot.command()
async def checkPrizes(ctx):
    await ctx.message.delete()
    prizes = ""
    for dict in data:
        if(dict["Players"] == ctx.author.display_name):
            for key in dict:
                if (dict[key] == "0" or dict[key]=="" or key=="Players" or key=="Username" or key=="Attended" or key=="Late(Total)" or key=="Late(Time Not Specified)" or key=="Not Attended(Total)" or key=="Not Attended(Reason Not Specified)"):
                    pass
                elif(dict[key] == "1"):
                    prizes+=f"• {key}(One Time Use)\n"
                else:
                    prizes+=f"• {key}(Multi-Use {dict[key]})\n"
    member = bot.get_user(userIDs[ctx.author.display_name])
    if (prizes==""):
        await member.send(f"You have no prizes.", delete_after=30)
    else:
        await member.send(f"Your Prizes:\n{prizes}")
    


bot.run(token,  log_handler=handler, log_level=logging.DEBUG)