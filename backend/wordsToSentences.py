import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up ChromeOptions for Brave Browser
options = Options()
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

def translate_broken_english(sentence):
    """Translates a broken English sentence using the given website."""
    try:
        # Open the translation website
        driver.get("https://anythingtranslate.com/translators/broken-english-to-english-translator/")
        time.sleep(2)  # Allow page to load

        # Locate input box and enter the sentence
        broken_english_box = driver.find_element(By.ID, "to-translate-text")
        broken_english_box.clear()
        broken_english_box.send_keys(sentence)

        # Locate the translate button and ensure it's clickable
        translate_button = driver.find_element(By.CSS_SELECTOR, ".translation-submit-button")
        actions = ActionChains(driver)
        actions.move_to_element(translate_button).perform()  # Scroll into view
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".translation-submit-button"))
        )
        translate_button.click()

        # Wait for translation to complete
        time.sleep(3)

        # Retrieve translated text
        output_box = driver.find_element(By.ID, "translated-text")
        translated_text = output_box.get_attribute("value")

        return translated_text

    except Exception as e:
        return f"Error: {str(e)}"

# List of broken English sentences
sentences = [
    "yesterday me go store buy apple, but forgot money",
    "you want eat lunch now or later"
]

# Translate each sentence
for sentence in sentences:
    translated = translate_broken_english(sentence)
    print(f"Broken English: {sentence}\nTranslated: {translated}\n")

# Quit the browser session
driver.quit()
