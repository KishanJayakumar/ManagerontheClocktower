import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

GUILD_ID = discord.Object(id=1287829703121567977)
response = requests.get("https://sheetdb.io/api/v1/uz4ah8dd3yjrv")
data = response.json()

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
        await member.send(f"You got the {arg2}(One Time Use) for {arg4}!", delete_after=36000.0)
    else:
        await member.send(f"You got the {arg2}(Multi-Use {arg3}) for {arg4}!", delete_after=36000.0)

@bot.command()
async def usePrize(ctx, arg1, arg2=None):
    await ctx.message.delete()
    used = False
    for dict in data:
        if(dict["Players"] == ctx.author.display_name):
            for key in dict:
                if(key == arg1):
                    if(dict[key] == "0" or dict[key] == ""):
                        await ctx.send("You don't have this!", delete_after=5.0)
                    else:
                        temp = int(dict[key])-1
                        dict[key] = str(temp)
                        newdata = {key:dict[key]}
                        requests.patch(f"https://sheetdb.io/api/v1/uz4ah8dd3yjrv/Players/{ctx.author.display_name}", json=newdata)
                        used = True
    member = bot.get_user(userIDs["Kishan"])
    member2 = bot.get_user(userIDs[ctx.author.display_name])
    if(used == True):
        if(arg2 == None):
            await member.send(f"Player {ctx.author.display_name} has used {arg1}.", delete_after=3600.0)
        else:
            await member.send(f"Player {ctx.author.display_name} has used {arg1}, with the extra context of {arg2}.", delete_after=300.0)
        await member2.send(f"Your prize use request has gone through successfully", delete_after=30.0)
    else:
        await member2.send(f"Your prize use request has not gone through successfully", delete_after=30.0)

@bot.command()
async def checkPrizes(ctx, arg1=None):
    await ctx.message.delete()
    prizes = ""
    for dict in data:
        if(arg1 == None):
            if(dict["Players"] == ctx.author.display_name):
                for key in dict:
                    if (dict[key] == "0" or dict[key]=="" or key=="Players" or key=="Username" or key=="Attended" or key=="Late(Total)" or key=="Late(Time Not Specified)" or key=="Not Attended(Total)" or key=="Not Attended(Reason Not Specified)"):
                        pass
                    elif(dict[key] == "1"):
                        prizes+=f"• {key}(One Time Use)\n"
                    else:
                        prizes+=f"• {key}(Multi-Use {dict[key]})\n"
        else:
            if(dict["Players"] == arg1):
                for key in dict:
                    if (dict[key] == "0" or dict[key]=="" or key=="Players" or key=="Username" or key=="Attended" or key=="Late(Total)" or key=="Late(Time Not Specified)" or key=="Not Attended(Total)" or key=="Not Attended(Reason Not Specified)"):
                        pass
                    elif(dict[key] == "1"):
                        prizes+=f"• {key}(One Time Use)\n"
                    else:
                        prizes+=f"• {key}(Multi-Use {dict[key]})\n"
    if (prizes=="" and arg1==None):
        await ctx.send(f"You have no prizes.", delete_after=30.0)
    elif (arg1==None):
        await ctx.send(f"Your Prizes:\n{prizes}", delete_after=3600.0)
    elif (prizes==""):
        await ctx.send(f"{arg1} has no prizes.", delete_after=30.0)
    else:
        await ctx.send(f"{arg1} Prizes:\n{prizes}", delete_after=3600.0)

@bot.command()
async def acrobat(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Acrobat(Townsfolk)
Each night*, choose a player: if they are or become drunk or poisoned tonight, you die.

This means that the acrobat will choose a player every night except the first and if they are or become drunk or poisoned that night they will die. This role might seem quite useless at first and you may wonder why it is a Townsfolk but if let's say there are two roles in the list that can get you drunk or poisoned, this allows you to discover that at least one of them is in play if you die, letting you know that their information may be compromised.

Tips:
- Just sit around as you get information if you die
- Once you die share that information as soon as possible so that the town knows they might not be able to trust the information of the person you selected or discover that some of their abilities and information are compromised""", delete_after=600.0)

@bot.command()
async def alchemist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Alchemist(Townsfolk)
You have a Minion ability. When using this, the Storyteller may prompt you to choose differently.

You learn what minion ability you gain on the first night, and then follow that minion’s actions, however you are still on the good team. This means that if you are a minion role that states that your team wins after a certain thing happens the good team will win not the evil team. You will still register good and as an Alchemist not as your minion ability. If your ability adds or removes certain characters that will still happen. 

Tips:
- Minion abilities tend to be far more powerful than your regular townsfolk so try not to sacrifice yourself for the greater good
- An ability that seems like it only helps the evil team may help you hinder the evil team by giving them bad effects
- If you have an ability that helps the good team try to help them without letting them know what you are so that you don’t get killed
- If you have a win condition ability tell everyone so that you can try to have an easy win
- If you have an ability that won’t help your team at all and will instead hinder them then maybe the good team is stacked with good abilities
- If you truly don’t know what to do with your ability simply approach the storyteller and ask what in the world it is""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Boffin(Minion) and the Alchemist are in play and the Alchemist gets the Boffin ability, the Alchemist learns that the demon gains an extra town ability but doesn’t learn what ability it is.
- If the Spy(Minion) and the Alchemist are in play then the Alchemist doesn’t get to look at the grimoire but instead makes the Spy not register falsely
- If the Summoner(Minion) and the Alchemist are in play, the game starts with a demon but if the Alchemist chooses a player to make as the demon their alignment stays the same, becoming either a good demon or an evil demon
- If the Widow(Minion) and the Alchemist are in play, the Alchemist doesn’t get to look at the grimoire and picks a player to poison permanently""", delete_after=600.0)

@bot.command()
async def alsaahir(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Alsaahir(Townsfolk)
Each day, if you publicly guess which players are Minion(s) and which are Demon(s), good wins.

The Alsaahir's guesses need to be public, and they need to be during the day. They don't have to guess every day. Other players may pretend to be the Alsaahir and make a guess. Like the Juggler or the Gossip, the Storyteller will briefly pretend that player is the Alsaahir. If the Alsaahir guesses the Demon player as the Demon, and the Minion players as Minions, the game ends immediately. The Alsaahir must guess all Demon and Minion players. The Alsaahir doesn't need to guess specific minion characters, nor demon characters.

Tips:
- Make a guess every day! Every guess you make narrows down who the Demon and Minion players are.
- Wait a few days before making your first guess, to hide that you are the Alsaahir. The evil team may want to poison and kill you if they know who you are, so hiding your role helps you stay sober and live longer.
- Use your guesses to intentionally rule out pairs or groups of players that worry you. For example, if the Librarian is claiming to confirm the Saint, you can prove that they are not the evil team by guessing them as the Minion and Demon.
- If you die at night, pay attention to the guesses you made right before you died. You may have scared the evil team by getting too close to the truth!
- Encourage good players to come out and share their information, so they can be a demon target instead of you. It's better for you to stay alive as long as possible, because the Alsaahir's power grows as the game progresses.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Alsaahir and Vizier(Minion) are in the same game, the Alsaahir must also guess which Demon(s) are in play.""", delete_after=600.0)

@bot.command()
async def amnesiac(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Amnesiac(Townsfolk)
You do not know what your ability is. Each day, privately guess what it is: you learn how accurate you are.

The amnesiac has an unknown ability. The storyteller may wake them at night if their ability must have them wake. The amnesiac may visit the storyteller privately to guess what their ability is, and will get a answer that ranges from Cold to Hot. If the amnesiac successfully guesses their ability the storyteller will tell them so.

Tips:
- Remember that if you aren’t woken at night your ability is most likely passive
- You may guess vague details to gain information before starting to specify what you think your ability is
- Make sure your questions are relevant to the actions you are taking
- You will likely not get an ability similar to characters like the artist or the fisherman
- Your ability is likely more powerful than the average ability so try your best to learn your role so you can use it to its best power
- Remember that you can always converse with the other players to try to put your heads together on what it is
- Remember that your ability will be reasonable so you have a chance to guess""", delete_after=600.0)

@bot.command()
async def artist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Artist(Townsfolk)
Once per game, during the day, privately ask the Storyteller any yes/no questions.

Going to the Storyteller Privately, you may ask a question without limitation phrased however you like, however, the only answers I can give you are “Yes”, “No” or “I Don’t Know”. If you ask a question I cannot answer with these three phrases then I will ask you to ask another question but to my inability to answer said question. But this is a one-per-game ability so you must be careful with what you decide to ask.

