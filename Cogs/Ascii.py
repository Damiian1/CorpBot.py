import asyncio
import discord
import random
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import DisplayName
from   Cogs import Nullify
import requests
import urllib
	
class Ascii:
    
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def ascii(self, ctx, *, text : str = None):
		"""Beautify some text (font list at http://artii.herokuapp.com/fonts_list)."""

		if text == None:
			await self.bot.send_message(ctx.message.channel, 'Usage: `$ascii [font (optional)] [text]`\n(font list at http://artii.herokuapp.com/fonts_list)')
			return

		# Get list of fonts
		fonturl = "http://artii.herokuapp.com/fonts_list"
		get_request = self.bot.loop.run_in_executor(None, requests.get, fonturl)
		response = await get_request
		fonts = response.text.split()

		font = None
		# Split text by space - and see if the first word is a font
		parts = text.split()
		if len(parts) > 1:
			# We have enough entries for a font
			if parts[0] in fonts:
				# We got a font!
				font = parts[0]
				text = ' '.join(parts[1:])
	
		url = "http://artii.herokuapp.com/make?{}".format(urllib.parse.urlencode({'text':text}))
		if font:
			url += '&font={}'.format(font)
		get_request = self.bot.loop.run_in_executor(None, requests.get, url)
		response = await get_request
		await self.bot.say("```Markup\n {} ```".format(response.text))