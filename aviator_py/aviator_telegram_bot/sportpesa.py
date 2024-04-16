import logging
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

import time


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Chrome options for headless mode
chrome_options = Options()  # Test for the existence of the input fieldloggin

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "--log-path=/path/to/logfile.log")  # Enable browser logs
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument(
    "--disable-features=IsolateOrigins,site-per-process")


# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

actions = ActionChains(driver)


url = "https://www.ke.sportpesa.com/en/sports-betting/football-1/"
logging.info(f"Navigating to {url}")
driver.get(url)
print(url)

# Wait for the username and password fields to be present
wait = WebDriverWait(driver, 20)
logging.info("Waiting for username and password fields...")
username_field = wait.until(
    EC.presence_of_element_located((By.ID, "username")))
password_field = wait.until(
    EC.presence_of_element_located((By.ID, "password")))

# Enter the login credentials
logging.info("Entering login credentials...")
username_field.send_keys("")
password_field.send_keys("@")

# Find and click the login button (if present)
try:
    login_button = driver.find_element(
        By.XPATH, '//input[@data-qa="common-login-submit"]')
    logging.info("Clicking the login button...")
    login_button.click()
    logging.info("Login successful!")
except Exception:
    logging.error("Login button not found or unable to click.")


# Click the Casino link
try:
    logging.info("Finding the Casino link...")
    casino_link = driver.find_element(
        By.XPATH, "//*[@id='tools']/div/div/div/div[1]/ul/item-menu[3]/li/a")
    logging.info("Casino link found!")
    logging.info("Clicking the Casino link...")
    casino_link.click()
    logging.info("Casino link clicked successfully!")

    # Wait for the casino iframe to be present and switch to it
    logging.info("Waiting for the casino iframe to be present...")
    casino_iframe = wait.until(
        EC.presence_of_element_located((By.ID, "casino-iframe")))
    driver.switch_to.frame(casino_iframe)

    # Wait for the div with id 'root' to be present and visible
    logging.info("Waiting for the div with id 'root' to be present...")
    root_div = wait.until(EC.visibility_of_element_located((By.ID, "root")))

    target_child_div = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='Popular-list']/child::*[1]")))

    # Hovering over the card
    actions.move_to_element(target_child_div).perform()

    time.sleep(5)

    play_button_element = target_child_div.find_element(
        By.XPATH, ".//div[@class='sc-hUOJWJ QAhsU']/button")

    # play_button_element = wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, "//div[@class='sc-hUOJWJ QAhsU']/button")))

    print(play_button_element)
    driver.execute_script("arguments[0].click();", play_button_element)

    driver.execute_script("return    document.readyState;")

    logging.info('Card accessed')


except Exception as e:
    logging.error(f"Error in clicking the Casino link or button: {str(e)}")
    import traceback
    traceback.print_exc()


new_url = driver.current_url
print("New URL:", new_url)

time.sleep(10)

# inputting the bet amount
# Find the input element and the span element

locators = """
            const selector = 'body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature > div.bet-block > app-spinner > div > div.input > input'
            const spanSelector = 'body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.bet-controls > app-bet-controls > div > app-bet-control:nth-child(1) > div > div.first-row.auto-game-feature > div.buttons-block > button > span > label.amount > span:nth-child(1)'
            
            function updateInputValue() {
                // Function to validate input as a float
                function isValidFloat(value) {
                    return !isNaN(parseFloat(value));
                }

                const inputElement = document.querySelector(selector);
                const betButtonSpan = document.querySelector(spanSelector);

                if (inputElement && betButtonSpan) {
                    // Clear the input value
                    inputElement.value = '';

                    // Prompt the user for a new value
                    const newValue = prompt('Enter a new value:');

                    // Validate the input as a float
                    if (isValidFloat(newValue)) {
                    // Update the input value with the parsed float value
                    inputElement.value = parseFloat(newValue);

                    // Update the text content of the span within the bet button
                    betButtonSpan.textContent = inputElement.value;

                    // Dispatch an input event to trigger any associated updates
                    inputElement.dispatchEvent(new Event('input', { bubbles: true }));

                    return `Input value updated to: ${inputElement.value}`;
                    } else {
                    return 'Invalid input. Please enter a valid number.';
                    }
                } else {
                    console.log('Input element or bet button span not found.');
                }
                
                updateInputValue();

            }


        """


# Execute the JavaScript function
driver.execute_script(locators)

# placing a bet
try:
    driver.execute_script(
        "document.querySelector('.btn.btn-success.bet').click();")

    time.sleep(30)
except Exception as e:
    print("An error occurred:", e)


driver.quit()