Tips:
- Ask your question early, every night you don’t use it the more you risk losing your ability by getting killed
- Avoid hyper-specific questions so that you’ll be able to get good information no matter what I answer
- Questions don’t have to be game-specific, if you really need to you, can ask a question like “Does the Demon’s first name start with A?”
- If you wish to hold your question you can use it after obtaining information or confirm a piece of information that the town has""", delete_after=600.0)

@bot.command()
async def atheist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Atheist(Townsfolk)
The Storyteller can break the game rules, and if executed, good wins, even if you are dead. [No evil characters]

The Atheist knows that all players are good and that there is no such thing as Demons. With the Atheist in play, there are no evil players—no Minions and no Demons. Good wins if the Storyteller is executed. Any living player may nominate the Storyteller, and the Storyteller is executed if 50% or more of the living players vote. If the Atheist is not in play and the Storyteller is executed, evil wins. Good loses if just two players are alive. The Storyteller may break any of the game’s rules. They may kill a player who nominated to simulate a Witch curse, kill players at night to simulate a Demon attacking, give players false information to simulate drunkenness, change characters at night to simulate a Pit-Hag, or even have the wrong number of Outsiders in play.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- If you are the Atheist, you know who the Demon is: nobody. You know exactly what to do to win the game: execute the Storyteller. If you can convince the other players that you are indeed the Atheist, then that will be enough to win the game.
- Reveal your character early. There isn't really much point lying about who you are, since there are no evil players to fool, and no Demon attacks to avoid at night.
- Don't be too fussed if the other players don't believe you at first, and want to execute a few players. Executing the Storyteller on day one just because one player claims to be the Atheist is a big risk for most players to take, and it is smart to play for a few days to get as much information as possible.
- If there are characters on the script that could make you drunk, such as the Drunk, do everything you can to figure out whether or not you are drunk. If you are the Drunk, then you are not the Atheist at all, there is no Atheist in play, there are hidden evil players amongst you, and executing the Storyteller will result in the evil team winning.
- Don't be afraid to die. Most players will want to kill the Atheist at some stage, just in case you are evil. Dying so that the good team can win is worth it, even though it will result in the Storyteller killing an extra player (or more!) that night.""", delete_after=600.0)

@bot.command()
async def balloonist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Balloonist(Townsfolk)
Each night, you learn a player of a different character type than last night. [+0 or +1 Outsider]

The Balloonist learns 1 townfolk name, 1 outsider name, 1 minion name and 1 demon name over the course of 4 nights. After they’ve learned all 4 it is their job to figure out who is which so that they are able to pin point who the demon is. The order you learn these names is random.

Tips:
- The Balloonist is very powerful even if you’ve died second or third night as you might have a demon name early.
- If you’ve gotten all four names check for confirmed players, such as confirmed good or evil so that you are able to cross them off your list of characters who might be the demon
- If you have all four names but all are suspicious don’t be afraid as at least you know the demon is among those four.
- Remember that there are many factors that may change the demon so you may not have the current demon’s name in your information
- This is a very simple information role but you will typically end up dying without having all names so try your best to make deductions.""", delete_after=600.0)
    if(arg1=="true"):
        await member.send(f"""Jinxes:
- If the Marionette(Minion) believes they are the Balloonist, +1 Outsider may have been added.""", delete_after=600.0)

@bot.command()
async def banshee(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Banshee(Townsfolk)
If the Demon kills you, all players learn this. From now on, you may nominate twice per day and vote twice per nomination.

When alive, the Banshee nominates and votes like a regular player. When dead, they may nominate twice per day, even though dead players may normally not nominate at all. When dead, they may vote for any nomination they wish and do not need a vote token to do so. They may vote twice for the same nomination. The Banshee only gains these powers if they were killed by the Demon. Dying by execution or to a non-Demon ability does not count.

Tips:
- Get killed by the Demon, by any method that works for you!
- You can come out as the Banshee while still alive, if you have information backing you up, forcing the evil team to kill you and confirm you or leave you alive to the final three and have the Demon options reduced to one of the other two remaining players.
- You get confirmed when you die – take advantage of this. Get hold of every bit of information you can.
- Your votes become disproportionately powerful – as the numbers alive dwindle, your two votes become a larger and larger proportion of the votes required to get someone on the block. This is, however, a double-edged sword – you’re going to be having a major impact on the execution that gets most votes regardless of whether you’re right or not, so sometimes you might want to hold your fire if you have doubts!
- Your nominations may end up being the only good nominations remaining – unlike normally, when the game ends if there’s only evil alive to nominate, you can still nominate in death, so don’t preclude worlds where all living players are evil. It could literally come down to you correctly nominating the 1-in-3 that is the Demon of evil players living.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Banshee and Leviathan(Demon) are in the same game, Each night*, the Leviathan chooses an alive good player (different to previous nights): a chosen Banshee dies & gains their ability.
- If the Banshee and Riot(Demon) are in the same game, Each night*, Riot chooses an alive good player (different to previous nights): a chosen Banshee dies & gains their ability.
- If the Banshee and Leviathan(Demon) are in the same game and the Demon kills the Banshee, the players still learn that the Banshee has died.""", delete_after=600.0)

@bot.command()
async def bountyHunter(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Bounty Hunter(Townsfolk)
You start knowing 1 evil player. If the player you know dies, you learn another evil player tonight. [1 Townsfolk is evil]

The Bounty Hunter learns an evil player, and once that player dies, they learn another evil player. Simple right? Unfortunately, with great power comes great consequences, and so when Bounty Hunter is in the game, one of the Townsfolk turn on the good team and become evil! (The evil townsfolk doesn’t know who is on their team, though!)

Tips:
- Since you know for a fact who is evil, why not get that dastardly fiend out early by telling everyone your information!
- You know who an evil player is, but they don’t know you know… Maybe this is a time to sit back in the shadows and pay attention to who they talk to, whether they seem to start without a bluff and then get one after a certain conversation, or maybe they just seem entirely lost and not sure who to talk to. Try to extract as much information from this evil player before putting them on the chopping block.
- Once you’re public as a Bounty Hunter, you’re a target for the Demon to kill, so choose your moment to make your information public with great care. Come out too early and you can just be killed before you get the full extent of your potential information. Come out too late and you won’t be able to convince enough people to execute your target in order to get more information.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Bounty Hunter and Kazali(Demon) are in the same game, an evil Townsfolk is only created if the Bounty Hunter is still in play after the Kazali acts.
- If the Bounty Hunter and Philosopher(Townsfolk) are in the same game, if the Philosopher gains the Bounty Hunter ability, a Townsfolk might turn evil.""", delete_after=600.0)
        
@bot.command()
async def cannibal(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Cannibal(Townsfolk)
You have the ability of the recently killed executee. If they are evil, you are poisoned until a good player dies by execution.

After an execution, you gain the person who was executed’s ability but do not discover their role, until another successful execution where your ability then switches to that player's ability. If an evil role is executed then you are poisoned and will go through actions but will not have an ability until someone else is executed. Once again you do not discover what role you gain, but instead go through the motions of the dead person’s role. If the Cannibal has an “even if dead” ability, such as the Recluse, or an ability that implies it works while dead, such as the Ravenkeeper or Sweetheart, the Cannibal keeps that ability when they die, but loses their Cannibal ability.

Tips:
- Execute players as much as possible, even if they are good you will at the very least reduce the pain of it a bit by inheriting their ability.
- If a town member claiming to be a once-per-game ability gets executed you can now use that ability or double-check that information.
- Be sure to talk to the executees about what role they are so that you know  if you need to trigger it, for example, the artist, otherwise you may pass up that role without realizing you could have used that ability.
- Remember that if an evil player is executed you will most likely go through the motions of the ability they claimed to have.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Cannibal and Butler(Outsider) are in the same game and the Cannibal inherits the Butler's ability the cannibal learns that they are now the Butler
- If the Cannibal and Juggler(Townsfolk) are in the same game, the Juggler guesses on their first day and the Cannibal inherits the Juggler’s ability they learn how many guesses the Juggler got correct.
- If the Cannibal and Poppy Grower(Townsfolk) are in the same game and the Cannibal inherits the Poppy Grower’s ability, and then dies or loses the Poppy Grower ability, the Demon and Minions learn each other that night.
- If the Cannibal and Zealot(Outsider) are in the same game and the Cannibal inherits the Zealot’s ability the cannibal learns that they are now the Zealot.""", delete_after=600.0)

@bot.command()
async def chambermaid(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Chambermaid(Townsfolk)
Each night, choose 2 alive players (not yourself): you learn how many woke tonight due to their ability

The chambermaid wakes up every night and chooses two players, and learns how many of those two players woke up at nighttime(Not including past nights) to use their ability. It does not detect characters who woke for any other reason, such as if the Storyteller woke a Minion to let them know who the Demon is, woke the Demon to give them their starting Demon info, woke a player due to the ability of a different character, or woke someone accidentally.

Tips:
- Your ability triggers on anyone who wakes at night, good or evil, so if someone who is waking at night is claiming to be a character that doesn’t it would make them suspicious but make sure to go talk to that player as they may have a reason to be hiding their role and may come clean if you simply confront them.
- Early in the game, you can tell players what you know about them before they have revealed their character. This helps them to trust you.
- Pick players to verify their claims by checking whether or not they are waking up.
- Pick the same players a couple of nights in a row. Some characters don't act consistently every night. For example, an Assassin claiming to be an Innkeeper could wake up one night when you check them, appearing to be legitimate. However once they have killed, they do not wake up again, meaning that checking them for a second night will give them away as being dishonest.
- Find a player with an ability that doesn't act at night, like the Fool or Minstrel - if you trust this player, you can use them as base for checking a single person thoroughly.
- Pick as many players as you can, casting a wide net and getting a good amount of information on the entire town.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Chambermaid and Mathematician(Townsfolk) are in the same game, the Chambermaid learns if the Mathematician wakes tonight or not, even though the Chambermaid wakes first.""", delete_after=600.0)

@bot.command()
async def chef(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Chef(Townsfolk)
You start knowing how many pairs of evil players there are.

This role is on the simpler side, on the first night and only on the first night you get information, this information tells you how many evil players are sitting next to another evil player. For example, in a typical 10-player game, if you get a zero that means none of the good is sitting right next to each other, if you get one at night, that means that 2 of the evils are sitting right next to each other, if you get a 2 then that means that either all the evil are sitting in a row (Good, Evil, Evil, Evil, Good) or there is a recluse triggering your ability as well (Good, Recluse, Evil, Good, Evil, Evil). Those are the general cases but pay attention to any effects that may add more evil characters into the game.

Tips:
- Your info is typically not very helpful alone but quite useful when combined with other information.
- If you have a confirmed minion somewhere and you got a zero on your ability that means most likely their neighbours are both good unless a mezepheles converted someone.
- Your information is valuable in the late game as with more confirmed information you can figure things out by combining that with your information.""", delete_after=600.0)

