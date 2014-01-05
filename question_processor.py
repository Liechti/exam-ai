import nltk
import utils
import parse
from article_processor import advanced_tagger

questions = parse.parse_test("exams/102.txt") 
choice = [utils.get_question(questions,i)['question'] for i in range(41,45)]
art = utils.get_question(questions,41)['article']


DP = ['PRP', 'PRP$', 'NP']
def Why_movement(question):
    #assume the question starts with WHY, and only consider do/does/did & is/am/are/was/were/
    tok = advanced_tagger(question)[0]
    tag = advanced_tagger(question)[1]
    tok = tok[1:]   #remove WHY
    start_index = 1
    if tok[1] in ["n't", 'not', 'NOT']:
        start_index = 2
    aux = tok[:start_index]
      
    DP_index = [x for x, y in enumerate(tag) if y[1] in DP]
    tok = tok[start_index:DP_index[0]] + aux + tok[DP_index[0]:]
    
    return ' '.join(tok)

POS = ['true', 'truth', 'correct']
NEG = ['false', 'incorrect']       

def tf_decider(sentence):
    tok = nltk.word_tokenize(sentence)
    index = 0
    for w in POS:
        if tok.count(w):
            index = tok.index(w)
    if index != 0 and tok[index-1].lower() not in ['not',"n't"]:
        return 1
    return -1

def find_target(sentence):
    tok = nltk.word_tokenize(sentence)
    return ' '.join(tok[tok.index('about')+1:-1])

def tf_processor(sentence, target):
    tok = nltk.word_tokenize(sentence)
    tag = nltk.pos_tag(tok)
    PRP_index = [x for x, y in enumerate(tag) if y[1] in ['PRP', 'PRP$']]
    for i in PRP_index:
        tok[i] = target
    return ' '.join(tok) 

    
KEYS = ['main', 't/f', 'bold_face', 'who', 'why', 'what']
CLASS = ['others'] +KEYS
KEYWORDS={'main':['main', 'mainly'], 't/f':['true','correct','truth','false','incorrect'], 'bold_face':['[',']'], \
              'who':['who'], 'why':['why'], 'what':['which','what']}
def classify(question):
    for key in KEYS:
        if utils.classify(question,KEYWORDS[key]):
            return key 
        
        
    return CLASS[0]
def wh_processor(question, choice):
    #for WHO & WHAT/WHICH questions
    tok = nltk.word_tokenize(question.lower())
    
    for w in tok:
        if w in KEYWORDS['who']+KEYWORDS['what']:
            Wh_index = tok.index(w)
   
    result = tok[:Wh_index]+nltk.word_tokenize(choice)+tok[Wh_index+1:]
    
    return ' '.join(result)
 
#testing
#q=utils.get_question(questions,55)['question']