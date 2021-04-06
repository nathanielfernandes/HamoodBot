import discord, json, random, html, asyncio
from games.DefaultGame import DefaultGame


class Trivia(DefaultGame):
    def __init__(
        self,
        ctx,
        bot,
        playerTwo=None,
        category="any",
        # difficulty="any",
        wager: int = 0,
    ):
        self.category = self.validate_category(category)
        self.difficulty = "any"  # self.validate_difficulty(difficulty)

        super().__init__(
            ctx=ctx,
            bot=bot,
            playerTwo=playerTwo,
            wager=wager,
            game_name="trivia",
            thumbnail="https://cdn.discordapp.com/attachments/749779300181606411/789384532746174464/question-marks.png",
            reactions={
                "<:chessA:776347125272412161>": 0,
                "<:chessB:776347122341249044>": 1,
                "<:chessC:776347121694539777>": 2,
                "<:chessD:776347122496831498>": 3,
            },
            extra_info=f"Category: **{self.category[1]}**\n",  # Difficulty: **{self.difficulty}**",
            turn_based=False,
        )

        self.emojis = [
            "<:chessA:776347125272412161>",
            "<:chessB:776347122341249044>",
            "<:chessC:776347121694539777>",
            "<:chessD:776347122496831498>",
        ]

        self.scores = {self.playerOne.id: 0, self.playerTwo.id: 0}
        self.question_num = 0
        self.pause = False

    def next_question(self):
        if self.question_num + 1 < len(self.questions):
            self.question_num += 1
            self.current_question = self.questions[self.question_num]
            return True
        return False

    def is_correct(self, member, choice):
        if (
            self.current_question["options"][self.emojis[choice]]
            == self.current_question["correct_answer"]
        ):
            self.scores[member.id] += 1
            return True
        else:
            if member == self.playerOne:
                self.scores[self.playerTwo.id] += 1
            else:
                self.scores[self.playerOne.id] += 1
            return False

    async def game_start(self):
        self.questions = await self.get_questions(self.category, self.difficulty)
        self.current_question = self.questions[self.question_num]
        await self.update_message(embed=self.create_embed())

    async def update_game(self, member, move, emoji):
        if not self.pause:
            correct = self.is_correct(member, move)
            self.pause = True
            await self.message.edit(
                embed=self.correction_embed(correct=correct, member=member)
            )
            await asyncio.sleep(2)

            winner, loser, tie = None, None, False
            if not self.next_question():
                if self.scores[self.playerOne.id] > self.scores[self.playerTwo.id]:
                    winner = self.playerOne
                    loser = self.playerTwo
                elif self.scores[self.playerOne.id] < self.scores[self.playerTwo.id]:
                    loser = self.playerOne
                    winner = self.playerTwo
                else:
                    tie = True
                await self.end_game(winner=winner, loser=loser, tie=tie)

            if self.message is not None:
                await self.update_message(
                    embed=self.create_embed(winner=winner, tie=tie)
                )
            self.pause = False

    def correction_embed(self, correct: bool, member):
        ans = self.current_question["correct_answer"]
        if correct:
            msg = f"**Correct! {member}**"
            img = "https://cdn.discordapp.com/attachments/749779300181606411/789387042504572928/0-6616_view-samegoogleiqdbsaucenao-qcbbexbc5-green-check-mark-circle.png"
            color = discord.Color.green()
        else:
            msg = f"**Incorrect! {member}**"
            img = "https://cdn.discordapp.com/attachments/749779300181606411/789387314501386250/Incorrect_Symbol-512.png"
            color = discord.Color.red()

        embed = discord.Embed(
            title=msg, description=f"***{ans}*** was the correct answer.", color=color,
        )
        embed.set_thumbnail(url=img)

        return embed

    def create_embed(self, winner=None, tie=False):
        color = discord.Color.purple()
        desc = None
        if tie:
            title = "It's a draw!"
        elif winner is not None:
            title = f"**{winner}** won the game!"
        else:
            title = f"**{self.current_question['question']}**"
            desc = f"Question **{self.question_num+1}/10**"

        embed = discord.Embed(title=title, description=desc, color=color)

        wager = f"wager: {self.cash(self.wager)}" if self.wager > 0 else ""

        diff = ""
        if desc is not None:
            embed.add_field(
                name="Choices", value=f"{self.current_question['options_str']}",
            )
            diff = f"\nDifficulty: {self.current_question['difficulty'].capitalize()}"

        embed.add_field(
            name=f"{self.playerOne}: **{self.scores[self.playerOne.id]}**     {self.playerTwo}: **{self.scores[self.playerTwo.id]}**",
            value=f"Category: {self.current_question['category'].title()}{diff}\n{wager}",
            inline=False,
        )

        embed.set_author(name=self.game_name.title(), icon_url=self.thumbnail)

        return embed

    def format_question(self, q):
        correct_answer = html.unescape(q["correct_answer"])
        incorrect_answers = [html.unescape(i) for i in q["incorrect_answers"]]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        options = {self.emojis[i]: options[i] for i in range(4)}

        return {
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": html.unescape(q["question"]),
            "correct_answer": correct_answer,
            "options": options,
            "options_str": "\n".join([f"{i} **{options[i]}**" for i in self.emojis]),
        }

    async def get_questions(self, category=None, difficulty=None, amount=10):
        jr = await self.bot.ahttp.get(
            url=f"https://opentdb.com/api.php?amount={amount}{'&category='+ self.category[0] if self.category[0] != 'any' else ''}{'&difficulty='+self.difficulty if self.difficulty != 'any' else ''}&type=multiple",
            return_type="json",
        )
        if jr["response_code"] != 0:
            return
        return [self.format_question(q) for q in jr["results"]]

    def validate_category(self, categ):
        categories = {
            "Any Category": "any",
            "General Knowledge": "9",
            "Entertainment: Books": "10",
            "Entertainment: Film": "11",
            "Entertainment: Music": "12",
            "Entertainment: Musicals & Theatres": "13",
            "Entertainment: Television": "14",
            "Entertainment: Video Games": "15",
            "Entertainment: Board Games": "16",
            "Science & Nature": "17",
            "Science: Computers": "18",
            "Science: Mathematics": "19",
            "Mythology": "20",
            "Sports": "21",
            "Geography": "22",
            "History": "23",
            "Politics": "24",
            "Art": "25",
            "Celebrities": "26",
            "Animals": "27",
            "Vehicles": "28",
            "Entertainment: Comics": "29",
            "Science: Gadgets": "30",
            "Entertainment: Japanese Anime & Manga": "31",
            "Entertainment: Cartoon & Animations": "32",
            "movies": "11",
            "songs": "12",
            "tv": "14",
            "shows": "14",
        }

        for key in categories:
            if categ.lower() in key.lower():
                return categories[key], key

        return "any", "Any Category"

    # def validate_difficulty(self, diff):
    #     if diff.lower() in ["any", "easy", "medium", "hard"]:
    #         return diff.lower()
    #     else:
    #         return "any"