@bot.command()
async def choirboy(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Choirboy(Townsfolk)
If the Demon kills the King, you learn which player is the Demon. [+the King]

For the choirboy to be in play there must be a king in play as well. If the demon decides to kill the king, successfully kills them, and the choirboy is currently in play they learn which player the demon is.

Tips:
- The possibility of your mere presence is enough for the demon to hesitate killing the king. 
- If the King reveals themselves, try to visit them discreetly when you can. If you’re too obvious in trying to seek out the King, this might signal to the Demon that you’re the Choirboy. Maybe find a player you trust, and have them speak to the King on your behalf.
- If you die, don’t reveal this publicly, because just the threat of you being alive can be enough. You can take your secret with you to the grave. If there are characters like the Undertaker or Dreamer that learn who you are, it can be good to chat with them and get them to lie about your character.
- Character swap with another player and let them claim to be the Choirboy. If the Demon kills the fake Choirboy and then kills the King, you learn who the Demon is.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Choirboy and Kazali(Demon) are in play the Kazali can not choose the King to become a Minion.""", delete_after=600.0)

@bot.command()
async def clockmaker(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Clockmaker(Townsfolk)
You start knowing how many steps from the Demon to its nearest Minion.

The clockmaker learns on the first night how many seats you would have to walk to get to the nearest minion. Lets say we have players seating in this order (Danielle, Justin, Grace, Avaree, Lexie, Supriya, Alex) With Justin being the Demon and Alex being the Minion. The Clockmaker learns a 2 on the first night as if you were to go to Justin’s seat from Alex’s, the closest path would be to go to Danielles’ and then Justin’s (Remember that seats are in a circle).

Tips:
- You don't have to give your information out immediately; wait a couple of days so that you can observe the other players and see if you uncover anything suspicious while the evil team thinks the pressure is off.
- Your information is most valuable if you can identify a Minion. Figure out which player is a Minion, and you can pin down some very likely Demon suspects. You should try and coordinate with other good players in the game to uncover this information.
- If you get a very large number (> 3), then the Minions are probably sitting close together and away from their Demon. Similarly if you get a very small number (< 2), one of the Minions and the Demon are probably very close together.
- Remember if you are playing a one minion game then you only have 2 suspects after finding the minion. But if it isn’t you may be looking at the wrong minion and accusing innocent players.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Clockmaker and Summoner(Minion) are in the same game, if the Summoner is in play, the Clockmaker does not receive their information until a Demon is created.""", delete_after=600.0)

@bot.command()
async def courtier(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Courtier(Townsfolk)
Once per game, at night, choose a character: they are drunk for 3 nights & 3 days.

The Courtier chooses a character, not a player, and if that character is in play then they are drunk for 3 nights and 3 days. Simple mechanically. If the drunk or poisoned Courtier chooses a character, that character is not drunk, even if the Courtier later becomes sober and healthy. If the Courtier made a character drunk, but the Courtier becomes drunk or poisoned, the player they made drunk becomes sober again. If the Courtier becomes sober and healthy again before the three nights and three days have ended, that player becomes drunk yet again.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- You can only use your ability once in the entire game, so time it well! The later you make your choice, the more information you will have about the game's state and what characters are in play and causing mayhem. On the other hand, the evil team will be keen to target you as soon as they possibly can, so using your ability early can ensure you get it off and learn something before you die.
- Obviously one of the strongest uses of your ability is to target the demon - if you can block the demon by getting them drunk, then the good team will have three nights of reprieve and the evil team will be at a severe disadvantage.
- Another powerful strategy you have available to you is to get Minions drunk. A drunk Assassin or Godfather won't be able to unleash unexpected deaths on the town, though getting the timing right can be very tricky - only aim for these if you're really sure it's going to help the good team out. A drunk Devil's Advocate or Mastermind is a little more insidious, since the evil team often rely on their abilities to save them in a pinch, and the drunkenness will not be obvious right away.
- In most cases, getting good players drunk is probably not the best use of your ability, but there are some cases where it can be viable.
- If you're just not sure who to make drunk and you're rapidly running out of days, a valid option is to simply choose the most deadly character on the script. Whether or not they are in play, you can now be completely confident that they are not impacting your game at all.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Courtier and Summoner(Minion) are in the same game, If the Summoner is drunk on the 3rd night, the Summoner chooses which Demon, but the Storyteller chooses which player.
- If the Courtier and Vizier(Minion) are in the same game, If the Vizier loses their ability, they learn this. If the Vizier is executed while they have their ability, their team wins.""", delete_after=600.0)
        
@bot.command()
async def cultLeader(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Cult Leader(Townsfolk)
Each night, you become the alignment of an alive neighbour. If all good players choose to join your cult, your team wins.

The Cult Leader is able to publicly call for a vote to ask for players to join their cult. If all good players wish to join the cult then the Cult Leader’s team wins. The Cult Leader’s alignment is the same of one of their neighbours. If their alignment switches they are woken up to inform them of this.

Tips:
- Come out as the Cult Leader early, as your chances of being good are much higher early in the game. On the first night you can indeed turn evil, but this will probably not be the case. However, that being said, the town may be hesitant to gun for a Cult Leader win on the first day as this feels like a cheap win and they won't have much evidence either way about your alignment.
- Come out late as the Cult Leader since you'll have more information to share. However, beware, players are prone to distrusting Cult Leaders towards the end of the game as the chance you are evil increases on near the end of the game because good players are more likely to have died than evil.
- Come out as the Cult Leader while evil (without admitting that you are evil), because it will be easier to get the evil team to back your plays for executions and Cult Leader votes.
- Don't admit you are evil until you are good again, or else you might get executed and locked into evil. However, if it's the final day, coming out as evil can destroy the good team for an easy win. If you were evil the night before and you're good now, you can tell the group that you have been evil and that therefore one of your neighbours must be evil.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Cult Leader and Boffin(Minion) are in the same game, if the Demon has the Cult Leader ability, they can’t turn good due to this ability.
- If the Cult Leader and Pit-Hag(Minion) are in the same game, if the Pit-Hag turns an evil player into the Cult Leader, they can't turn good due to their own ability.""", delete_after=600.0)

@bot.command()
async def dreamer(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Dreamer(Townsfolk)
Each night, choose a player (not yourself or Travellers): you learn 1 good & 1 evil character, 1 of which is correct.

Every night you choose a player, if they are evil you get their role and a good role(Most likely whatever they are claiming at that point in time), if they are good you get their role and a evil role. Simple right?

Tips:
- Write down your information as it can get quite complex to remember everything.
- If you are revealing information try to get what that player is claiming as first.
- Any player who registers as a minion cannot be a demon so you may remove them from your list of suspects.
- It’s easy to tell if you are poisoned or drunk because if too many people aren’t adding up then something is wrong with you.
- Your info is more powerful in the early game when no one has claimed yet so you can avoid the storyteller knowing what the evil player is claiming when you are checking someone.
- Try to encourage secrecy so you can check as many players as possible before they’ve claimed anything.""", delete_after=600.0)
    
@bot.command()
async def empath(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Empath(Townsfolk)
Each night, you learn how many of your 2 alive neighbours are evil.

The empath learns how many of their neighbours are evil. If one of their immediate neighbours dies, it goes around until it reaches the next alive player. The empath only learns how many of their neighbours are evil but doesn’t learn who of the 2 triggered it. The Empath acts after the Demon, so if the Demon kills one of the Empath's alive neighbours, the Empath does not learn about the now-dead player.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- The information you receive should inform how you handle your neighbours.
  - If you get a "0", you are (probably) sitting between two good players who you can coordinate with and might want to try to keep alive.
  - If you get a count of "1", then one of your neighbours is trustworthy, and one is not. You should try to determine which one of your neighbours you trust, and eliminate the other one.
  - If you get a count of "2", then you are sitting between two evil players, and should probably look to change that as soon as possible.
- You get information based on the state of the game when you wake up (after the Demon has killed that night). This means that if one of your neighbours died in the night, you immediately start to learn about the next living player.
- If you trust your neighbours, keeping them alive drastically narrows the list of demon suspects.
- If your neighbours die, you will receive new information on the next nearest living player to you. Getting your neighbours killed means you know more. Coordinating with an Undertaker to confirm the identities of your neighbours and getting new information down the line is a powerful combo.
- Coming out with your information early (especially if you know you're sitting near evil players) can help you coordinate with the rest of the good team to further check out your suspects.
- Waiting to reveal your information means that you can protect your good neighbours or keep an eye on your evil ones, as well as gather a wider portfolio of information.""", delete_after=600.0)

