import parse
from grader import Grader
from utils import get_section

from solver import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
    questions = parse.parse_test("exams/102.txt")

    # Example: get all questions from section 3.
    section_three = get_section(questions, 3)

    # Uncomment to print all questions.
    
    for question in questions:
        print '--------------'
        for k,v in question.items():
            print k,':',v
    
    
    # Ngram search on section 1
    
    driverinit()
    #getcount('test')
    #section_one = get_section(questions, 1)
    section_tmp = [question for question in questions if 1 <= question['number'] <= 15 ]
    answers = [ngram_analysis(question) for question in section_tmp]
    print answers
    driverclose()
    
    # Example Grader
    
    #answers = ['B']*56
    answers.extend(['B']*41)
    nums = range(1, 57)

    grader = Grader("solutions/102ans.txt")
    
    # Uncomment to see example grader.
    grader.grade_questions(nums, answers)

if __name__ == "__main__":
    main()
    

