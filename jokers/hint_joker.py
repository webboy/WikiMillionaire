from data_models.question import Question


class HintJoker:
    def __init__(self):
        self.name = "Hint Joker"

    def apply(self, question: Question):
        question.show_hint = True
        return question

