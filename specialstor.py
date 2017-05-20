import discord
import asyncio
import aioodbc
import configparser
import os.path
import sys
import logging

log = logging.getLogger('SPECIALStor')
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

config = configparser.ConfigParser()

if os.path.isfile('./config.ini'):
	config.read('./config.ini')
else:
	config['Command'] = {'Prefix': '+ss'}
	config['API keys'] = {'Discord': ''}
	config['Logging'] = {'Level': 'INFO'}
	config['Other'] = {'ImagesPerRequest': 50}

	with open('./config.ini', 'w') as cfgfile:
		config.write(cfgfile)

	log.info('Config file generated!')
	log.info('Edit config.ini before starting SPECIALStor.')
	sys.exit(1)

level = logging.getLevelName(config.get('Logging', 'Level', fallback = 'INFO'))

try:
	log.setLevel(level = level)
except ValueError:
	log.setLevel(level = logging.INFO)

DISCORD_API_TOKEN = config.get('API keys', 'Discord')
COMMAND_PREFIX = config.get('Command', 'Prefix', fallback = '!')

client = discord.Client()
helpgame = discord.Game(name = COMMAND_PREFIX + 'help for help', url = "", type = 0)

@client.event
async def on_ready():
	log.info('Logged in as ' + client.user.name + ' (' + client.user.id + ')')
	log.info('Use this link to invite me to your server: ' + discord.utils.oauth_url(client.user.id, permissions = discord.Permissions(permissions = 19456)))
	await client.change_presence(game = helpgame, afk = False)

@client.event
async def on_error(event, *args, **kwargs):
	log.error('Exception occurred in ' + event, exc_info = True)

@client.event
async def on_message(message):
	if message.content.startswith(COMMAND_PREFIX) and not message.author.bot:
		await client.send_message(message.channel, 'Hello, ' + message.author.mention + '!')

log.info('SPECIALStor starting...')

try:
	client.run(DISCORD_API_TOKEN)
except:
	log.critical('An error occurred while starting SPECIALStor', exc_info = True)