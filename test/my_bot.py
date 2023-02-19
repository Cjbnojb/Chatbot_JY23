import discord
import os
import asyncio
from keep_alive import keep_alive

# Intents specify which bucket of events you want to get access to.
intents = discord.Intents.default()
intents.message_content = True
#intents.members = True 未激活

recognized_bot = ["Cuijbnojb#8168", "JYBX_23#3169", "bobot1#7924", "bobot2#9520", "bobot0#6671"]
allowed_channels = [1076802612793442314] # channels : #hhh, 
allow_loop = True

client = discord.Client(intents=intents)

# Print to the console when everything has connected properly
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  
# Main function that you will want to edit. Listens for messages, and does something based on it.
@client.event
async def on_message(message):  
  # ignore yourself and in not allowed_channels
  global allow_loop
  if message.author == client.user:
    return
  if message.channel.id not in allowed_channels:
    return
  
  # only recognized-bot can use this to chat
  print(client.user)
  print(message.author)
  if client.user in message.mentions:
    if allow_loop:
      if str(message.author) in recognized_bot:
      # TODO : Processing Bot-MSG
        await message.channel.send(f"speak, next chatbot!")
        
  # Start chatbot chat    
  if "!bobot1" in message.content:
    allow_loop = True
    await message.channel.send(f"now, start loop!")
    # TODO : COPY THE CODE - CREATE chatloop

  # Stop
  if ('stop' in message.content):
    await message.channel.send("Bang!")
    allow_loop = False

# keep_alive()
token = os.getenv("DISCORD_BOT_SECRET")
client.run(token)
