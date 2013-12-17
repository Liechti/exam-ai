import parse


def main():
    questions = parse.parse_test("exams/102.txt")
    print "Questions:",len(questions)

    for question in questions:
        print '--------------'
        for k,v in question.items():
            print k,':',v
        
if __name__ == "__main__":
    main()
    

