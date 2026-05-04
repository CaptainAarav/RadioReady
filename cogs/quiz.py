import disnake
from disnake.ext import commands
import json
import random

class QuizView(disnake.ui.View):
    def __init__(self, question: dict):
        super().__init__(timeout=30)
        self.question = question
        self.answered = False   
        self.score = 0

    @disnake.ui.button(label="A", style=disnake.ButtonStyle.primary)
    async def button_a(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("A", inter)

    @disnake.ui.button(label="B", style=disnake.ButtonStyle.primary)
    async def button_b(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("B", inter)

    @disnake.ui.button(label="C", style=disnake.ButtonStyle.primary)
    async def button_c(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("C", inter)
        
    @disnake.ui.button(label="D", style=disnake.ButtonStyle.primary)
    async def button_d(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.check_answer("D", inter)
        
    async def on_timeout(self):
        await self.message.edit(view=None)
        
    async def check_answer(self, chosen: str, inter: disnake.MessageInteraction):
        if self.answered:
            return
        self.answered = True
        if chosen == self.question["answer"]:
            self.score += 1
        await inter.response.defer()
        self.stop()

class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/questions.json", "r") as f:
            self.questions = json.load(f)
        
    @commands.slash_command(name="quiz", description="Take a quiz and test your knoledge and collect points!")
    async def quiz(self, inter: disnake.ApplicationCommandInteraction, number_of_questions: int = 5):
        total_score = 0    
    
        for i in range(0, number_of_questions):
            question = random.choice(self.questions)
            options = question["options"]
            description = f"{question['text']}\n\n🇦 {options['A']}\n🇧 {options['B']}\n🇨 {options['C']}\n🇩 {options['D']}"
            
            embed = disnake.Embed(
                title = f"Question {i + 1}",
                description= description,
                color = disnake.Color.blurple()
			)
            
            embed.set_author(
				name = "RadioReady",
				url = "https://github.com/CaptainAarav/RadioReady",
			)
            
            embed.set_footer(
				text = "SYLLABUS: V1.6"
			)
            
            view = QuizView(question)
            
            if i == 0:
                await inter.response.send_message(embed=embed, view=view)
                view.message = await inter.original_message()
            elif i > 0:
                view.message = await inter.followup.send(embed=embed, view=view)
            await view.wait()
            total_score += view.score
            
        await inter.followup.send(f"{inter.author.mention} Quiz complete! You scored **{total_score}/{number_of_questions}**")
        
def setup(bot):
    bot.add_cog(Quiz(bot))