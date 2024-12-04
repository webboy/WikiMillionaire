from data_models.question import Question

class FiftyJoker:
    def __init__(self):
        self.name = "Fifty / Fifty Joker"

    def apply(self, question: Question):

        options_list = list(question.options.items())  # Convert to a list of key-value pairs
        sliced_options = dict(options_list[:(len(options_list) // 2 + 1)])  # Slice and convert back to dictionary
        question.options = sliced_options  # Assign back to the dictionary

        return question