# tunes.py

# recordings.csv
# id	artist	recording	track	number	tune	tune_id		

# alias.csv
# tune_id	alias	name		

# sets.csv
# tuneset. date  member_id username settingorder name  tune_id setting_id  type   meter mode  abc

# tunes.csv
# tune_id	setting_id	name	type	meter	mode	abc	date	username	composer

import pandas as pd

import random as rand

import os

def rand_tune(session_tunes_df):
    row = rand.randint(1,len(session_tunes_df))
    tunes_row = session_tunes_df.iloc[row]
    return tunes_row

def main():
    my_wd = os.getcwd()
    ip_address = "localhost"
    port = "8080"
    base_tune_url = "http://"+ip_address + ":" + port +  "/tunes/"
    tunes_df, sets_df, alias_df = None,None,None
    print('here')
    try:
        tunes_df = pd.read_csv(os.path.join(my_wd,'tunes.csv'))
        sets_df = pd.read_csv(os.path.join(my_wd,'sets.csv'))
        sets_df['name'] = sets_df['name'].apply( lambda x : "The " + x[:len(x)-5] if x[-5:] == ", The" else x )
        alias_df = pd.read_csv(os.path.join(my_wd,'aliases.csv'))
        alias_df['name'] = alias_df['name'].apply( lambda x : "The " + x[:len(x)-5] if x[-5:] == ", The" else x )
        alias_df.alias = alias_df.alias.str.replace("'", "")
        # concatenate tunes and alias dataframes
        tunes_df['name'] = tunes_df['name'].apply( lambda x : "The " + x[:len(x)-5] if x[-5:] == ", The" else x )
        tunes = tunes_df.copy(deep=True).rename(columns = {'name' : 'alias'}).drop(['setting_id','type','meter','mode','abc','date','username','composer'], axis=1)
        tunes['name'] = tunes['alias']
        alias_df = pd.concat([tunes,alias_df])
        # add in tune type
        alias_df = alias_df. merge(tunes_df[['tune_id','type']], left_on='tune_id', right_on='tune_id', how='left')
        recordings_df = pd.read_csv(os.path.join(my_wd,'recordings.csv'))
    except OSError:
        print('One or more files not found')
    
    print("""
                                
                                
.---..                          
  |  |                          
  |  |--. .-.                   
  |  |  |(.-'                   
  '  '  `-`--'                  
 .-.                            
(   )               o           
 `-.  .-. .--..--.  .  .-. .--. 
(   )(.-' `--.`--.  | (   )|  | 
 `-'  `--'`--'`--'-' `-`-' '  `-
                                
                                                                               
                                   
    """)
    fred =  input('tune name (without punctuation):\n')
    
    
    alias_search= alias_df[alias_df.alias.str.contains(fred.strip(),case=False,regex=False)].drop(["alias"],axis=1).drop_duplicates().reset_index(drop=True)
    
    url_list = alias_search["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)

    #alias_search['url'] = url_list
    #list_tune_ids = alias_search['tune_id'].to_list()
    print(alias_search.to_string(index=False))
 
    tune_id = input('tune id:')
    if int(tune_id) < 1:
        tune = rand_tune(tunes_df)
        tune_id = tune.tune_id
        print(int(tune_id))
    
    print(tunes_df.loc[tunes_df["tune_id"] == int(tune_id), ["name",'type']].reset_index(drop=True).drop_duplicates().to_string(index=False))
    url = base_tune_url + str(tune_id)
    print(url)
    print('\nartists')   
    print(recordings_df.loc[recordings_df["tune_id"] == int(tune_id), ["artist"]].reset_index(drop=True).drop_duplicates().to_string(index=False))
    

    in_tunesets = sets_df[sets_df.tune_id == int(tune_id)]
    tunesets = in_tunesets["tuneset"].to_list() 

    in_sets = sets_df[sets_df["tuneset"].isin(tunesets)]
    if len(in_sets) > 0:
        filtered_sets = in_sets[["tune_id","name",]].copy(deep=True).reset_index(drop=True)
    
        url_list = in_sets["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)
        filtered_sets["url"] = url_list
        print('\n',len(filtered_sets),'tune(s) in sets')
        
        print(filtered_sets.groupby(['name','url']).size().sort_values(ascending=False).iloc[1:].to_string())
    
main()