@bot.command()
async def engineer(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Engineer(Townsfolk)
Once per game, at night, choose which Minions or which Demon is in play.

The Engineer can choose which Minion characters are in play, or which Demon is in play, but not both. When the Engineer creates new in-play characters, the Demon player remains the Demon, and the Minion players remain Minions. The number of evil players stays the same. If the Engineer tries to create an in-play character, that character stays as the same player. The Engineer doesn’t learn this, and may not use their ability again. If creating Minions, the Engineer chooses the same number of Minions that should be in play for the number of players.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- If you are the Engineer, you can broadly accomplish one of four things: deciding which Minions are in play, deciding which Minions are not in play, deciding which Demon is in play, deciding which Demon is not in play.
- If you want to choose which Minions are in play, this lets you and the entire good team know what you are facing. This can be crucial information.
- If you want to choose which Minions are not in play, simply choose the other Minions to be in play instead. If you want to avoid poisoning, then choosing characters other than the Poisoner may guarantee it. If your group is particularly susceptible to the Mastermind then you can make sure that you don't have to think about it by changing all Minions to other characters instead. Similarly, if you don't know what Demon you do want in play, but there is one Demon in particular that you definitely do NOT want in play, choose to turn the Demon into this character. You will still be facing a powerful adversary, but not the most feared adversary.\
- To prevent the evil team (or the good team!) killing you before you use your ability, use your ability on the first night. This guarantees that you will get to act. The downside to acting this early is that you miss out on the group discussion, and any pertinent information that may influence your decision, like which good characters are in play and which evil characters that they are particularly suited at combatting.
- To choose the most ideal Minions or Demon to create, wait until the second or third night, and generate as much discussion as you can in the meantime. To make the best decision possible, you'll need to know as many good characters that are in play, so that their particular abilities can be used to the fullest.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Engineer and Legion(Demon) are in the same script, Legion and the Engineer can not both be in play at the start of the game. If the Engineer creates Legion, most players (including all evil players) become evil Legion.
- If the Engineer and Summoner(Minion) are in the same game, if the Engineer removes a Summoner from play before that Summoner uses their ability, the Summoner uses their ability immediately.""", delete_after=600.0)

@bot.command()
async def exorcist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Exorcist(Townsfolk)
Each night*, choose a player (different to last night): the Demon, if chosen, learns who you are then doesn't wake tonight.

Each night, the Exorcist chooses a player. If they choose a player who is not the Demon, the Demon may still attack. If they choose the Demon, the Demon does not wake tonight, so does not choose players to attack tonight. The Demon learns that they cannot attack and who the Exorcist is. Any other Demon abilities still function such as the Zombuul staying alive if killed, the Pukka killing a player they attacked on a previous night, or the Shabaloth regurgitating a player. The Exorcist may not choose the same player two nights in a row.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- If a player dies at night, choose a different player on all following nights. You have probably chosen a non-Demon player, so you don't need to choose them again unless you suspect the player died at night for another reason (such as an assassin or gossip killing).
- If you choose a player at night, and there are no deaths that night, you may have found the Demon! Either tell the group publicly who you are and who you have chosen the following day, so that the group can know what you know, or wait for a night or two and choose the same player again, just to be sure. Sometimes, no deaths can occur at night for other reasons, but if you choose the same player multiple times, and each time there is no death at night, you can be fairly certain that you have found the Demon.
- As the game progresses, talk to the group and investigate which characters are in play, and how they are acting. There are many reasons that deaths may occur at night, even if you removed the Demon's ability to kill. There are also many reasons that no death occurred at night, even if you chose a non-Demon player.
- As the Exorcist, you are often weak in the early game, but gain power exponentially as the game progresses - because not only do you learn which players are not the Demon, there are fewer and fewer players alive to choose from. """, delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Exorcist and Leviathan(Demon) are in the same game, Evil does not win when more than 1 good player has been executed, if the Exorcist is alive and has ever successfully chosen the Leviathan.
- If the Exorcist and Riot(Demon) are in the same game, If the Exorcist chooses Riot on the 3rd night, Minions do not become Riot.
- If the Exorcist and Yaggababble(Demon) are in the same game, If the Exorcist chooses the Yaggababble, the Yaggababble ability does not kill tonight.""", delete_after=600.0)

@bot.command()
async def farmer(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Farmer(Townsfolk)
When you die at night, an alive good player becomes a Farmer.

The farmers ability is simple, if you die at night due to anything, another good player becomes a farmer, losing their old ability and any effects that may be going on due to it stop. Although seemingly detrimental to the good team this role is actually truly useful as it can be a powerful trap for the evil team. If you turn into the Farmer at night, reach out to the player that most recently died and reveal to them that you are a Farmer now. It’s very difficult to fake this interaction, meaning the two of you can trust each other.

Tips:
- As said above if you turn into the farmer reach out the the most recent dead person and tell them you turned into a farmer to create a chain of trust.
- If you die at night, play it cool and wait for somebody to approach you as the new Farmer that has been created.
- If you feel like you want to survive, come out as the Farmer, blatantly daring the Demon to kill you at night. This is especially effective if there are no other sources of deaths by night in the game. It might also confuse the Demon, who might second guess your motives.
- Claim to be a high priority target, like the Bounty Hunter or the Fortune Teller, and bait the Demon into killing you at night. Then, once you’ve died and confirmed who the new Farmer is, claim that you swapped characters with them and that they’re the real high priority target to try and bait the Demon into killing them too.
- Try not to come out right away publically as building up a large group of Farmers is much more powerful than a small group of Farmers. Backtracking through the information that the new Farmers may have valuable information that you can trust.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If a Farmer and Leviathan(Demon) are in the same game, Each night*, the Leviathan chooses an alive good player (different to previous nights): a chosen Farmer uses their ability but does not die.
- If a Farmer and Riot(Demon) are in the same game, Each night*, Riot chooses an alive good player (different to previous nights): a chosen Farmer uses their ability but does not die.""", delete_after=600.0)

@bot.command()
async def fisherman(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Fisherman(Townsfolk)
Once per game, during the day, visit the Storyteller for some advice to help your team win.

At any time during the day, the Fisherman can approach the Storyteller privately for some advice to help them win. The Storyteller’s pieces of advice are not “facts”. They are strategy tips that the Storyteller believes will help the Fisherman win if they are followed.

Tips:
- Try to mull over the advice you got and wonder why your storyteller used the specific language and why your storyteller would say that at this point
- If you think you’ll be killed or you are getting a lot of heat then use your ability but you want to hold out as long as possible as your advice can be more tailored to your win if you are closer to the end""", delete_after=600.0)

@bot.command()
async def flowergirl(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Flowergirl(Townsfolk)
Each night*, you learn if a Demon voted today.

A Demon’s vote counts whether or not the nominee was executed. The Flowergirl does not detect if the Demon raised their hand for other reasons, such as when the players “vote” on what to order for dinner, or when the players raise their hand to exile a Traveller. If the Demon changes players after the original Demon voted but before the Flowergirl wakes to learn their information, the Flowergirl detects the original Demon. If there are two (or more!) Demons, even dead Demons, the Flowergirl detects if any of them voted. If even one Demon voted, the Flowergirl learns a “yes”.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Pay attention! You need to keep track of who votes each day, or your information isn't going to be very helpful. Evil players can and will lie about whether they voted or not, so you can't rely on polling the group about who voted if you forget, either. Your information narrows the demon's location down every time you receive it, so make sure it's useful.
- Keep an eye on who doesn't vote as much the players who do. Evil players are less likely to want to vote and draw your attention, but if you get a number of players voting and get a 'no', then you know that the demon is among those who didn't that day. Also keep an eye out for players jumping on a bandwagon of a large voting majority - this could be the demon trying to disguise themselves among the large number of players, limiting your information.
- For an execution, only half the living player's votes are required. If an execution is happening, try to convince the group to limit their votes to only what is required. This will allow you to make a clean divide between two sets of players - if you receive a "yes", then you know the demon is among those asked to vote today. If "no", you know that the demon is among those who didn't.
- Your power allows you to detect the demon, so you are an extremely high value target for the evil team to undermine and kill early. Try and form an alliance with another player you think is good and let them do the talking for you.""", delete_after=600.0)

@bot.command()
async def fool(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Fool(Townsfolk)
The 1st time you die, you don't

The Fool is a simple role, if you are about to die at any point and aren’t protected by anything else you use up your fool protection

Tips:
- It is preferable if you die to the demon rather than execution to waste a demon kill
- Track the number of deaths to see if you were the one who prevented a death
- If you know another good player you trust, you can cover for them as you can’t die one time""", delete_after=600.0)

@bot.command()
async def fortuneTeller(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Fortune Teller(Townsfolk)
Each night, choose 2 players: you learn if either is a Demon. There is a good player that registers as a Demon to you.

The fortune teller gets to choose 2 players including themselves, and discovers whether one of them are the demon. However one good player is your red herring who will also trigger your demon radar(This can also be yourself). 

Tips:
- No’s are more useful for you so that you have confirmed non-demon players.
- You only learn about Demons, your no’s can still include the minions.
- Remember you can use yourself as one of them but if all your readings are Yes then you are your own red herring.""", delete_after=600.0)

