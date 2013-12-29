import nltk
import utils
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

FORBIDDEN = stopwords.words('english')

grammar = """
S:
    {<DP><VP>}
DP:
    {<DT><NP>}
    {<PRP.*>}
    {<DP><CC><DP>}
NP:
    {<NN.*|AP>*<NN.*><PP>*}
    {<NP><CC><NP>}
AP:
    {<AP>*<JJ.*>}
    {<AP><CC><AA>}
VP:
    {<RB.*>*<VB.*><DP>?<PP>?<RB.*>*}
    {<VP><CC><VP>}
PP:
    {<IN><DP>}
    {<PP><PP>}
    """
def content_extract(text):
    #extract important content terms.(text should be an string object)
    filtered_words = [w for w in text.split() if not w in FORBIDDEN]
    return filtered_words

def word_processor(word):
    NOUN = ['NN', 'NNS']
    VERB = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    if word[1] in NOUN:
        processed = word[0].lower()
        processed = nltk.WordNetLemmatizer().lemmatize(processed)
        return (processed, word[1])
    if word[1] in VERB:
        processed = nltk.WordNetLemmatizer().lemmatize(word[0], 'v')
        return (processed, word[1])
    return word       

def basic_processor(article):
    # tokenize, turn to lowr-case, lemmatize, POS-tagging,
    token= nltk.word_tokenize(article)
    tag=nltk.pos_tag(token)
    
    processed = []
    for word in tag:
        processed = processed + [word_processor(word)]
    return processed
                   
def leaves(tag, type):
    #chunk the tagged sentences, and yield the subtrees of the desired type(ex:'NP') 
    tree = nltk.RegexpParser(grammar).parse(tag)
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
        NP_terms = NP_terms + [' '.join([w[0] for w in term])]
    return NP_terms

def X_extractor(text,type):
    #extract Phrase of the desired type
    terms = [term for term in extractor(text,type)]
    X_terms = []
    for term in terms:
        X_terms = X_terms + [' '.join([w[0] for w in term])]
    return X_terms           
            
#testing the NP_extractor function
# import parse
#   
# questions = parse.parse_test("exams/102.txt")
# text = utils.get_question(questions, 42)['question']
# print text
# print basic_processor(text)
# 
# print X_extractor(text, 'VP')