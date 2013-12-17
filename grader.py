import csv

class Grader:

    def __init__(self, answer_file):
        self.answer_key = self._parse_answer_key(answer_file)
        self.num_correct = 0
        self.num_incorrect = 0

    def grade_question(self, n, guess):
        if self.answer_key[str(n)] == guess:
            self.num_correct += 1
            print str(n) + '.', guess,"is correct."
        else:
            self.num_incorrect += 1
            print str(n) + '.', guess, "is incorrect. (Correct =", \
                    self.answer_key[str(n)] + ')'

    def grade_questions(self, nums, guesses):
        try:
            for n,guess in zip(nums,guesses):
                self.grade_question(n, guess)
        except TypeError:
            print "Aborting. grade_questions takes two lists as parameters."
        self.generate_stats()

    def generate_stats(self):
        total = self.num_correct + self.num_incorrect
        print '------------------'
        print str(self.num_correct) + '/' + str(total), 'correct.'
        self.num_correct = 0
        self.num_incorrect = 0

    def _parse_answer_key(self, answer_file):
        with open(answer_file, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            return {row[0]: row[1] for row in reader}
