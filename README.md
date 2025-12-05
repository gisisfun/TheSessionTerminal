# tunes.py
## Installation Instructions

1. Download the archived thesession.org archives
https://github.com/adactio/TheSession-data
https://github.com/adactio/TheSession-archive
2. from github repository TheSession-data make a copy of the files
csv/recordings.csv
csv/tunes.csv
csv/sets.csv
csv/alias.csv
3. place into the folder TheSessionTerminal with the tunes.py file.

4. configure/install a local webserver and modify the configuration variables ip_address. and port in tunes.py file. make the base folder of the weh server to the contents of the TheSession-data folder.

5. open your python intepreter envirinment and install the modules pandas, os and random modules.

6. Run the python program tunes.py

## Files Metadata

### recordings.csv
id	artist	recording	track	number	tune	tune_id		

### alias.csv
tune_id	alias	name		

### sets.csv
tuneset. date  member_id username settingorder name  tune_id setting_id  type   meter mode  abc

### tunes.csv
tune_id	setting_id	name	type	meter	mode	abc	date	username	composer
