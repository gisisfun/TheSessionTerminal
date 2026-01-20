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
#
# id	
# artist	
# recording	
# track	
# number	
# tune	
# tune_id		

# alias.csv
#
# tune_id
# alias	
# name		

# sets.csv
#
# tuneset.
# date 
# member_id 
# username 
# settingorder 
# name  
# tune_id 
# setting_id  
# type   
# meter 
# mode  
# abc

# tunes.csv
#
# tune_id
# setting_id
# name 
# type
# meter
# mode
# abc 
# date
# username
# composer

# tune_popularity.csv
# 
# name	
# tune_id	
# tunebooks 


import pandas as pd
import random as rand
import os
import time
import re

# when 0 tune_id just create a random tune_id
def rand_tune(session_tunes_df):
    row = rand.randint(1,len(session_tunes_df))
    tunes_row = session_tunes_df.iloc[row]
    return str(tunes_row.tune_id)

# print file update date and time

def file_update_time(my_wd,fname,verbose):
    ti_m = os.path.getmtime(os.path.join(my_wd,fname))
    m_ti = time.ctime(ti_m)
    if verbose:
        print(fname,'modified at',m_ti)
    
def file_read(my_wd,fname):
    df = pd.read_csv(os.path.join(my_wd,fname))
    return df


def clean_filename(filename, replacement="_"):
    # Keep alphanumeric, underscores, hyphens, periods, and spaces
    # and replace all other with the replacement character.
    # The pattern [^a-zA-Z0-9_.\s-] matches any character NOT in the set.
    cleaned_filename = re.sub(r'[^a-zA-Z0-9_.\s-]', replacement, filename)
    
    # Optional: ensure no leading/trailing spaces, periods, or replacement chars
    cleaned_filename = cleaned_filename.strip(f" {replacement}.")

    # Avoid potential issues with completely empty filenames
    if not cleaned_filename:
        return "default_name"
        
    return cleaned_filename

# the any key (enter)

