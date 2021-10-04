import discord, requests, json, urllib
from discord.ext import commands, tasks
from os import system
from urllib.request import urlopen
from datetime import timedelta, datetime
import time

client = commands.Bot(command_prefix='$')
client.remove_command('help')

#ON READY
@client.event
async def on_ready():
    print('#[SPDR] - SpiderBot Success')

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command")
        print("#[SPDR] - Unknown command")

#KICK
@client.command(name='kick')
@commands.has_permissions(administrator=True)
async def kick(ctx, user: discord.Member, *, reason="none"):
    if user == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself")
        print(f"#[SPDR] - Failed selfkick on {user}")
        return
    
    await user.kick(reason=reason)
    kickembed=discord.Embed(title=":joy_cat: LowDog Kicked :joy_cat:", description=f"{user} has been kicked.")
    await ctx.send(embed=kickembed)
    print(f"#[SPDR] - Kicked {user} successfully")

#BAN
@client.command(name='ban')
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.Member, *, reason="none"):
    if user == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself, NN Dog")
        print(f"#[SPDR] - Failed selfban on {user}")
        return
    await user.ban(reason=reason)
    banembed=discord.Embed(title=":joy_cat: LowDog Banned :joy_cat:", description=f"{user} has been banned.")
    await ctx.send(embed=banembed)
    print(f"#[SPDR] - Banned {user} successfully")

#CLEAR CHANNEL
@client.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("Invalid Channel")
        return
    clearembed=discord.Embed(title=":exclamation: Channel Cleared :exclamation:", description=f"#{channel.name} has been cleared.")
    clear_channel = discord.utils.get(ctx.guild.channels, name=channel.name)
    if clear_channel is not None:
        new_channel = await clear_channel.clone(reason="none")
        await clear_channel.delete()
        await new_channel.send(embed=clearembed)
        print(f"#[SPDR] - {ctx.message.author} cleared the {channel.name} channel")
    else:
        await ctx.send(f"No channel named {channel.name} was found!")
        print(f"#[SPDR] - {ctx.message.author} failed clear, invalid channel")

#START AUCTION
@client.command(name='startauction')
@commands.has_permissions(administrator=True)
async def startauction(ctx, name: str, sBid: int, bNow):
    global activeName
    global auctionRunning
    global minBid
    activeName = name
    auctionRunning = 1
    minBid = sBid
    newauction=discord.Embed(title=":money_with_wings: New Auction :money_with_wings:", description=f"{ctx.message.author} has began an auction: \n Name: {name} \n Starting Bid: ${sBid} \n BIN: ${bNow}")
    await ctx.send(embed=newauction)
    print(f"#[SPDR] - {ctx.message.author} started an auction, auction status set to true")


#END AUCTION
@client.command(name='endauction')
@commands.has_permissions(administrator=True)
async def endauction(ctx, name, sPrice, winner: discord.Member):
    auctionRunning = 0
    endauction=discord.Embed(title=":money_with_wings: Auction Ended :money_with_wings:", description=f"{ctx.message.author} has ended an auction: \n Winner: {winner} \n Name: {name} \n Price: ${sPrice}")
    await ctx.send(embed=endauction)
    print(f"#[SPDR] - {ctx.message.author} ended an auction, auction status set to false")
    
#PLACE BID
@client.command()
async def bid(ctx, name, bid: int):
    if activeName != name:
        notrunning = discord.Embed(title=":warning: Invalid Name :warning:", description=f"{name} Is Not For Auction")
        await ctx.send(embed=notrunning)
        print(f"#[SPDR] - {ctx.message.author} tried to bid on an invalid name")
    else:
        if auctionRunning==1:
            if bid<minBid:
                pooralert = discord.Embed(title=":warning: Below Min Bid :warning:", description="Bid Is Below Minimium Bid")
                await ctx.send(embed=pooralert)
                print(f"#[SPDR] - {ctx.message.author} tried to bid below the minimium bid")
            else:
                bidsuccess=discord.Embed(title=":money_with_wings: BID PLACED :money_with_wings:", description=f"Name: {name} \n Bidder: {ctx.message.author} \n Bid: ${bid}")
                await ctx.send(embed=bidsuccess)
                print(f"#[SPDR] - {ctx.message.author} placed a bid on {name} for ${bid}")
        else:
            bidalert=discord.Embed(title=":money_with_wings: No Auction Running :money_with_wings:", description=f"There is currently no active auction")
            await ctx.send(embed=bidalert)
            print(f"#[SPDR] - {ctx.message.author} tried to bid on {name} when no auction was available for ${bid}")
    

#Run Client
client.run('your token here')
