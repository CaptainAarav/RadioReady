import disnake
from disnake.ext import commands
import json
import random

class QuizView(disnake.ui.View):
    def __init__(self, question: dict):
        super().__init__(timeout=30)
        self.question = question
        self.answered = False

    @disnake.ui.button(label="A", style=disnake.ButtonStyle.secondary)
    async def button_a(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("A", inter)

    @disnake.ui.button(label="B", style=disnake.ButtonStyle.secondary)
    async def button_b(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("B", inter)

    @disnake.ui.button(label="C", style=disnake.ButtonStyle.secondary)
    async def button_c(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("C", inter)
        
    async def check_answer(self, chosen: str, inter: disnake.MessageInteraction):
        if self.answered:
            return
        self.answered = True
        # your logic here — check chosen against self.question["answer"]
        # send a response telling them if they're right or wrong

class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/questions.json", "r") as f:
            self.questions = json.load(f)
        
    @commands.slash_command(name="quiz", description="Take a quiz and test your knoledge and collect points!")
    async def quiz(self, inter: disnake.ApplicationCommandInteraction, number_of_questions: int = 5):
        for i in range(0, number_of_questions):
            question = random.choice(self.questions)
            embed = disnake.Embed(
                title = f"Question {i + 1}",
                description= question["text"],
                color = disnake.Color.blurple()
			)
            
            embed.set_author(
				name = "RadioReady",
				url = "https://github.com/CaptainAarav/RadioReady",
			)
            
            embed.set_footer(
				text = "SYLLABUS: V1.6"
			)
            
            if i == 0:
                await inter.response.send_message(embed=embed)
            elif i > 0:
                await inter.followup.send(embed=embed)
            

        
def setup(bot):
    bot.add_cog(Quiz(bot))