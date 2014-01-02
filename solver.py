# This file should contain solution methods to problems.
import utils
import time
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
    ques_s = question['question'].strip().split(' ')
    blank_id = ques_s.index('['+str(question['number'])+']')
    prob = {}
    for i in 'a','b','c','d':
        prob[i] = max(search_result(question[i]+' '+ques_s[blank_id+1]),
                      search_result(ques_s[blank_id-1]+' '+question[i]),
                      search_result(question[i]+' '+ques_s[blank_id+1]+' '+ques_s[blank_id+2]),
                      search_result(ques_s[blank_id-2]+' '+ques_s[blank_id-1]+' '+question[i]),
                      search_result(ques_s[blank_id-1]+' '+question[i]+' '+ques_s[blank_id+1]) )
        print '* '+question[i]+' ==> '+str(prob[i])+'\n'
    
    print 'Question '+str(question['number'])+' I guess '+max(prob, key=prob.get)+'\n'
    time.sleep(15)
    return max(prob, key=prob.get)
    
    
def search_result(inputtext):
    excepttime = -1
    while 1:
        try:
            excepttime += 1
            if excepttime >= 3:
                print inputtext, 'not found'
                return 0
            
            driver.get("https://www.google.com/?q="+inputtext+"&tbs=bks:1,cdr:1,cd_min:1980,cd_max:2008&lr=lang_en")
            driver.find_element_by_name("q").send_keys(Keys.RETURN)
            driver.find_element_by_id("main").click()
            #print driver.title
            time.sleep(1)
            word = driver.execute_script("return document.getElementById('resultStats').firstChild.nodeValue")
            print inputtext, getvalue(word)
            return getvalue(word)
        except:
            pass


def getvalue(resultString):
    ''' get result count from Google search '''
    return int(resultString[3:-4].replace(',', ''))
