import disnake
from disnake.ext import commands
from models import User
from datetime import datetime

now = datetime.now()

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(name="my_stats", description="View your own user stats.")
    async def my_stats(self, inter: disnake.ApplicationCommandInteraction):
        user, _ = await User.get_or_create(discord_id = inter.author.id)
        rank = ""
        progress = 0
        filled = 0
        remaining = 0
        
        if user.correct_answers < 50:
            progress = (user.correct_answers / 50) * 100
            filled = int(user.correct_answers / 50 * 20)
            remaining = 50 - user.correct_answers
            rank = "foundation"
        elif user.correct_answers > 49 and user.correct_answers < 100:
            progress = (user.correct_answers / 50) * 100
            filled = int(user.correct_answers / 100 * 20)
            remaining = 50 - user.correct_answers
            rank = "intermediate"
        else:
            progress = 100
            filled = 20
            remaining = "no"
            rank = "full"
            
        progressBar = "█" * filled + "░" * filled - 20
        
        description = f"""Quizzes Done: **{user.total_quizzes}** 
        \n\n
        Correct Answers: **{user.correct_answers}** 
        \n\n 
        Decibels: **{user.db_points}** 
        \n\n
        Rank: **{rank}**, you have to do {remaining} more to get to the next rank!
        \n
        {progressBar} {progress}%"""
        
        embed = disnake.Embed(
			title=f"**📊 Your Stats {inter.author}**",
			description=description,
			color=disnake.Color.blurple()
		)
        
        embed.set_author(
			name="RadioReady",
			url="https://github.com/CaptainAarav/RadioReady"
		)
        
        embed.set_footer(text=f"Stats based of data at {now.strftime("%d/%m/%Y %H:%M")}")
        
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(name="search_stats", description="Search another persons stats up.")
    async def search_stats(self, inter: disnake.ApplicationCommandInteraction, other_person: disnake.User):
        await inter.response.send_message("Here are there stats!")
        
    @commands.user_command(name="see_stats")
    async def see_stats(self, inter: disnake.ApplicationCommandInteraction, other_person: disnake.User):
        await inter.response.send_message("Here are there stats!")
        
    @commands.slash_command(name="give_decibels", description="Give someone else some of your decibels.")
    async def give(self, inter: disnake.ApplicationCommandInteraction, amount: int, other_person: disnake.User):
        await inter.response.send_message("gave decibels to user!")
        
def setup(bot):
    bot.add_cog(UserCommands(bot))