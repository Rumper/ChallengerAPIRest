import pandas as pd
import operator
from stop_words import get_stop_words
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from os import path
from collections import defaultdict


class ContentBased:
    """
        Recommendation model of articles based on tags.
        The model vectorizes each article in order to calculate the similarity.
    """
    TRAINNING_FILE = path.dirname(__file__) + "/datas/training_datas.csv"
    MIN_NEIGHBORS = 10

    def __init__(self, stop_words=None, token_pattern=None, metric='cosine', n_neighbors=5):
        if stop_words is None:
            self.stop_words = get_stop_words("spanish")

        if token_pattern is None:
            token_pattern = '(?u)\\b[a-zA-Z]\\w\\w+\\b'
        try:
            self.data_trainnig = pd.read_csv(self.TRAINNING_FILE)
        except Exception:
            raise FileNotFoundError(_("File no found %s") % self.TRAINNING_FILE)

        self.n_neighbors = n_neighbors if n_neighbors > self.MIN_NEIGHBORS else self.MIN_NEIGHBORS
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=token_pattern)
        self.nearest_neigbors = NearestNeighbors(metric=metric, n_neighbors=n_neighbors, algorithm='brute')

        self._fit()

    def append(self, rows):
        """
        
        :param rows: new datas by training
        :return: 
        """
        self.data_trainning = self.data_trainnig.append(rows)
        self._fit()

    def _fit(self):
        self.fit(self.data_trainnig, column_description=self.data_trainnig.columns[1])

    def fit(self, data, column_description):
        """
         Train the model:
         1 / Vectorization of each article (Extraction and weighting of attributes)
         2 / We calculate the closest items
        """
        self.data = data
        datas_por_tags = self.tfidf_vectorizer.fit_transform(data[column_description])
        self.nearest_neigbors.fit(datas_por_tags)

    def predict(self, description):
        """
        Returns the most similar items to the proposed description
        """
        description = self.tfidf_vectorizer.transform([description])
        if description.sum() == 0:
            return None
        else:
            _, indices = self.nearest_neigbors.kneighbors(description)
            dict_predict = defaultdict(int)
            categories_predict = self.data.iloc[indices[0], :].get(self.data_trainnig.columns[0])

            for category in categories_predict:
                dict_predict[category] += 1
            categories = sorted(dict_predict.items(), key=operator.itemgetter(1))

            return [category.lower() for category, _ in categories]