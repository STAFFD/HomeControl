import requests
import re

def getRandomVideo():
    url = "https://random-ize.com/random-youtube/goo-f.php"
    headers = {"content-type": "text/html",
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
               }
    try:
        response = requests.get(url, headers=headers)
    except Exception as reason:
        print(reason)
    if response.status_code != 200:
        print("Error encountered 500")
    else:

        content = response.content.decode("utf8")
        return re.findall("https.+\" ", content)[0].split('"')[0]


if __name__ == '__main__':
    print(getRandomVideo())
