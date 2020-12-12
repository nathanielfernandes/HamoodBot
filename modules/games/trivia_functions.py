import requests
import json
import random
import html


class _Trivia:
    def __init__(self, playerOne, playerTwo, server):
        self.questions = self.get_questions()
        self.timer = None
        self.question_num = -1
        self.current_question = self.questions[self.question_num]

        self.score = {playerOne.id: 0, playerTwo.id: 0}

        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.server = server

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

    def get_questions(self, amount=10):
        response = requests.get(
            f"https://opentdb.com/api.php?amount={amount}&type=multiple"
        ).json()

        if response["response_code"] == 1:
            return

        return [self.format_question(q) for q in response["results"]]

    def next_question(self):
        if self.question_num <= 9:
            self.question_num += 1
            self.current_question = self.questions[self.question_num]

