from sklearn.preprocessing import OneHotEncoder
import pandas as pd

ID_COLUMNS = ['pitcher','batter']
CATEGORICAL_COLUMNS = ['p_throws','pitch_team',
                       'stand','bat_team']
INTEGER_COLUMNS = ['balls','strikes','outs_when_up',
                   'inning','pitch_count',
                   'pitch_number','bat_score',
                   'fld_score']
BINARY_ID_COLUMNS = ['on_1b','on_2b','on_3b']


class SeasonEncoder(object):
  
  def __init__(self, season_data, one_hot=True):
    self.season_data = season_data
    self.one_hot = one_hot
    self._encoded_data = None
    self.encodings = {}
    
  @property
  def encoded_data(self):
    if self._encoded_data is None:
      self._encoded_data = pd.DataFrame()
      
      self._encoded_data[ID_COLUMNS] = self.season_data[ID_COLUMNS]
      self._encoded_data[INTEGER_COLUMNS] = self.season_data[INTEGER_COLUMNS]     
      self._encoded_data[BINARY_ID_COLUMNS] = self.season_data[BINARY_ID_COLUMNS] >= 0
      
      for col in CATEGORICAL_COLUMNS:
        self.encodings[col] = {val:idx for idx,val in 
                      enumerate(self.season_data[col].unique())}
        self._encoded_data[col] = self.season_data[col].replace(
                      self.encodings[col])
      
      if self.one_hot:
        for col in ID_COLUMNS + CATEGORICAL_COLUMNS:
          one_hot = pd.get_dummies(self._encoded_data[col], prefix='%s_' %col)
          self._encoded_data = pd.concat((self._encoded_data.drop(col, axis=1), one_hot), axis=1)
                
    return self._encoded_data
  
  def decode(self, encoded_data):
    pass