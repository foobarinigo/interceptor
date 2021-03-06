# Check if a range of items are in stock at various vendors, tweet if so
import requests

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    url = 'https://www.badurl.com/product/602019/msi-geforce-rtx-2060-gaming-z-dual-fan-6gb-gddr6-pcie-30-graphics-card'
    button_text = 'value="Locate In Store"'
    verbose = True

    # Request init: mock a chrome browser
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    headers = {'User-Agent': user_agent} # ,"cache-control":"max-age=0"}

    # searches a page for a "Sold Out"-like string
    # if the string isn't found and page didn't error, notify as "in stock"
    # This will fail if (looking at you Best Buy) a vendor changes to "Coming Soon" or some such
    # which is rare
    try:
        r = requests.get(url, headers=headers, timeout = 2)
    except requests.exceptions.RequestException as e:
        print("Exception " + str(e))
        pass
    else:
        status_code = r.status_code
        soldout_pos = r.text.find(button_text)
        print("HTTP status code " + str(status_code))
        print("Substring position " + str(soldout_pos))
        print(r.text)

