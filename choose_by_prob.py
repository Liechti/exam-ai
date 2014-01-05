#method to choose by Googling

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def choose_by_prob(question):
    
    driver = webdriver.Firefox()
    
    prob = {}
    prob['a'] = get_prob_by_search(driver, question['a'])
    prob['b'] = get_prob_by_search(driver, question['b'])
    prob['c'] = get_prob_by_search(driver, question['c'])
    prob['d'] = get_prob_by_search(driver, question['d'])
    
    driver.quit()
    return max(prob)
    
def get_prob_by_search(driver, inputtext):
    
    driver.get("https://www.google.com/?q=\""+inputtext+"\"&tbs=bks:1,cdr:1,cd_min:1980,cd_max:2008&lr=lang_en")
    
    assert "Google" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys(Keys.RETURN)
    elem3 = driver.find_element_by_id("main")
    elem3.click()
    
    word = driver.execute_script("return document.getElementById('resultStats').firstChild.nodeValue")
    print inputtext, getvalue(word)
    return getvalue(word)
    
def getvalue(resultString):
    return int(resultString[3:-4].replace(',', ''))

if __name__ == "__main__":
    question = {}
    question['a'] = 'surrendered'
    question['b'] = 'postponed'
    question['c'] = 'abandoned'
    question['d'] = 'opposed'
    question['question'] = 'question'
    question['section_number'] = 'sec'
    question['number'] = '12'
    question['article'] = 'article'
    print choose_by_prob(question)
    