import disnake
from disnake.ext import commands
import json
import random
from models import User

class QuizView(disnake.ui.View):
    def __init__(self, question: dict):
        super().__init__(timeout=30)
        self.question = question
        self.answered = False
        self.score = 0
        self.chosen = None

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
        self.chosen = chosen
        self.answered = True
        if chosen == self.question["answer"]:
            self.score += 1
        await inter.response.defer()
        await self.message.edit(view=None)
        self.stop()


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/questions.json", "r") as f:
            self.questions = json.load(f)

    @commands.slash_command(name="quiz", description="Take a quiz and test your knowledge and collect points! PS: You have 30s for each question.")
    async def quiz(self, inter: disnake.ApplicationCommandInteraction, number_of_questions: int = 5):
        total_score = 0
        results = []

        for i in range(0, number_of_questions):
            question = random.choice(self.questions)
            options = question["options"]
            description = f"{question['text']}\n\n🇦  {options['A']}\n\n🇧  {options['B']}\n\n🇨  {options['C']}\n\n🇩  {options['D']}"

            embed = disnake.Embed(
                title=f"Question {i + 1}",
                description=description,
                color=disnake.Color.blurple()
            )

            embed.set_author(
                name="RadioReady",
                url="https://github.com/CaptainAarav/RadioReady",
            )

            embed.set_footer(text="SYLLABUS: V1.6")

            view = QuizView(question)
            file = disnake.File(question["image"], filename="question.png") if "image" in question else None

            if "image" in question:
                embed.set_image(url="attachment://question.png")

            if i == 0:
                if file:
                    await inter.response.send_message(embed=embed, view=view, file=file)
                else:
                    await inter.response.send_message(embed=embed, view=view)
                view.message = await inter.original_message()
            else:
                if file:
                    view.message = await inter.followup.send(embed=embed, view=view, file=file)
                else:
                    view.message = await inter.followup.send(embed=embed, view=view)

            await view.wait()
            total_score += view.score
            results.append({
                "question": question,
                "chosen": view.chosen,
                "correct": view.score == 1
            })

        desc = f"You scored **{total_score}/{number_of_questions}**\n\n"
        for r in results:
            emoji = "✅" if r["correct"] else "❌"
            desc += f"{emoji} {r['question']['text'][:60]}...\n"
            desc += f"Your answer: **{r['chosen'] if r['chosen'] else 'No answer'}**"
            if not r["correct"]:
                desc += f"　✔️ Correct: **{r['question']['answer']}**"
            desc += "\n\n"

        summary_embed = disnake.Embed(
            title=f"📊 {inter.author.display_name}'s Results",
            description=desc,
            color=disnake.Color.green() if total_score >= number_of_questions * 0.73 else disnake.Color.red()
        )

        summary_embed.set_author(
            name="RadioReady",
            url="https://github.com/CaptainAarav/RadioReady",
        )

        summary_embed.set_footer(text="SYLLABUS: V1.6")

        await inter.followup.send(embed=summary_embed)

def setup(bot):
    bot.add_cog(Quiz(bot))