# This is a sample Python script.
import requests
import tweepy
import time
import json
import secrets
from datetime import datetime

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def load_cards(path):
    # Read in a json list of cards, urls, sold out codes
    with open(path) as f:
        cards = json.load(f)

    return cards

def is_instock(card):
    # searches a page where a 3080 is sold for a "Sold Out"-like string
    # if the string isn't found and page didn't error, notify as "in stock"
    r = requests.get(card['url'], headers=headers)
    status_code = r.status_code
    soldout_pos = r.text.find(card['button'])

    if( status_code < 300 ):
        if( soldout_pos < 0 ):
            return True

        if( debug ):
            print('\n' + card['id'])
            print(card['vendor'])
            print("HTTP status code " + str(status_code))
            print("Substring position " + str(soldout_pos))

    else:
        print('ERROR: Page returned status: ' + status_code)

    return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    headers = {'User-Agent': user_agent} # ,"cache-control":"max-age=0"}

    debug = True
    cards = []

    # Auth with twitter
    # TODO: How long does session stay authenticated?
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret_key)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    cards = load_cards('./cards.json')

    while True:
        debug_message = "DEBUG_MESSAGE( " + str(datetime.now()) + " ):"

        for card in cards:
            message = card['id'] + " in stock at " + card['vendor'] + \
                " " + card['url']

            if( is_instock(card) ):
                print(message)
                api.update_status(message)

            if( debug ):
                # Careful about hammering the api
                # api.update_status(message)
                debug_message = debug_message + "\n" + message

        if( debug ):
            print("\n" + debug_message)

        time.sleep(60)

