from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
import pandas as pd

class PandasSimpleImputer(BaseEstimator, TransformerMixin):
    def __init__(self, strategy='mean'):
        self.strategy = strategy;
        self.imputer = None
    def fit(self, X, y=None):
        self.imputer = SimpleImputer(strategy=self.strategy).fit(X)
        return self
    def transform(self, X):
        Ximp = self.imputer.transform(X)
        Ximputed = pd.DataFrame(Ximp, index=X.index, columns=X.columns)
        return Ximputed
        



