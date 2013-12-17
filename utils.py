# Assortment of useful functions.

def get_section(questions, number):
    return [x for x in questions if x['section_number'] == number]
