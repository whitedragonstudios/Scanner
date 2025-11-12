import requests

class News_Report():
    def __init__(self, country, news_key, banned_list = []):
        self.country = country
        self.news_key = news_key
        self.banned_list = banned_list or []
        self.articles = self.update_news()

    def get_news(self):
        try: 
            NEWS_response = requests.get(f"https://newsapi.org/v2/top-headlines?country={self.country}&apiKey={self.news_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: (get_news) api request >>>", e)
            NEWS_response = healine_list ={'articles': ["Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error"]}
        #print("A  >>> NEWS_response", NEWS_response)
        return NEWS_response


    def parse_news(self):
        news_list = self.news_response['articles']
        parsed_news = []
        for item in news_list:
            source = item['source']['name']
            artilce = item['title']
            url = item['url']
            if source not in self.banned_list:
                parsed_news.append({'src':source, "art":artilce,"url":url})
        return parsed_news


    def update_news(self):
        self.news_response = self.get_news()
        articles = self.parse_news()
        return articles

