# tunes.py

# 1. Download the archived thesession.org archives
#  https://github.com/adactio/TheSession-data
#  https://github.com/adactio/TheSession-archive
# 2. from github repository TheSession-data make a copy of the files
# csv/recordings.csv
# csv/tunes.csv
# csv/sets.csv
# csv/alias.csv
# place into the folder TheSessionTerminal with the tunes.py file.
#
# 3. configure/install a local webserver and modify the configuration variables ip_address. and port in tunes.py file. make the base folder of the weh server to the contents of the TheSession-data folder.
# 
# 4. open your python intepreter envirinment and install the modules pandas, os and random modules.
#
# 5. Run the python program tunes.py

# files meta data
#
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

# when 0 tune_id just create a random tune_id
def rand_tune(session_tunes_df):
    row = rand.randint(1,len(session_tunes_df))
    tunes_row = session_tunes_df.iloc[row]
    return tunes_row

# the any key (enter)
def enter_key():
    input('\n enter key to continue\n')

# hi tech spash screen
def the_session_splash():
    print("""
              
--.--|                              
  |  |---.,---.                     
  |  |   ||---'                     
  `  `   '`---'                     
                                             
,---.               o               
`---.,---.,---.,---..,---.,---.     
    ||---'`---.`---.||   ||   |     
`---'`---'`---'`---'``---'`   '     
                                                             
--.--               o          |    
  |  ,---.,---.,-.-..,---.,---.|    
  |  |---'|    | | |||   |,---||    
  `  `---'`    ` ' '``   '`---^`---'                                                        
    """)

def main():
    my_wd = os.getcwd()
    # configure urls for webserver
    ip_address = "localhost"
    port = "8080"
    # put it all together
    base_tune_url = "http://"+ip_address + ":" + port +  "/tunes/"
    tunes_df, sets_df, alias_df = None,None,None
    move_the_The = lambda x : "The " + x[:len(x)-5] if x[-5:] == ", The" else x 
    try:
        # load the tunes.csv file and make it reel.
        tunes_df = pd.read_csv(os.path.join(my_wd,'tunes.csv'))
        # load the sets file and do the same.
        sets_df = pd.read_csv(os.path.join(my_wd,'sets.csv'))
        sets_df['name'] = sets_df['name'].apply( move_the_The )
        # load the alias.csv file and the same stuff.
        alias_df = pd.read_csv(os.path.join(my_wd,'aliases.csv'))
        alias_df['name'] = alias_df['name'].apply( move_the_The)
        alias_df.alias = alias_df.alias.str.replace("'", "")
        # concatenate tunes and alias dataframes to make it more searchable.
        tunes_df['name'] = tunes_df['name'].apply( move_the_The )
        # clean up bits I don't need and blend tune and alias names.'
        tunes = tunes_df.copy(deep=True).rename(columns = {'name' : 'alias'}).drop(['setting_id','type','meter','mode','abc','date','username','composer'], axis=1)
        tunes['name'] = tunes['alias']
        alias_df = pd.concat([tunes,alias_df])
        # add in tune type
        alias_df = alias_df. merge(tunes_df[['tune_id','type']], left_on='tune_id', right_on='tune_id', how='left')
        # load the recordings.csv file
        recordings_df = pd.read_csv(os.path.join(my_wd,'recordings.csv'))
    except OSError:
        print('One or more files not found')
    
    # ask the user for a tune name and teturn a list of candidate tunes.    
    the_session_splash()
    fred =  input('tune name:\n')
    # search for tune name.
    alias_search= alias_df[alias_df.alias.str.contains(fred.strip(),case=False,regex=False)].drop(["alias"],axis=1).drop_duplicates().reset_index(drop=True)
    # add on a webserver url.
    url_list = alias_search["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)
    # print the results.
    print('\nlist of tunes with the keywords <',fred,'>\n')
    print(alias_search.to_string(index=False))
     # user can type in a tune_id from the last step or a 0 value to get a random tune.
    tune_id = input('\ntune id (0 for random tune):')
    print('')
    if int(tune_id) < 1:
        tune = rand_tune(tunes_df)
        tune_id = tune.tune_id
        print(int(tune_id))
        
    # print out the tune and type for the supplied tune_id.
    
    print(tunes_df.loc[tunes_df["tune_id"] == int(tune_id), ["name",'type']].reset_index(drop=True).drop_duplicates().to_string(index=False))
    url = base_tune_url + str(tune_id)
    print(url)
    # print out a list if artists from recordungs.csv who have recorded the tune.
    # convert series of artist names to a list after filtering for tune_id
    print('\nlist of artists\n')   
    recordings = recordings_df.loc[recordings_df["tune_id"] == int(tune_id), ["artist"]].reset_index(drop=True).drop_duplicates().set_index('artist')
    # dataframe series turned into a list, can print thst nicely. messy code that looks nice on screen.
    nothing_to_see_here = [print(x) for x in recordings.index.to_list()]
    nothing_to_see_here = None
    # pause screen output for next output.
    enter_key()
    # print list of tunes related by sets.
    in_tunesets = sets_df[sets_df.tune_id == int(tune_id)]
    tunesets = in_tunesets["tuneset"].to_list() 

    in_sets = sets_df[sets_df["tuneset"].isin(tunesets)]
    if len(in_sets) > 0:
        filtered_sets = in_sets[["tune_id","name",]].copy(deep=True).reset_index(drop=True)
    
        url_list = in_sets["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)
        filtered_sets["url"] = url_list
        
        print('\nlist of tunes in sets by frequency\n')
        print('\n',len(filtered_sets),'tune(s) in sets')
        print(filtered_sets.groupby(['name','url']).size().sort_values(ascending=False).iloc[1:].to_string())
    
main()

