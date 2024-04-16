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

# Configure Chrome options
chrome_options = Options()

# chrome_options.add_argument("--disable-gpu")  # Commented out
chrome_options.add_argument(
    "--log-path=/path/to/logfile.log")  # Enable browser logs
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument(
    "--disable-features=IsolateOrigins,site-per-process")

# Create a new instance of the Chrome driver (non-headless mode)
driver = webdriver.Chrome(options=chrome_options)

actions = ActionChains(driver)

url = "https://www.ke.sportpesa.com/en/sports-betting/football-1/"
logging.info(f"Navigating to {url}")
driver.get(url)
print(url)

# Wait for the username and password fields to be present
wait = WebDriverWait(driver, 60)
logging.info("Waiting for username and password fields...")
username_field = wait.until(
    EC.presence_of_element_located((By.ID, "username")))
password_field = wait.until(
    EC.presence_of_element_located((By.ID, "password")))

# Enter the login credentials
logging.info("Entering login credentials...")
username_field.send_keys("")
password_field.send_keys("")

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

    # play_button_element.click()
    driver.execute_script("arguments[0].click();", play_button_element)

    time.sleep(6)

    logging.info('Card accessed')

except Exception as e:
    logging.error(f"Error in clicking the Casino link or button: {str(e)}")
    import traceback

    traceback.print_exc()

new_url = driver.current_url
print("New URL:", new_url)

time.sleep(5)

# Checking the provably fair algorithms variables ie clientSeed and  serverSeed
variables_js = """






"""
# result = driver.execute_script(variables_js)
# print(result)


# inputting the bet amount
# Find the input element and the span element

script = """
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

                    // Enter the amount of stake  value
                    const newValue = 2.00;

                    // Validate the input as a float
                    if (isValidFloat(newValue)) {
                    // Update the input value with the parsed float value
                    inputElement.value = parseFloat(newValue);

                    // Update the text content of the span within the bet button
                    betButtonSpan.textContent = inputElement.value;

                     // Dispatch the focusout event to simulate moving the cursor away from the input field
                    const focusOutEvent = new FocusEvent('focusout', { bubbles: true });
                    inputElement.dispatchEvent(focusOutEvent);

                    return `Input value updated to: ${inputElement.value}`;
                    } else {
                    return 'Invalid input. Please enter a valid number.';
                    }
                } else {
                    console.log('Input element or bet button span not found.');
                }



            }

            updateInputValue();

        """

# Execute the JavaScript function
driver.execute_script(script)

# # clicking the button
# driver.execute_script(
#     "document.querySelector('.btn.btn-success.bet').click();")

js_script = """
// Load CryptoJS library via CDN
 var script = document.createElement('script');
 script.src = 'https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js';
 script.onload = function() {
    

    function getRandomNumber() {
      return Math.random() * (19999 - 10000) + 1;
    }
     //get seeds
     async function getSeeds() {
            try {
                const elementSelector = 'body > app-root > app-game > div > div.main-container > div.main-header > app-header > div > div.second-block.d-flex > div > div.user-wrapper.h-100.dropdown > div.dropdown-toggle';
                const hambugerMenu = document.querySelector(elementSelector);

                if (hambugerMenu) {
                hambugerMenu.click();
                } else {
                console.log('Hamburger menu element not found.');
                return null;
                }

                await new Promise((resolve) => setTimeout(resolve, 150)); // Wait for dropdown to open

                const dropdownMenu = document.querySelector('body > app-root > app-game > div > div.main-container > div.main-header > app-header > div > div.second-block.d-flex > div > div.user-wrapper.h-100.show.dropdown > div.user-menu-dropdown.dropdown-menu.show');

                if (!dropdownMenu) {
                console.log('Dropdown menu element not found.');
                return null;
                }

                const musicDiv = dropdownMenu.querySelector('app-settings-menu > div > div.second-block > div:nth-child(2) > div:nth-child(2)');
                musicDiv.click();

                await new Promise((resolve) => setTimeout(resolve, 150)); // Wait for settings menu to load

                const clientSpan = document.querySelector('div.key-container.random .key span:not(.current)');
                const clientSeed = clientSpan ? clientSpan.textContent.trim() : undefined;

                const serverDiv = document.querySelector('.server-seed-value-block .key-container .key');
                const serverSeed = serverDiv ? serverDiv.textContent.trim() : undefined;

                results = await getSeeds(); 
                // Target the close button within the modal header
                const closeButton = document.querySelector('.modal-header button.close');

                // Click the close button
                if (closeButton) {
                closeButton.click();
                } else {
                console.error('Close button not found in the modal header');
                }

                return [clientSeed, serverSeed];
            } catch (error) {
                console.error('An error occurred:', error);
                return null;
            }
        } 
     //*get seeds

      // SHA-512 hashing function
     function sha512(input) {
         return CryptoJS.SHA512(input).toString(CryptoJS.enc.Hex);
     }

     // Function to calculate the game result coefficient
     function calculateGameResult(serverSeed, clientSeed) {
         // Merge server seed and client seed
         var mergedSeed = serverSeed + clientSeed;

         // Hash the merged seed using SHA-512
         var hash = sha512(mergedSeed);

         // Convert the hash to a decimal value between 0 and 1
         var decimalValue = parseInt(hash.substr(0, 13), 16) / Math.pow(2, 52);

         // Calculate the multiplier (result coefficient) based on the decimal value
         var multiplier = Math.floor(decimalValue * 100) / 100 + 1; // Round to 2 decimal places and add 1

         // Return the multiplier
         return multiplier;
     }

    // Wait for the cashout button and click it
    async function waitForCashoutButton() {
        let interval = setInterval(async function() {
            const cashoutButton = document.querySelector('button.btn-warning.cashout');
            if (cashoutButton ) {
                let resultCoefficient = '';
                if (!cashoutButton.getAttribute('data-coefficient')) { 
                clearInterval(interval);  
                    var results = await getSeeds(); 
                    if (!results) return; // Exit if seeds are not obtained
        
                    // Place a bet 
                     resultCoefficient = calculateGameResult(results[1], results[0]);
                     cashoutButton.setAttribute('data-coefficient', resultCoefficient);
                }
                 
                cashoutButton.innerText = 'Cashout at ' + resultCoefficient + 'x'; 
            } else {
               // cashoutButton.removeAttribute('data-coefficient');
            }
        }, 500);
    }

    // Call the waitForCashoutButton function to start the process
    waitForCashoutButton();
    };
 document.head.appendChild(script);
"""

# Execute the JavaScript code
# for i in range(100000):
driver.execute_script(js_script)
# time.sleep(10)

time.sleep(5000000)
driver.quit()
