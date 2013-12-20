def getcount(inputtext):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.Firefox()
    driver.get("https://www.google.com/?q=\"abandoned until\"&tbs=bks:1,cdr:1,cd_min:1980,cd_max:2008&lr=lang_en")
    assert "Google" in driver.title
    elem = driver.find_element_by_name("q")
    elem.send_keys(Keys.RETURN)
    count = driver.find_element_by_id("resultStats")
    print count.text()
    
if __name__ == "__main__":
    getcount("abandoned until")