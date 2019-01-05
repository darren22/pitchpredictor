import pandas as pd
import numpy as np
import os
import re

DATA_FILE_PATTERN = '%s-\d\d-\d\d_%s-\d\d-\d\d\.csv'
STRING_COLUMNS = ['if_fielding_alignment','of_fielding_alignment']
RENAME_COLUMNS = {'pitcher.1':'pitcher-1', 'fielder_2.1':'fielder_2-1'}
ID_COLUMNS = ['game_pk', 'pitcher-1', 'fielder_2-1', 'fielder_3', 
              'fielder_4', 'fielder_5', 'fielder_6', 'fielder_7', 
              'fielder_8', 'fielder_9', 'batter', 'pitcher']
BSO_COLUMNS = ['balls', 'strikes', 'outs_when_up']
PITCH_TYPE_SUBGROUPS = {'FA':'fastball',
                        'FF':'fastball',
                        'FT':'fastball',
                        'FC':'hard break',
                        'SI':'hard break',
                        'SL':'hard break',
                        'FS':'change-up',
                        'SF':'change-up',
                        'CH':'change-up',
                        'CU':'slow break',
                        'CB':'slow break',
                        'KC':'slow break',
                        'SC':'slow break',
                        'KN':'knuckleball',
                        'EP':'other',
                        'UN':'other',
                        'XX':'other',
                        'PO':'other',
                        'FO':'other',
                        'IN':'other',
                        -1:'other'
                        }
PITCH_TYPE_GROUPS = {'fastball':'hard',
                     'hard break':'hard',
                     'change-up':'off-speed',
                     'slow break':'off-speed',
                     'knuckleball':'off-speed',
                     'other':'other'}

class Season(object):
  
  def __init__(self, season, folder='data'):
    self.season = season
    self.folder = os.path.abspath(folder)
    self.data = None
    
  @property
  def regular_season(self):
    self._load_data()
    return self.data[self.data['game_type']=='R']
    
  def _load_data(self):
    if self.data is None:
      self.data = pd.DataFrame()
      pattern = DATA_FILE_PATTERN %(self.season, self.season)
      filenames = filter(lambda s: re.match(pattern,s), os.listdir(self.folder))
      for filename in filenames:
        data = pd.read_csv(os.path.join(self.folder, filename), 
                           dtype={s:str for s in STRING_COLUMNS})
        data = data.rename(RENAME_COLUMNS, axis='columns')
        
        self.data = pd.concat((self.data, data))
    
      # set all ID columns to int32, ballls/strikes/outs to int8, with unknown/NaN as -1
      dtypes = {c:np.int32 for c in ID_COLUMNS}
      dtypes.update({c:np.int8 for c in BSO_COLUMNS})
      self.data = self.data.replace(np.NaN,-1).astype(dtypes)
      
      # order the data chronologically
      self.data = self.data.sort_values(by=['game_date','game_pk',
                                            'at_bat_number','pitch_number'])
      
      # setup pitch type subgroups & groups
      self.data['pitch_type_subgroup'] = self.data.pitch_type.map(
          lambda pt: PITCH_TYPE_SUBGROUPS[pt])
      self.data['pitch_type_group'] = self.data.pitch_type_subgroup.map(
          lambda ptsg: PITCH_TYPE_GROUPS[ptsg])
      
      # set pitch & bat teams from home & away
      topidx = self.data.inning_topbot=='Top'
      self.data['bat_team'] = self.data['home_team']
      self.data.loc[topidx,'bat_team'] = self.data.loc[topidx,'away_team']
      self.data['pitch_team'] = self.data['away_team']
      self.data.loc[topidx,'pitch_team'] = self.data.loc[topidx,'home_team']
      
      # compute pitch counts
      self.data['pitch_count'] = self.data.groupby(by=['game_pk','pitcher']).cumcount()