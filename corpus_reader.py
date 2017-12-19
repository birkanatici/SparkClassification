import json

from pymongo import MongoClient

from utils import token_stem_merge


class corpus_reader:

    def __init__(self, _isytu=False):

        self.isytuhaber = _isytu

        client = MongoClient()
        if self.isytuhaber:
            db = client.ytuhaber
        else:
            db = client.haberler

        self.collection = db.news

    def get_corpus(self, _iscache=False):

        category_dist = {}
        news_tuples = []

        cats = ["spor", "kelebek", "ekonomi", "teknoloji", "yerel-haberler", "dunya"]

        if self.isytuhaber:

            if _iscache:
                n_list = self.get_corpus_from_cache("ytu_news_cache.txt")
                category_list = self.get_corpus_from_cache("ytu_category_cache.txt")
            else:
                news_list = self.collection.find()
                category_list = self.collection.find().distinct('category')
                n_list = [{'text': token_stem_merge(news['text']), 'category': news['category']} for news in news_list]

                self.corpus_cache("ytu_news_cache.txt", n_list)
                self.corpus_cache("ytu_category_cache.txt", category_list)

        else:

            if _iscache:

                n_list = self.get_corpus_from_cache("news_cache.txt")
                category_list = self.get_corpus_from_cache("category_cache.txt")

            else:

                news_list = self.collection.find({'source': 'hurriyet', 'category': {'$in': cats}})
                category_list = self.collection.find({'source': 'hurriyet', 'category': {'$in': cats}}).distinct('category')

                n_list = [{'text': token_stem_merge(news['text']), 'category': news['category']} for news in news_list]

                self.corpus_cache("news_cache.txt", n_list)
                self.corpus_cache("category_cache.txt", category_list)

        for i in range(len(category_list)):
            category_dist.update(dict([(category_list[i], i)]))

        for item in n_list:
            text = item['text']
            category_id = category_dist.get(item['category'])
            news_tuples.append((text, category_id))

        print("News Count: ", str(len(news_tuples)))

        return news_tuples, category_dist

    def get_corpus_from_cache(self, _filename):

        with open("./resources/cache/"+_filename) as json_file:
            data = json.load(json_file)

        return data

    def corpus_cache(self, _filename, _data):

        with open("./resources/cache/"+_filename, 'w') as outfile:
            json.dump(_data, outfile)

        print(_filename + " cached.")