@bot.command()
async def gambler(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Gambler(Townsfolk)
Each night*, choose a player & guess their character: if you guess wrong, you die.

Each night except the first, the Gambler chooses a player and guesses their character by pointing to its icon on the character sheet. If the guess is correct, nothing happens. If the guess is incorrect, the Gambler dies. The Gambler does not learn from the Storyteller whether their guess is correct or incorrect. The Gambler may choose any player, dead or alive, even themself.

Tips:
- The Gambler is a high risk, high reward character. You get reliable information that can't be easily tainted, but you put your life on the line to do it. What a thrill!
- Probably one of the strongest uses of your ability is to confirm other good players. Backing up the claims of a couple of players and their characters will go a long way to building trust, and there's really no bad option to confirm: knowing for certain that a Pacifist is in play can be just as useful as knowing that a Chambermaid is who they say they are.
- Choose the good players you most want to know about. The nature of your ability means that you're not the most likely to survive until final day, so try to maximize your chances of getting useful information before your luck runs out.
- There's a difference between taking a well reasoned gamble and throwing caution to the wind entirely and leaving it all up to Lady Luck. Using your ability to try and guess evil characters can be like this. Even if you have very strong suspicions that someone is evil, you still have to guess if they are a Minion or a Demon, and then you have four options in each category! The odds are not really in your favor. With that said...get it right, and you've hit the jackpot.
- If you don't have any idea who to guess, you can guess yourself. Since you know for certain you are the Gambler, your ability will definitely not kill you that night, guaranteeing that you aren't responsible for your death.""", delete_after=600.0)
    
@bot.command()
async def general(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# General(Townsfolk)
Each night, you learn which alignment the Storyteller believes is winning: good, evil, or neither.

The General simply discovers who the storyteller believes is winning, and many factors may be included, such as how many players of each team are still alive, how much information the good team has, how successful the evil team’s bluffs seem to be, which players the group wants to execute next, or how experienced the Demon player is. All of these, and more, will inform the Storyteller’s judgment.

Tips:
- Keep in mind that your role interacts with the personal opinion of the Storyteller. This opinion will inevitably be influenced by more than just mechanics. Does your group of players include someone who is widely regarded as a very cunning evil player? Perhaps you have someone in your game who is considerably more experienced than others? What are the strategies and tactics that your Storyteller considers to be most effective? These things, and many more, can and will influence your information each night.
- Take note of how your information changes from night to night. If you can survive long enough, you will essentially have a line graph showing how the good team’s fortunes have altered over the course of play.
- Take note of how your information changes from night to night. If you can survive long enough, you will essentially have a line graph showing how the good team’s fortunes have altered over the course of play.
- Pay attention to what other players are saying, particularly group consensus. If the group is confident that certain players are evil and should be executed tomorrow, and those players are actually evil, then the Storyteller is likely to tell you that the good team is winning, even if there are more dead good players than evil.""", delete_after=600.0)

