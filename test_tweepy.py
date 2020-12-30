import tweepy
import secrets

if __name__ == '__main__':
    # Auth w/ twitter
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret_key)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    api = tweepy.API(auth)

    tweet_text = 'Notification test from JohnsStockRobot w/ link #1 '
    tweet_url = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p"
    api.update_status(tweet_text + tweet_url)
