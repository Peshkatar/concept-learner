# import modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class ConceptLearner:
    def __init__(self, df_: pd.DataFrame, class_column: str, test_size_: float = 0.2) -> None:
        self._df = df_
        self._class_column = class_column
        self._train, self._test = self._split(test_size_)
        
    def _split(self, test_size_: float) -> tuple[pd.DataFrame]:
        """Splits dataset into training and test"""
        return train_test_split(self._df, test_size=test_size_)
    
    def model(self) -> pd.Series:
        """Calls algorithms"""
        self._lgg_series = self._lgg_set(self._train)
    
    def prediction(self) -> None:
        indecies = np.where((self._test[self._lgg_series.index] == self._lgg_series).all(axis=1) == True)[0]
        self._test["predicted_spam"] = 0
        self._test.iloc[indecies, -1] = 1

        
    def _lgg_set(self, D: pd.DataFrame) -> pd.Series:
        """
        1 2 3 4 5 6 7
        Input : data D.
        Output : logical expression H . 
        1. x ← first instance from D; 
        2. H ← x;
        3. while instances left do
        4. x ←next instance from D;
        5. H ←LGG(H,x); 
        6. end
        7. return H
        """
        D = D.loc[D[self._class_column] == 1, D.columns != self._class_column] # Learn description of spam mails and dont take into account class column
        H = D.iloc[0, :] # First row

        for i in range(D.shape[0]-1):
            x = D.iloc[i+1, :] # Next row in iteration
            H = self._lgg_conj(H, x)
        return H
    
    def _lgg_conj(self, H: pd.Series, x: pd.Series) -> pd.Series:
        """
        Input : conjunctions H, x.
        Output : conjunction z.
        1. z ← conjunction of all literals common to x and y;
        2. return z;
        """
        # Iterate over all values in H and keep only common values
        for i in H.index: 
            if H[i] != x[i]:
                del H[i]
        return H
    
    def confusion_matrix(self) -> pd.crosstab:
        return pd.crosstab(self._test[self._class_column], self._test["predicted_spam"], rownames=["Actual"], colnames=["Predicted"])

    @property    
    def accuracy(self) -> float:
        cm = self.confusion_matrix()
        TP = cm.iloc[0, 0]
        TN = cm.iloc[0, 1]
        return (TP + TN) / cm.sum().sum()
    
    @property
    def precision(self) -> float:
        cm = self.confusion_matrix()
        TP = cm.iloc[0, 0]
        FP = cm.iloc[0, 1]
        return TP/(FP + TP)
    
    @property
    def sensitivity(self) -> float:
        cm = self.confusion_matrix()
        TP = cm.iloc[0, 0]
        FN = cm.iloc[1, 0]
        return TP/(TP+FN)
    
    @property    
    def true_positive_rate(self) -> float:
        cm = self.confusion_matrix()
        return cm.iloc[1, 1] / cm.iloc[:, 1].sum()
    
    @property    
    def true_negative_rate(self) -> float:
        cm = self.confusion_matrix()
        return cm.iloc[0, 0] / cm.iloc[:, 0].sum()
    
    @property
    def get_df(self) -> pd.DataFrame:
        return self._test
    
    @property
    def get_lgg(self) -> pd.Series:
        return self._lgg_series
    
    @property
    def get_conjective_rule(self) -> None:
        for i, value in self._lgg_series.items():
            print(f"{i} = {value} ∧ ", end="")
