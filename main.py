import parse
import grade

def main():
    questions = parse.parse_test("exams/102.txt")
    print "Questions:",len(questions)

    for question in questions:
        print '--------------'
        for k,v in question.items():
            print k,':',v
    
    answers = ['A']*56
    grade.grade(answers, "solutions/102ans.txt")
    
if __name__ == "__main__":
    main()
    

