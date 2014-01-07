import nltk
import nltk.data
from nltk.corpus import treebank, stopwords, brown
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import random
from pprint import pprint

# 10 x 10 grid
elimination_matrix = [[0 for x in xrange(10)] for y in xrange(10)]

import time

def print_matrix():
    pprint(elimination_matrix)
    ones = 0
    for i in elimination_matrix:
        for j in i:
            if j == 1:
                ones += 1
    print "Elimations", ones

def _parse_paragraph(section):
    '''Returns a list with the sentence for needed for each question.'''

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(section[0]['article'].strip())
    
    questions = []
    for sentence in sentences:
        for n in range(int(section[0]['number']), int(section[-1]['number'])+1):
            if '['+str(n)+']' in sentence:
                questions.append(sentence)

    return questions
       
  
#def tag_matching(question, possibile_tags, n_lookback, n_lookahead):
def tag_matching(sequences):

    treebank_sentences = treebank.tagged_sents()
    #treebank_sentences = brown.tagged_sents()

    # Return best count/sequence
    best = (0, None)

    count = 0
    errors = 0

    resultset = []

    for seq in sequences:
        for sent in treebank_sentences:
            for i, word in enumerate(sent):
                if sent[i][1] == seq[0]:
                    try:
                        if sent[i+1][1] == seq[1]:
                            count += 1
                            #if sent[i+2][1] == seq[2]:
                            #   count += 1
                    except IndexError:
                        errors += 1
        if count > best[0]:
            best = (count, seq)
        resultset.append((seq, count, errors))
        count, erros = 0, 0
    return resultset

def round_one(section):
    questions = _parse_paragraph(section)
    choices = [section[0]['a'],
               section[0]['b'],
               section[0]['c'],
               section[0]['d'],
               section[0]['e'],
               section[0]['f'],
               section[0]['g'],
               section[0]['h'],
               section[0]['i'],
               section[0]['j']]

    #ends = range(31, 40)

    stopset = set(stopwords.words('english'))
    import string

  
    brown_sents = treebank.tagged_sents()
    unigram_tagger = nltk.UnigramTagger(brown_sents)
    bigram_tagger = nltk.BigramTagger(brown_sents, backoff=unigram_tagger)
            
    for q, n in zip(questions, range(31,41)):
        guess_idx = 0
        possible_tags = []
        print 'question:', str(n)
        for choice in choices:
            tokens = nltk.word_tokenize(q.replace('['+str(n)+']', choice))
            cleanup = [token for token in tokens if token not in string.punctuation]
     
            guess_idx = cleanup.index(choice)
            #guess_idx = tokens.index(choice)
            tgs = nltk.pos_tag(cleanup) #cleanup
            #tgs = unigram_tagger.tag(cleanup)
            possible_tags.append(tgs)

        sequences = []
        ind_sequences = [] #same thing but with choice ind
       
        for p, j in zip(possible_tags, range(0,10)):
            if 0 < guess_idx < len(tokens)-1:
                try:
                    print p[guess_idx-1], p[guess_idx]
                    sequences.append((p[guess_idx-1][1], p[guess_idx][1]))#, p[guess_idx+1][1]))
                    ind_sequences.append((j,(p[guess_idx-1][1], p[guess_idx][1])))#, p[guess_idx+1][1])))
                except IndexError:
                    print guess_idx, 'oh no!'
        #for s in ind_sequences:
        #    print s
        sequences = list(set(sequences))


        resultset = tag_matching(sequences)

        occurrences = [result[1] for result in resultset]

        if occurrences:
            biggest = max(occurrences)
        else:
            #print 'error'
            continue

        to_throw = [item for item in occurrences if item * 2 < biggest]

        for r in resultset:
            if r[1] < 10:
                #print 'Throwout', r
                for i,s in enumerate(ind_sequences):
                    if r[0] == s[1]:                      
                        elimination_matrix[n-31][i] = 1
            for bad in to_throw:
                if r[1] == bad:
                    for i,s in enumerate(ind_sequences):
                        if r[0] == s[1]:
                            elimination_matrix[n-31][i] = 1

    print_matrix()

def round_two(section, rng):
    global elimination_matrix
 
    choices = [section[0]['a'],
               section[0]['b'],
               section[0]['c'],
               section[0]['d'],
               section[0]['e'],
               section[0]['f'],
               section[0]['g'],
               section[0]['h'],
               section[0]['i'],
               section[0]['j']]

    reduced = []
    rows = elimination_matrix[rng]

    for i, choice in enumerate(choices):
        if rows[i] == 1:
            continue
        else:
            reduced.append(choice)
    print reduced
        
    questions = _parse_paragraph(section)
    print questions[rng]

    driver = webdriver.Firefox()
    driver.get("http://www.google.com")
    regex = re.compile("[\d+,]+")
    for choice in reduced:
        tokens = nltk.word_tokenize(questions[rng].replace('['+str(rng+31)+']', choice))
        guess = tokens.index(choice)
        query = '"'+' '.join([tokens[guess-1], tokens[guess], tokens[guess+1]]) + '"'

        search = driver.find_element_by_name('q')

        
        search.send_keys(query)
        search.submit()
        time.sleep(random.randint(3,7))
        source = driver.page_source
        soup = BeautifulSoup(source)
        results = soup.find_all(id='resultStats')
        
        print 'CHOICE', choice
        print results[0].text
        
        search = driver.find_element_by_name('q')
        time.sleep(random.randint(20,30))
        search.clear()
        time.sleep(2)
        #print results[0].text
        
    driver.close()
    time.sleep(60)
    print '----------------------------'

'''
Reference matrices (after stage 1)
#102
elimination_matrix = [[0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
                          [1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
                          [1, 0, 0, 1, 1, 1, 1, 0, 1, 0],
                          [0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 0, 0, 1, 0, 1, 1, 1]]

#101
elimination_matrix = [[0, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                          [0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
                          [0, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                          [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                          [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
                          [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
                          [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                          [0, 0, 0, 0, 1, 1, 0, 0, 1, 0]]
'''
