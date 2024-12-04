import wikipedia

class WikipediaService:
    """
    Service class for interacting with Wikipedia.
    """

    def __init__(self, language: str = "en"):
        """
        Initialize the WikipediaService with a default language.
        :param language: The language code for Wikipedia (default is "en").
        """
        wikipedia.set_lang(language)

    def get_random_summary(self) -> str:
        """
        Fetch the summary text of a random Wikipedia page.
        :return: The summary text of the random page.
        """
        try:
            # Get a random page title
            random_title = wikipedia.random()

            # Fetch the summary for the random page
            return wikipedia.summary(random_title, sentences=10, auto_suggest=False)
        except Exception as e:
            return f"Error: {e}"
