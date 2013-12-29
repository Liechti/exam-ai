# Assortment of useful functions.

def get_section(questions, number):
    return [x for x in questions if x['section_number'] == number]

def get_question(questions, number):
    return questions[number-1]

def classify(question, keywords):
    '''
    Example usage:
    question['what'] = classify(question['question'], ['what', 'which'])
    '''
    if any(keyword in question.lower() for keyword in keywords):
        return True
    return False


 

