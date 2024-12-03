import spacy
import random
import wikipedia

def generate_question_with_spacy(text: str, source: str):
    """
    Generate a trivia question from input text using spaCy with better distractors and diverse questions.
    :param text: The input text for question generation.
    :param source: Source URL for the text.
    :return: A dictionary representing the question object.
    """
    # Load spaCy language model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Step 1: Extract entities for key facts and distractors
    entities = {
        "PERSON": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "ORG": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "GPE": [ent.text for ent in doc.ents if ent.label_ == "GPE"],
        "DATE": [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    }

    # Step 2: Choose a question type based on available entities
    if entities["PERSON"]:
        key_fact = random.choice(entities["PERSON"])
        question = f"Who is {key_fact}?"
        distractors = entities["PERSON"]  # Contextual distractors
    elif entities["GPE"]:
        key_fact = random.choice(entities["GPE"])
        question = f"Where is {key_fact} located?"
        distractors = entities["GPE"]
    elif entities["ORG"]:
        key_fact = random.choice(entities["ORG"])
        question = f"What is the purpose of {key_fact}?"
        distractors = entities["ORG"]
    elif entities["DATE"]:
        key_fact = random.choice(entities["DATE"])
        question = f"When did {key_fact} occur?"
        distractors = entities["DATE"]
    else:
        return {"error": "No suitable entities found for question generation."}

    print(entities)

    # Step 3: Enhance distractors
    distractors = [d for d in distractors if d != key_fact]  # Exclude the correct answer
    if len(distractors) < 5:
        # Add random words as fallback distractors
        random_words = [token.text for token in doc if token.is_alpha and token.text != key_fact]
        distractors.extend(random.sample(random_words, min(5 - len(distractors), len(random_words))))

    # Step 4: Create options and assign the correct answer
    all_options = [key_fact] + distractors[:5]
    random.shuffle(all_options)
    options = {chr(65 + i): opt for i, opt in enumerate(all_options)}
    correct_answer = next(k for k, v in options.items() if v == key_fact)

    # Step 5: Return the question object
    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "source": source
    }

page_text = wikipedia.summary("Python (programming language)", sentences=10).replace("\n", "")

print(page_text)
print(generate_question_with_spacy(page_text, "wikipedia"))