def enter_key():
    input('\nenter key to continue\n')

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
    debug = False
    my_wd = os.getcwd()
    
    # configure urls for webserver
    
    ip_address = "localhost"
    port = "8080"
    
    # put it all together
    
    base_tune_url = "http://"+ip_address + ":" + port +  "/tunes/"
    tunes_df, sets_df, alias_df = None,None,None
    move_the_The = lambda x : "The " + x[:len(x)-5] if x[-5:] == ", The" else x 
    try:
        
        # load the tunes.csv file and make it real.
        file_update_time(my_wd,'tunes.csv',debug)
        tunes_df = file_read(my_wd,'tunes.csv')
        tunes_df['date'] = pd.to_datetime(tunes_df['date'])
        
        # load the sets file and do the same.
        file_update_time(my_wd,'sets.csv',debug)
        sets_df = file_read(my_wd,'sets.csv')
        sets_df['name'] = sets_df['name'].apply( move_the_The )
        
        # load the tune_popularity.csv file and the same stuff.
        file_update_time(my_wd,'tune_popularity.csv',debug)
        tune_popularity_df = file_read(my_wd,'tune_popularity.csv').drop(["name"], axis=1)
        
        # add in tunebooks
        
        sets_df = sets_df. merge(tune_popularity_df[['tune_id','tunebooks']], left_on='tune_id', right_on='tune_id', how='left').sort_values(by=['tunebooks'], ascending=False)
       
        # load the alias.csv file and the same stuff.
        
        file_update_time(my_wd,'aliases.csv',debug)
        alias_df = file_read(my_wd,'aliases.csv')
        
        alias_df['name'] = alias_df['name'].apply( move_the_The)
        alias_df.alias = alias_df.alias.str.replace("'", "")
        
        # concatenate tunes and alias dataframes to make it more searchable.
        
        tunes_df['name'] = tunes_df['name'].apply( move_the_The )
        
        # clean up bits I don't need and blend tune and alias names.
        
        tunes = tunes_df.copy(deep=True).rename(columns = {'name' : 'alias'}).drop(['setting_id','type','meter','mode','abc','date','username','composer'], axis=1)
        tunes['name'] = tunes['alias']
        alias_df = pd.concat([tunes,alias_df])
        
        # add in tune type
        
        alias_df = alias_df. merge(tunes_df[['tune_id','type']], left_on='tune_id', right_on='tune_id', how='left')
        
        # load the recordings.csv file
        file_update_time(my_wd,'recordings.csv',debug)
        recordings_df = file_read(my_wd,'recordings.csv')
        
    except OSError:
        print('One or more files not found')
    
    # ask the user for a tune name and teturn a list of candidate tunes.    
    the_session_splash()
    fred =  input('tune name: (no response to contine to tune id)\n')
    if fred != "":
        
        # search for tune name if not blank
    
        alias_search= alias_df[alias_df.alias.str.contains(fred.strip(),case=False,regex=False)].drop(["alias"],axis=1).drop_duplicates().reset_index(drop=True)
    
        # add on a webserver url.
    
        url_list = alias_search["tune_id"].apply(lambda x: f"{base_tune_url}{x}").reset_index(drop = True)
    
        # print the results.
    
        print('\nlist of tunes with the keywords <',fred,'>\n')
        print(alias_search.to_string(index=False))
    
     # user can type in a tune_id from the last step or a 0 value to get a random tune.
     
    tune_id = input('\ntune id (0 for random tune):')
    print('')
    try:
        if (int(tune_id) < 1):
            tune_id = rand_tune(tunes_df)
    except ValueError:
        tune_id = rand_tune(tunes_df)
    print(int(tune_id))     
        
    # extract the tune, type, abc and mode for the supplied tune_id for all settings
    
    tune_result = tunes_df.loc[tunes_df["tune_id"] == int(tune_id), ["name","type","abc","mode","meter","composer","date"]].reset_index(drop=True)
    tune_result["year"] = tune_result['date'].dt.year
    print('year',tune_result.loc[0,"year"])
    
    # print only first setting of tune
    
    pd.set_option('display.max_colwidth', None)
    print(tune_result.loc[0,"name"])
    print('ABC')
    
    # build the abc output
    
    abc = "T:" + tune_result.loc[0,"name"] + "\nR:" + tune_result.loc[0,"type"] +  "\nK:" + tune_result.loc[0,"mode"] + "\nM:" + tune_result.loc[0,"meter"]
    #if tune_result.loc[0,"type"] == "jig":
        # jig reel hornpipe
    abc = abc + "\nL:1/8"
    if not pd.isnull(tune_result.loc[0,"composer"]):
         abc = abc + "\nC:" + tune_result.loc[0,"composer"]
    abc = abc + "\n" + tune_result.loc[0,"abc"] + "\n"
    print(abc)
    
    print(base_tune_url + str(tune_id))
    print('\n')
    print('https://thesession.org/tunes/'+str(tune_id))
    print('\n')
    
    # write it out to a file
    
    with open(os.path.join(my_wd,"mp3",clean_filename(tune_result.loc[0,"name"]+".abc")), "w") as f:
      f.write("X:1\n"+abc*3)
      
    with open(os.path.join(my_wd,"pdf",clean_filename(tune_result.loc[0,"name"]+".abc")), "w") as f:
      f.write("X:1\n"+abc)
      # linux bits
      
      # abc2midi 'Siobh_n McCaughey_s.abc' -o 'Siobh_n McCaughey_s.mid'
      
      # timidity 'Siobh_n McCaughey_s.mid' -Ow -o 'Siobh_n McCaughey_s.wav'
      
      # sox 'Siobh_n McCaughey_s.wav' 'Siobh_n McCaughey_s.mp3' speed 1.33
      
      # rm 'Siobh_n McCaughey_s.wav' 
      # rm 'Siobh_n McCaughey_s.mid' 
      
      # 1. Convert .abc to .ps (PostScript)
      # abcm2ps tune.abc -O tune.ps

       # 2. Convert .ps to .pdf
       # ps2pdf tune.ps
       #  fred = "\""+"here"+"\""
             

      
    enter_key()
    
    # print out a list of artists from recordings.csv who have recorded the tune.
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
        
        # exclude 1st row as it is the tune of interest
        
        print(filtered_sets.groupby(['name','url']).size().sort_values(ascending=False).iloc[1:].to_string())
    
main()
