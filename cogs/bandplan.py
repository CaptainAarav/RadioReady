import disnake
from disnake.ext import commands
from datetime import datetime
import json

class Bandplan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/bandplan.json", "r") as f:
            self.bandplans = json.load(f)
            
    @commands.slash_command(name="view_bandplan", description="View info on a specific bandplan.")
    async def view_bandplan(self, inter: disnake.ApplicationCommandInteraction, selected_bandplan: str = ):
        
            
def setup(bot):
    bot.add_cog(Bandplan(bot))