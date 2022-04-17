from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
import pandas as pd

class PandasStandardScaler(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stand_scale = None
    def fit(self, X, y=None):
        self.stand_scale = StandardScaler().fit(X)
        return self
    def transform(self, X):
        Xss = self.stand_scale.transform(X)
        Xscaled = pd.DataFrame(Xss, index=X.index, columns=X.columns)
        return Xscaled

