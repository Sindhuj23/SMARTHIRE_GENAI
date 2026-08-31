def validate_question(question):

    if not question:
        return False, "Please enter a question."

    question = question.strip()

    if len(question) < 2:
        return False, "Please enter a little more detail."

    if len(question) > 10000:
        return False, "Your question is too long."

    return True, ""


def clean_response(response):

    if not response:
        return "I couldn't generate a response."

    return response.strip()
