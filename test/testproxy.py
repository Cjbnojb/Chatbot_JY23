import discord
import os
import asyncio
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

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
    
  # Start chatbot chat    
  if "!bobot1" in message.content:
    allow_loop = True
    await message.channel.send(f"now, start loop!")
    # TODO : COPY THE CODE - CREATE chatloop

  # Stop
  if ('stop' in message.content):
    await message.channel.send("Bang!")
    allow_loop = False

client.run("MTA3Mzg0NjgxMzAxNjIxNTU3Mg.GYQNTk.JVrBRLiYKfQp40OB-Iyw7sC37fsVp1Qp9B9a4w")