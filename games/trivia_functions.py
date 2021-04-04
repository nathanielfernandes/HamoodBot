import requests
import json
import random
import html


class _Trivia:
    def __init__(
        self,
        playerOne="one",
        playerTwo="two",
        server="server",
        category="any",
        difficulty="any",
    ):

        self.category = self.check_category(category)
        self.difficulty = self.check_difficulty(difficulty)

        self.game_started = False

        self.questions = self.get_questions(category, difficulty)

        self.timer = None
        self.question_num = 0
        self.current_question = self.questions[self.question_num]

        try:
            self.score = {playerOne.id: 0, playerTwo.id: 0}
        except AttributeError:
            self.score = {playerOne: 0, playerTwo: 0}
            pass

        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.server = server

        self.choices = [
            "<:chessA:776347125272412161>",
            "<:chessB:776347122341249044>",
            "<:chessC:776347121694539777>",
            "<:chessD:776347122496831498>",
        ]

        self.wait = False

    def format_question(self, q):
        c = [
            "<:chessA:776347125272412161>",
            "<:chessB:776347122341249044>",
            "<:chessC:776347121694539777>",
            "<:chessD:776347122496831498>",
        ]

        correct_answer = html.unescape(q["correct_answer"])
        incorrect_answers = [html.unescape(i) for i in q["incorrect_answers"]]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        options = {c[i]: options[i] for i in range(4)}

        return {
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": html.unescape(q["question"]),
            "correct_answer": correct_answer,
            "options": options,
            "options_str": "\n".join([f"{i} **{options[i]}**" for i in c]),
        }

    def get_questions(self, category=None, difficulty=None, amount=10):
        response = requests.get(
            f"https://opentdb.com/api.php?amount={amount}{'&category='+ self.category[0] if self.category[0] != 'any' else ''}{'&difficulty='+self.difficulty if self.difficulty != 'any' else ''}&type=multiple"
        ).json()

        if response["response_code"] != 0:
            return

        return [self.format_question(q) for q in response["results"]]

    def next_question(self):
        self.question_num += 1
        if self.question_num <= 9:
            self.current_question = self.questions[self.question_num]

    def check_answer(self, choice, player):
        if (
            self.current_question["options"][self.choices[choice]]
            == self.current_question["correct_answer"]
        ):
            self.score[player.id] += 1
            self.next_question()
            return True
        else:
            if player == self.playerOne:
                self.score[self.playerTwo.id] += 1
            else:
                self.score[self.playerOne.id] += 1

            self.next_question()
            return False

    def check_category(self, categ):
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

    def check_difficulty(self, diff):
        if diff.lower() in ["any", "easy", "medium", "hard"]:
            return diff.lower()
        else:
            return "any"
