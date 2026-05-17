import disnake
from disnake.ext import commands
from datetime import datetime
import json

class QCode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open ("data/qcodes.json", "r") as f:
            self.qcodes = json.load(f)

    async def qcode_autocomplete(self, inter: disnake.ApplicationCommandInteraction, string: str):
        return [q for q in self.qcodes.keys() if string.lower() in q.lower()]

    @commands.slash_command(name="qcode_info", description="Look up a Q-code e.g. QRM, QSL, QTH")
    async def qcode_info(self, inter: disnake.ApplicationCommandInteraction, selected_qcode: str = commands.Param(autocomplete=qcode_autocomplete, description="The qcode you want to view e.g. QSO")):
        now = datetime.now()

        if selected_qcode not in self.qcodes:
            await inter.response.send_message("Qcode not found!", ephemeral=True)
            return

        qcode = self.qcodes[selected_qcode]
        desc = f"Name: **{selected_qcode}** \n\n Meaning: **{qcode['meaning']}** \n\n Question: **{qcode['question']}** \n\n Notes: **{qcode['notes']}**"

        embed = disnake.Embed(
            title=f"**Qcode info for {selected_qcode}**",
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
    bot.add_cog(QCode(bot))