import nltk
import utils
from nltk.corpus import wordnet 
from nltk.corpus import stopwords

PUNCTUATION = [ ".", ",", ":", ";", "!", "?" ,'"', "''", '``']
FORBIDDEN = stopwords.words('english') + PUNCTUATION

grammar = """
DP:
    {<PRP.*>}
    
NP:
    {<NN.*|JJ.*>*<NN.*>}
        
AP:
    {<JJ.*>*}
    
VP:
    {<RB.*>*<VB.*><DP>?<PP>?<RB.*>*}
"""
def content_extract(tok):
    #extract important content terms.(input should be tokenized)
    filtered_words = [w for w in tok if not w.lower() in FORBIDDEN ]
    return filtered_words

def word_processor(word,x='x'):
    if x == 'n':
        processed = word.lower()
        processed = nltk.WordNetLemmatizer().lemmatize(processed)
        return processed
    if x == 'v':
        processed = nltk.WordNetLemmatizer().lemmatize(word, 'v')
        return processed
    return word       

def basic_processor(article):
    # tokenize, turn to lowr-case, lemmatize, POS-tagging,
    token = nltk.word_tokenize(article)
    tag = nltk.pos_tag(token)
    
    processed = []
    for word in tag:
        processed = processed + [word]
    return processed
                   
def leaves(tag, type):
    #chunk the tagged sentences, and yield the subtrees of the desired type(ex:'NP') 
    tree = nltk.RegexpParser(grammar).parse(tag)
    #print tree
    for subtree in tree.subtrees(filter = lambda t: t.node == type):
        yield subtree.leaves()
   
def extractor(text,type):
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        tag = basic_processor(sent)
        for leaf in leaves(tag, type):
            term= [w for w in leaf]
            yield term
            
def NP_extractor(text):
    #extract Noun Phrase from the article
    terms = [term for term in extractor(text,'NP')]
    NP_terms = []
    for term in terms:
        NP_terms = NP_terms + [[w for w in term]]
        #NP_terms = NP_terms + [' '.join([w[0] for w in term])]
    for i in range(0,len(NP_terms)):
        np = NP_terms[i]
        #print np
        string = ' '.join([w[0] for w in np])
            #print string
        type = np[-1][1]
        NP_terms[i] = (string, type)
    
    return NP_terms

def X_extractor(text,type):
    #extract Phrase of the desired type
    terms = [term for term in extractor(text,type)]
    X_terms = []
    for term in terms:
        X_terms = X_terms + [' '.join([w[0] for w in term])]
    return X_terms           

def advanced_tagger(sentence):
    NP = X_extractor(sentence, 'NP')
    tok = nltk.word_tokenize(sentence)
    tag = nltk.pos_tag(tok)
    for np in NP:
        index = utils.find_sublist(nltk.word_tokenize(np), tok)[0]  #have trouble if occur multiple times
        tok = tok[:index[0]] + [np] + tok[index[1]+1:]
        tag = tag[:index[0]] + [(np, 'NP')] +tag[index[1]+1:]
     
    return (tok, tag)

def eigen(text):
    #i/p should be string
    tag = advanced_tagger(text)[0]
    eigen = content_extract(tag)
    for e in eigen:
        if len(nltk.word_tokenize(e)) != 1:
            eigen.extend(nltk.word_tokenize(e))   
    return eigen 
      
def word_similarity(w1,w2):
    w1 = wordnet.synsets(w1)
    w2 = wordnet.synsets(w2)
    sim = []
    for x in w1:
        for y in w2:
            sim.append(x.path_similarity(y))
    sim = [0 if s == None else s for s in sim]
    if len(sim) == 0:
        return 0
    similarity = (sum(sim)/len(sim) + max(sim))/2

    return similarity

def similarity(eigen_1, eigen_2):
    #i/p should be 2 eigen_lists, return the normalized similarity of the sentences
    sim = []
    for x in eigen_1:
        for y in eigen_2:
            if x == y:
                sim.append(100)
            if x != y:
                sim.append(10*word_similarity(x,y))
    if len(sim) == 0:
        return 0
        
    return sum(sim)/len(sim)

PRON =[['she','f','s'], ['her','f','s'], ['herself','f','s'], ['hers','f','s'], ['he','m','s'], ['him','m','s'], ['himself','m','s'], ['his','m','s'], \
['it','n','s'], ['its','n','s'], ['itself','n','s'], ['i','n','s'], ['me','n','s'], ['my','n','s'], ['myself','n','s'], ['yourself','n','s'], \
['our','n','p'], ['their','n','p'], ['ours','n','p'], ['theirs','n','p'], ['we','n','p'], ['us','n','p'], ['they','n','p'], ['them','n','p'], \
['ourselves','n','p'], ['yourselves','n','p'], ['themselves','n','p'], ['you','n','*'], ['your','n','*'], ['yours','n','*']] 
def pronoun_analyse(pron):
    for p in PRON:
        if pron == p[0]:
            return p
    return [pron,'n','*']

def pronoun_resolution(article):
    article = nltk.sent_tokenize(article)
    candidate = []
    last = []
    this = []
    for s in article:
        print s
        last = this
        this = NP_extractor(s)
        candidate = merge (candidate, this)
        
        DP = X_extractor(s, 'DP')
        
        if DP != []:
            for pron in DP:
                pron = pronoun_analyse(pron)
                candi = constraint(pron, candidate)
                #print candi
                target = preference(pron, candi, this, last, nltk.word_tokenize(s))
                print pron[0]+' '+target[0]
                  
                
def preference(pron, candidate, this, last, sent):
    if candidate == []:
        return ['','*','*']
    
    score = [0]*len(candidate)
    for i in range(0,len(candidate)):
        score[i]=i
        if candidate[i][0] in [n[0] for n in this]:
            score[i] = score[i] + 5
            if sent.index(pron[0]) > sent.index(nltk.word_tokenize(candidate[i][0])[0]):
                score[i] = score[i] + 5
                
        if candidate[i][0] in [n[0] for n in last]:
            score[i] = score[i] + 10
      
    return candidate[score.index(max(score))]


def constraint(pron, candidate):
    temp = []
    
    for c in candidate:
        if c[1] == pron[1] or pron[1] == 'n' or c[1] == 'n':
            if c[2] == pron[2] or pron[2] == '*':
                temp = temp +[c]
    return temp
             
def merge(x, y):
    for n in y:
        x = x + [[n[0], gender(n), number(n)]]
    return x     

def number(noun):
    if noun[1] in ['NN','NNP']:
        return 's'
    return 'p'

FEMALE = [n for n in nltk.corpus.names.words('female.txt')]
MALE = [n for n in nltk.corpus.names.words('male.txt')]
def gender(noun):
    if noun[0] in FEMALE:
        return 'f'
    if noun [0] in MALE:
        return 'm'
    return 'n'