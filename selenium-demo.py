from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



# TEST 1: Correct title
def test1(driver):
    assert driver.title == "BalaRosh – Bags For Every Occasion"

# TEST 2: Redirects to correct location
def test2(driver):
    driver.find_element(By.XPATH, "//*[@id='post-5']/div/div/div/section[3]/div/div[1]/div/div[5]/div/div/a").click()
    assert driver.current_url == "https://balarosh.com/product-category/totes/"
    
    driver.find_element(By.XPATH, '//*[@id="main"]/div/ul/li[7]/div[1]/a').click()
    assert driver.current_url == "https://balarosh.com/product/midnight-black/"

# TEST 3: Correct image is uploaded
def test3(driver):
    img = driver.find_element(By.XPATH, '//*[@id="product-1154"]/div[1]/div/div/div[1]/img')
    source = img.get_attribute('src')
    assert source == "https://balarosh.com/wp-content/uploads/2022/01/DSC_9961-600x600.jpg"

# TEST 4: Cart value is being updated
def test4(driver):
    cart_value = driver.find_element(By.XPATH, '//*[@id="ast-site-header-cart"]/div[1]/a/div/span').get_attribute('textContent')
    cart_value = cart_value.replace(" ", "")
    cart_value = cart_value.replace("\t", "")
    cart_value = cart_value.replace("\n", "")
    assert cart_value == "0"
    
    
    driver.find_element(By.XPATH, '//*[@id="product-1154"]/div[2]/form/button').click()
    cart_value = driver.find_element(By.XPATH, '//*[@id="ast-site-header-cart"]/div[1]/a/div/span').get_attribute('textContent')
    cart_value = cart_value.replace(" ", "")
    cart_value = cart_value.replace("\t", "")
    cart_value = cart_value.replace("\n", "")
    assert cart_value == "1"
    
    
def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")

    # Chrome web driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://balarosh.com")
    try:
        test1(driver)
        test2(driver)
        test3(driver)
        test4(driver)
    except AssertionError as e:
        print(e)
if __name__=="__main__":
    main()