import requests

# This class gets news from an API and processes it for display in flask and js
class News_Report():
    def __init__(self, country, news_key, banned_list = [], autorun = True):
        # News Report needs the api key and country stored in config database 
        self.country = country
        self.news_key = news_key
        # A banned list can be passed to not display certain news sources defaults to an empty list
        self.banned_list = banned_list or []
        # Autorun is true by default to automically send api request.
        self.autorun = autorun or True
        if self.autorun:
            self.articles = self.update_news()


    # get news sends API request and returns json dictionary of news articles.
    def get_news(self):
        try: 
            NEWS_response = requests.get(f"https://newsapi.org/v2/top-headlines?country={self.country}&apiKey={self.news_key}").json()
        except requests.exceptions.RequestException as e:
            print("ERROR: (get_news) api request >>>", e)
            # error in request returns usable data for parse_news
            NEWS_response = healine_list ={'articles': ["Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error"]}
        #print("A  >>> NEWS_response", NEWS_response)
        return NEWS_response

    # parse news organizes news articles into a list of dictionaries which flask expects.
    def parse_news(self,news_response):
        parsed_news = []
        for item in news_response['articles']:
            source = item['source']['name']
            article = item['title'] # further testing if title or description returns best short form results.
            url = item['url']
            # check sourcse against banned list.
            if source not in self.banned_list:
                parsed_news.append({'src':source, "art":article,"url":url}) 
        return parsed_news


    # Flow control for the class calls both methods and passes data between them
    def update_news(self):
        news_response = self.get_news()
        articles = self.parse_news(news_response)
        return articles

