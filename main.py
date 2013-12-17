import parse
from grader import Grader
from utils import get_section

def main():
    questions = parse.parse_test("exams/102.txt")

    # Example: get all questions from section 3.
    section_three = get_section(questions, 3)

    # Uncomment to print all questions.
    '''
    for question in questions:
        print '--------------'
        for k,v in question.items():
            print k,':',v
    '''

    # Example Grader
    answers = ['B']*56
    nums = range(1, 57)

    grader = Grader("solutions/102ans.txt")

    # Uncomment to see example grader.
    #grader.grade_questions(nums, answers)

if __name__ == "__main__":
    main()
    

