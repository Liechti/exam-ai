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

def find_sublist(sub,sent):
    #both sub & main should be tokenized, returns the occurrences' first index
    results=[]
    LEN=len(sub)
    for ind in (i for i,e in enumerate(sent) if e==sub[0]):
        if sent[ind:ind+LEN]==sub:
            results.append((ind,ind+LEN-1))
    return results
