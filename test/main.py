
import discord
import os
import asyncio
#from keep_alive import keep_alive
import json
import spacy
import random
import numpy as np
from simpleneighbors import SimpleNeighbors

## load model
nlp = spacy.load('en_core_web_lg')
movie_lines = {}
responses = {}
nns = SimpleNeighbors(300)

# load chatbot
# Intents specify which bucket of events you want to get access to.
intents = discord.Intents.default()
intents.message_content = True

recognized_bot = [
  "Cuijbnojb#8168", "JYBX_23#3169", "bobot1#7924", "bobot2#9520", "bobot0#6671"
]
allowed_channels = [1076802612793442314]  # channels : #hhh,
allow_loop = True

client = discord.Client(intents=intents)


## calculate sentence vector
def sentence_mean(nlp, s):
  if s == "":
    s = " "
  doc = nlp(s, disable=['tagger', 'parser'])
  return np.mean(np.array([w.vector for w in doc]), axis=0)


## file -> dict
def turns_init():
  # turns
  for line in open("./cornell movie-dialogs corpus/movie_lines.txt",
                   encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    if len(parts) == 5:
      movie_lines[parts[0]] = parts[4]
    else:
      movie_lines[parts[0]] = ""
  # turns which has responses
  for line in open("./cornell movie-dialogs corpus/movie_conversations.txt",
                   encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    line_ids = json.loads(parts[3].replace("'", '"'))
    for first, second in zip(line_ids[:-1], line_ids[1:]):
      responses[first] = second


## create a dataset of sentence which has reply
def nns_built():
  for i, line_id in enumerate(random.sample(list(responses.keys()), 10000)):
    # show progress
    if i % 2000 == 0: print(i, line_id, movie_lines[line_id])
    line_text = movie_lines[line_id]
    summary_vector = sentence_mean(nlp, line_text)
    if np.any(summary_vector):
      nns.add_one(line_id, summary_vector)
  nns.build()


def pick_near(s):
  return (nns.nearest(sentence_mean(nlp, s), 5)[0])


# # Print to the console when everything has connected properly
# @client.event
# async def on_ready():
#   print(f'We have logged in as {client.user}')


# # Main function that you will want to edit. Listens for messages, and does something based on it.
# @client.event
# async def on_message(message):
#   # ignore yourself and in not allowed_channels
#   global allow_loop
#   if message.author == client.user:
#     return
#   if message.channel.id not in allowed_channels:
#     return
#   await message.channel.send(movie_lines[pick_near(message.content)])
#   # # only recognized-bot can use this to chat
#   # print(client.user)
#   # print(message.author)
#   # if client.user in message.mentions:
#   #   if allow_loop:
#   #     if str(message.author) in recognized_bot:
#   #       # TODO : Processing Bot-MSG
#   #       await message.channel.send(f"speak, next chatbot!")

#   # # Start chatbot chat
#   # if "!bobot1" in message.content:
#   #   allow_loop = True
#   #   await message.channel.send(f"now, start loop!")
#   #   # TODO : COPY THE CODE - CREATE chatloop

#   # # Stop
#   # if ('stop' in message.content):
#   #   await message.channel.send("Bang!")
#   #   allow_loop = False


# keep_alive()
if __name__ == '__main__':
  #token = os.getenv("DISCORD_BOT_SECRET")
  turns_init()
  nns_built()
  print()
  print(movie_lines[responses[pick_near("don't shoot me")]])
  while(True) :
    s = input("You : ")
    print(f'Mbot : ',{movie_lines[responses[pick_near(s)]]})

  #client.run(token)
