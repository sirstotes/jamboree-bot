import os

from random import randint
import discord
from discord.ext import commands
from dotenv import load_dotenv
#from bs4 import BeautifulSoup
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('VERIFICATION_CHANNEL')

intents = discord.Intents().all()
client = discord.Client()
bot = commands.Bot(command_prefix='j!', intents=intents)
bot.remove_command('help')

@bot.command()
async def help(ctx):
    await ctx.send('```General Commands:\n   j!submit [link] - Submit a game (remember to send the spectate link, not the replay link)\n   j!score - Shows your current score\n   j!get ["player"] - Shows the score of player (do not remove "")\n   j!leaderboard - Shows the leaderboard\nMod Commands:\nj!give ["player"] [amount]\nj!take ["player"] [amount]\nj!set ["player"] [value]\n```')
@bot.command()
async def set(ctx, member: discord.Member, value : int):
    if ctx.message.author.guild_permissions.manage_guild:
        player_file = open("players.txt","r+")
        read = player_file.readlines()
        print(read)
        player_file.close()
        print("%d will be set to %d"%(member.id,value))
        await ctx.send("%s has %d points."%(member.display_name, value))
        player_file = open("players.txt","w+")
        for i in range(len(read)):
            line = read[i]
            if str(member.id) in line:
                read[i+1] = str(value)+"\n"
                player_file.writelines(read)
                player_file.close()
                return
        player_file.writelines(read)
        player_file.write("\n"+str(member.id))
        player_file.write("\n"+str(value))
        player_file.close()
    else:
        await ctx.send("You do not have permission to use this command.")
@bot.command()
async def give(ctx, member: discord.Member, amount : int):
    if ctx.message.author.guild_permissions.manage_guild:
        player_file = open("players.txt","r+")
        read = player_file.readlines()
        player_file.close()

        player_file = open("players.txt","w+")
        for i in range(len(read)):
            line = read[i]
            if str(member.id) in line:
                read[i+1] = str(int(read[i+1])+amount)+"\n"
                player_file.writelines(read)
                player_file.close()
                await ctx.send("%s has %d points."%(member.display_name, int(read[i+1])))
                return
        player_file.writelines(read)
        player_file.write("\n"+str(member.id))
        player_file.write("\n"+str(amount))
        player_file.close()
        await ctx.send("%s has %d points."%(member.display_name, amount))
    else:
        await ctx.send("You do not have permission to use this command.")
@bot.command()
async def take(ctx, member: discord.Member, amount : int):
    if ctx.message.author.guild_permissions.manage_guild:
        player_file = open("players.txt","r+")
        read = player_file.readlines()
        player_file.close()

        player_file = open("players.txt","w+")
        for i in range(len(read)):
            line = read[i]
            if str(member.id) in line:
                read[i+1] = str(int(read[i+1])-amount)+"\n"
                player_file.writelines(read)
                player_file.close()
                await ctx.send("%s has %d points."%(member.display_name, int(read[i+1])))
                return
        player_file.writelines(read)
        player_file.write("\n"+str(member.id))
        player_file.write("\n"+str(-amount))
        player_file.close()
        await ctx.send("%s has %d points."%(member.display_name, -amount))
    else:
        await ctx.send("You do not have permission to use this command.")
@bot.command()
async def get(ctx, member: discord.Member):
    print("Returning the score of %s"%(member.display_name))
    player_file = open("players.txt","r+")
    read = player_file.readlines()
    print(read)
    for i in range(len(read)):
        line = read[i]
        if str(member.id) in line:
            print(read[i+1])
            player_file.close()
            await ctx.send("%s has %d points."%(member.display_name, int(read[i+1])))
            return
    player_file.write("\n"+str(member.id))
    player_file.write("\n0")
    player_file.close()
    await ctx.send("%s has %d points."%(member.display_name, 0))
@bot.command()
async def score(ctx):
    print("Returning the score of %s"%(ctx.message.author.display_name))
    player_file = open("players.txt","r+")
    read = player_file.readlines()
    print(read)
    for i in range(len(read)):
        line = read[i]
        if str(ctx.message.author.id) in line:
            print(read[i+1])
            player_file.close()
            await ctx.send("%s has %d points."%(ctx.message.author.display_name, int(read[i+1])))
            return
    player_file.write("\n"+str(ctx.message.author.id))
    player_file.write("\n0")
    player_file.close()
    await ctx.send("%s has %d points."%(ctx.message.author.display_name, 0))
