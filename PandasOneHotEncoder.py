from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

class PandasOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.one_hot = None
    def fit(self, X, y=None):
        self.one_hot = OneHotEncoder().fit(X)
        return self
    def transform(self, X):
        Xoh = self.one_hot.transform(X).toarray()
        Xoh_features = self.one_hot.get_feature_names_out(X.columns)
        Xonehot = pd.DataFrame(Xoh, index=X.index, columns=Xoh_features)
        return Xonehot

