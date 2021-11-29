import requests
import re
from bs4 import BeautifulSoup
import urllib.request

# target url
url = 'http://www.reddit.com'


class get():
    def __init__(self):
        pass

    def get_topics(self,url,parser ='html.parser' ):

        # making requests instance
        reqs = requests.get(url)
    
        # using the BeaitifulSoup module
        soup = BeautifulSoup(reqs.text, parser)
        for tag in soup.find_all('h3', class_='_eYtD2XCVieq6emjKBH3m'):
            pat = r"(?<=\>)[^}]*(?=\<)"
            res = re.findall(pat, str(tag))
            print(res)


        print("########## URL ##########")

        url_req = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_req, parser, from_encoding=url_req.info().get_param('charset'))
        for link in soup.find_all('a', href=re.compile("https")):
            res_url = link['href'] +".json"
            print(res_url)
   

if __name__ == "__main__":
    test = get()
    test.get_topics(url)
