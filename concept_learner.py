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
        return train_test_split(self._df, test_size=test_size_, random_state=20)
    
    def model(self) -> pd.Series:
        """Calls algorithms"""
        self._lgg_series = self._lgg_set(self._train)
    
    def predict(self) -> None:
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

    def accuracy(self) -> float:
        return (self._test.predicted_spam == self._test.is_spam).sum() / self._test.shape[0]
        
    def sensitivity(self) -> float:
        return self._test.loc[self._test.predicted_spam == self._test.is_spam, "is_spam"].sum() / (self._test.is_spam == 1).sum()
    
    def specificity(self) -> float:
        return 1 - self.sensitivity()
    
    @property
    def get_frame(self) -> pd.DataFrame:
        return self._test
    
    @property
    def get_lgg(self) -> pd.Series:
        return self._lgg_series
    
    def get_conjunctive_rule(self) -> None:
        for i, (l, value) in enumerate(self._lgg_series.items()):
            if i < len(self._lgg_series)-1:
                print(f"{l} = {value}", end=" ∧ ")
            else:
                print(f"{l} = {value}")
    
    def __len__(self) -> int:
        return len(self._lgg_series)