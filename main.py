import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
from tortoise import Tortoise


load_dotenv()

TOKEN = os.getenv("TOKEN")
DEV_MODE = os.getenv("DEV_MODE") == "true"
test_guilds = [1505669040881012988] if DEV_MODE else None
bot = commands.InteractionBot(intents=disnake.Intents.default(), test_guilds=test_guilds)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception):
	await inter.response.send_message(f"An error occurred: {error}", ephemeral=True)
	raise error

async def setup_db():
	await Tortoise.init(
		db_url="sqlite://db.sqlite3",
		modules={"models": ["models"]}
	)
	await Tortoise.generate_schemas()

bot.loop.create_task(setup_db())

@bot.slash_command(name="ping", description="pings the bot and checks whether it's responding")
async def ping(inter: disnake.ApplicationCommandInteraction):
	await inter.response.send_message(f"{inter.author.mention}, Pong!")
 
bot.load_extension("cogs.quiz")
bot.load_extension("cogs.user")
bot.load_extension("cogs.bandplan")
bot.load_extension("cogs.qcode")

bot.run(TOKEN)