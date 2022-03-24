from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import tkinter as tk
import random


# shows popup notifications about the tests
NOTIF = True


def alert(msg, title):
    if NOTIF:
        popup = tk.Tk()
        popup.title(title)

        window_width = 300
        window_height = 80
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()
    else:
        pass


def randomWord():
    x = ""
    for i in range(7):
        x += chr(random.randint(97, 97+25))

    return x

# TEST 1: Correct title
def test1(driver):
    assert driver.title == "BalaRosh – Bags For Every Occasion"
    alert("Test 1 passed. Page title matches", "Success")

# TEST 2: Redirects to correct location
def test2(driver):
    driver.find_element(By.XPATH, "//*[@id='post-5']/div/div/div/section[3]/div/div[1]/div/div[5]/div/div/a").click()
    assert driver.current_url == "https://balarosh.com/product-category/totes/"
    
    driver.find_element(By.XPATH, '//*[@id="main"]/div/ul/li[7]/div[1]/a').click()
    assert driver.current_url == "https://balarosh.com/product/midnight-black/"

    alert("Test 2 passed. Redirection done correctly", "Success")

# TEST 3: Correct image is uploaded
def test3(driver):
    img = driver.find_element(By.XPATH, '//*[@id="product-1154"]/div[1]/div/div/div[1]/img')
    source = img.get_attribute('src')
    assert source == "https://balarosh.com/wp-content/uploads/2022/01/DSC_9961-600x600.jpg"

    alert("Test 3 passed. Correct Image uploaded", "Success")

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

    alert("Test 4 passed. Item successfully added to cart.", "Success")    
    
def test5(driver):
    contact_button = driver.find_element(By.CSS_SELECTOR, "a[href='https://balarosh.com/contact/']")
    contact_button.click()

    # fill in data
    driver.find_element(By.ID, ('wpforms-14-field_0')).send_keys(randomWord())
    driver.find_element(By.ID, ('wpforms-14-field_0-last')).send_keys(randomWord())
    driver.find_element(By.ID, ('wpforms-14-field_1')).send_keys(randomWord() + "@gmail.com")
    driver.find_element(By.ID, ('wpforms-14-field_2')).send_keys("This is the text added by selenium for the test!!")

    time.sleep(4)

    driver.find_element(By.ID, ('wpforms-submit-14')).click()

    confirmation = driver.find_element(By.XPATH, ("//*[@id='wpforms-confirmation-14']/p"))
    text = confirmation.get_attribute('textContent')

    assert text == "Thanks for contacting us! We will be in touch with you shortly."

    alert("Test 5 completed. Contact form submitted.", "Success")

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")

    # Chrome web driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://balarosh.com")

    currentTest = 1
    try:
        test1(driver)
        currentTest += 1
        test2(driver)
        currentTest += 1
        test3(driver)
        currentTest += 1
        test4(driver)
        currentTest += 1
        time.sleep(5)
        test5(driver)
    except AssertionError as e:
        print(e)
        alert("Test " + str(currentTest) + " Failed", "Error")
    finally:
        time.sleep(5)

if __name__=="__main__":
    main()