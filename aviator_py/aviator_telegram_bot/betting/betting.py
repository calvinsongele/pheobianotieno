import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def place_bet(driver, amount):
    """
    Place a bet with the specified amount in the Aviator game.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        amount (float): The amount to bet.

    Returns:
        bool: True if the bet was placed successfully, False otherwise.
    """
    try:
        # Find the input field for entering the bet amount
        bet_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input")))

        # Clear the input field and enter the bet amount
        bet_input.clear()
        bet_input.send_keys(str(amount))

        # Find and click the "Place Bet" button
        place_bet_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button")))
        place_bet_button.click()

        logging.info(f"Placed a bet with amount: {amount}")
        return True
    except Exception as e:
        logging.error(f"Error in placing bet: {str(e)}")
        return False


def cash_out(driver):
    """
    Cash out the current bet in the Aviator game.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if the cash out was successful, False otherwise.
    """
    try:
        # Find and click the "Cash Out" button
        cash_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "your_cash_out_button_selector")))
        cash_out_button.click()

        logging.info("Cashed out the current bet")
        return True
    except Exception as e:
        logging.error(f"Error in cashing out: {str(e)}")
        return False
