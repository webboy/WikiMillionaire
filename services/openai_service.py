from openai import OpenAI
from dotenv import load_dotenv
import os
from data_models.question import Question


class OpenAIService:
    """
    Service class for interacting with OpenAI's API.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAIService instance by using the provided API key or loading it from the .env file.
        :param api_key: (Optional) The OpenAI API key for authenticating requests.
        """
        if not api_key:
            load_dotenv()  # Load environment variables from .env
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or not api_key.strip():
            raise ValueError("API key must be provided either as an argument or in the .env file.")

        self.api_key = api_key.strip()

        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key)

    def get_question_from_text(self, text: str, source: str):
        # GPT prompt for question generation
        prompt = f"""
            Based on the following text, generate a multiple-choice trivia question.
            The question should include:
            1. The question text.
            2. Six answer options (A-F) with only one correct answer. Make correct answer appear at random position.
            3. Clearly indicate the correct answer by its letter.
            4. Provide the correct answer as part of the response.    
            5. Include a hint to help the user answer the question.

            Text:
            {text}
            
            Make sure you always put the correct answer in option A.
            
            Format your response as pure JSON (no extra characters) with the following structure:
            {{
                "question": "Your generated question here",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D",
                    "E": "Option E",
                    "F": "Option F"
                }},
                "correct_answer": "A",
                "source": "{source}"
                "hint": "Your hint here"
            }}
            """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4o-mini"
            )

            return Question.from_json(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
