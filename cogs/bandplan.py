import disnake
from disnake.ext import commands
from datetime import datetime
import json

class BandPlan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/bandplan.json", "r") as f:
            self.bandplans = json.load(f)

    async def bandplan_autocomplete(self, inter: disnake.ApplicationCommandInteraction, string: str):
        return [b for b in self.bandplans.keys() if string.lower() in b.lower()]

    @commands.slash_command(name="view_bandplan", description="View info on a specific band.")
    async def bandplan_info(self, inter: disnake.ApplicationCommandInteraction, selected_bandplan: str = commands.Param(autocomplete=bandplan_autocomplete, description="The band you want to view e.g. 2m")):
        now = datetime.now()
        if selected_bandplan not in self.bandplans:
            await inter.response.send_message("Band not found!", ephemeral=True)
            return

        bandplan = self.bandplans[selected_bandplan]
        desc = f"Range: **{bandplan['range']}**\n\nStatus: **{bandplan['status']}**\n\nCalling Frequency: **{bandplan['calling_frequency']}**\n\nModes: **{bandplan['modes']}**\n\nNotes: {bandplan['notes']}"

        embed = disnake.Embed(
            title=f"**Bandplan info for {bandplan['name']}**",
            description=desc,
            color=disnake.Color.blurple()
        )

        embed.set_author(
            name="RadioReady",
            url="https://github.com/CaptainAarav/RadioReady"
        )

        embed.set_footer(text=f"Data most recent of {now.strftime('%d/%m/%Y %H:%M')}")

        await inter.response.send_message(embed=embed)



def setup(bot):
    bot.add_cog(BandPlan(bot))