@bot.command()
async def leaderboard(ctx):
    player_file = open("players.txt","r+")
    read = player_file.readlines()
    player_file.close()
    output = "**All Players:**```yaml\n"
    players = []
    for i in range(1, len(read), 2):
        if bot.get_user(int(read[i])) != None:
            players.append([ctx.message.author.guild.get_member(int(read[i])).display_name, int(read[i+1])])
    def sortSecond(val): 
        return val[1]
    players.sort(key=sortSecond,reverse=True)
    for i in range(len(players)):
        player = players[i]
        output += ""+player[0]+": "+str(player[1])+"\n"
    output += "```"
    await ctx.send(output)
@bot.command()
async def submit(ctx, game : str):
    if "skudpaisho.com" in game:
        page = requests.get(game)
        #check if webpage exists
        if page.status_code == 200:
            #-check if page is on list of pages
            game_file = open("games.txt", "r+")
            read = game_file.readlines()
            for i in range(1, len(read), 1):
                if game in read[i]:
                    print("REPEAT FOUND")
                    if int(read[i-1]) == ctx.message.author.id:
                        await ctx.send("Error: You have already submitted that game.")
                        return
            game_file.close()
            #--add page to list of pages
            game_file = open("games.txt", "a")
            game_file.write("\n"+str(ctx.message.author.id))
            game_file.write("\n"+game)
            game_file.close()
            print("Game is now in document")
            #--check if date is valid
            await ctx.send("Your game is submitted and awaiting verification!")
            confirmation_message = await ctx.guild.get_channel(int(CHANNEL)).send(str(ctx.message.author.id)+"\n"+ctx.message.author.display_name+" submitted "+game)
            await confirmation_message.add_reaction("❌")
            await confirmation_message.add_reaction("✅")
            await confirmation_message.add_reaction("‼️")
            await confirmation_message.add_reaction("⚠️")
            """soup = BeautifulSoup(page.content, 'html.parser')
            if "<h4>Adevăr Pai Sho</h4>" in str(page.content):
                print("Adevar Game")
                await ctx.send("Game submitted! Your score will increase by one.")
            else:
                await ctx.send("Error: Invalid Game")"""
        else:
            print("Error: "+str(page.status_code))
            await ctx.send("Error: Unable to Connect")
    else:
        print("Error")
        await ctx.send("Error: Invalid URL")
@bot.event
async def on_reaction_add(reaction, user):
    if user.guild_permissions.manage_guild and reaction.message.author == bot.user and user != bot.user:
            if "submitted" in reaction.message.content:
                print("Reaction")
                userid = int(reaction.message.content[0:18])
                print(userid)
                member = user.guild.get_member(userid)
                if str(reaction) == "✅":
                    print("Game Accepted")
                    if userid != None and member != None:
                        player_file = open("players.txt","r+")
                        read = player_file.readlines()
                        player_file.close()

                        player_file = open("players.txt","w+")
                        for i in range(len(read)):
                            line = read[i]
                            if str(member.id) in line:
                                read[i+1] = str(int(read[i+1])+1)+"\n"
                                player_file.writelines(read)
                                player_file.close()
                                await reaction.message.channel.send("Game verified! %s has %d points."%(member.display_name, int(read[i+1])))
                                await reaction.message.delete()
                                await member.send("Your game has been verified. You now have %d points."%(int(read[i+1])))
                                return
                        player_file.writelines(read)
                        player_file.write("\n"+str(member.id))
                        player_file.write("\n"+str(1))
                        player_file.close()
                        await reaction.message.channel.send("Game verified! %s has 1 point."%(member.display_name))
                        await member.send("Your game has been verified. You now have 1 point.")
                        await reaction.message.delete()
                elif str(reaction) == "❌":
                    print("Game Denied")
                    await reaction.message.channel.send("Game submission by %s denied!"%(member.display_name))
                    await reaction.message.delete()
                    await member.send("Your game has been denied. No reason specified")
                elif str(reaction) == "‼️":
                    print("Game Denied")
                    await reaction.message.channel.send("Game submission by %s denied!"%(member.display_name))
                    await reaction.message.delete()
                    await member.send("Your game has been denied. Reason: invalid game")
                elif str(reaction) == "⚠️":
                    print("Game Denied")
                    await reaction.message.channel.send("Game submission by %s denied!"%(member.display_name))
                    await reaction.message.delete()
                    await member.send("Your game has been denied. Reason: wronk kind of link. (Remember to send the spectate link, not the replay link)")
                else:
                    print(reaction)
bot.run(TOKEN)