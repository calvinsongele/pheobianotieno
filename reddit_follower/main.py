import sys, logging
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from args import *
from carl import RedditBot, GhostLog
import secrets


if __name__ == "__main__":
    logger = GhostLog
    if "-v" in sys.argv or "--verbose" in sys.argv:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.ERROR)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(logging.FileHandler(".log"))
        formatter = logging.Formatter(
            "\033[91m[ERROR!]\033[0m %(asctime)s \033[95m%(message)s\033[0m"
        )
        logger.handlers[0].setFormatter(formatter)

    if len(sys.argv) == 1:
        logger.error("No arguments provided. Use -h or --help for help.")
        if "-v" not in sys.argv or "--verbose" not in sys.argv:
            sys.exit("No arguments provided. Use -h or --help for help.")
        sys.exit(1)
    else:
        args = cmdline_args()

    if args["newaccounts"]:
        try:
            bot = RedditBot(
                verbose=args["verbose"]
            )
            for i in range(1000):
                username = ""
                password = ""
                email = f"{secrets.token_hex(8)}@gmail.com"
                bot.reddit_signup(username, password)
                with open(args["newaccounts"], "a") as new_accounts:
                    new_accounts.write(f"{username},{password}")
        except FileNotFoundError:
            logger.error(f"accounts file not found: {args['newaccounts']}")
            sys.exit(1)

    if args["accounts"]:
        try:
            with open(args["accounts"], "r") as f:
                accounts = f.readlines()
        except FileNotFoundError:
            logger.error(f"Accounts file not found: {args['accounts']}")
            sys.exit(1)

    else:
        logger.error("No accounts file provided. Use -h or --help for help.")

    if args["links"]:
        try:
            with open(args["links"], "r") as f:
                links = f.readlines()
        except FileNotFoundError:
            logger.error(f"Links file not found: {args['links']}")
            sys.exit(1)
    else:
        logger.error("No links file provided. Use -h or --help for help.")
        sys.exit(1)

    # print(accounts)
    # print(links)
    print("The accounts used:\n")

    for acc in accounts:
        bot = RedditBot(
            verbose=args["verbose"]
        )
        if acc not in ["\n", "\r\n"]:
            username, password = acc.split(",")
            try:
                bot.reddit_login(username, password)
                with open("used_accounts.txt", "a") as good_accounts:
                    good_accounts.write(f"{username},{password}")
            except NoSuchElementException:
                logger.error(f"Invalid account \003[4m{username}\033[0m")
                print(username)

            for entry in links:
                contents = entry.strip("\n").split("|")
                link = contents[0]
                action = contents[1]
                if action == "upvote":
                    bot.vote(link, True)
                elif action == "downvote":
                    bot.vote(link, False)
                elif action == "comment":
                    bot.comment(link, contents[2])
                elif action in ["join", "leave"]:
                    bot.join_community(link, action == "join")
                sleep(10)
            #bot.reddit_logout()
            bot.shutdown()

# py main.py --accounts accounts.txt --links posts.txt

""""

"""