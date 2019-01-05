import pandas as pd
import numpy as np
import warnings

warnings.simplefilter(action='ignore', 
                      category=pd.errors.PerformanceWarning)

class BaselinePredictor(object):
  
  def __init__(self, group_by=['pitcher','stand','balls','strikes'],
               pitch_type_column='pitch_type'):
    self.group_by = group_by
    self.pitch_type_column = pitch_type_column
    
  def predict(self, season_data):
    game_pks = season_data.game_pk.unique()
    num_train_games = int(game_pks.size / 2)
    train_games = game_pks[:num_train_games]
    test_games = game_pks[num_train_games:]
    
    train_data = season_data[season_data.game_pk.isin(train_games)]
    test_data = season_data[season_data.game_pk.isin(test_games)]
    
    train_counts = train_data.pivot_table(values='game_pk',
                                          columns=self.pitch_type_column,
                                          index=self.group_by,
                                          aggfunc=len).replace(np.NaN, 0)
    train_likeliest = train_counts.idxmax(axis=1)
    
    test_counts = test_data.pivot_table(values='game_pk',
                                        columns=self.pitch_type_column,
                                        index=self.group_by,
                                        aggfunc=len).replace(np.NaN, 0)
    test_totals = test_counts.sum(axis=1)
    
    train_test_idx = train_likeliest.index.intersection(test_counts.index)
    
    train_likeliest_with_test = train_likeliest[train_test_idx]
    test_likeliest_counts = test_counts.lookup(train_likeliest_with_test.index,
                                               train_likeliest_with_test.values)
    
    test_totals_with_train = test_totals[train_test_idx]
    
    accuracy = test_likeliest_counts.sum() / test_totals_with_train.sum()
    
    return accuracy