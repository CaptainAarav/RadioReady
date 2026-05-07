import disnake
from disnake.ext import commands
from models import User
from datetime import datetime

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def get_rank(self, correct_answers: int):
        if correct_answers < 50:
            return "Foundation", int((correct_answers / 50) * 100), int(correct_answers / 50 * 20), 50 - correct_answers
        elif correct_answers < 100:
            return "Intermediate", int((correct_answers / 100) * 100), int(correct_answers / 100 * 20), 100 - correct_answers
        else:
            return "Full", 100, 20, 0
    
    @commands.slash_command(name="my_stats", description="View your own user stats.")
    async def my_stats(self, inter: disnake.ApplicationCommandInteraction):
        now = datetime.now()
        user, _ = await User.get_or_create(discord_id = inter.author.id)
        
        rank, progress, filled, remaining = self.get_rank(user.correct_answers)
            
        progressBar = ("█" * filled) + ("░" * (20 - filled))
        next_rank_text = "you have reached the highest rank!" if remaining == 0 else f"you have to do {remaining} more to get to the next rank!"
        
        description = f"\n\n Quizzes Done: **{user.total_quizzes}** \n\n Correct Answers: **{user.correct_answers}** \n\n Decibels: **{user.db_points}** \n\n Rank: **{rank}**, {next_rank_text} \n\n {progressBar} {progress}%"
        
        #epsteins favorite number
        #00685
        
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
        now = datetime.now()
        user, _ = await User.get_or_create(discord_id = other_person.id)
        
        rank, progress, filled, remaining = self.get_rank(user.correct_answers)
            
        progressBar = ("█" * filled) + ("░" * (20 - filled))
        next_rank_text = "they have reached the highest rank!" if remaining == 0 else f"they have to do {remaining} more to get to the next rank!"
        
        description = f"\n\n Quizzes Done: **{user.total_quizzes}** \n\n Correct Answers: **{user.correct_answers}** \n\n Decibels: **{user.db_points}** \n\n Rank: **{rank}**, {next_rank_text} \n\n {progressBar} {progress}%"
        
        embed = disnake.Embed(
			title=f"**📊 Stats for {other_person.name}**",
			description=description,
			color=disnake.Color.blurple()
		)
        
        embed.set_author(
			name="RadioReady",
			url="https://github.com/CaptainAarav/RadioReady"
		)
        
        embed.set_footer(text=f"Stats based of data at {now.strftime("%d/%m/%Y %H:%M")}")
        
        await inter.response.send_message(embed=embed)
        
    @commands.user_command(name="see_stats")
    async def see_stats(self, inter: disnake.ApplicationCommandInteraction, other_person: disnake.User):
        now = datetime.now()
        user, _ = await User.get_or_create(discord_id = other_person.id)
        
        rank, progress, filled, remaining = self.get_rank(user.correct_answers)
            
        progressBar = ("█" * filled) + ("░" * (20 - filled))
        next_rank_text = "they have reached the highest rank!" if remaining == 0 else f"they have to do {remaining} more to get to the next rank!"
        
        description = f"\n\n Quizzes Done: **{user.total_quizzes}** \n\n Correct Answers: **{user.correct_answers}** \n\n Decibels: **{user.db_points}** \n\n Rank: **{rank}**, {next_rank_text} \n\n {progressBar} {progress}%"
        
        embed = disnake.Embed(
			title=f"**📊 Stats for {other_person.name}**",
			description=description,
			color=disnake.Color.blurple()
		)
        
        embed.set_author(
			name="RadioReady",
			url="https://github.com/CaptainAarav/RadioReady"
		)
        
        embed.set_footer(text=f"Stats based of data at {now.strftime("%d/%m/%Y %H:%M")}")
        
        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(name="give_decibels", description="Give someone else some of your decibels.")
    async def give(self, inter: disnake.ApplicationCommandInteraction, amount: int, other_person: disnake.User):
        now = datetime.now()
        user, _ = await User.get_or_create(discord_id = inter.author.id)
        other_user, _ = await User.get_or_create(discord_id = other_person.id)
        user_balance = user.db_points
        other_user_balance = other_user.db_points
        
        if other_person.id == inter.author.id:
            await inter.response.send_message("You can't give decibels to yourself!", ephemeral=True)
            return
        
        if amount <= 0:
            await inter.response.send_message("You can not give negative or 0 decibels!", ephemeral=True)
            return
        
        if user_balance >= amount:
            user.db_points -= amount
            other_user.db_points += amount
            await user.save()
            await other_user.save()
            
            embed = disnake.Embed(
                title=f"**Gave {amount} decibels to {other_person.name}**",
                description=f"You succesfully gave {amount} to {other_person.name}, you now have **{user_balance}** decibels remaining",
                color=disnake.Color.green()
            )
            
            embed.set_author(
                name="RadioReady",
                url="https://github.com/CaptainAarav/RadioReady"
            )
            
            embed.set_footer(text=f"Transfer done on {now.strftime("%d/%m/%Y %H:%M")}")
            
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"**Failed to give {amount} decibels to {other_person.name}**",
                description=f"Transfer of {amount} decibels to {other_person.name} did not go through, this is because you do not have enough balance. \n You have {user_balance} decibals which is less than {amount} decibals",
                color=disnake.Color.red()
            )
            
            embed.set_author(
                name="RadioReady",
                url="https://github.com/CaptainAarav/RadioReady"
            )
            
            embed.set_footer(text=f"{now.strftime("%d/%m/%Y %H:%M")}")
            
            await inter.response.send_message(embed=embed)
        
        
        
def setup(bot):
    bot.add_cog(UserCommands(bot))