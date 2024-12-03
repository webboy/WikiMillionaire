import wikipedia
from services.openai_service import OpenAIService

service = OpenAIService()
print("++++++++++++++++++++++++++++ TEXT ++++++++++++++++++++++++++++")
# Get a random page title
wikipedia.set_lang('en')
random_title = wikipedia.random()

# Fetch the page content using the title
page = wikipedia.page(random_title)
page_text = page.summary
print(page_text)
print("++++++++++++++++++++++++++++ QUESTION ++++++++++++++++++++++++++++")
question = service.get_question_from_text(page_text, "wikipedia")
question.shuffle_options()
print(question.format())