@bot.command()
async def gossip(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Gossip(Townsfolk)
Each day, you may make a public statement. Tonight, if it was true, a player dies.

The Gossip may publicly make one statement per day, meaning that they claim they are the gossip and then make the statement when everyone is gathered(Typically this is when everyone has been gathered for nominations), and if the statement they had said is true, an extra player will die at night.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Get over your fear of death! A lot of Gossips will be tentative about using their ability, since they're worried about causing a death accidentally. While it's true you should be cautious with any ability that could cause death, the potential gain in information more than makes up for the risk.
- You are an extremely flexible and versatile information gatherer. Since you can make literally any statement you like about anything, you can cover gaps in the good team, back up other players' information, or ask that one question that everyone desperately wants to know but have no way to find out!
- Be precise with your statements! A vague statement that could be true OR false (e.g. "The demon made someone look evil yesterday.") won't be helpful to you when you're trying to figure out if someone died as a result of your ability. Instead, aim for binary statements that are definitely true or false (e.g., "The demon nominated yesterday.")
- Deliberately say statements that you believe are false. This reduces the risk that you will kill a player, but still allow you to gain information. If nobody dies (or at least, you don't think anyone died because of you), then you can reverse your statement to get the truth!
- Deliberately say true statements! This can be advantageous for two reasons. One, if someone dies because of you, it'll be hard to deny you're the Gossip (providing you can trace that death back to you and not one of the many other causes). This will be less effective in a game with a multi-kill demon. Two, if someone dies as a result of your ability, then you can be very confident that the statement was true.""", delete_after=600.0)

@bot.command()
async def grandmother(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Grandmother(Townsfolk)
You start knowing a good player & their character. If the Demon kills them, you die too.

This means that you know that player is confirmed good and know their character to back them up if needed but, keep in mind that that player doesn’t know you are their grandmother so you must earn their trust. If the demon kills them at night you also die.

Tips:
- To gain your grandchild’s trust hard claim to them and tell them their role before they tell you themselves, this will give you more credibility.
- Try to always back them up and try to make yourself a bigger target than them, perhaps taking credit for their actions as if you die your grandchild won’t die with you.
- Encourage any protection characters to protect your grandchild to avoid an extra kill at night.
- Don’t reveal your grandchild unless absolutely necessary as if the evil team figures it out that’s an easy 2 kills for 1.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Leviathan(Demon) is in play with the Grandmother then Evil wins if the grandchild is executed.""", delete_after=600.0)

@bot.command()
async def highPriestess(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# High Priestess(Townsfolk)
Each night, learn which player the Storyteller believes you should talk to most.

The High Priestess can be shown the same player multiple times in a row, or a different player every night. The shown player can be alive or dead. The shown player can be good or evil. There are no official criteria that determine which player the Storyteller must show to the High Priestess. It is up to the Storyteller’s judgement as to what they think will most benefit the High Priestess and the good team in general. It could be because the player has important information that has not been revealed yet. Or because the player is evil and has a bluff that doesn’t make sense. Or because the player is trustworthy and needs to be trusted more. Or because the player is good but on the wrong track and needs to be corrected. Or something new.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Talk to the person the Storyteller gives you as soon as possible every day – the Storyteller believes they’re the most important person for you to talk to, so you should get hold of them immediately in order to try to gain trust and use their information to dictate how you should approach the rest of your day.
- Don’t talk to your given player immediately. Instead, observe who they talk to and see if you can gain any clues as to why you should be talking to them from how they’re behaving and interacting.
- Tell the person you saw that you’re the High Priestess and learnt them, see if they know a good reason why they might have been shown. Your information can be very nebulous but it’s possible that the player you saw has good theories based on whatever they’ve gained from their own character as to what they can offer to you and to the good team more widely.
- Don’t tell that person that you’re the High Priestess, the Storyteller may not be intending for you to share all of your information with this player, only for them to potentially have things to say that might help you.
- On the first night, the player you learn is most likely either a good player who already has information so that they can share it with you or a Minion who you might be able to get a social read from or trap without a bluff.
- As the game goes on, the Storyteller is most likely to point you towards players that have information they haven’t fully shared yet (even if that information is just their character), dead players that need to know other information you’ve garnered or evil players who can’t further their agenda if they’re in a conversation with you rather than their evil fellows or the players they’re attempting to manipulate.""", delete_after=600.0)

@bot.command()
async def huntsman(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Huntsman(Townsfolk)
Once per game, at night, choose a living player: the Damsel, if chosen, becomes a not-in-play Townsfolk. [+the Damsel]

The Huntsman saves the Damsel before the Minions find her... hopefully. The Damsel can be in play without the Huntsman. During the setup phase, if the Huntsman is in play and the Damsel isn’t, the Damsel is added. If a Damsel is already in play, the Huntsman doesn’t add a second Damsel. If the Huntsman correctly chooses the Damsel at night, the Damsel becomes a not-in-play Townsfolk immediately. The Storyteller chooses which Townsfolk character, and the Damsel learns which one.
When the Damsel becomes a Townsfolk, they gain that Townsfolk ability and lose the Damsel ability.
The Huntsman gets one guess, and makes it at night.

Tips:
- Find the Damsel ASAP. You have one shot and you’re racing against either you or them dying before you can find them! This can be more important in smaller games as the chances of either player dying early is higher, but also your chances of being correct with a blind pick is higher.
- Wait to use your ability until you're really sure. You only have one opportunity to get it right and there is a lot of fun to be had during the hunting. Try to partner up with characters that can learn about characters like Dreamer.
- The Damsel is likely to be flighty and paranoid, and may even be trying to get themselves killed. Use your ability on people who seem shifty or quiet as they might be a Damsel. If a player seems to be keen to volunteer themselves for execution, privately ask them if they'd like you to guess them as the Damsel that night.
- Privately claim to be the Damsel to other players. This can be useful to flush out the Damsel and the various Minions.
- Stay alive at any cost. You can claim you've used your ability already, or that you’ve already found your Damsel, meaning you’re no longer a threat to evil.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Marionette(Minion) thinks they are the Huntsman, the Damsel was added.
- If the Huntsman and Kazali(Demon) are in the same game, if the Kazali chooses the Damsel to become a Minion, and a Huntsman is in play, a good player becomes the Damsel.""", delete_after=600.0)

@bot.command()
async def innkeeper(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Innkeeper(Townsfolk)
Each night*, choose 2 players: they can't die tonight, but 1 is drunk until dusk.

The innkeeper only protects players at night and gets the bonus of being able to prevent 2 players from dying, however in the process the people you have chosen may get drunk making their ability not work. 

Tips:
- The Innkeeper, like the Monk, makes players safe from being killed by the Demon. They are also safe from death caused by Outsiders, Minions, Townsfolk, and Travellers.
- Your ability is powerful and when used effectively you can stall the evil team and keep your fellow good team safe. The price of your ability is steep, however - anyone protected by you becomes unreliable as they may be drunk for the night that they survive. Coordinating with your fellow good players to find ideal targets to protect is absolutely vital - some characters (such as the Pacifist and the Exorcist) become stronger the longer they survive, and you can enable that.
- Be mindful of the drunkenness your ability causes! Don't protect people who need to receive reliable information or use their ability with any sort of guarantee that night. If you know for example that a Courtier is about to use their ability, you protecting them may cause them to become drunk and waste their powerful ability!
- Protect different people than who you publicly claim to be protecting. If the evil team believes what you are saying, they will not want to waste time targeting players who can't be killed. Meanwhile, you secretly protect other players that are potential victims, hopefully blocking the evil team from a necessary kill.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If Leviathan(Demon) and Innkeeper are in the same game, the Innkeeper-protected players are safe from all evil abilities.
- If Riot(Demon) and Innkeeper are in the same game, the Innkeeper-protected players are safe from all evil abilities.""", delete_after=600.0)

@bot.command()
async def investigator(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Investigator(Townsfolk)
You start knowing that 1 of 2 players is a particular Minion.

The Investigator learns that a particular Minion character is in play, but not exactly which player it is. During the first night, the Investigator learns that one of two players is a specific Minion. They learn this only once and then learn nothing more.

Tips:
- Tell the group what your information is as soon as possible on the first day. You probably won't be able to determine which of the two players is the Minion, but if you are believed, then the good team will probably have enough time to execute both players, guaranteeing that a Minion is dead on the final day.
- Whilst your information by itself will probably not be enough to condemn a specific player, it might combine well with another good player's information, such as the Empath or the Chef. If you trust them, you can team up to execute a Minion early in the game, which removes their voting power and gives you an advantage.
- If you have a strong suspicion regarding one of the 2 players shown to you, simply say nothing and study their behaviour. If they continually come to the defense of a particular player, that player is likely the Demon. If they continually try to get a particular player executed, that player is probably good.
- Instead of revealing your information publicly, confide in other members of the town secretly. Someone else may have information that exonerates or condemns one of your choices, and it may be easier to persuade them to tell you what they know in secret.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Investigator and Vizier(Minion) are in the same game and if the Investigator learns that the Vizier is in play, the existence of the Vizier is not announced by the Storyteller.""", delete_after=600.0)

@bot.command()
async def juggler(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Juggler(Townsfolk)
On your 1st day, publicly guess up to 5 players' characters. That night, you learn how many you got correct.

On the first day, they may guess which players are which characters. That night, the Juggler learns how many guesses they got right...if they are not killed beforehand. They must make their guesses publicly, so everyone hears what is guessed. They may guess zero characters, or up to five characters, and these characters and players may be different or the same. If the Juggler made their guesses while drunk or poisoned, but is sober and healthy when their ability triggers that night, then the Storyteller still gives them true information.

Tips:
- Try to guess as many good characters as you can! The more good characters you are able to name and confirm, the more good players you'll have in the town that you can trust. This also helps protect you and other information gathering characters from the Demon - you might be a prime target alone, but the Demon will have to choose very carefully if a Savant, Flowergirl and yourself are out and active.
- Guessing that someone is an evil character is powerful if you can confirm it, but difficult without a lead.
- Guess the maximum amount of characters you can - you'll get a read on 5 people, and the number you get back will give you a LOT to work with, whether or not it backs up the claims made to you. Getting the fabled 5 is incredibly tricky, but manage it and you'll have 5 people you can completely trust - a massive blow for the evil team!
- Guess a small number of characters for focused information on a particular set of players. This can be especially effective for targeting evil players.
- A proactive Juggler is a high priority target for the Demon. Consider getting someone to double up with you to confuse the Demon about where the real Juggler is.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Juggler and Cannibal(Townsfolk) are in the same game, and if the Juggler guesses on their first day and dies by execution, tonight the living Cannibal learns how many guesses the Juggler got correct.""", delete_after=600.0)

@bot.command()
async def king(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# King(Townsfolk)
Each night, if the dead equal or outnumber the living, you learn 1 alive character. The Demon knows you are the King.

At the start of the game, the Demon learns who the King is. If a King is created mid-game, the Demon learns who the King is that night. If the king lives long enough, they will start to learn what roles are still alive in the game. There may not be a Choirboy in play. But if there is, and they are still alive when the Demon kills the King, the Choirboy learns who the Demon is.

Tips:
- The King is one of the few characters who can come out early and confidently. The Demon knows who the King is and knows they might be a possible trap if killed too early in the game. Because the Demon can only kill the King if they’re confident the Choirboy is out of the way, the King is likely to survive to the end game.
- Even if there isn’t a choirboy it would be good to get someone to cooperate with you to pretend to be, or just tell people you’ve heard of a choirboy.
- Coming out straight away as the King creates a fun gambit. Because the only other characters who are certain whether the King is in play or not are the Choirboy and the Demon.
- Because the King’s information at the end of the game can be very powerful and because Kings are prime suspects of being the Demon, the chance that a public King survives to the end game is quite low. If you go public, focus on using your position to form a trusted court around you rather than surviving.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Leviathan(Demon) and King are in play and at least 1 player is dead, the King learns an alive character each night.
- If the Riot(Demon) and King are in play and at least 1 player is dead, the King learns an alive character each night.""", delete_after=600.0)

@bot.command()
async def knight(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Knight(Townsfolk)
You start knowing 2 players that are not the Demon.

On the first night, the Knight learns two players who are not the Demon. On subsequent nights, they learn nothing more. The Knight can learn Townsfolk, Outsiders or even Minions’ names but does not learn which character type they are.

Tips:
- You know the two players you learnt aren’t the Demon. If both of them survive to the final three, you know two players that aren’t the Demon and therefore know who the Demon is and can win the game with your information!
- Hide what you learnt from the town - the Demon is going to actively want to kill the players you saw to avoid getting found out on the final day, so not telling people who you learnt means the Demon doesn’t know who to kill.
- Conceal your information and try to make the two players you saw just suspicious enough that they might be Demon candidates, but not suspicious enough that they get executed. This gives them the best odds of surviving to the final day.
- Come out with your information as early as possible to try to convince the good team to trust the players you know. Statistically they’re most likely to be good players too and can benefit from that trust and if they’re not good, they’re Minions, so it’s not the worst thing to give them a little undeserved trust.
- Hunt for sources of drunk or poison – you need to know if your information is true! If you suspect you were made drunk or poisoned on the first night, you probably want to kill both players that you saw as they’re more likely to be the Demon. Finding out you were drunk or poisoned can therefore win the game.
- Only reveal the players you learnt when they are nominated, to help keep them from being executed. This keeps the information from the Demon as long as you can, without hindering your ability to keep those players alive.""", delete_after=600.0)

@bot.command()
async def librarian(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Librarian(Townsfolk)
You start knowing that 1 of 2 players is a particular Outsider. (Or that zero are in play.)

During the first night, the Librarian learns that one of two players is a specific Outsider. They learn this only once and then learn nothing more. The Drunk is an Outsider. If the Librarian learns that one of two players is the Drunk, they do not learn the Townsfolk that the Drunk's player thinks they are.

Tips:
- It is vital to figure out early which of the two players is the one you have information about. The player that you know is good even if they are an Outsider - while their ability may be detrimental to the good team, they are a guaranteed good vote and also one player who you know for sure is definitely not the Demon.
- If you get a 0, this information is super powerful if you aren't the Drunk or poisoned, as then you know for sure there are no Outsiders in the game.
- You learn your information on the first night of the game. Revealing what you know early can help confirm a player as good, which might in turn confirm other information from Townsfolk.
- If you do not reveal your information until late in the game and the player you are confirming is still alive, then you can reveal them on the final day or close to it, taking them out of contention as a potential Demon and reducing the number of players for the good team to deliberate on from 3 to 2.
- Characters like the Saint would rather die at night than by execution. Since Outsiders are generally not targets a Demon will want to kill, you can try to bait the Imp into attacking them during the night. Perhaps you could imply that they are a powerful Townsfolk, or else you can make it known that they are confirmed not to be the Demon, meaning the real Demon will have to kill them in the night or have only 1 other person who might be the demon at the end of the game.""", delete_after=600.0)

@bot.command()
async def lycanthrope(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Lycanthrope(Townsfolk)
Each night*, choose an alive player. If good, they die & the Demon doesn’t kill tonight. One good player registers as evil.

The Lycanthrope must choose an alive player each night. If the Lycanthrope chooses a dead player, the Storyteller shakes their head no and prompts the Lycanthrope to choose a different player. If the player that the Lycanthrope chooses is good, that player dies, and the Demon can not kill tonight. If the player the Lycanthrope attacks is evil, that player does not die, and the Demon may still kill tonight. If the Lycanthrope attacks a good player but that good player doesn’t die, the Demon may still kill tonight. One good player registers as evil. They also register as evil to the Lycanthrope, so cannot be killed by the Lycanthrope.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Try to identify good players whose death will not cause a catastrophic loss of utility to the good team. By killing them and identifying them as good, you can begin to build a circle of trust among your allies.
- Beware of characters who can register as different alignments, such as the Spy and the Recluse. They may die in the night or live through the night despite you choosing them, confusing your information.
- In order to regain control of night-time deaths, the evil team will need to neutralize you. Consider being somewhat reserved in your daytime conversations.
- To build trust with other good players and to share as much information with the good team as possible, publicly claim to be the Lycanthrope on the first day. Since you choose who dies at night, the only way that you can die is if the good team executes you. You don't need to fear the Demon killing you, so being forthright and public with your information is usually very helpful for the good team.
- Don't be afraid to attack good players at night. If you attack an evil player, this allows the Demon to attack a good player anyway. Since a good player is almost certainly going to be the player that dies at night, who would you rather have choose which good player dies? You? Or the Demon?
- If you are fairly certain that a particular player is evil, and you don't mind dying to learn whether or not you are correct, attack them at night. If they are evil, they will not die to your choice and either the Demon will kill them by chance and have killed an evil player for you or they will not die and the Demon will kill another player - which is great because you've just learnt that a particular player is evil and the player that died instead is almost certainly good.""", delete_after=600.0)
    
@bot.command()
async def Magician(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Magician(Townsfolk)
The Demon thinks you are a Minion. Minions think you are a Demon.

On the first night, instead of learning which player is the Demon, the Minions are told that both players—the Demon and the Magician—are the Demon. On the first night, the Demon learns that the Magician player is one of its Minions. The Magician does not wake to learn anything. The Storyteller can point to the Magician and the evil players in any order, so that the evil players won’t know which player is the Magician. If the Poppy Grower dies and the Demon and Minions learn who each other are mid-game, the Magician ability has an effect that night, just as if it was the first night.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Look as evil as you can. Make poor decisions on who to nominate. Vote haphazardly. Say that trustworthy players are untrustworthy, or vice versa. The evil players think that you might be evil, so if you act more evil than the others, they may believe that you are the evil player, and the Magician is elsewhere.
- Evil players that believe that you are evil will tend to keep you alive. The Minions think that you might be the Demon. If you are nominated, pay attention to who doesn't vote for you, or who seems afraid to vote for you. You may have found some Minions.
- Choose a different character to bluff as, or stay silent about who you are for as long as possible. If the evil team learns that you are the Magician, the Minions will learn who the real Demon is and the Demon will learn who the real Minions are - this won't end the game, but it would mean that your ability no longer causes any disruption to the evil team.
- If you can find a confirmed good player, such as the Virgin or the Slayer, or an almost confirmed good player, such as the only Outsider in a one-Outsider game, tell them that you are the Magician. You need to stay alive as long as possible, and having at least one good player (plus several evil players) who don't want to execute you will help this.
- Stay alive as long as possible. Don't get executed. The Demon probably won't kill you at night, because they think that you are a Minion, so staying alive is up to you and the good team. The longer you are alive, the more your ability has an effect.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Magician and Lil’ Monsta(Demon) are in the same game, each night, the Magician chooses a Minion: if that Minion & Lil' Monsta are alive, that Minion babysits Lil’ Monsta.
- If the Magician and Spy(Minion) are in the same game, when the Spy sees the Grimoire, the Demon and Magician's character tokens are removed.
- If the Magician and Vizier(Minion) are in the same game, if the Vizier and Magician are both in play, the Demon does not learn the Minions.
- If the Magician and Widow(Minion) are in the same game, when the Widow sees the Grimoire, the Demon and Magician's character tokens are removed.""", delete_after=600.0)

@bot.command()
async def mathematician(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Mathematician(Townsfolk)
Each night, you learn how many players' abilities worked abnormally (since dawn) due to another character's ability.

The Mathematician knows how many things have gone wrong since dawn today. When an ability does not work in the intended way due to another character’s interference, the Mathematician will learn that it happened. They’ll learn that something went wrong if a piece of information was false but was supposed to be true, or if an ability should have worked but didn’t, due to another character. The Mathematician does not learn which players this happened to, only how many times it happened.

Tips:
- The Mathematician does not detect drunkenness or poisoning itself, but does detect when drunk or poisoned players’ abilities did not work as intended. The Recluse registering as evil to the Chef, and the poisoned Soldier dying from the Imp’s attack, would each be detected. The poisoned Empath getting true information would not.
- Remember that you won’t detect your own ability failing
- Your information is valuable, but only if you know what the rest of the town is doing. Get chatty with your fellow players and find out what their information is - figuring out who has an ability that isn't working correctly will help out the good team a lot. 
- Pay attention to game changes that would affect your data, and be wary if your data suddenly changes.
- Beware of the Vortox! Just like everyone else, all of your information will be false. If you are getting a low number, but it seems like a lot of Townsfolk are getting misinformation, you can suspect that this is in play. In particular, getting a '0' when others appear to be getting bad information is a great tell that you are poisoned OR a Vortox is in town.
- Unlike other townsfolk, the Mathematician doesn't need to be shy in coming out. Not only is your information most useful when shared, but even one night of it is incredibly powerful when it comes to helping the town.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Mathematician and Chambermaid(Townsfolk) are in the same game, the Chambermaid learns if the Mathematician wakes tonight or not, even though the Chambermaid wakes first.
- If the Mathematician and Lunatic(Outsider) are in the same game, the Mathematician learns if the Lunatic attacks a different player(s) than the real Demon attacked.""", delete_after=600.0)

@bot.command()
async def mayor(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Mayor(Townsfolk)
If only 3 players live & no execution occurs, your team wins. If you die at night, another player might die instead.

The Mayor can win by peaceful means on the final day. To survive, the Mayor sometimes "accidentally" gets someone else killed. If the Mayor is attacked and would die, the Storyteller may choose that a different player dies. Nobody learns how they died at night, just that they died. If there are just three players alive at the end of the day, and no execution occurred that day, then the game ends and good wins. Travellers count as players for the Mayor's victory, so must be exiled first. Remember that exiles are not executions.

Tips:
- Remember, if the Demon attacks the Mayor, and the Storyteller instead chooses a dead player, the Soldier, or a player protected by the Monk, that player does not die tonight, resulting in no kills that night.
- Your power activates on the final day, when just three players are alive. You may not know who the Demon is, but you can definitely win by not executing. Do whatever you can to convince the group that you are the Mayor. Everything. If the good team believes you, they will either not nominate anybody, or will deliberately tie votes so that no execution occurs.
- It is often best not to reveal that you are the Mayor until late in the game. If you reveal early, the Demon may spend night after night trying to kill you, and the Storyteller may let that attempt succeed.
- You might want to tell people that you're the Mayor. Winning the game with your ability requires trust from your fellow players, and being open and honest is a fine way to acheive that trust.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Mayor and Leviathan(Demon) are in the same game, no execution occurs on day 5, good wins.
- If the Mayor and Riot(Demon) are in the same game, the Mayor may choose to stop nominations. If they do so when only 1 Riot is alive, good wins. Otherwise, evil wins.""", delete_after=600.0)

@bot.command()
async def minstrel(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Minstrel(Townsfolk)
When a Minion dies by execution, all other players (except Travellers) are drunk until dusk tomorrow.

If a Minion is executed and dies, all players (except the Minstrel) become drunk immediately and stay drunk all through the night and all the following day. Townsfolk, Outsiders, Minions, and even Demons become drunk, but not Travellers. This doesn’t happen if a Minion died at night. If a dead Minion is executed, the Minstrel ability does not trigger—a dead character cannot die again! If a Minion is executed but does not die, the Minstrel’s ability does not trigger. If the Minstrel is drunk or poisoned when a Minion dies by execution, the Minstrel ability does not trigger.

Tips:
- At first glance, the Minstrel does not seem that powerful, but in actuality you gain some of the most reliable information in the game. After any day with an execution, you know with confidence that if anyone dies at night, the recent executee is not a Minion.
- If the town does successfully execute a Minion, the Minstrel ability will activate, and nobody will die that night. This does not mean that a night without death is any guarantee that your ability was the cause though.
- Gun for executions! The more executions, the better chance you have of getting a minion. Good players may be reluctant to execute anyone who isn't a demon suspect as the death count can be unexpected and heavy in Bad Moon Rising, but it is worth it to remove powerful Minions like the Assassin or Mastermind from play before they can do too much damage.
- Demons may be less likely to target you since they underestimate your power! Unless Minions are getting executed left and right, the Minstrel is likely to survive a little longer than other townsfolk without protections, simply because a Demon is going to be much more worried about an Exorcist or a Tea Lady surviving for another night.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Minstrel and Legion(Demon) are in the same game and if Legion died by execution today, Legion keeps their ability, but the Minstrel might learn they are Legion.""", delete_after=600.0)

@bot.command()
async def monk(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Monk(Townsfolk)
Each night*, choose a player (not yourself): they are safe from the Demon tonight.

Each night except the first, the Monk may choose to protect any player except themself. If the Demon attacks a player who has been protected by the Monk, then that player does not die. The Demon does not get to attack another player, there is simply no death tonight. The Monk does not protect against the Demon nominating and executing someone.

Tips:
- Your job is to try to prevent as many kills as possible at night. Try to predict who the Demon may target each night based on the available information in the game and how the players are acting. Every Demon is different, and figuring out the methodology of yours can enable you to save more than one player.
- Don't try to predict what the Demon will do. Instead, talk to your fellow players and find someone to keep alive at all costs.
- You are the only player that you cannot protect, and if you thwart the Demon, they are probably going to want to identify and kill you, so try to avoid the Demon's attention.
- If you successfully protect someone at night, you can be reasonably certain that they are good, since the Demon wanted them dead.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Leviathan(Demon) and Monk are in play, the Monk-protected player is safe from all evil abilities.
- If the Riot(Demon) and Monk are in play, the Monk-protected player is safe from all evil abilities.""", delete_after=600.0)

@bot.command()
async def nightwatchman(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Nightwatchman(Townsfolk)
Once per game, at night, choose a player: they learn you are the Nightwatchman.

No explanation, its pretty straightforward.

Tips:
- As the Nightwatchman, the two most important questions for you to ask yourself are "When should I use my ability?" and "On whom should I use my ability?" (Using the word "whom" instead of "who" makes you sound waaaay smarter ;)
- Using your ability early in the game makes sure that you get to use your ability. Like the Seamstress or the Slayer, it would be a shame to die on the first few days or nights of the game and never get to use your ability at all. using your ability early, even on a less-than-ideal player, means you get some benefit. And will often be more than enough. If someone, anyone, knows that you are the Nightwatchman, then they won't vote for you to be executed and will probably convince others that you are the Nightwatchman too.
- You can even use your ability on the first night if you want. This guarantees that you will gain some benefit, since no deaths can occur until the first day or the second night.
- Using your ability late in the game is riskier, because you will need both skill and luck to stay alive to get to that point, but much more useful. In extreme cases, it can win the game. For example, if just three players are alive and you choose one of them to learn that you are the Nightwatchman (and they reveal this to the group), then the possible Demon candidates has been reduced from one in three to one in two, or this may even reveal who the Demon is specifically, if the player you chose can be confirmed as good.""", delete_after=600.0)

@bot.command()
async def noble(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Noble(Townsfolk)
You start knowing 3 players, 1 and only 1 of which is evil

The noble starts knowing exclusively 2 Good players and 1 Evil player. This is helpful as if this information is publicly revealed and combined with other info its really helpful.

Tips:
- Wait until the game is nearly over to reveal what you know. It is likely that the Storyteller showed you one player that was a Minion, and did not show you the Demon player. If there are just 3 players left alive, and two of the players you know are dead, and you are fairly certain that the alive player you know is not the Demon, that increases your odds of choosing the right player to execute. If two players you know are still alive, that's even better (As you can tell I didn’t write this one but it is a great tip)
- If you can figure out which one is evil you know the other two are guaranteed good which helps clear two players.""", delete_after=600.0)

@bot.command()
async def oracle(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Oracle(Townsfolk)
Each night*, you learn how many dead players are evil.

Because the Oracle acts after the Demon attacks each night, the Oracle’s info refers to the players that are dead when dawn breaks and all players open their eyes. The Oracle detects dead Minions and Demons, but also any other players that are evil, such as evil Travellers, or Townsfolk or Outsiders that have been turned evil.

Tips:
- So long as you are getting a "0", you can trust that all the dead players are good, and can therefore work with them and use their information.
- The moment you are getting a "1" or more, evil has entered the realm of the dead, and you should now be very careful about who you speak to. Outsource your suspicions to the dead - they'll be incentivised to prove themselves good and can do a lot of the work of accusations for you.
- Most players who die at night will be good players; evil players want to stay alive as long as possible, so the demon will be focusing their kill on good player threats. If you suddenly start getting a read on an evil player, you should start your suspicions with the most recent executee.""", delete_after=600.0)

@bot.command()
async def pacifist(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Pacifist(Townsfolk)
Executed good players might not die.

When a good player is executed, the Storyteller chooses whether they die or live. As always, when abilities like this function in obvious ways, the group is not told why something has happened, only what has happened. The group learns that an execution succeeded, but that the executed player did not die—that is all. If a player is executed and remains alive, that still counts as the execution for today. No other nominations may happen.

Tips:
- Don't come out! Your ability keeps good players safe (at the Storyteller's discretion), and the evil team will want to remove you from play as soon as possible.
- You should always come out eventually, but how you choose to do so is up to you. For example, you may know a player you trust 100% is good, and reveal to them early and secretly. If your ability saves someone later, they will know immediately it was you. If you don't have someone you trust that much, then simply play carefully until you die, or until it's late enough in the game that people need to know who you are anyway.
- Your ability is more potent in the late game, so survive as long as you can. The Storyteller is simply more likely to save a good player at a critical juncture as the game comes to a climax than they are to rescue someone from the town's blood thirst on the first day.
- Wait for your ability to trigger before making any sort of reveal. Seeing someone be saved from execution unexpectedly will prime the good team to believe you are in play anyway, whereas revealing early and then seeing your ability activate may lean them towards believing some shenanigans are at play.""", delete_after=600.0)

@bot.command()
async def philosopher(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Philosopher(Townsfolk)
Once per game, at night, choose a good character: gain that ability. If this character is in play, they are drunk.

The Philosopher has no ability until they decide which character they want to emulate. They can do this once per game. When they do so, they gain that character’s ability. They do not become that character.
They may want to wait a while to choose. If the Philosopher chooses a character that is already in play, the player of that character becomes drunk. 

Tips:
- If the Philosopher then dies or becomes drunk or poisoned, the player they are making drunk becomes sober again. 
- If the Philosopher chose a character that was not in play at the time but is in play now, that character is drunk. 
- If the Philosopher gains an ability that works at night, they wake when that character would wake. If this ability is used on the first night only, they use it tonight.
- The Philosopher's strongest asset is their versatility. You can emulate any good character on the list! Try to get a read on what the good team is lacking and/or what would be most effective in countering the evil team. Every Townsfolk is a viable option!
- Using your ability early can often be to your benefit - the earlier you act, the more information and impact your new ability will have on the game overall. It also means that if the Demon kills you, at least you've gotten something to work with. Nobody wants to die a mere Philosopher!
- Selecting an ability later in the game is more risky, but allows you to make a more considered choice about who you become. You'll have a better idea of who is in play, what sort of evil you're competing with, and what kind of character would be most effective to strengthen the good team's position.""", delete_after=600.0)
    if(arg1=="true"):
        await ctx.send(f"""Jinxes:
- If the Philosopher and Bounty Hunter(Townsfolk) are on the same script, and the Philosopher gains the Bounty Hunter ability, a Townsfolk might turn evil.""", delete_after=600.0)

@bot.command()
async def pixie(ctx, arg1=None):
    await ctx.message.delete()
    await ctx.send(f"""# Pixie(Townsfolk)
You start knowing 1 in-play Townsfolk. If you were mad that you were this character, you gain their ability when they die.

The Pixie learns one townsfolk who is currently in play. The Pixie does not learn which player is this character. If they pretend to be this character, (Whether this is one day or multiple) they will inherit that character abilities. If you reveal you are the Pixie before you inherit their ability then you will lose the chance to inherit it. When the Townsfolk player dies, the Pixie does not learn this, and is not told that they have gained a new ability. They may learn this has happened if they wake at night and start gaining information, or are prompted to choose players.""", delete_after=600.0)
    await ctx.send(f"""Tips:
- Be as mad as possible as the Townsfolk you know is in play. Claim to be that character. Give the information that character would know. Claim to use your ability. Claim, loudly and often, that the other player is lying. Get them killed by any means necessary. Once this is all done, you will gain that character's ability - totes worth it!
- Be mad as the duplicate character from minute one, day one, and keep up the charade for every following day. This will go a long way to convincing the group that you are the duplicate character, as well as showing the Storyteller that you are mad.
- Don't be mad at all about being your duplicate character at all for a few days. Say nothing about it. Then, on the day that you think that you can get this player executed, be very mad as this character. If the Storyteller sees that you "have been" mad as the duplicate character, and that your madness got the duplicate character executed, they will very likely give you the Pixie madness benefit - that player's ability when that player dies.
- Once you have gained the ability of your duplicate character, you can safely come out publicly as the Pixie. You've got the new ability locked in now, so use it as much as you want, and let the duplicate character (and the group) know that you were the Pixie all along. An apology to the poor good player that you threw under the bus might be necessary ;)""", delete_after=600.0)



bot.run(token,  log_handler=handler, log_level=logging.DEBUG)