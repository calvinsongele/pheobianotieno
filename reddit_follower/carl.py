import contextlib
import time, enum, random, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from ghost import GhostLog


class DefaultLinksEnum(enum.Enum):
    home = "https://www.reddit.com/"
    login = "https://www.reddit.com/login/"
    register = "https://www.reddit.com/register/"


class Timeouts:
    def short_pause():
        time.sleep(random.random() + random.randint(0, 1))

    def medium_pause():
        time.sleep(random.random() + random.randint(1, 2))

    def long_pause():
        time.sleep(random.random() + random.randint(5, 10))


class RedditBot:
    def __init__(self, verbose: bool = False):
        self.logger = GhostLog
        if verbose:
            self.verbose = True
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(logging.StreamHandler())
            formatter = logging.Formatter(
                "\033[93m[INFO]\033[0m %(asctime)s \033[95m%(message)s\033[0m"
            )
            self.logger.handlers[0].setFormatter(formatter)

        self.logger.info("Booting up webdriver")
        options = webdriver.ChromeOptions()
        options.add_argument("log-level=3")
        options.add_argument("--lang=en")
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
        self.driver = webdriver.Chrome(options=options)
        self.logger.info("Webdriver booted up")

    def reddit_signup(self, email: str, password: str):
        self.reddit_logout()
        self.logger.info(f"Registering in \033[4m{email}\033[0m")
        self.driver.get(DefaultLinksEnum.login.value)
        Timeouts.long_pause()
        # send in email and pause
        email_f = self.driver.find_element(By.NAME, "username")

        for ch in email:
            email_f.send_keys(ch)
        # press submit button
        Timeouts.medium_pause()

        # get username
        username = self.driver.find_element(By.NAME, "username")
        Timeouts.medium_pause()
        # send in email and pause
        password_f = self.driver.find_element(By.NAME, "username")
        for ch in password:
            password_f.send_keys(ch)
        # press submit button and solve robots test
        return password_f

    def reddit_login(self, username: str, password: str):
        self.reddit_logout()
        self.logger.info(f"Logging in as \033[4m{username}\033[0m")
        self.driver.get(DefaultLinksEnum.login.value)
        # self.driver.find_element(By.LINK_TEXT, "Log In").click()

        Timeouts.long_pause()
        try:
            username_f = self.driver.find_element(By.NAME, "username")
        except NoSuchElementException:
            WebDriverWait(self.driver, 100).until(
                expected_conditions.frame_to_be_available_and_switch_to_it((By.XPATH,
                                                                            '//*[@id="loginUsername"]')
                                                                           ))
        #     username_f = self.driver.find_element(By.NAME)
        # username_f.send_keys(username)

        for ch in username:
            username_f.send_keys(ch)
            # Timeouts.short_pause()
        Timeouts.medium_pause()

        password_f = self.driver.find_element(By.NAME, "password")
        # password_f.send_keys(password)

        for ch in password:
            password_f.send_keys(ch)
            # Timeouts.short_pause()
        Timeouts.medium_pause()

        with contextlib.suppress(Exception):
            password_f.send_keys(Keys.ENTER)
        Timeouts.medium_pause()

        assert "https:www.reddit.com/login" not in self.driver.current_url, "Login failed"

        self.popup_handler()
        self.cookies_handler()
        self.logger.info(f"Logged in successfully.")

    def reddit_logout(self) -> None:
        self.logger.info("Clearing browser data")

        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get("chrome://settings/clearBrowserData")
        Timeouts.short_pause()

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)
        actions.perform()
        Timeouts.short_pause()

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER)
        actions.perform()
        Timeouts.medium_pause()

        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def vote(self, link: str, action: bool) -> None:
        if action:
            self.logger.info(f"Upvoting \033[4m{link}\033[0m")
        else:
            self.logger.info(f"Downvoting \033[4m{link}\033[0m")
        self.get_link(link, handle_nsfw=True)

        if action:
            button = self.driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div["
                                              "1]/div[3]/div[1]/div/div[1]/div/button[1] "
                                              )
        else:
            button = self.driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div["
                                              "1]/div[ "
                                              "3]/div[1]/div/div[1]/div/button[2] "
                                              )

        button.click()
        Timeouts.medium_pause()

    def comment(self, link: str, comment: str) -> None:
        self.logger.info(f"Commenting on \033[4m{link}\033[0m")

        self.get_link(link, handle_nsfw=True)

        html_body = self.driver.find_element(By.XPATH, "/html/body")
        html_body.send_keys(Keys.PAGE_DOWN)
        Timeouts.short_pause()

        if comment:
            try:
                textbox = self.driver.find_element(By.XPATH,
                                                   "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div["
                                                   "2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div "
                                                   )
            except NoSuchElementException:
                textbox = self.driver.find_element(By.XPATH,
                                                   '//*[@id="AppRouter-main-content"]/div/div/div[2]/div[3]/div[1]/div['
                                                   '2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div/div',
                                                   )
            textbox.click()

            for ch in comment:
                textbox.send_keys(ch)
                Timeouts.short_pause()

            try:
                comment_button = self.driver.find_element(By.XPATH,
                                                          "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div["
                                                          "2]/div[1]/div[2]/div[3]/div[2]/div/div/div[3]/div[1]/button "
                                                          )
            except NoSuchElementException:
                comment_button = self.driver.find_element(By.XPATH,
                                                          '//*[@id="AppRouter-main-content"]/div/div/div[2]/div['
                                                          '3]/div[1]/div[2]/div[3]/div[2]/div/div/div[3]/div['
                                                          '1]/button')

            comment_button.click()

        Timeouts.medium_pause()

    def join_community(self, link: str, join: bool) -> None:
        if join:
            self.logger.info(f"Joining \033[4m{link}\033[0m")
        else:
            self.logger.info(f"Leaving \033[4m{link}\033[0m")

        self.get_link(link, handle_nsfw=True)

        try:
            join_button = self.driver.find_element(By.CLASS_NAME, "join-btn")
        except NoSuchElementException:
            join_button = self.driver.find_element(By.CLASS_NAME, "py-xs")

        button_text = join_button.text.lower()


        click_js = """
            // button-primary button-medium button join-btn leading-none px-sm py-xs 
            let shadowHost = document.querySelector('shreddit-subreddit-header-buttons');
            let jointbtn = document.querySelector('shreddit-subreddit-header-buttons').shadowRoot.querySelector('div').querySelector('faceplate-tracker').querySelector('shreddit-join-button').shadowRoot.querySelector('.join-btn');
            var res = 'button not clicked yet';
            if (jointbtn){
                jointbtn.click();
                res = 'button found and clicked';
            } else {
            res = 'btn not found';
            }
            return res;
        """

        clickedbtn = self.driver.execute_script(click_js)
        print(clickedbtn)
        if join and button_text == "join" or not join and button_text == "joined":
            print('join btn found')
        # join_button.click()

    Timeouts.medium_pause()

    def get_link(self, link: str, handle_nsfw: bool = False) -> None:
        self.driver.get(link)
        Timeouts.medium_pause()

        if handle_nsfw:
            with contextlib.suppress(NoSuchElementException):
                nsfw_button = self.driver.find_element(By.XPATH,
                                                       "/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div["
                                                       "2]/button "
                                                       )
                nsfw_button.click()
            Timeouts.medium_pause()

    def popup_handler(self) -> None:
        with contextlib.suppress(NoSuchElementException):
            close_button = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div["
                                                    "2]/div/div[1]/span[2]/div/div[2]/button "
                                                    )
            close_button.click()

    def cookies_handler(self) -> None:
        with contextlib.suppress(NoSuchElementException):
            accept_button = self.driver.find_element(By.XPATH,
                                                     "/html/body/div[1]/div/div/div/div[3]/div/form/div/button"
                                                     )
            accept_button.click()

    def shutdown(self) -> None:
        self.logger.info("Closing the bot")
        self.driver.quit()
