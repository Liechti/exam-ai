# This file should contain solution methods to problems.
import re, utils, time, random, operator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def semantic_analysis(question):
    pass

''' Ngram by googling, for section 1 & 2 '''

def driverinit():
    global driver 
    print 'driverinit'
    driver = webdriver.Firefox()

def driverclose():
    driver.quit()
    
    
def ngram_analysis(question):
    print 'Input str == '+question['question']+'\n'
    ques_s = question['question'].strip().replace(',','').replace('.','').replace(':','').replace('?','').split(' ')
    blank_id = ques_s.index('['+str(question['number'])+']')
    length = len(ques_s)
    
    prob = {}
    point = {}
    
    #log of resultStat (smooth by 10)
    for i in 'a','b','c','d':
        point[i] = 1
        if blank_id > 0:
            point[i] *= (10 + search_result(ques_s[blank_id-1]+' '+question[i]))
        if blank_id < length-1:
            point[i] *= (10 + search_result(question[i]+' '+ques_s[blank_id+1]))
        if blank_id < length-2:
            point[i] *= (10 + search_result(question[i]+' '+ques_s[blank_id+1]+' '+ques_s[blank_id+2])) 
        if blank_id > 1:
            point[i] *= (10 + search_result(ques_s[blank_id-2]+' '+ques_s[blank_id-1]+' '+question[i]))
        if 0 < blank_id < length-1:
            point[i] *= (10 + search_result(ques_s[blank_id-1]+' '+question[i]+' '+ques_s[blank_id+1]))
    
    #previous version
    '''
    for i in 'a','b','c','d':
        point[i] = 0
    if blank_id > 0: 
        for i in 'a','b','c','d':
            prob[i] = search_result(ques_s[blank_id-1]+' '+question[i])
        choice, weight = decision(prob)
        point[choice] += weight 
    if blank_id < length-1: 
        for i in 'a','b','c','d':
            prob[i] = search_result(question[i]+' '+ques_s[blank_id+1]) 
        choice, weight = decision(prob)
        point[choice] += weight
    if blank_id < length-2: 
        for i in 'a','b','c','d':
            prob[i] = search_result(question[i]+' '+ques_s[blank_id+1]+' '+ques_s[blank_id+2]) 
        choice, weight = decision(prob)
        point[choice] += weight
    if blank_id > 1: 
        for i in 'a','b','c','d':
            prob[i] = search_result(ques_s[blank_id-2]+' '+ques_s[blank_id-1]+' '+question[i])
        choice, weight = decision(prob)
        point[choice] += weight 
    if 0 < blank_id < length-1: 
        for i in 'a','b','c','d':
            prob[i] = search_result(ques_s[blank_id-1]+' '+question[i]+' '+ques_s[blank_id+1])
        choice, weight = decision(prob)
        point[choice] += weight*2 
    '''
    
    print point
    print 'Question '+str(question['number'])+' I guess '+max(point, key=point.get)+'\n'
    time.sleep(15)
    return max(point, key=point.get)

    
def decision(prob):
    sorted_p = sorted(prob.iteritems(), key=operator.itemgetter(1))
    if sorted_p[-1][1] > sorted_p[-2][1]*10 and sorted_p[-1][1] > 1000:
        print 'point '+sorted_p[-1][0]+' += 4\n'
        return (sorted_p[-1][0], 4)
    elif sorted_p[-1][1] <= sorted_p[-2][1]*10 and sorted_p[-1][1] > 10000:
        print 'point '+sorted_p[-1][0]+' += 2\n'
        return (sorted_p[-1][0], 2)
    elif sorted_p[-1][1] != 0:
        print 'point '+sorted_p[-1][0]+' += 1\n'
        return (sorted_p[-1][0], 1)
    else:
        print 'no contributions\n'
        return (sorted_p[-1][0], 0)

    
def search_result(inputtext):
    excepttime = -1
    while 1:
        try:
            excepttime += 1
            if excepttime >= 3:
                print inputtext, '"search exception"'
                return 0
            
            driver.get("https://www.google.com/?q=\""+inputtext+"\"&tbs=bks:1,cdr:1,cd_min:1980,cd_max:2008&lr=lang_en")
            driver.find_element_by_name("q").send_keys(Keys.RETURN)
            driver.find_element_by_id("main").click()
            #print driver.title
            time.sleep(random.randint(1,5))
            word = driver.execute_script("return document.getElementById('resultStats').firstChild.nodeValue")
            notfound = driver.execute_script("return document.getElementById('topstuff').firstChild")
            #print notfound
            print inputtext, getvalue(word) if notfound is None else '"no result"'
            return getvalue(word) if notfound is None else 0
        except:
            pass


def getvalue(resultString):
    ''' get result count from Google search '''
    return int(re.search(r'\d+', resultString.replace(',','')).group())
