
import pandas as pd
import random as rand
import os
#import string
my_wd = os.getcwd()
ip_address = "localhost"
port = "8080"
base_tune_url = "http://"+ip_address + ":" + port +  "/tunes/"
tunes_df, sets_df, alias_df = None,None,None
try:
    tunes_df = pd.read_csv(os.path.join(my_wd,'tunes.csv'))
    sets_df = pd.read_csv(os.path.join(my_wd,'sets.csv'))
    alias_df = pd.read_csv(os.path.join(my_wd,'aliases.csv'))
    alias_df.alias = alias_df.alias.str.replace("'", "")
    # concatenate tunes and alias dataframes
    tunes = tunes_df.copy(deep=True).rename(columns = {'name' : 'alias'}).drop(['setting_id','type','meter','mode','abc','date','username','composer'], axis=1)
    tunes['name'] = tunes['alias']
    alias_df = pd.concat([tunes,alias_df])
    # add in tune type
    alias_df = alias_df.merge(tunes_df[['tune_id','type']], left_on='tune_id', right_on='tune_id', how='left')
    
except OSError:
    print('One or more files not found')
    
def rand_tune(session_tunes_df):
    row = rand.randint(1,len(session_tunes_df))
    tunes_row = session_tunes_df.iloc[row]
    return tunes_row
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
#try:
    
alias_search= alias_df[alias_df.alias.str.contains(fred.strip(),case=False,regex=False)].drop(["alias"],axis=1).drop_duplicates().reset_index(drop=True)
#pd.merge(alias_search, df2, left_on='id', right_on='id1', how='left').drop('id1', axis=1))
#except:
#print("error")
url_list = alias_search["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)

#alias_search['url'] = url_list
list_tune_ids = alias_search['tune_id'].to_list()
print(alias_search.to_string(index=False))
#style.hide(("tune_id")))#.


tune_id = input('\ntune id:\n')
if int(tune_id) < 1:
    tune = rand_tune(tunes_df)
    tune_id = tune.tune_id
    print(int(tune_id))

print(tunes_df.loc[tunes_df["tune_id"] == int(tune_id), ["name",'type']].reset_index(drop=True).drop_duplicates().to_string(index=False))

#print(tunes_df[tunes_df.tume_id == int(tune_id)])

url = base_tune_url + str(tune_id)
print(url)
#print(name+'\n' + str(url))

in_tunesets = sets_df[sets_df.tune_id == int(tune_id)]
tunesets = in_tunesets["tuneset"].to_list() 

in_sets = sets_df[sets_df["tuneset"].isin(tunesets)]
if len(in_sets) > 0:
    filtered_sets = in_sets[["tune_id","name",]].copy(deep=True).reset_index(drop=True)
    
    url_list = in_sets["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)
    filtered_sets["url"] = url_list
    print('\n',len(filtered_sets),'tune(s) in sets')
    #print(filtered_sets.drop(['tune_id'],axis=1).drop_duplicates().to_string(index = False))
    print(filtered_sets.groupby(['name','url']).size().sort_values(ascending=False).iloc[1:].to_string())
    


