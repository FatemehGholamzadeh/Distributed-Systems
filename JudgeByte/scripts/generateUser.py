from selenium import webdriver


chromedriver_location = "C:/Users\SG\Downloads\Compressed\chromedriver_win32/chromedriver"
driver = webdriver.Chrome(chromedriver_location)
def create_user():
    name_input = '/html/body/div[1]/form/p[1]/input'
    username_input = '/html/body/div[1]/form/p[2]/input'
    password_input = '/html/body/div[1]/form/p[3]/input'
    password_input2 = '/html/body/div[1]/form/p[5]/input'
    signup_submit = '/html/body/div[1]/form/input[2]'

    for i in range(20):
        driver.get('http://127.0.0.1:8000/coders/signup/')
        driver.find_element_by_xpath(username_input).send_keys("user_" + str(i))
        driver.find_element_by_xpath(name_input).send_keys("name_" + str(i))
        driver.find_element_by_xpath(password_input).send_keys("mitra1341")
        driver.find_element_by_xpath(password_input2).send_keys("mitra1341")
        driver.find_element_by_xpath(signup_submit).click()

def upload_code():

    username_input ='/html/body/div[1]/form/p[1]/input'
    password_input= '/html/body/div[1]/form/p[2]/input'
    login_submit = '/html/body/div[1]/form/input[2]'
    code_box ='/html/body/div[1]/form/p[2]/textarea'
    code_submit='/html/body/div[1]/form/input[2]'

    for i in range(20):
        driver.get('http://127.0.0.1:8000/login/')
        driver.find_element_by_xpath(username_input).send_keys("user_" + str(i))
        driver.find_element_by_xpath(password_input).send_keys("mitra1341")
        driver.find_element_by_xpath(login_submit).click()
        driver.get('http://127.0.0.1:8000/submissions/submit/hello-world/')
        driver.find_element_by_xpath(code_box).send_keys("this is my code :" + "user_"+str(i))
        driver.find_element_by_xpath(code_submit).click()

def upload_code2(id):

    username_input ='/html/body/div[1]/form/p[1]/input'
    password_input= '/html/body/div[1]/form/p[2]/input'
    login_submit = '/html/body/div[1]/form/input[2]'
    code_box ='/html/body/div[1]/form/p[2]/textarea'
    code_submit='/html/body/div[1]/form/input[2]'
    driver.get('http://127.0.0.1:8000/login/')
    driver.find_element_by_xpath(username_input).send_keys("user_" + str(id))
    driver.find_element_by_xpath(password_input).send_keys("mitra1341")
    driver.find_element_by_xpath(login_submit).click()
    driver.get('http://127.0.0.1:8000/submissions/submit/hello-world/')
    driver.find_element_by_xpath(code_box).send_keys("this is my code :" + "user_" + str(id))
    driver.find_element_by_xpath(code_submit).click()


# upload_code()
for i in range(10):
    upload_code2(i)