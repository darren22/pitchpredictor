import os
import pandas as pd
from pybaseball import statcast
from datetime import datetime,timedelta

seasons = [2016,2017]
block_days = 5
group_blocks = 5
data_folder = 'data'

data_path = os.path.join(os.path.abspath(os.curdir), data_folder)
date_format = '%Y-%m-%d'

for season in seasons:
  start_date = datetime(season,1,1)
  end_date = datetime(season,12,31)

  block_start_date = start_date
  group_start_date = start_date
  group_count = 0
  group_data = pd.DataFrame()

  while end_date >= block_start_date:
    
    block_end_date = block_start_date + timedelta(days=block_days-1)
    if block_end_date > end_date:
      block_end_date = end_date  
      
    print('Getting data for %s to %s' %(block_start_date.strftime(date_format),
                                        block_end_date.strftime(date_format)))
                                        
    block_data = statcast(start_dt = block_start_date.strftime(date_format),
                          end_dt = block_end_date.strftime(date_format))

    block_start_date = block_end_date + timedelta(days=1)
                          
    if len(block_data):
      group_data = pd.concat((group_data, block_data))
      group_count += 1
      if group_count == group_blocks:
        group_filename = '%s_%s.csv' %(group_start_date.strftime(date_format),
                                       block_end_date.strftime(date_format))
        group_data.to_csv(os.path.join(data_path, group_filename))

        group_start_date = block_start_date
        group_count = 0
        group_data = pd.DataFrame()
  
  if group_count > 0:
    group_filename = '%s_%s.csv' %(group_start_date.strftime(date_format),
                                   block_end_date.strftime(date_format))
    group_data.to_csv(os.path.join(data_path, group_filename))

    
