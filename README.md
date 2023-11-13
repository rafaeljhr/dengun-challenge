# Dengun Challenge

## Files present in this repository

- 'forcast_collector.py' : Main challenge file. Python script that will collect the hourly temperature from [here](https://weather.com/weather/hourbyhour/l/ISXX0026:1:IS) and save the data in a json file named "forcast_data.json.
- 'forcast_collector.yml' : GitHub pipeline file.
- 'md5sum.txt' : MD5Sum gotten from the 'forcast_collector.py' script. This file is generated from a pre-commit hook.
- 'validate_json.py' : Python script that will validate the structure of 'forcast_data.json', outputting True or False, if 'forcast_data.json' structure is in accordance with the challenge.


## MD5 hash verification 

How I have hashed on Ubuntu: 
```
md5sum forcast_collector.py > md5sum.txt
```

Verifying forcast_collector.py checksums on Ubuntu:
```
md5sum -c md5sum.txt
```

Expected output: `forcast_collector.py: OK`