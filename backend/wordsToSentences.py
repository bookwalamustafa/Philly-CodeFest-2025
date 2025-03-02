import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Needed for explicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1) Set up ChromeOptions to point to Brave’s binary
options = Options()
# Adjust this path if Brave is in a different location on your machine:
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# 2) Initialize ChromeDriver with the Brave binary
driver = webdriver.Chrome(options=options)

try:
    # Go to the Broken English to English translator page
    driver.get("https://anythingtranslate.com/translators/broken-english-to-english-translator/")
    
    # Wait for page to load
    time.sleep(2)
    
    # Scroll down a little (adjust the value as needed)
    driver.execute_script("window.scrollTo(0, 200)")
    
    # 1) Locate input <textarea> by ID and enter text
    broken_english_box = driver.find_element(By.ID, "to-translate-text")
    broken_english_box.clear()
    broken_english_box.send_keys("ME GO STORE YESTERDAY BUY APPLE.")

    # 2) Locate the "Translate" button by class (or any other unique selector)
    #    Then scroll into view using ActionChains
    translate_button = driver.find_element(By.CSS_SELECTOR, ".translation-submit-button")
    actions = ActionChains(driver)
    actions.move_to_element(translate_button).perform()
    time.sleep(1)  # small delay for page layout to settle

    # 2a) Use an explicit wait to ensure the button is clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".translation-submit-button"))
    )

    # Now click the button
    translate_button.click()

    # 3) Wait for translation to process (3s is arbitrary; ideally use an explicit wait for the output too)
    time.sleep(3)

    # 4) Retrieve the translated text from the output <textarea> by ID
    output_box = driver.find_element(By.ID, "translated-text")
    translated_text = output_box.get_attribute("value")

    print("Translated text:", translated_text)

finally:
    driver.quit()






# import time
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By

# # Initialize Chrome WebDriver
# driver = webdriver.Chrome()

# try:
#     # Go to the Broken English to English translator page
#     driver.get("https://anythingtranslate.com/translators/broken-english-to-english-translator/")
    
#     # Give the page a moment to load
#     time.sleep(2)

#     # 1) Locate the input <textarea> by ID and enter text
#     broken_english_box = driver.find_element(By.ID, "to-translate-text")
#     broken_english_box.clear()
#     broken_english_box.send_keys("ME GO STORE YESTERDAY BUY APPLE.")

#     # 2) Locate the "Translate" button by class (or any other unique selector)
#     translate_button = driver.find_element(By.CSS_SELECTOR, ".translation-submit-button")
    
#     # *** Scroll the button into view before clicking (Option 1) ***
#     actions = ActionChains(driver)
#     actions.move_to_element(translate_button).perform()  # Scroll/move to element
#     time.sleep(1)  # slight pause to let any layout shift happen
    
#     # Now click the button
#     translate_button.click()

#     # 3) Wait for translation to process
#     time.sleep(3)  # For a real app, consider using an explicit wait

#     # 4) Retrieve the translated text from the output <textarea> by ID
#     output_box = driver.find_element(By.ID, "translated-text")
#     translated_text = output_box.get_attribute("value")  # For textareas, "value" typically holds the text

#     print("Translated text:", translated_text)

# finally:
#     driver.quit()
