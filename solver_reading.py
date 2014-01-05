import nltk
import article_processor
from article_processor import eigen, similarity
import question_processor
import utils

def solver(question):
    cat = question_processor.classify(question['question'])
    if cat == 'main':
        return main_solver(question)
    if cat == 'bold_face':
        return bold_solver(question)
    if cat == 't/f':
        return truth_solver(question)
    if cat == 'who':
        return wh_solver(question)
    if cat == 'why':
        return why_solver(question)
    if cat == 'what':
        return wh_solver(question)
    else:
        return 1     
           
def wh_solver(question):
    choice = [question[i] for i in ['a', 'b', 'c', 'd']]    
    choice = [question_processor.wh_processor(question['question'], c) for c in choice]
        
    sentences = nltk.sent_tokenize(question['article'])
    
    probability =[]
    for c in choice:
        ind = sent_search(sentences, c, 1)
        sim = [similarity(eigen(c),eigen(sentences[i])) for i in ind]
        probability.append(sum(sim))
    
    print probability
    return probability.index(max(probability))
                
           
def main_solver(question):
    choice = [question[i].lower() for i in ['a', 'b', 'c', 'd']]
    eigen_c = [eigen(c) for c in choice]
                           
    article = question['article']
    eigen_a = main_process(article)[0] + main_process(article)[1]

    probability = []
    for e in eigen_c:
        sim = similarity(e,eigen_a)
        probability.append(sim)
    print probability
    return probability.index(max(probability))
    
def main_process(text):
    NP = article_processor.X_extractor(text, 'NP')
    VP = article_processor.X_extractor(text, 'VP')
  
    NP_t = [article_processor.word_processor(n, 'n') for n in NP]

    VP_t = [article_processor.word_processor(v, 'v') for v in VP]
    return [NP_t, VP_t]
    
def bold_solver(question):
    sentences = nltk.sent_tokenize(question['article'])
    ind = sent_search(sentences, ['[',']'], 1)[0]
    eigen_q = eigen(sentences[ind-1]) + eigen(sentences[ind])
    
    choice = [question[i].lower() for i in ['a', 'b', 'c', 'd']]
    eigen_c = [eigen(i) for i in choice]
    
    probability =[]
    for c in eigen_c:
        sim = similarity(c,eigen_q)
        probability.append(sim)
    
    print probability
    return probability.index(max(probability))

def truth_solver(question):
    pol = question_processor.tf_decider(question['question'])
    target = question_processor.find_target(question['question'])
    
    choice = [question_processor.tf_processor(question[i].lower(), target) for i in ['a', 'b', 'c', 'd']]
    sentences = nltk.sent_tokenize(question['article'])
    
    probability =[]
    for c in choice:
        ind = sent_search(sentences, eigen(c), 1)[0]
        sim = similarity(eigen(c),eigen(sentences[ind]))
        probability.append(sim*polarity(c)*polarity(sentences[ind])*pol)
    
    print probability
    return probability.index(max(probability))
            
             
NEGATIVES = ['no', 'not', 'none', 'nobody', 'nothing', 'neither', 'Nowhere', 'Never']
def polarity(sent):
    tok = nltk.word_tokenize(sent)
    polarity = 1
    for w in tok:
        if w in NEGATIVES:
            polarity = (-1)*polarity
    return polarity

def why_solver(question):
    result = question_processor.Why_movement(question['question'])
    eigen_q = eigen(result)
    
    choice = [question[i].lower() for i in ['a', 'b', 'c', 'd']]
    eigen_c = [eigen(i) for i in choice]
        
    for e in eigen_c[0]+eigen_c[1]:
        if (eigen_c[1].count(e) + eigen_c[2].count(e) + eigen_c[3].count(e)) >= 2:
            eigen_c[0].remove(e)
            eigen_c[1].remove(e)  
            eigen_c[2].remove(e)  
            eigen_c[3].remove(e)    
                 
    sentences = nltk.sent_tokenize(question['article'])
    index = sent_search(sentences, eigen_q, 1)[0]
       
    sim = [similarity(eigen(sentences[index]),c) for c in eigen_c]
    
    probability = sim
    print probability
    return probability.index(max(probability))
    
def sent_search(sentences, keyword, N):
    score = [0]*len(sentences)
        
    for i in range(0, len(sentences)):
        s = sentences[i]
        for w in keyword:
            if utils.classify(s, [w]):
                score[i] = score[i] + 1
    
    index = sorted(range(len(score)), key=lambda i: score[i])[-N:]
    return index
#testing 
#import parse
# questions = parse.parse_test("exams/102.txt") 
# for x in range(41,57):
#     question = utils.get_question(questions, x)
#     print '#', x, ' ', solver(question)