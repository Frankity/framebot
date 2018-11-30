import discord
import asyncio
import yaml

from plugins.warframe import warframe
from models import *

client = discord.Client()


def initialize_db():
    db.connect()
    db.create_tables([Alerts], safe=True)
    db.close()


initialize_db()

try:
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
except Exception as e:
    print(e)
    raise


@client.event
async def on_ready():
    print('logged in')
    print('nick: ' + client.user.name)
    print('playing: ' + config['playing'])
    print('id: ' + client.user.id)
    print('-------------')
    await client.change_presence(game=discord.Game(name=config['playing']))


async def get_alerts():
    await client.wait_until_ready()
    while not client.is_closed:
        try:
            d = warframe.get_alerts()
            for a in d:

                embed = discord.Embed(description=' ')
                embed.title = "Planet / System: %s" % (a['mission']['node'])
                embed.colour = 0xff6600  # blurple
                embed.add_field(name='Type', value=a['mission']['type'])
                embed.add_field(name='Faction', value=a['mission']['faction'])
                embed.add_field(name='Credits', value=a['mission']['reward']['credits'])
                embed.add_field(name='Item', value=a['mission']['reward']['itemString'] if a['mission']['reward']['itemString'] else "Nothing")
                embed.add_field(name='Max/Min Level', value="%s - %s" % (a['mission']['minEnemyLevel'], a['mission']['maxEnemyLevel']))
                embed.add_field(name='AchWing Required?', value=a['mission']['archwingRequired'])

                embed.set_thumbnail(url=a['mission']['reward']['thumbnail'])

                # await asyncio.sleep(5)

                await client.send_message(discord.Object(id=config['alerts_channel']), embed=embed)

        except Exception as e:
            print(e)
        await asyncio.sleep(60)

try:
    client.loop.create_task(get_alerts())
    client.run(config['token'])
except Exception as e:
    raise
