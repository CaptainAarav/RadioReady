import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
from tortoise import Tortoise


load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = commands.InteractionBot(test_guilds=[1500567010734772316])

@bot.event
async def on_ready():
    await Tortoise.init(
		db_url="sqlite://db.sqlite3",
		modules={"models": ["models"]}
	)
    await Tortoise.generate_schemas()
    print("Bot is ready!")

@bot.slash_command(name="ping", description="pings the bot and checks weather it's responding")
async def ping(inter: disnake.ApplicationCommandInteraction):
	await inter.response.send_message(f"{inter.author.mention}, Pong!")
 
bot.load_extension("cogs.quiz")
bot.load_extension("cogs.user")
bot.load_extension("cogs.bandplan")
bot.load_extension("cogs.qcode")

bot.run(TOKEN)