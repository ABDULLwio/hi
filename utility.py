from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup
def get_news():
    url="https://www.aljazeera.com/tag/israel-war-on-gaza/"
    data=requests.get(url)
    html = BeautifulSoup(data.text, 'html.parser')
    title=html.select('h3>a>span')
    discription=html.select("div.gc__excerpt>p")
    return (title,discription)