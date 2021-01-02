# Check if a range of items are in stock at various vendors, tweet if so
import requests
import tweepy
import time
import json
import secrets
from datetime import datetime

def load_cards(path):
    # Read in a json list of cards, urls, sold out codes
    with open(path) as f:
        card_data = json.load(f)

    return card_data

def is_instock(card):
    # searches a page for a "Sold Out"-like string
    # if the string isn't found and page didn't error, notify as "in stock"
    # This will fail if (looking at you Best Buy) a vendor changes to "Coming Soon" or some such
    # which is rare
    r = requests.get(card['url'], headers=headers)
    status_code = r.status_code
    soldout_pos = r.text.find(card['button'])

    if( status_code < 300 ):
        if( verbose ):
            print('\n' + card['id'] + ' at ' + card['vendor'])
            print("HTTP status code " + str(status_code))
            print("Substring position " + str(soldout_pos))

        if( soldout_pos < 0 ):

            return True

    else:
        print('ERROR: Page returned status: ' + str(status_code))

    return False

def loop_and_tweet(card_list):
    # Check if an item is in stock, and if so, tweet about it
    now = str(datetime.now())
    debug_message = "DEBUG_MESSAGE( " + now + " ):"

    for card in card_list:
        message = card['id'] + " in stock at " + card['vendor'] + \
                  " " + now + " " + card['url']

        instock = is_instock(card)
        if( instock ):
            api.update_status(message)
            log.write(message)

        debug_message = debug_message + "\n" + message

    if (verbose):
        print("\n" + debug_message)


if __name__ == '__main__':
    # Showtime
    ### verbose: output helpful messages to the console and the log file
    ### repeat: run on a 60 second timer
    ### repeat_time: time to wait between calls
    ### cards: list of websites, cards we're looking for
    ### log: logfile for when we find stuff (record of twitter failing too...)

    verbose = True
    repeat = True
    repeat_time = 60
    cards = load_cards('./cards.json')
    log = open('./instock_record.txt', 'a')

    # Request init: mock a chrome browser
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    headers = {'User-Agent': user_agent} # ,"cache-control":"max-age=0"}

    # Auth with twitter
    # TODO: How long does session stay authenticated? Apparently up to ~24 hr
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret_key)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    while True:
        # I don't care about exact scheduling so this should be fine?
        # It's probably better to loop here than cron so as only to auth once?
        loop_and_tweet(cards)

        if (repeat):
            time.sleep(repeat_time)
        else:
            break

    log.close()