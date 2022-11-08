# coding: UTF-8
import os
import discord

my_secret = os.environ['DISCORD_TOKEN']
DISCORD_GUILD = {
  1039253144082858196: {
    "members": {},
  }
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  add_s = 's' if len(message.attachments) > 1 else ''
  if message.attachments:
    if message.author not in DISCORD_GUILD[message.guild.id].get('members'):
      DISCORD_GUILD[message.guild.id].get('members').update(
        {message.author: 0})
    DISCORD_GUILD[message.guild.id].get('members')[message.author] += len(
      message.attachments)
    await message.channel.send(
      f'{len(message.attachments)} point{add_s} pour {message.author}!')

  if message.content.startswith('/score'):
    scores = [(m.name, DISCORD_GUILD[message.guild.id].get('members')[m])
              for m in DISCORD_GUILD[message.guild.id].get('members')]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    max = 0
    for s in scores:
      max = s[1] if s[1] > max else max
      add_s = 's' if s[1] > 1 else ''
      await message.channel.send(f'{s[0]} avec {s[1]} point{add_s}')
      if max != s[1] and s[1] == 1:
        await message.channel.send('Looser!')


#    a = [('toto', 2), ('tata', 1), ('tutu', 1)]
#    max = 0
#    for s in a:
#      max = s[1] if s[1] > max else max
#      add_s = 's' if s[1] > 1 else ''
#      await message.channel.send(f'{s[0]} avec {s[1]} point{add_s}')
#      if max != s[1] and s[1] == 1:
#        await message.channel.send('Looser!')

client.run(my_secret)
