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


class SubmitView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.submit = None

    @disnake.ui.button(label="✅ Submit to Leaderboard", style=disnake.ButtonStyle.success)
    async def submit_yes(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.submit = True
        await inter.response.defer()
        self.stop()

    @disnake.ui.button(label="❌ Keep Private", style=disnake.ButtonStyle.danger)
    async def submit_no(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.submit = False
        await inter.response.defer()
        self.stop()


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/questions.json", "r") as f:
            self.questions = json.load(f)

    @commands.slash_command(name="quiz", description="Take a quiz via DM and test your knowledge! PS: You have 30s for each question.")
    async def quiz(self, inter: disnake.ApplicationCommandInteraction, number_of_questions: int = commands.Param(default=5, description="How many questions do you want?", gt=0, lt=26)):
        await inter.response.defer(ephemeral=True)

        try:
            await inter.author.send("📻 **Quiz Starting!** Get ready for your first question...")
        except disnake.Forbidden:
            await inter.edit_original_response(content="❌ I couldn't DM you! Please enable DMs from server members.")
            return

        await inter.edit_original_response(content="📬 Check your DMs! Your quiz has started.")

        user, _ = await User.get_or_create(discord_id=inter.author.id)
        total_score = 0
        results = []

        for i in range(0, number_of_questions):
            question = random.choice(self.questions)
            options = question["options"]
            description = f"{question['text']}\n\n🇦  {options['A']}\n\n🇧  {options['B']}\n\n🇨  {options['C']}\n\n🇩  {options['D']}"

            embed = disnake.Embed(
                title=f"Question {i + 1} of {number_of_questions}",
                description=description,
                color=disnake.Color.blurple()
            )

            embed.set_author(
                name="RadioReady",
                url="https://github.com/CaptainAarav/RadioReady",
            )

            embed.set_footer(text="SYLLABUS: V1.6 | You have 30 seconds to answer")

            view = QuizView(question)

            if "image" in question:
                file = disnake.File(question["image"], filename="question.png")
                embed.set_image(url="attachment://question.png")
                dm_message = await inter.author.send(embed=embed, view=view, file=file)
            else:
                dm_message = await inter.author.send(embed=embed, view=view)

            view.message = dm_message

            await view.wait()
            total_score += view.score
            results.append({
                "question": question,
                "chosen": view.chosen,
                "correct": view.score == 1
            })

        passed = total_score >= number_of_questions * 0.73
        bonus = "**You earned 100 Decibels!**" if passed else ""
        desc = f"You scored **{total_score}/{number_of_questions}** {bonus}\n\n"

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
            color=disnake.Color.green() if passed else disnake.Color.red()
        )

        summary_embed.set_author(
            name="RadioReady",
            url="https://github.com/CaptainAarav/RadioReady",
        )

        summary_embed.set_footer(text="SYLLABUS: V1.6")

        submit_view = SubmitView()
        await inter.author.send(
            content="Would you like to submit your results to the leaderboard?",
            embed=summary_embed,
            view=submit_view
        )

        await submit_view.wait()

        if submit_view.submit:
            user.correct_answers += total_score
            user.total_quizzes += 1
            if passed:
                user.db_points += 100
            await user.save()

            await inter.author.send("✅ Your results have been submitted to the leaderboard!")
        else:
            await inter.author.send("👍 No worries! Your results have been kept private.")


def setup(bot):
    bot.add_cog(Quiz(bot))