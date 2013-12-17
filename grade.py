import parse

def grade(answers, answer_key_file):
    answer_key =  parse.parse_answers(answer_key_file)
    
    num_correct = 0
    num_incorrect = 0
    for answer, solution in zip(answers, answer_key):
        if answer == solution:
            num_correct += 1
        else:
            num_incorrect += 1

    print "Number of correct answers:", num_correct
    print "Number of incorrect answers:", num_incorrect
