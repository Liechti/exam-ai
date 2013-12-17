# Parses a test into a list of dictionaries.
# Each dictionary contains the following keys:
# 
#  'section_number'
#  'number'
#  'article'
#  'question'
#  'a'
#  'b'
#  'c'
#  'd'
#

import re
from bs4 import BeautifulSoup

def process_question(question, section_number):
    find_question = re.compile("\d*\.(.*?)\n")
    find_a = re.compile("\(A\)\s*(.*?)[\(|\n]")
    find_b = re.compile("\(B\)\s*(.*?)[\(|\n]")
    find_c = re.compile("\(C\)\s*(.*?)[\(|\n]")
    find_d = re.compile("\(D\)\s*(.*?)[\(|\n]")
    
    text = find_question.findall(question.text.strip())

    # Dictionary containing all relevant information from each question.
    d = {}
    d['section_number'] = int(section_number)
    d['number'] = int(question.name[1:]) # convert qN -> N
    if text:
        d['question'] = text[0].strip()
    else:
        d['question'] = None
    d['article'] = None
    d['a'] = find_a.findall(question.text)[0].strip()
    d['b'] = find_b.findall(question.text)[0].strip()
    d['c'] = find_c.findall(question.text)[0].strip()
    d['d'] = find_d.findall(question.text)[0].strip()
    
    return d

def match_articles_to_questions(articles, questions):
    first = re.compile("(\d*)\-to")
    last = re.compile("\-to\-q(\d*)")
    for article in articles:
        first_question = int(first.findall(article.name)[0])
        last_question = int(last.findall(article.name)[0])
        for n in range(first_question, last_question+1):
            for question in questions:
                if question['number'] == n:
                    question['article'] = article.text.strip()
                    break
    return questions


def parse_test(test_file):
    with open(test_file,'r') as f:
        test = f.read()
        soup = BeautifulSoup(test)
        # Remove empty strings
        soup.contents = [x for x in soup.contents if len(x) > 1]
        sections = soup.contents
        print "Number of sections:", len(sections)

        questions = []
        articles = []
        
        for i, section in enumerate(sections):
            section_number = i+1
            for question in section:
                try:
                    getattr(question, 'text')
                    if '-to-' in question.name:
                        articles.append(question)
                    else:
                        questions.append(process_question(question, 
                                                          section_number))
                except AttributeError:
                    pass
        questions = match_articles_to_questions(articles, questions)

    return questions
